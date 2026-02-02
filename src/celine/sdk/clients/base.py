from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from celine.sdk.auth.provider import TokenProvider


@dataclass
class AsyncServiceClient:
    """A small helper for curated SDK wrappers.

    This class is *not* tied to generated code; wrappers can use it to build
    an httpx.AsyncClient with consistent auth/headers.
    """

    base_url: str
    token_provider: TokenProvider | None = None
    timeout: float = 10.0

    def _build_client(self, headers: dict[str, str] | None = None) -> httpx.AsyncClient:
        return httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout, headers=headers)

    async def _auth_headers(self) -> dict[str, str]:
        if not self.token_provider:
            return {}
        token = await self.token_provider.get_token()
        return {"Authorization": f"Bearer {token.access_token}"}
