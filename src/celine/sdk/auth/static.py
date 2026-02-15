# celine/sdk/auth/static.py
"""
Static token provider — wraps a pre-existing access token.

Used by BFF services that forward the caller's JWT to downstream APIs.
No refresh, no client-credentials flow — just holds the token as-is.
"""
from __future__ import annotations

import time

from celine.sdk.auth.models import AccessToken
from celine.sdk.auth.provider import TokenProvider


class StaticTokenProvider(TokenProvider):
    """Token provider that returns a fixed access token.

    Usage::

        provider = StaticTokenProvider("eyJ...")
        token = await provider.get_token()
        assert token.access_token == "eyJ..."

    The token is assumed valid for the lifetime of the provider instance.
    ``is_valid()`` always returns True (the upstream has already validated it).
    """

    def __init__(self, access_token: str) -> None:
        # Strip "Bearer " prefix if present
        if access_token.lower().startswith("bearer "):
            token = access_token.strip()
            parts = token.split()
            access_token = parts[-1] if parts else token

        self._token = AccessToken(
            access_token=access_token,
            # Far future — we don't manage expiry for forwarded tokens
            expires_at=time.time() + 86400,
        )

    async def get_token(self) -> AccessToken:
        return self._token
