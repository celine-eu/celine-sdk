"""Signature algorithms are pinned — docs/specifications/identity.md REQ-0043.

The key set decides the algorithm, not the token. Every case uses a real key and
a real signature; only the JWKS fetch is replaced, as in the rest of the suite.
"""

from __future__ import annotations

import base64
import json
import time

import jwt as pyjwt
import pytest
from cryptography.hazmat.primitives.asymmetric import ec

from celine.sdk.auth.jwt import ALLOWED_JWT_ALGORITHMS, JwtUser

from conftest import ISSUER

_SECRET = b"a-shared-secret-of-at-least-32-bytes!!"


def _serve(monkeypatch: pytest.MonkeyPatch, jwk: pyjwt.PyJWK) -> None:
    class _Client:
        def get_signing_key_from_jwt(self, token: str) -> pyjwt.PyJWK:
            return jwk

    monkeypatch.setattr(
        "celine.sdk.auth.jwt._get_jwks_client", lambda jwks_uri: _Client()
    )


def _claims(**extra) -> dict:
    now = int(time.time())
    return {"iss": ISSUER, "sub": "user-123", "iat": now, "exp": now + 300, **extra}


class TestAlgorithmAllowList:
    # @verifies REQ-0043
    def test_the_allow_list_is_asymmetric_only(self):
        assert set(ALLOWED_JWT_ALGORITHMS) == {"RS256", "ES256"}

    # @verifies REQ-0043
    def test_a_symmetric_key_in_the_key_set_does_not_verify_anything(
        self, oidc, monkeypatch
    ):
        """A key set that (wrongly) published a shared secret must not turn into a
        way to accept HS256 tokens signed with it.
        """
        k = base64.urlsafe_b64encode(_SECRET).rstrip(b"=").decode()
        _serve(monkeypatch, pyjwt.PyJWK({"kty": "oct", "k": k, "kid": "s"}))
        token = pyjwt.encode(_claims(), _SECRET, algorithm="HS256")
        with pytest.raises(pyjwt.InvalidAlgorithmError):
            JwtUser.from_token(token, oidc)

    # @verifies REQ-0043
    def test_a_caller_cannot_widen_the_allow_list(self, oidc, make_token):
        with pytest.raises(ValueError, match="algorithm"):
            JwtUser.from_token(make_token(), oidc, algorithms=["HS256"])

    # @verifies REQ-0043
    def test_a_caller_can_narrow_the_allow_list(self, oidc, make_token):
        with pytest.raises(pyjwt.InvalidAlgorithmError):
            JwtUser.from_token(make_token(), oidc, algorithms=["ES256"])

    # @verifies REQ-0043
    def test_an_ec_p256_key_verifies_es256(self, oidc, monkeypatch):
        private = ec.generate_private_key(ec.SECP256R1())
        jwk = pyjwt.PyJWK(
            json.loads(pyjwt.algorithms.ECAlgorithm.to_jwk(private.public_key()))
        )
        _serve(monkeypatch, jwk)
        token = pyjwt.encode(_claims(), private, algorithm="ES256")
        assert JwtUser.from_token(token, oidc).sub == "user-123"

    # @verifies REQ-0043
    def test_the_token_header_cannot_choose_another_algorithm_for_the_key(
        self, oidc, monkeypatch
    ):
        """An RSA key the key set marks RS256 verifies RS256 only, even if the
        header names another algorithm the same key could compute.
        """
        from cryptography.hazmat.primitives.asymmetric import rsa

        private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        data = json.loads(pyjwt.algorithms.RSAAlgorithm.to_jwk(private.public_key()))
        _serve(monkeypatch, pyjwt.PyJWK({**data, "alg": "RS256"}))
        token = pyjwt.encode(_claims(), private, algorithm="PS256")
        with pytest.raises(pyjwt.InvalidAlgorithmError):
            JwtUser.from_token(token, oidc)


class TestExpiryIsRequired:
    # @verifies REQ-0043
    def test_a_token_without_exp_is_refused(self, oidc, signing_key):
        claims = _claims()
        del claims["exp"]
        token = pyjwt.encode(claims, signing_key, algorithm="RS256")
        with pytest.raises(pyjwt.MissingRequiredClaimError, match="exp"):
            JwtUser.from_token(token, oidc)
