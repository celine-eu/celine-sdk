"""REQ-0091: a broker token is requested for the broker."""
from __future__ import annotations

from celine.sdk.auth import OidcClientCredentialsProvider, StaticTokenProvider
from celine.sdk.broker.mqtt import MqttBroker, MqttConfig


def _provider(scope: str | None = None) -> OidcClientCredentialsProvider:
    return OidcClientCredentialsProvider(
        base_url="http://keycloak.example.org/realms/celine",
        client_id="svc-example",
        client_secret="secret",
        scope=scope,
    )


# @verifies REQ-0091
def test_the_broker_asks_for_the_broker_scope():
    http = _provider()

    broker = MqttBroker(MqttConfig(), token_provider=http)

    assert broker.token_provider is not http
    assert broker.token_provider._scope == "mqtt"
    assert http._scope is None, "the caller's HTTP provider is not changed"


# @verifies REQ-0091
def test_a_requested_scope_is_kept_alongside_the_broker_scope():
    broker = MqttBroker(MqttConfig(), token_provider=_provider("openid a.events.read"))

    assert broker.token_provider._scope == "openid a.events.read mqtt"


# @verifies REQ-0091
def test_the_scope_is_not_requested_twice():
    assert _provider("mqtt").with_scope("mqtt")._scope == "mqtt"


# @verifies REQ-0091
def test_no_token_scope_uses_the_provider_as_given():
    http = _provider()

    for off in (None, ""):
        assert MqttBroker(MqttConfig(token_scope=off), token_provider=http).token_provider is http


# @verifies REQ-0091
def test_a_static_token_is_used_as_given():
    static = StaticTokenProvider("eyJ.example.token")

    assert MqttBroker(MqttConfig(), token_provider=static).token_provider is static
