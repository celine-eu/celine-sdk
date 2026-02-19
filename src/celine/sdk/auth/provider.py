from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Awaitable, Callable

from celine.sdk.auth.models import AccessToken

TokenRenewedCallback = Callable[[], Awaitable[None]]


class TokenProvider(ABC):
    def __init__(self) -> None:
        self._on_token_renewed: list[TokenRenewedCallback] = []

    def add_token_renewed_listener(self, callback: TokenRenewedCallback) -> None:
        """Register an async callback invoked whenever a new token is issued."""
        self._on_token_renewed.append(callback)

    async def _fire_token_renewed(self) -> None:
        for cb in self._on_token_renewed:
            try:
                await cb()
            except Exception as exc:
                import logging

                logging.getLogger(__name__).warning(
                    "token_renewed callback error: %s", exc
                )

    @abstractmethod
    async def get_token(self) -> AccessToken:
        """Return a valid access token (refreshing/re-authenticating as needed)."""
        raise NotImplementedError
