"""Tests for `celine.sdk.broker` — docs/specifications/messaging.md.

No broker is started. `aiomqtt.Client` is replaced by a fake with the same
surface, which is enough to exercise the parts that actually break in
production: the reconnect state machine, resubscription, topic matching and
dispatch.
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone

import pytest

from celine.sdk.auth.models import AccessToken
from celine.sdk.auth.provider import TokenProvider
from celine.sdk.broker import (
    BrokerMessage,
    MqttBroker,
    MqttConfig,
    QoS,
    create_mqtt_broker,
)

pytestmark = pytest.mark.asyncio


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class FakeMessage:
    def __init__(self, topic: str, payload: bytes, qos: int = 1) -> None:
        self.topic = topic
        self.payload = payload
        self.qos = qos


class FakeMessages:
    """The `client.messages` async iterator, fed by the test."""

    def __init__(self) -> None:
        self.queue: asyncio.Queue = asyncio.Queue()
        self.raise_on_next: Exception | None = None

    def __aiter__(self) -> "FakeMessages":
        return self

    async def __anext__(self) -> FakeMessage:
        if self.raise_on_next is not None:
            raise self.raise_on_next
        item = await self.queue.get()
        if isinstance(item, Exception):
            raise item
        if item is None:
            raise StopAsyncIteration
        return item


class FakeClient:
    instances: list["FakeClient"] = []

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs
        self.subscribed: list[tuple[str, int]] = []
        self.published: list[dict] = []
        self.entered = False
        self.closed = False
        self.messages = FakeMessages()
        self.publish_error: Exception | None = None
        FakeClient.instances.append(self)

    async def __aenter__(self) -> "FakeClient":
        self.entered = True
        return self

    async def __aexit__(self, *exc) -> None:
        self.closed = True

    async def subscribe(self, topic: str, qos: int = 0) -> None:
        self.subscribed.append((topic, qos))

    async def publish(
        self, topic: str, payload: bytes, qos: int = 0, retain: bool = False
    ) -> None:
        if self.publish_error is not None:
            raise self.publish_error
        self.published.append(
            {"topic": topic, "payload": payload, "qos": qos, "retain": retain}
        )


class FakeTokenProvider(TokenProvider):
    def __init__(self, ttl: float = 3600) -> None:
        super().__init__()
        self.issued = 0
        self.ttl = ttl

    async def get_token(self) -> AccessToken:
        self.issued += 1
        return AccessToken(
            access_token=f"token-{self.issued}", expires_at=time.time() + self.ttl
        )


@pytest.fixture(autouse=True)
def fake_aiomqtt(monkeypatch):
    FakeClient.instances = []
    monkeypatch.setattr("celine.sdk.broker.mqtt.aiomqtt.Client", FakeClient)
    return FakeClient


async def _connected(**config) -> MqttBroker:
    broker = MqttBroker(MqttConfig(reconnect_interval=0.01, **config))
    await broker.connect()
    return broker


def _collector(sink: list):
    async def handler(message) -> None:
        sink.append(message)

    return handler


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class TestConfig:
    # @verifies REQ-0079
    async def test_every_client_gets_an_identifier(self):
        auto = MqttConfig()
        assert auto.client_id and auto.client_id.startswith("celine-")
        assert MqttConfig().client_id != auto.client_id
        assert MqttConfig(client_id="fixed").client_id == "fixed"

    # @verifies REQ-0079
    async def test_keyword_arguments_override_a_supplied_config(self):
        broker = MqttBroker(MqttConfig(host="a"), host="b", port=8883)
        assert (broker.config.host, broker.config.port) == ("b", 8883)
        assert create_mqtt_broker(host="c").config.host == "c"

    # @verifies REQ-0078
    async def test_retries_are_unlimited_unless_bounded(self):
        unlimited = MqttBroker(MqttConfig(max_reconnect_attempts=0))
        assert not unlimited._give_up(1000)
        bounded = MqttBroker(MqttConfig(max_reconnect_attempts=2))
        assert not bounded._give_up(2)
        assert bounded._give_up(3)

    # @verifies REQ-0077
    async def test_tls_is_off_unless_asked_for(self):
        assert MqttBroker(MqttConfig(use_tls=False))._build_tls_context() is None
        assert MqttBroker(MqttConfig(use_tls=True))._build_tls_context() is not None


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------


class TestLifecycle:
    # @verifies REQ-0070
    async def test_connecting_makes_the_broker_ready(self):
        broker = await _connected()
        assert broker.is_connected
        assert FakeClient.instances[0].entered
        await broker.disconnect()

    # @verifies REQ-0070
    async def test_connecting_twice_does_not_build_a_second_client(self):
        broker = await _connected()
        await broker.connect()
        assert len(FakeClient.instances) == 1
        await broker.disconnect()

    # @verifies REQ-0072
    async def test_subscriptions_are_applied_on_connect(self):
        broker = MqttBroker(MqttConfig())
        result = await broker.subscribe(["events/#"], _collector([]))
        assert result.success
        assert broker.subscription_count == 1
        await broker.connect()
        assert FakeClient.instances[0].subscribed == [("events/#", 1)]
        await broker.disconnect()

    # @verifies REQ-0071
    async def test_subscriptions_survive_a_reconnect(self):
        """The registry is the source of truth and is never cleared on reconnect:
        a consumer that loses its connection loses no subscription.
        """
        broker = await _connected()
        await broker.subscribe(["events/#"], _collector([]))
        await broker._on_token_renewed()  # any reconnect trigger will do
        await asyncio.sleep(0.05)
        assert len(FakeClient.instances) == 2
        assert FakeClient.instances[1].subscribed == [("events/#", 1)]
        assert FakeClient.instances[0].closed
        await broker.disconnect()

    # @verifies REQ-0075
    async def test_disconnecting_stops_everything(self):
        broker = await _connected()
        await broker.subscribe(["events/#"], _collector([]))
        await broker.disconnect()
        assert not broker.is_connected
        assert broker.subscription_count == 0
        assert FakeClient.instances[0].closed
        assert broker._conn_task is None
        assert broker._listen_task is None

    # @verifies REQ-0077
    async def test_a_connect_timeout_is_a_connection_error(self, monkeypatch):
        """aiomqtt has no default timeout, so a broker that accepts the TCP
        connection and never completes the handshake would hang startup instead of
        failing into the retry loop.
        """

        class Hanging(FakeClient):
            async def __aenter__(self):
                await asyncio.sleep(10)

        monkeypatch.setattr("celine.sdk.broker.mqtt.aiomqtt.Client", Hanging)
        broker = MqttBroker(MqttConfig(connect_timeout=0.01))
        with pytest.raises(ConnectionError, match="timed out"):
            await broker._do_connect()

    # @verifies REQ-0076
    async def test_a_reconnect_signal_during_a_connect_attempt_is_not_lost(self):
        """The flag is cleared at the top of each attempt rather than after
        teardown, so a signal posted while connecting is still pending when the
        loop reaches its wait.
        """
        broker = await _connected()
        broker._reconnect_requested.set()
        await asyncio.sleep(0.05)
        assert len(FakeClient.instances) == 2
        await broker.disconnect()

    # @verifies REQ-0075
    async def test_sleeping_returns_early_on_shutdown(self):
        broker = MqttBroker(MqttConfig())
        broker._shutdown.set()
        started = time.monotonic()
        await broker._sleep_or_shutdown(5)
        assert time.monotonic() - started < 1


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


class TestCredentials:
    # @verifies REQ-0080
    async def test_a_token_is_presented_as_the_username(self):
        """The platform's broker expects the JWT in the username field, with the
        literal `jwt` as the password. Documented the other way round once, and
        that is why this is pinned.
        """
        broker = MqttBroker(MqttConfig(), token_provider=FakeTokenProvider())
        assert await broker._get_credentials() == ("token-1", "jwt")

    # @verifies REQ-0080
    async def test_without_a_provider_the_configured_credentials_are_used(self):
        broker = MqttBroker(MqttConfig(username="u", password="p"))
        assert await broker._get_credentials() == ("u", "p")

    # @verifies REQ-0081
    async def test_a_renewed_token_reconnects_immediately(self):
        provider = FakeTokenProvider()
        broker = MqttBroker(MqttConfig(reconnect_interval=30), token_provider=provider)
        await broker.connect()
        await broker._on_token_renewed()
        await asyncio.sleep(0.05)
        # A second client despite a 30s reconnect interval: nothing is broken, so
        # the interval is skipped.
        assert len(FakeClient.instances) == 2
        first, second = (c.kwargs["username"] for c in FakeClient.instances)
        assert first == "token-1"
        assert second != first  # the new connection presents a fresh token
        await broker.disconnect()

    # @verifies REQ-0081
    async def test_renewal_is_ignored_before_the_first_connect_and_after_shutdown(self):
        """The initial issuance must not trigger a reconnect of the connection it
        was fetched for.
        """
        broker = MqttBroker(MqttConfig(), token_provider=FakeTokenProvider())
        await broker._on_token_renewed()
        assert not broker._reconnect_requested.is_set()

        await broker.connect()
        broker._shutdown.set()
        broker._reconnect_requested.clear()
        await broker._on_token_renewed()
        assert not broker._reconnect_requested.is_set()
        broker._shutdown.clear()
        await broker.disconnect()

    # @verifies REQ-0082
    async def test_the_watcher_refreshes_ahead_of_expiry(self):
        """The provider announces a renewal only from inside `get_token()`, so the
        broker has to ask for one before the token lapses rather than after a
        connection is refused.
        """
        provider = FakeTokenProvider(ttl=0.05)
        broker = MqttBroker(
            MqttConfig(token_refresh_margin=0.0), token_provider=provider
        )
        task = asyncio.create_task(broker._token_watcher())
        await asyncio.sleep(0.2)
        broker._shutdown.set()
        task.cancel()
        assert provider.issued >= 2

    # @verifies REQ-0082
    async def test_a_failing_token_fetch_is_retried_not_fatal(self):
        class Failing(FakeTokenProvider):
            async def get_token(self):
                self.issued += 1
                raise RuntimeError("keycloak is down")

        provider = Failing()
        broker = MqttBroker(MqttConfig(), token_provider=provider)
        task = asyncio.create_task(broker._token_watcher())
        await asyncio.sleep(0.05)
        assert not task.done()
        broker._shutdown.set()
        task.cancel()


# ---------------------------------------------------------------------------
# The teardown invariant
# ---------------------------------------------------------------------------


class TestTeardown:
    # @verifies REQ-0083
    async def test_a_cancelled_listener_does_not_request_a_reconnect(self):
        """The trap this module documents: a clean shutdown that starts
        reconnecting to a broker nobody wants.
        """
        broker = MqttBroker(MqttConfig())
        broker._client = FakeClient()
        broker._shutdown.set()
        broker._listen_task = asyncio.create_task(broker._listen_loop())
        await asyncio.sleep(0)
        await broker._cancel_listen_task(silent=True)
        assert not broker._reconnect_requested.is_set()

    # @verifies REQ-0083
    async def test_an_abnormal_listener_exit_does_request_a_reconnect(self):
        """The other half: a dropped connection must be noticed. Only the
        deliberate path is silent.
        """
        broker = MqttBroker(MqttConfig())
        client = FakeClient()
        client.messages.raise_on_next = OSError("connection reset")
        broker._client = client
        await broker._listen_loop()
        assert broker._reconnect_requested.is_set()
        assert broker.get_stats()["error_count"] == 1

    # @verifies REQ-0083
    async def test_a_closed_stream_requests_a_reconnect(self):
        broker = MqttBroker(MqttConfig())
        client = FakeClient()
        await client.messages.queue.put(None)  # broker closed the connection
        broker._client = client
        await broker._listen_loop()
        assert broker._reconnect_requested.is_set()


# ---------------------------------------------------------------------------
# Topics
# ---------------------------------------------------------------------------


class TestTopics:
    # @verifies REQ-0084
    async def test_the_prefix_is_applied_with_exactly_one_separator(self):
        broker = MqttBroker(MqttConfig(topic_prefix="celine/"))
        assert broker._full_topic("events/a") == "celine/events/a"
        assert broker._full_topic("/events/a") == "celine/events/a"
        assert MqttBroker(MqttConfig(topic_prefix=""))._full_topic("e") == "e"

    # @verifies REQ-0087
    @pytest.mark.parametrize(
        "topic,pattern,expected",
        [
            ("a/b/c", "a/b/c", True),
            ("a/b/c", "a/+/c", True),
            ("a/b/c", "a/#", True),
            ("a/b/c", "#", True),
            ("a/b/c", "a/b", False),
            ("a/b", "a/b/c", False),
            ("a/b/c", "a/+/d", False),
            ("a/b/c", "b/#", False),
        ],
    )
    async def test_wildcards_follow_mqtt(self, topic, pattern, expected):
        assert MqttBroker._match(topic, pattern) is expected

    # @verifies REQ-0084
    async def test_matching_applies_the_prefix_too(self):
        """A prefix applied when subscribing but not when matching delivers
        nothing, and reports no error while doing it.
        """
        broker = MqttBroker(MqttConfig(topic_prefix="celine"))
        assert broker._topic_matches("celine/events/a", ["events/+"])
        assert not broker._topic_matches("events/a", ["events/+"])


# ---------------------------------------------------------------------------
# Publishing
# ---------------------------------------------------------------------------


class TestPublish:
    # @verifies REQ-0085
    async def test_publishing_while_disconnected_fails_as_a_result(self):
        """A broker outage is an expected condition on this path; callers must be
        able to handle it without a try block.
        """
        broker = MqttBroker(MqttConfig())
        result = await broker.publish(BrokerMessage(topic="t", payload={"a": 1}))
        assert not result.success
        assert "Not connected" in result.error

    # @verifies REQ-0085
    async def test_an_unserialisable_payload_fails_as_a_result(self):
        broker = await _connected()
        circular: dict = {}
        circular["self"] = circular
        result = await broker.publish(BrokerMessage(topic="t", payload=circular))
        assert not result.success
        assert "Serialization error" in result.error
        await broker.disconnect()

    # @verifies REQ-0086
    async def test_a_value_json_cannot_express_is_stringified_rather_than_refused(self):
        """Serialisation falls back to `str`, which is why a payload holding a
        `datetime`, a `UUID` or a domain object publishes instead of failing. The
        cost is that a value nobody meant to send goes out as its repr.
        """
        broker = await _connected()
        stamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        await broker.publish(BrokerMessage(topic="t", payload={"at": stamp}))
        sent = json.loads(FakeClient.instances[0].published[0]["payload"])
        assert sent["at"] == str(stamp)
        await broker.disconnect()

    # @verifies REQ-0085
    async def test_a_broker_error_on_publish_is_reported_and_counted(self):
        broker = await _connected()
        FakeClient.instances[0].publish_error = OSError("no route to host")
        result = await broker.publish(BrokerMessage(topic="t", payload={"a": 1}))
        assert not result.success and "no route" in result.error
        assert broker.get_stats()["error_count"] == 1
        await broker.disconnect()

    # @verifies REQ-0086
    async def test_a_payload_carries_a_timestamp_and_correlation_id(self):
        broker = await _connected()
        stamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        await broker.publish(
            BrokerMessage(
                topic="t", payload={"a": 1}, correlation_id="c-1", timestamp=stamp
            )
        )
        sent = json.loads(FakeClient.instances[0].published[0]["payload"])
        assert sent["created"] == stamp.isoformat()
        assert sent["correlation_id"] == "c-1"
        await broker.disconnect()

    # @verifies REQ-0086
    async def test_the_callers_own_keys_are_never_overwritten(self):
        broker = await _connected()
        await broker.publish(
            BrokerMessage(
                topic="t",
                payload={"created": "mine", "correlation_id": "mine"},
                correlation_id="c-1",
            )
        )
        sent = json.loads(FakeClient.instances[0].published[0]["payload"])
        assert sent == {"created": "mine", "correlation_id": "mine"}
        await broker.disconnect()

    # @verifies REQ-0084
    async def test_publishing_honours_the_prefix_qos_and_retain(self):
        broker = await _connected(topic_prefix="celine")
        await broker.publish(
            BrokerMessage(
                topic="events/a", payload={}, qos=QoS.EXACTLY_ONCE, retain=True
            )
        )
        published = FakeClient.instances[0].published[0]
        assert published["topic"] == "celine/events/a"
        assert published["qos"] == 2 and published["retain"] is True
        await broker.disconnect()

    # @verifies REQ-0086
    async def test_a_model_is_published_on_a_topic_derived_from_its_type(self):
        from pydantic import BaseModel

        class Payload(BaseModel):
            community_id: str = "rec-1"

        class Event(BaseModel):
            type: str = "dt.community.updated"
            payload: Payload = Payload()

        broker = await _connected()
        result = await broker.publish_event(Event())
        assert result.success
        assert (
            FakeClient.instances[0].published[0]["topic"]
            == "dt/community/updated/rec-1"
        )
        await broker.disconnect()


# ---------------------------------------------------------------------------
# Subscribing and dispatch
# ---------------------------------------------------------------------------


class TestSubscribe:
    # @verifies REQ-0072
    async def test_subscribing_on_a_live_connection_takes_effect_at_once(self):
        broker = await _connected()
        result = await broker.subscribe(
            ["a/#", "b/+"], _collector([]), qos=QoS.AT_MOST_ONCE
        )
        assert result.success and result.subscription_id
        assert FakeClient.instances[0].subscribed == [("a/#", 0), ("b/+", 0)]
        await broker.disconnect()

    # @verifies REQ-0073
    async def test_a_refused_subscription_is_not_left_registered(self):
        """A registration the broker never accepted would be silently re-applied on
        the next reconnect and reported as active in the meantime.
        """
        broker = await _connected()

        async def refuse(topic, qos=0):
            raise OSError("not authorised")

        FakeClient.instances[0].subscribe = refuse
        result = await broker.subscribe(["forbidden/#"], _collector([]))
        assert not result.success and "not authorised" in result.error
        assert broker.subscription_count == 0
        await broker.disconnect()

    # @verifies REQ-0074
    async def test_unsubscribing_something_unknown_is_false(self):
        broker = MqttBroker(MqttConfig())
        assert await broker.unsubscribe("sub-nope") is False
        sub = await broker.subscribe(["a/#"], _collector([]))
        assert await broker.unsubscribe(sub.subscription_id) is True
        assert broker.subscription_count == 0


class TestDispatch:
    # @verifies REQ-0087
    async def test_only_matching_subscriptions_receive_a_message(self):
        broker = MqttBroker(MqttConfig())
        matched: list = []
        missed: list = []
        await broker.subscribe(["events/+"], _collector(matched))
        await broker.subscribe(["other/#"], _collector(missed))
        await broker._dispatch(FakeMessage("events/a", b'{"v": 1}'))
        assert [m.payload for m in matched] == [{"v": 1}]
        assert missed == []

    # @verifies REQ-0088
    async def test_a_payload_that_is_not_json_is_delivered_raw(self):
        """Discarding it would lose the only evidence of a misbehaving publisher."""
        broker = MqttBroker(MqttConfig())
        seen: list = []
        await broker.subscribe(["#"], _collector(seen))
        await broker._dispatch(FakeMessage("events/a", b"\xff not json"))
        assert seen[0].payload["_raw"].endswith("not json")
        assert seen[0].raw_payload == b"\xff not json"

    # @verifies REQ-0089
    async def test_a_handler_that_raises_does_not_affect_the_others(self):
        broker = MqttBroker(MqttConfig())
        seen: list = []

        async def broken(message):
            raise RuntimeError("handler bug")

        await broker.subscribe(["#"], broken)
        await broker.subscribe(["#"], _collector(seen))
        await broker._dispatch(FakeMessage("events/a", b"{}"))
        assert len(seen) == 1
        assert broker.get_stats()["error_count"] == 1

    # @verifies REQ-0088
    async def test_an_unknown_qos_falls_back_to_at_least_once(self):
        broker = MqttBroker(MqttConfig())
        seen: list = []
        await broker.subscribe(["#"], _collector(seen))
        await broker._dispatch(FakeMessage("events/a", b"{}", qos=9))
        assert seen[0].qos == QoS.AT_LEAST_ONCE

    # @verifies REQ-0090
    async def test_the_broker_reports_its_counters(self):
        broker = await _connected()
        sub = await broker.subscribe(["events/#"], _collector([]))
        await broker.publish(BrokerMessage(topic="events/a", payload={}))
        await broker._dispatch(FakeMessage("events/a", b"{}"))
        stats = broker.get_stats()
        assert stats["connected"] is True
        assert stats["publish_count"] == 1
        assert stats["receive_count"] == 1
        assert stats["error_count"] == 0
        assert stats["subscription_count"] == 1
        assert stats["subscriptions"] == [
            {"id": sub.subscription_id, "topics": ["events/#"]}
        ]
        await broker.disconnect()
