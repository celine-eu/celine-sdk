"""Tests for the token providers — docs/specifications/identity.md.

No network: `mock_http` replaces `httpx.AsyncClient` with one wired to a
transport under the test's control, and records what was sent.
"""

from __future__ import annotations

import time
from urllib.parse import parse_qs

import httpx
import pytest

from celine.sdk.auth.models import AccessToken
from celine.sdk.auth.oidc import OidcClientCredentialsProvider
from celine.sdk.auth.oidc_discovery import OidcDiscoveryClient
from celine.sdk.auth.provider import TokenProvider
from celine.sdk.auth.static import StaticTokenProvider

pytestmark = pytest.mark.asyncio

ISSUER = "https://auth.test/realms/celine"
TOKEN_ENDPOINT = f"{ISSUER}/protocol/openid-connect/token"


def _discovery_body() -> dict:
    return {
        "issuer": ISSUER,
        "token_endpoint": TOKEN_ENDPOINT,
        "jwks_uri": f"{ISSUER}/protocol/openid-connect/certs",
    }


def _form(request: httpx.Request) -> dict[str, str]:
    return {k: v[0] for k, v in parse_qs(request.content.decode()).items()}


def _provider(**kwargs) -> OidcClientCredentialsProvider:
    return OidcClientCredentialsProvider(
        base_url=kwargs.pop("base_url", ISSUER),
        client_id=kwargs.pop("client_id", "svc"),
        client_secret=kwargs.pop("client_secret", "shh"),
        **kwargs,
    )


def _handler(
    *,
    expires_in: int | None = 300,
    refresh_token: str | None = None,
    refresh_fails: bool = False,
):
    """A Keycloak-shaped stub: discovery, then the token endpoint."""
    issued = {"n": 0}

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/.well-known/openid-configuration"):
            return httpx.Response(200, json=_discovery_body())
        form = _form(request)
        if form.get("grant_type") == "refresh_token" and refresh_fails:
            return httpx.Response(400, json={"error": "invalid_grant"})
        issued["n"] += 1
        body: dict = {"access_token": f"issued-{issued['n']}"}
        if expires_in is not None:
            body["expires_in"] = expires_in
        if refresh_token is not None:
            body["refresh_token"] = refresh_token
        return httpx.Response(200, json=body)

    return handle


# ---------------------------------------------------------------------------
# AccessToken
# ---------------------------------------------------------------------------


class TestAccessToken:
    # @verifies REQ-0034
    async def test_every_import_path_reaches_the_same_class(self):
        """`celine.sdk.auth.jwt` used to define a second, byte-identical class of
        the same name. An `isinstance` check across the two paths then failed in a
        way that reads as impossible.
        """
        from celine.sdk.auth import AccessToken as exported
        from celine.sdk.auth.jwt import AccessToken as via_jwt
        from celine.sdk.auth.models import AccessToken as via_models

        assert exported is via_models
        assert via_jwt is via_models
        assert isinstance(AccessToken("abc", time.time() + 300), via_jwt)

    # @verifies REQ-0034
    async def test_it_carries_its_expiry_and_renders_a_header(self):
        token = AccessToken(access_token="abc", expires_at=time.time() + 300)
        assert token.token_type == "Bearer"
        assert token.refresh_token is None
        assert token.to_header() == "Bearer abc"

    # @verifies REQ-0034
    async def test_validity_ends_a_leeway_before_expiry(self):
        """Early on purpose: a token handed out at the last moment is refused by
        the time it arrives.
        """
        assert AccessToken("abc", time.time() + 300).is_valid()
        assert not AccessToken("abc", time.time() + 10).is_valid()
        assert AccessToken("abc", time.time() + 10).is_valid(leeway=0)
        assert not AccessToken("abc", time.time() - 1).is_valid(leeway=0)


# ---------------------------------------------------------------------------
# StaticTokenProvider
# ---------------------------------------------------------------------------


class TestStaticTokenProvider:
    # @verifies REQ-0035
    async def test_it_is_exported_beside_the_other_provider(self):
        """It was reachable only through the submodule, which is why every service
        forwarding a caller's token imported a private path.
        """
        from celine.sdk.auth import StaticTokenProvider as Exported

        assert Exported is StaticTokenProvider

    # @verifies REQ-0035
    async def test_a_forwarded_token_is_returned_unchanged(self):
        token = await StaticTokenProvider("eyJ.abc.def").get_token()
        assert token.access_token == "eyJ.abc.def"
        assert token.is_valid()

    # @verifies REQ-0035
    async def test_a_bearer_prefix_is_stripped(self):
        for raw in ("Bearer eyJ.abc", "bearer eyJ.abc", "BEARER eyJ.abc"):
            assert (await StaticTokenProvider(raw).get_token()).access_token == "eyJ.abc"

    # @verifies REQ-0035
    async def test_only_a_value_beginning_with_the_scheme_is_stripped(self):
        """Pinning the edge rather than claiming more than the code does: the
        prefix is recognised at position zero, so a header value that arrived with
        leading whitespace is passed through as-is. Callers hand over
        `request.headers["authorization"]`, which is already trimmed.
        """
        token = await StaticTokenProvider("  Bearer eyJ.abc").get_token()
        assert token.access_token == "  Bearer eyJ.abc"

    # @verifies REQ-0035
    async def test_it_never_refreshes(self, mock_http):
        seen = mock_http(lambda r: httpx.Response(500))
        provider = StaticTokenProvider("eyJ.abc")
        first = await provider.get_token()
        second = await provider.get_token()
        assert first is second
        assert seen == []


# ---------------------------------------------------------------------------
# Renewal listeners
# ---------------------------------------------------------------------------


class TestRenewalListeners:
    # @verifies REQ-0036
    async def test_listeners_are_told_when_a_token_is_issued(self, mock_http):
        mock_http(_handler())
        provider = _provider()
        calls: list[str] = []

        async def listener() -> None:
            calls.append("fired")

        provider.add_token_renewed_listener(listener)
        await provider.get_token()
        assert calls == ["fired"]
        # The cached path issues nothing, so nothing is announced.
        await provider.get_token()
        assert calls == ["fired"]

    # @verifies REQ-0036
    async def test_a_failing_listener_neither_stops_the_others_nor_the_issuance(
        self, mock_http
    ):
        """A token was obtained. Dropping it because a subscriber misbehaved would
        take the service down for a reason unrelated to authentication.
        """
        mock_http(_handler())
        provider = _provider()
        calls: list[str] = []

        async def broken() -> None:
            calls.append("broken")
            raise RuntimeError("subscriber is having a bad day")

        async def healthy() -> None:
            calls.append("healthy")

        provider.add_token_renewed_listener(broken)
        provider.add_token_renewed_listener(healthy)
        token = await provider.get_token()
        assert token.access_token == "issued-1"
        assert calls == ["broken", "healthy"]

    # @verifies REQ-0036
    async def test_an_abstract_provider_cannot_be_used_directly(self):
        with pytest.raises(TypeError):
            TokenProvider()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


class TestDiscovery:
    # @verifies REQ-0039
    async def test_the_well_known_document_is_read_once(self, mock_http):
        seen = mock_http(_handler())
        client = OidcDiscoveryClient(ISSUER)
        first = await client.get_config()
        second = await client.get_config()
        assert first is second
        assert first.token_endpoint == TOKEN_ENDPOINT
        assert len(seen) == 1
        assert seen[0].url.path.endswith("/.well-known/openid-configuration")

    # @verifies REQ-0039
    async def test_a_trailing_slash_is_not_a_second_url(self, mock_http):
        seen = mock_http(_handler())
        await OidcDiscoveryClient(f"{ISSUER}/").get_config()
        assert str(seen[0].url) == f"{ISSUER}/.well-known/openid-configuration"


# ---------------------------------------------------------------------------
# Client credentials
# ---------------------------------------------------------------------------


class TestClientCredentials:
    # @verifies REQ-0037
    async def test_it_authenticates_at_the_discovered_endpoint(self, mock_http):
        seen = mock_http(_handler())
        token = await _provider(scope="registry:admin").get_token()
        assert token.access_token == "issued-1"
        assert str(seen[1].url) == TOKEN_ENDPOINT
        assert _form(seen[1]) == {
            "grant_type": "client_credentials",
            "client_id": "svc",
            "client_secret": "shh",
            "scope": "registry:admin",
        }

    # @verifies REQ-0037
    async def test_no_scope_is_sent_when_none_is_configured(self, mock_http):
        seen = mock_http(_handler())
        await _provider().get_token()
        assert "scope" not in _form(seen[1])

    # @verifies REQ-0037
    async def test_a_valid_token_is_reused_without_a_request(self, mock_http):
        seen = mock_http(_handler())
        provider = _provider()
        first = await provider.get_token()
        second = await provider.get_token()
        assert first is second
        assert len(seen) == 2  # discovery + one authentication

    # @verifies REQ-0039
    async def test_a_response_without_an_expiry_is_treated_as_five_minutes(
        self, mock_http
    ):
        mock_http(_handler(expires_in=None))
        before = time.time()
        token = await _provider().get_token()
        assert 299 <= token.expires_at - before <= 301

    # @verifies REQ-0038
    async def test_a_near_expired_token_is_refreshed_rather_than_reauthenticated(
        self, mock_http
    ):
        seen = mock_http(_handler(expires_in=1, refresh_token="r1"))
        provider = _provider()
        await provider.get_token()
        await provider.get_token()
        grants = [_form(r).get("grant_type") for r in seen if r.method == "POST"]
        assert grants == ["client_credentials", "refresh_token"]

    # @verifies REQ-0038
    async def test_a_failed_refresh_falls_back_to_authenticating(self, mock_http):
        """A refresh token rejected by the identity provider — revoked, rotated,
        expired — must not leave the service without credentials.
        """
        seen = mock_http(_handler(expires_in=1, refresh_token="r1", refresh_fails=True))
        provider = _provider()
        await provider.get_token()
        token = await provider.get_token()
        assert token.access_token == "issued-2"
        grants = [_form(r).get("grant_type") for r in seen if r.method == "POST"]
        assert grants == ["client_credentials", "refresh_token", "client_credentials"]

    # @verifies REQ-0036
    # @verifies REQ-0038
    async def test_renewal_is_announced_on_every_issuance(self, mock_http):
        mock_http(_handler(expires_in=1, refresh_token="r1"))
        provider = _provider()
        fired: list[int] = []

        async def listener() -> None:
            fired.append(1)

        provider.add_token_renewed_listener(listener)
        await provider.get_token()
        await provider.get_token()
        assert len(fired) == 2
