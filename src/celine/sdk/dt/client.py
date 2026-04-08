# celine/sdk/dt/client.py
"""
DTClient — main entry point for Digital Twin API access.

Wraps the generated ``celine.sdk.openapi.dt.AuthenticatedClient`` with a
``TokenProvider`` for authentication, and exposes domain-specific sub-clients.
"""
from __future__ import annotations

import logging
from functools import cached_property

from httpx import Timeout

from celine.sdk.auth.provider import TokenProvider
from celine.sdk.openapi.dt import AuthenticatedClient
from celine.sdk.dt.community import CommunityClient
from celine.sdk.dt.grid import GridClient
from celine.sdk.dt.participant import ParticipantClient

logger = logging.getLogger(__name__)


class DTClient:
    """High-level Digital Twin API client.

    Args:
        base_url: DT runtime base URL (e.g. ``http://dt:8000``).
        token_provider: Any ``TokenProvider`` implementation — use
            ``StaticTokenProvider`` for forwarded JWTs or
            ``OidcClientCredentialsProvider`` for service-to-service.
        timeout: Request timeout in seconds.

    Usage::

        dt = DTClient(
            base_url="http://dt:8000",
            token_provider=StaticTokenProvider(user_jwt),
        )

        balance = await dt.communities.energy_balance("rec-folgaria")
        values = await dt.participants.get_value("p-123", "meter_readings", start="2024-01-01")
    """

    def __init__(
        self,
        *,
        base_url: str,
        token_provider: TokenProvider,
        timeout: float = 10.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._token_provider = token_provider
        self._timeout = timeout
        self._openapi_client: AuthenticatedClient | None = None

    async def _get_client(self) -> AuthenticatedClient:
        """Get or create the generated AuthenticatedClient with a fresh token."""
        token = await self._token_provider.get_token()

        # The generated AuthenticatedClient is attrs-based and expects
        # the token at construction time. We recreate it when the token
        # changes to keep things simple.
        if (
            self._openapi_client is None
            or self._openapi_client.token != token.access_token
        ):
            self._openapi_client = AuthenticatedClient(
                base_url=self._base_url,
                token=token.access_token,
                timeout=Timeout(self._timeout),
                raise_on_unexpected_status=True,
            )

        return self._openapi_client

    @cached_property
    def communities(self) -> CommunityClient:
        """Access the energy community domain API."""
        return CommunityClient(self)

    @cached_property
    def participants(self) -> ParticipantClient:
        """Access the participant domain API."""
        return ParticipantClient(self)

    @cached_property
    def grid(self) -> GridClient:
        """Access the grid resilience domain API."""
        return GridClient(self)
