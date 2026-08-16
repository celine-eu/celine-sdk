"""Shared fixtures: a real signing key, real JWTs, and a clean environment.

Nothing here stubs token verification. `JwtUser.from_token` is what twelve
repositories rely on to decide whether a token is genuine, and a mocked
validator proves only that the mock was called — it cannot catch a token that
should have been rejected.

So tokens are genuinely signed and genuinely verified. The **only** seam is the
JWKS *fetch*, which would otherwise need a live Keycloak: `_get_jwks_client` is
replaced by a stub handing back the test public key, which leaves the signature,
`exp`, `nbf`, `iss` and `aud` checks fully in force (REQ-0021).
"""

from __future__ import annotations

import os
import time
from typing import Any, Callable

import httpx
import jwt as pyjwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from celine.sdk.settings.models import OidcSettings

ISSUER = "https://auth.test/realms/celine"
JWKS_URI = "https://auth.test/realms/celine/protocol/openid-connect/certs"


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Strip `CELINE_*` from the environment.

    Every settings class reads env vars, so a developer's shell (or a `.env`
    exported before `task test`) would otherwise decide what the tests assert.
    """
    for key in list(os.environ):
        if key.startswith("CELINE_"):
            monkeypatch.delenv(key, raising=False)


# ---------------------------------------------------------------------------
# Keys and tokens
# ---------------------------------------------------------------------------


def _new_key() -> rsa.RSAPrivateKey:
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def _pem_private(key: rsa.RSAPrivateKey) -> bytes:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


# Generated once per session: 2048-bit key generation is the slowest thing in
# this suite by an order of magnitude.
_SIGNING_KEY = _new_key()
_FOREIGN_KEY = _new_key()


@pytest.fixture(scope="session")
def signing_key() -> rsa.RSAPrivateKey:
    return _SIGNING_KEY


@pytest.fixture(scope="session")
def foreign_key() -> rsa.RSAPrivateKey:
    """A key the issuer does not publish — used to forge a signature."""
    return _FOREIGN_KEY


@pytest.fixture
def oidc() -> OidcSettings:
    """Settings pointing at the test issuer, with no audience configured."""
    return OidcSettings(base_url=ISSUER, jwks_uri=JWKS_URI, audience=None)


@pytest.fixture
def make_token() -> Callable[..., str]:
    """Build a signed JWT.

    Defaults produce a valid user token from the test issuer. Every part is
    overridable so a test can make exactly one thing wrong.
    """

    def _make(
        claims: dict[str, Any] | None = None,
        *,
        key: rsa.RSAPrivateKey | None = None,
        issuer: str | None = ISSUER,
        expires_in: float = 300,
        issued_ago: float = 0,
        not_before: float | None = None,
        sub: str | None = "user-123",
        algorithm: str = "RS256",
    ) -> str:
        now = time.time()
        payload: dict[str, Any] = {
            "iat": int(now - issued_ago),
            "exp": int(now + expires_in),
        }
        if issuer is not None:
            payload["iss"] = issuer
        if sub is not None:
            payload["sub"] = sub
        if not_before is not None:
            payload["nbf"] = int(now + not_before)
        payload.update(claims or {})
        return pyjwt.encode(
            payload,
            _pem_private(key or _SIGNING_KEY),
            algorithm=algorithm,
        )

    return _make


from celine.sdk.auth import jwt as _jwt_module

# Captured before any test replaces the module attribute, so the memoisation
# itself (REQ-0021) can still be exercised.
_REAL_GET_JWKS_CLIENT = _jwt_module._get_jwks_client


@pytest.fixture
def real_get_jwks_client():
    return _REAL_GET_JWKS_CLIENT


@pytest.fixture(autouse=True)
def patched_jwks(monkeypatch: pytest.MonkeyPatch) -> None:
    """Replace only the JWKS fetch. Verification itself stays live."""

    class _StubJwk:
        key = _SIGNING_KEY.public_key()

    class _StubJwksClient:
        def get_signing_key_from_jwt(self, token: str) -> _StubJwk:
            return _StubJwk()

    monkeypatch.setattr(
        "celine.sdk.auth.jwt._get_jwks_client",
        lambda jwks_uri: _StubJwksClient(),
    )


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_http(monkeypatch: pytest.MonkeyPatch) -> Callable[[Callable], list]:
    """Route every `httpx.AsyncClient` through a handler, recording requests.

    The SDK constructs its own clients inside the functions under test, so
    there is nowhere to inject a transport — the class itself is what gets
    replaced.
    """

    def _install(handler: Callable[[httpx.Request], httpx.Response]) -> list:
        seen: list[httpx.Request] = []

        def _recording(request: httpx.Request) -> httpx.Response:
            seen.append(request)
            return handler(request)

        real = httpx.AsyncClient

        class _MockedAsyncClient(real):  # type: ignore[misc, valid-type]
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                kwargs["transport"] = httpx.MockTransport(_recording)
                super().__init__(*args, **kwargs)

        monkeypatch.setattr(httpx, "AsyncClient", _MockedAsyncClient)
        return seen

    return _install
