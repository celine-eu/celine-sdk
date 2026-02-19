"""MQTT broker implementation for the CELINE SDK.

Architecture
------------
A single ``_connection_loop`` task owns the aiomqtt.Client lifecycle.
External code (token callbacks, network errors) never touch the client
directly — they post to a ``_reconnect_requested`` asyncio.Event and
let the loop act.

                 connect()
                     │
             ┌───────▼────────┐
             │  _connection_  │◄──── _reconnect_requested.set()
             │     loop       │         (token renewed / net error)
             └───────┬────────┘
                     │  owns
          ┌──────────▼──────────┐
          │   aiomqtt.Client    │
          │   + _listen_task    │
          └─────────────────────┘

Token provider integration
--------------------------
The OIDC provider calls ``_on_token_renewed`` whenever it issues a new token.
We post a reconnect request.  The loop tears down cleanly, fetches fresh
credentials, reconnects, and resubscribes every tracked subscription.
"""

from __future__ import annotations

import asyncio
import json
import logging
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import aiomqtt

from celine.sdk.auth.provider import TokenProvider
from celine.sdk.broker.contracts import (
    BrokerBase,
    BrokerMessage,
    MessageHandler,
    PublishResult,
    QoS,
    ReceivedMessage,
    SubscribeResult,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class MqttConfig:
    host: str = "localhost"
    port: int = 1883
    client_id: str | None = None
    username: str | None = None
    password: str | None = None
    use_tls: bool = False
    ca_certs: str | None = None
    certfile: str | None = None
    keyfile: str | None = None
    keepalive: int = 60
    clean_session: bool = True
    reconnect_interval: float = 5.0
    max_reconnect_attempts: int = 0  # 0 = unlimited
    topic_prefix: str = ""
    token_refresh_margin: float = 30.0
    connect_timeout: float = 10.0  # seconds; aiomqtt has no default timeout

    def __post_init__(self) -> None:
        if self.client_id is None:
            self.client_id = f"celine-{uuid4().hex[:8]}"


# ---------------------------------------------------------------------------
# Internal subscription record
# ---------------------------------------------------------------------------


@dataclass
class _Subscription:
    id: str
    topics: list[str]
    handler: MessageHandler
    qos: QoS


# ---------------------------------------------------------------------------
# MqttBroker
# ---------------------------------------------------------------------------


class MqttBroker(BrokerBase):
    """
    MQTT broker implementation using aiomqtt.

    Reconnection and resubscription are managed by a single dedicated
    ``_connection_loop`` asyncio task.

    Supports both:
    * Plain username/password (MqttConfig.username / password)
    * JWT auth via a TokenProvider (credentials refreshed automatically)

    Usage::

        async with MqttBroker(MqttConfig(host="localhost"), token_provider=p) as broker:
            await broker.subscribe(["events/#"], handler)
            await asyncio.sleep(3600)
    """

    def __init__(
        self,
        config: MqttConfig | None = None,
        token_provider: TokenProvider | None = None,
        **kwargs: Any,
    ) -> None:
        if config is None:
            config = MqttConfig(**kwargs)
        else:
            for k, v in kwargs.items():
                if hasattr(config, k):
                    setattr(config, k, v)

        self._config = config
        self._token_provider = token_provider

        # Source of truth for subscriptions — never cleared on reconnect.
        self._subscriptions: dict[str, _Subscription] = {}
        self._subs_lock = asyncio.Lock()

        # Set by anything that wants a reconnect; cleared at the *start* of
        # each connect attempt (not after teardown) to avoid missing signals.
        self._reconnect_requested = asyncio.Event()

        # Set by disconnect() to stop the loop.
        self._shutdown = asyncio.Event()

        # Set by the connection loop once the client is live and subscribed.
        self._ready = asyncio.Event()

        # The live client — only written by _connection_loop.
        self._client: aiomqtt.Client | None = None

        # Background tasks.
        self._conn_task: asyncio.Task | None = None
        self._listen_task: asyncio.Task | None = None
        self._token_watcher_task: asyncio.Task | None = None

        # Stats.
        self._publish_count = 0
        self._receive_count = 0
        self._error_count = 0

    # ------------------------------------------------------------------
    # BrokerBase / Broker protocol
    # ------------------------------------------------------------------

    @property
    def is_connected(self) -> bool:
        return self._ready.is_set()

    @property
    def config(self) -> MqttConfig:
        return self._config

    @property
    def token_provider(self) -> TokenProvider | None:
        return self._token_provider

    @property
    def subscription_count(self) -> int:
        return len(self._subscriptions)

    async def connect(self) -> None:
        """Start the connection loop and wait for the first successful connect.

        Idempotent — safe to call when already connected.
        """
        if self._conn_task is not None and not self._conn_task.done():
            logger.debug("Already connecting / connected")
            return

        self._shutdown.clear()
        self._ready.clear()
        self._reconnect_requested.clear()

        self._conn_task = asyncio.create_task(
            self._connection_loop(), name="mqtt-connection-loop"
        )
        # Wait for the first successful connection before registering the
        # token renewal callback.  The initial connect() itself causes a token
        # to be issued — if we registered the listener first, that issuance
        # would fire _on_token_renewed and immediately tear down the brand-new
        # connection before any subscriptions are in place.
        await self._ready.wait()

        if self._token_provider is not None:
            self._token_provider.add_token_renewed_listener(self._on_token_renewed)
            self._token_watcher_task = asyncio.create_task(
                self._token_watcher(), name="mqtt-token-watcher"
            )

    async def disconnect(self) -> None:
        """Gracefully stop everything."""
        self._shutdown.set()

        await self._cancel_listen_task(silent=True)

        if self._token_watcher_task and not self._token_watcher_task.done():
            self._token_watcher_task.cancel()
            try:
                await self._token_watcher_task
            except asyncio.CancelledError:
                pass
        self._token_watcher_task = None

        if self._conn_task and not self._conn_task.done():
            self._conn_task.cancel()
            try:
                await self._conn_task
            except asyncio.CancelledError:
                pass
        self._conn_task = None

        await self._close_client()
        self._ready.clear()
        async with self._subs_lock:
            self._subscriptions.clear()
        logger.info("MQTT broker disconnected")

    async def publish(self, message: BrokerMessage) -> PublishResult:
        if not self.is_connected or self._client is None:
            return PublishResult(success=False, error="Not connected to MQTT broker")

        topic = self._full_topic(message.topic)
        payload_dict = dict(message.payload)
        ts = message.timestamp or datetime.now(timezone.utc)
        payload_dict.setdefault("_timestamp", ts.isoformat())
        if message.correlation_id:
            payload_dict.setdefault("_correlationId", message.correlation_id)

        try:
            payload_bytes = json.dumps(payload_dict, default=str).encode()
        except (TypeError, ValueError) as exc:
            return PublishResult(success=False, error=f"Serialization error: {exc}")

        try:
            await self._client.publish(
                topic=topic,
                payload=payload_bytes,
                qos=message.qos.value,
                retain=message.retain,
            )
            self._publish_count += 1
            logger.debug(
                "Published to %s (qos=%d, %d bytes)",
                topic,
                message.qos.value,
                len(payload_bytes),
            )
            return PublishResult(success=True, message_id=str(uuid4()))
        except Exception as exc:
            self._error_count += 1
            logger.error("Publish failed on %s: %s", topic, exc)
            return PublishResult(success=False, error=str(exc))

    async def subscribe(
        self,
        topics: list[str],
        handler: MessageHandler,
        qos: QoS = QoS.AT_LEAST_ONCE,
    ) -> SubscribeResult:
        sub_id = f"sub-{uuid4().hex[:8]}"

        async with self._subs_lock:
            self._subscriptions[sub_id] = _Subscription(
                id=sub_id, topics=topics, handler=handler, qos=qos
            )

        # If already connected, subscribe immediately on the live client.
        if self.is_connected and self._client is not None:
            try:
                for topic in topics:
                    full = self._full_topic(topic)
                    await self._client.subscribe(full, qos=qos.value)
                    logger.info("Subscribed to: %s", full)
            except Exception as exc:
                self._error_count += 1
                async with self._subs_lock:
                    self._subscriptions.pop(sub_id, None)
                return SubscribeResult(success=False, error=str(exc))

        logger.debug("Registered subscription %s → %s", sub_id, topics)
        return SubscribeResult(success=True, subscription_id=sub_id)

    async def unsubscribe(self, subscription_id: str) -> bool:
        async with self._subs_lock:
            sub = self._subscriptions.pop(subscription_id, None)
        if sub is None:
            return False
        logger.info("Unsubscribed %s (topics: %s)", subscription_id, sub.topics)
        return True

    # ------------------------------------------------------------------
    # Connection loop — the single owner of aiomqtt.Client
    # ------------------------------------------------------------------

    async def _connection_loop(self) -> None:
        """Manage the full client lifecycle: connect → listen → reconnect.

        The loop wakes when ``_reconnect_requested`` is set (network error or
        token renewal) and tears down + rebuilds the connection.

        Key invariant: ``_reconnect_requested`` is cleared at the TOP of each
        connect attempt, not after teardown.  This ensures that any signal
        posted *during* the connect or the running session is never lost.
        """
        attempt = 0

        while not self._shutdown.is_set():

            # Clear BEFORE connecting so signals during connect are not lost.
            self._reconnect_requested.clear()

            # --- connect ---
            try:
                await self._do_connect()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                attempt += 1
                if self._give_up(attempt):
                    logger.error(
                        "Giving up after %d failed connection attempts", attempt
                    )
                    return
                wait = self._config.reconnect_interval
                logger.error(
                    "Connection failed (attempt %d): %s — retrying in %.1fs",
                    attempt,
                    exc,
                    wait,
                )
                await self._sleep_or_shutdown(wait)
                continue

            # --- live ---
            attempt = 0
            self._listen_task = asyncio.create_task(
                self._listen_loop(), name="mqtt-listen-loop"
            )
            self._ready.set()
            logger.info(
                "MQTT ready — %d subscription(s) active", len(self._subscriptions)
            )

            # Block here until something requests a reconnect.
            await self._reconnect_requested.wait()

            if self._shutdown.is_set():
                break

            # --- tear down ---
            logger.info("Reconnect triggered — tearing down current connection")
            self._ready.clear()

            # Cancel with silent=True: the listen task's finally would set
            # _reconnect_requested again, but we are already handling the
            # reconnect — we do not want a second one queued.
            await self._cancel_listen_task(silent=True)
            await self._close_client()

            wait = self._config.reconnect_interval
            logger.info("Reconnecting in %.1fs...", wait)
            await self._sleep_or_shutdown(wait)
            # Loop back: _reconnect_requested.clear() is the first thing above.

        logger.debug("Connection loop exiting")

    # ------------------------------------------------------------------
    # Listen loop
    # ------------------------------------------------------------------

    async def _listen_loop(self) -> None:
        """Drain messages from the live client; request reconnect on any error."""
        if self._client is None:
            return
        try:
            async for message in self._client.messages:
                await self._dispatch(message)
            # Clean exhaustion = broker closed the connection.
            logger.warning("MQTT message stream ended (broker closed connection)")
        except asyncio.CancelledError:
            # Normal cancellation during deliberate teardown — do not reconnect.
            raise
        except Exception as exc:
            self._error_count += 1
            logger.error("Listener error: %s — triggering reconnect", exc)
        finally:
            # Request reconnect only on abnormal exit (not cancelled, not shutdown).
            if not self._shutdown.is_set():
                self._reconnect_requested.set()

    # ------------------------------------------------------------------
    # Token provider callback
    # ------------------------------------------------------------------

    async def _token_watcher(self) -> None:
        """Proactively refresh the token before it expires.

        The token provider only fires _fire_token_renewed() from inside
        get_token() — there is no background scheduler in the provider itself.
        This task fills that gap.

        Strategy:
          1. Fetch the current token to learn its expiry.
          2. Sleep until (expires_at - token_refresh_margin).
          3. The provider's is_valid() uses a 30s leeway by default, so sleeping
             until (expires_at - margin) guarantees is_valid() returns False when
             we call get_token(), forcing a real refresh + callback fire.
          4. Repeat with the new token.

        token_refresh_margin must be >= 30 (the provider's is_valid leeway) for
        the forced refresh to actually happen.  Default is 30.0.
        """
        import time as _time

        while not self._shutdown.is_set():
            # Step 1: get current token (may be cached, that's fine)
            try:
                if not self._token_provider:
                    raise ValueError("token provider is not set")
                token = await self._token_provider.get_token()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(
                    "Token watcher: get_token failed: %s — retrying in 10s", exc
                )
                await self._sleep_or_shutdown(10)
                continue

            # Step 2: sleep until refresh window
            margin = self._config.token_refresh_margin
            sleep_for = max(0.0, token.expires_at - _time.time() - margin)
            logger.debug("Scheduling token refresh in %.1f seconds", sleep_for)
            await self._sleep_or_shutdown(sleep_for)

            if self._shutdown.is_set():
                break

            # Step 3: token is now within the margin window — is_valid() returns
            # False, so get_token() will authenticate/refresh and fire the callback
            logger.debug("Token refresh window reached — requesting new token")
            try:
                if not self._token_provider:
                    raise ValueError("token provider is not set")
                await self._token_provider.get_token()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                logger.warning(
                    "Token watcher: refresh failed: %s — retrying in 10s", exc
                )
                await self._sleep_or_shutdown(10)
            # Loop: next iteration reads the new token's expiry

    async def _on_token_renewed(self) -> None:
        """Called by the OIDC provider when a fresh token is issued."""
        if self._shutdown.is_set():
            return
        logger.info("Token expiring, reconnecting with fresh credentials")
        self._reconnect_requested.set()

    # ------------------------------------------------------------------
    # Connect / disconnect helpers
    # ------------------------------------------------------------------

    async def _do_connect(self) -> None:
        """Build and enter a new aiomqtt.Client, then resubscribe all topics."""
        username, password = await self._get_credentials()
        tls_context = self._build_tls_context()

        logger.info(
            "Connecting to MQTT broker at %s:%d",
            self._config.host,
            self._config.port,
        )

        client = aiomqtt.Client(
            hostname=self._config.host,
            port=int(self._config.port),
            identifier=self._config.client_id,
            username=username,
            password=password,
            tls_context=tls_context,
            keepalive=self._config.keepalive,
            clean_session=self._config.clean_session,
        )
        try:
            await asyncio.wait_for(
                client.__aenter__(), timeout=self._config.connect_timeout
            )
        except asyncio.TimeoutError:
            raise ConnectionError(
                f"MQTT connect timed out after {self._config.connect_timeout}s "
                f"({self._config.host}:{self._config.port})"
            )
        self._client = client

        logger.info(
            "Connected to MQTT broker %s:%d as %s%s",
            self._config.host,
            self._config.port,
            self._config.client_id,
            " (JWT auth)" if self._token_provider else "",
        )

        await self._resubscribe_all()

    async def _close_client(self) -> None:
        client, self._client = self._client, None
        if client is not None:
            try:
                await client.__aexit__(None, None, None)
            except Exception as exc:
                logger.debug("Error closing MQTT client: %s", exc)

    async def _cancel_listen_task(self, *, silent: bool = False) -> None:
        """Cancel the listen task.

        ``silent=True`` is used during deliberate teardown: the task's finally
        block will try to set ``_reconnect_requested``, but since we are
        already in the reconnect/shutdown path that signal is noise.  The
        CancelledError is always swallowed here regardless.
        """
        task, self._listen_task = self._listen_task, None
        if task is None or task.done():
            return
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            if not silent:
                logger.debug("Listen task error on cancel: %s", exc)

    # ------------------------------------------------------------------
    # Resubscribe
    # ------------------------------------------------------------------

    async def _resubscribe_all(self) -> None:
        async with self._subs_lock:
            subs = list(self._subscriptions.values())
        if not subs or self._client is None:
            return
        for sub in subs:
            for topic in sub.topics:
                full = self._full_topic(topic)
                await self._client.subscribe(full, qos=sub.qos.value)
                logger.debug("Resubscribed to: %s", full)
        logger.info("Resubscribed %d subscription(s)", len(subs))

    # ------------------------------------------------------------------
    # Message dispatch
    # ------------------------------------------------------------------

    async def _dispatch(self, message: aiomqtt.Message) -> None:
        self._receive_count += 1
        topic = str(message.topic)
        raw = message.payload if isinstance(message.payload, bytes) else b""

        try:
            payload = json.loads(raw.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = {"_raw": raw.decode(errors="replace")}

        received = ReceivedMessage(
            topic=topic,
            payload=payload,
            raw_payload=raw,
            qos=QoS(message.qos) if message.qos in (0, 1, 2) else QoS.AT_LEAST_ONCE,
            timestamp=datetime.now(timezone.utc),
        )

        async with self._subs_lock:
            subs = list(self._subscriptions.values())

        for sub in subs:
            if self._topic_matches(topic, sub.topics):
                try:
                    await sub.handler(received)
                except Exception as exc:
                    self._error_count += 1
                    logger.error("Handler error in %s: %s", sub.id, exc)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _give_up(self, attempt: int) -> bool:
        m = self._config.max_reconnect_attempts
        return bool(m and attempt > m)

    async def _sleep_or_shutdown(self, seconds: float) -> None:
        """Sleep for ``seconds``, waking early if shutdown is requested."""
        try:
            await asyncio.wait_for(
                asyncio.shield(self._shutdown.wait()), timeout=seconds
            )
        except asyncio.TimeoutError:
            pass

    async def _get_credentials(self) -> tuple[str | None, str | None]:
        if self._token_provider is not None:
            token = await self._token_provider.get_token()
            return token.access_token, "jwt"
        return self._config.username, self._config.password

    def _build_tls_context(self) -> ssl.SSLContext | None:
        if not self._config.use_tls:
            return None
        ctx = ssl.create_default_context()
        if self._config.ca_certs:
            ctx.load_verify_locations(self._config.ca_certs)
        if self._config.certfile and self._config.keyfile:
            ctx.load_cert_chain(self._config.certfile, self._config.keyfile)
        return ctx

    def _full_topic(self, topic: str) -> str:
        if self._config.topic_prefix:
            return f"{self._config.topic_prefix.rstrip('/')}/{topic.lstrip('/')}"
        return topic

    def _topic_matches(self, topic: str, patterns: list[str]) -> bool:
        return any(self._match(topic, self._full_topic(p)) for p in patterns)

    @staticmethod
    def _match(topic: str, pattern: str) -> bool:
        tp = topic.split("/")
        pp = pattern.split("/")
        for i, seg in enumerate(pp):
            if seg == "#":
                return True
            if i >= len(tp):
                return False
            if seg != "+" and seg != tp[i]:
                return False
        return len(tp) == len(pp)

    # ------------------------------------------------------------------
    # Extras preserved from original
    # ------------------------------------------------------------------

    async def publish_event(
        self,
        event: Any,
        topic: str | None = None,
        qos: QoS = QoS.AT_LEAST_ONCE,
        retain: bool = False,
    ) -> PublishResult:
        """Publish a Pydantic event model, deriving the topic from the event type."""
        if topic is None:
            event_type = getattr(event, "type", None)
            if event_type and hasattr(event, "payload"):
                community_id = getattr(event.payload, "community_id", "unknown")
                type_parts = event_type.replace("dt.", "").replace(".", "/")
                topic = f"dt/{type_parts}/{community_id}"
            else:
                topic = "dt/events/unknown"

        if hasattr(event, "model_dump"):
            payload_dict = event.model_dump(mode="json", by_alias=True)
        elif hasattr(event, "dict"):
            payload_dict = event.dict(by_alias=True)
        else:
            payload_dict = dict(event)

        return await self.publish(
            BrokerMessage(
                topic=topic,
                payload=payload_dict,
                qos=qos,
                retain=retain,
                correlation_id=getattr(event, "correlation_id", None),
                timestamp=getattr(event, "timestamp", None),
            )
        )

    def get_stats(self) -> dict[str, Any]:
        return {
            "connected": self.is_connected,
            "publish_count": self._publish_count,
            "receive_count": self._receive_count,
            "error_count": self._error_count,
            "subscription_count": len(self._subscriptions),
            "subscriptions": [
                {"id": s.id, "topics": s.topics} for s in self._subscriptions.values()
            ],
        }


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def create_mqtt_broker(**kwargs: Any) -> MqttBroker:
    return MqttBroker(MqttConfig(**kwargs))
