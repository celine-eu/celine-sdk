from __future__ import annotations

from abc import ABC, abstractmethod

from celine.sdk.auth.models import AccessToken


class TokenProvider(ABC):
    @abstractmethod
    async def get_token(self) -> AccessToken:
        """Return a valid access token (refreshing/re-authenticating as needed)."""
        raise NotImplementedError
