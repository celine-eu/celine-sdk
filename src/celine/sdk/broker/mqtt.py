from __future__ import annotations

import asyncio
import json
import logging
import ssl
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol, runtime_checkable
from uuid import uuid4

import aiomqtt

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


@runtime_checkable
class TokenProviderProtocol(Protocol):
    async def get_token(self) -> Any: ...


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
    max_reconnect_attempts: int = 0
    topic_prefix: str = ""
    token_refresh_margin: float = 30.0

    def __post_init__(self) -> None:
        if self.client_id is None:
            self.client_id = f"celine-{uuid4().hex[:8]}"


@dataclass
class _Subscription:
    id: str
    topics: list[str]
    handler: MessageHandler
    qos: QoS


class MqttBroker(BrokerBase):
    def __init__(
        self,
        config: MqttConfig | None = None,
        token_provider: TokenProviderProtocol | None = None,
        **kwargs: Any,
    ):
        if config is None:
            config = MqttConfig(**kwargs)
        else:
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)

        self._config = config
        self._token_provider = token_provider

        self._client: aiomqtt.Client | None = None
        self._connected = False
        self._lock = asyncio.Lock()

        self._subscriptions: dict[str, _Subscription] = {}
        self._listener_task: asyncio.Task | None = None
        self._token_refresh_task: asyncio.Task | None = None

    @property
    def is_connected(self) -> bool:
        return self._connected and self._client is not None

    def _build_tls_context(self) -> ssl.SSLContext | None:
        if not self._config.use_tls:
            return None
        context = ssl.create_default_context()
        if self._config.ca_certs:
            context.load_verify_locations(self._config.ca_certs)
        if self._config.certfile and self._config.keyfile:
            context.load_cert_chain(
                certfile=self._config.certfile,
                keyfile=self._config.keyfile,
            )
        return context

    def _full_topic(self, topic: str) -> str:
        if self._config.topic_prefix:
            prefix = self._config.topic_prefix.rstrip("/")
            return f"{prefix}/{topic.lstrip('/')}"
        return topic

    async def _get_credentials(self) -> tuple[str | None, str | None]:
        if self._token_provider:
            token = await self._token_provider.get_token()
            # Convention: mosquitto-go-auth expects username=jw... or jwt; DT uses username "jwt"
            access_token = (
                getattr(token, "access_token", None)
                or getattr(token, "token", None)
                or str(token)
            )
            expires_at = getattr(token, "expires_at", None)
            if isinstance(expires_at, (int, float)):
                self._schedule_token_refresh(float(expires_at))
            return "jwt", access_token
        return self._config.username, self._config.password

    def _schedule_token_refresh(self, expires_at: float) -> None:
        if self._token_refresh_task and not self._token_refresh_task.done():
            self._token_refresh_task.cancel()

        refresh_in = max(
            0.0, expires_at - time.time() - self._config.token_refresh_margin
        )
        self._token_refresh_task = asyncio.create_task(
            self._refresh_token_and_reconnect(refresh_in),
            name="mqtt-broker-token-refresh",
        )

    async def _refresh_token_and_reconnect(self, delay: float) -> None:
        try:
            await asyncio.sleep(delay)
            if not self._connected:
                return
            logger.info("MQTT token expiring: reconnecting with fresh credentials")
            subs = list(self._subscriptions.values())
            await self._disconnect_internal()
            await self._connect_internal()
            # resubscribe
            if subs and self._client:
                for sub in subs:
                    for topic in sub.topics:
                        await self._client.subscribe(
                            self._full_topic(topic), qos=sub.qos.value
                        )
                self._start_listener()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.error("Error during token refresh: %s", exc)

    async def _connect_internal(self) -> aiomqtt.Client:
        tls_ctx = self._build_tls_context()
        username, password = await self._get_credentials()

        client = aiomqtt.Client(
            hostname=self._config.host,
            port=self._config.port,
            # client_id=self._config.client_id,
            username=username,
            password=password,
            tls_context=tls_ctx,
            keepalive=self._config.keepalive,
            clean_session=self._config.clean_session,
        )
        await client.__aenter__()

        self._client = client
        self._connected = True

        return client

    async def _disconnect_internal(self) -> None:
        if self._listener_task and not self._listener_task.done():
            self._listener_task.cancel()
        self._listener_task = None

        if self._token_refresh_task and not self._token_refresh_task.done():
            self._token_refresh_task.cancel()
        self._token_refresh_task = None

        if self._client is not None:
            try:
                await self._client.__aexit__(None, None, None)
            finally:
                self._client = None
        self._connected = False

    async def connect(self) -> None:
        async with self._lock:
            if self._connected:
                return

            attempts = 0
            while True:
                try:
                    client = await self._connect_internal()
                    # resubscribe existing
                    for sub in self._subscriptions.values():
                        for topic in sub.topics:
                            await client.subscribe(
                                self._full_topic(topic), qos=sub.qos.value
                            )
                    if self._subscriptions:
                        self._start_listener()
                    return
                except Exception as exc:
                    attempts += 1
                    logger.warning(
                        "MQTT connect failed (attempt %d): %s", attempts, exc
                    )
                    if (
                        self._config.max_reconnect_attempts
                        and attempts >= self._config.max_reconnect_attempts
                    ):
                        raise
                    await asyncio.sleep(self._config.reconnect_interval)

    async def disconnect(self) -> None:
        async with self._lock:
            await self._disconnect_internal()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.disconnect()

    def _start_listener(self) -> None:
        if self._listener_task and not self._listener_task.done():
            return
        self._listener_task = asyncio.create_task(
            self._listener_loop(), name="mqtt-broker-listener"
        )

    async def _listener_loop(self) -> None:
        assert self._client is not None
        try:
            async for msg in self._client.messages:
                await self._dispatch_message(msg)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.error("MQTT listener error: %s", exc)

    async def _dispatch_message(self, msg: aiomqtt.Message) -> None:
        raw = bytes(msg.payload)
        try:
            payload_obj = json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:
            payload_obj = {}

        received = ReceivedMessage(
            topic=str(msg.topic),
            payload=(
                payload_obj if isinstance(payload_obj, dict) else {"value": payload_obj}
            ),
            raw_payload=raw,
            qos=QoS(msg.qos),
            message_id=(
                str(getattr(msg, "mid", None))
                if getattr(msg, "mid", None) is not None
                else None
            ),
            timestamp=datetime.now(timezone.utc),
        )

        # find matching subscriptions by exact topic filter list; aiomqtt already filters by broker
        for sub in list(self._subscriptions.values()):
            # We can't easily know which filter matched, but handler can inspect topic.
            try:
                await sub.handler(received)
            except Exception as exc:
                logger.error("MQTT message handler error: %s", exc)

    async def publish(self, message: BrokerMessage) -> PublishResult:
        await self.connect()
        assert self._client is not None

        topic = self._full_topic(message.topic)
        payload = json.dumps(message.payload, separators=(",", ":")).encode("utf-8")

        try:
            info = await self._client.publish(
                topic, payload=payload, qos=message.qos.value, retain=message.retain
            )
            mid = str(getattr(info, "mid", None)) if info is not None else None
            return PublishResult(success=True, message_id=mid)
        except Exception as exc:
            return PublishResult(success=False, error=str(exc))

    async def subscribe(
        self,
        topics: list[str],
        handler: MessageHandler,
        qos: QoS = QoS.AT_LEAST_ONCE,
    ) -> SubscribeResult:
        await self.connect()
        assert self._client is not None

        sub_id = uuid4().hex
        self._subscriptions[sub_id] = _Subscription(
            id=sub_id, topics=list(topics), handler=handler, qos=qos
        )

        for topic in topics:
            await self._client.subscribe(self._full_topic(topic), qos=qos.value)

        self._start_listener()
        return SubscribeResult(subscription_id=sub_id)

    async def unsubscribe(self, subscription_id: str) -> bool:
        sub = self._subscriptions.pop(subscription_id, None)
        if not sub:
            return False
        await self.connect()
        assert self._client is not None

        # Unsubscribe topics (best-effort) — may affect other subs; keep simple for now.
        for topic in sub.topics:
            try:
                await self._client.unsubscribe(self._full_topic(topic))
            except Exception:
                pass
        return True


def create_mqtt_broker(**kwargs: Any) -> MqttBroker:
    return MqttBroker(MqttConfig(**kwargs))
