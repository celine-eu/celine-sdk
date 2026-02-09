# celine/sdk/dt/community.py
"""
CommunityClient — curated async wrapper for the it_energy_community domain.

All methods delegate to the generated ``celine.sdk.openapi.dt.api.it_energy_community``
module functions. Error handling converts generated error types into clean exceptions.
"""
from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

from celine.sdk.openapi.dt.api.it_energy_community import (
    energy_balance_communities_it_community_id_energy_balance_get as _energy_balance,
    community_summary_communities_it_community_id_summary_get as _summary,
    it_energy_community_get_value as _get_value,
    it_energy_community_post_value as _post_value,
    it_energy_community_info as _info,
    it_energy_community_list_values as _list_values,
    it_energy_community_list_simulations as _list_sims,
    it_energy_community_describe_value as _describe_value,
    it_energy_community_describe_simulation as _describe_sim,
)
from celine.sdk.openapi.dt.models import ValuesRequest, Payload
from celine.sdk.openapi.dt.models.http_validation_error import HTTPValidationError
from celine.sdk.openapi.dt.types import UNSET

if TYPE_CHECKING:
    from celine.sdk.dt.client import DTClient

logger = logging.getLogger(__name__)


class DTApiError(Exception):
    """Raised when a DT API call fails."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _unwrap(result: Any, context: str = "") -> Any:
    """Unwrap a generated API response, raising on errors."""
    if result is None:
        raise DTApiError(f"No response from DT API{f': {context}' if context else ''}")
    if isinstance(result, HTTPValidationError):
        detail = getattr(result, "detail", None)
        raise DTApiError(
            f"Validation error{f' ({context})' if context else ''}: {detail}", 422
        )
    return result


class CommunityClient:
    """Async client for the Italian Energy Community DT domain.

    Not instantiated directly — use ``DTClient.communities``.
    """

    def __init__(self, dt: DTClient) -> None:
        self._dt = dt

    async def info(self, community_id: str) -> dict[str, Any]:
        """Get domain info and available capabilities for a community."""
        client = await self._dt._get_client()
        result = await _info.asyncio(community_id=community_id, client=client)
        return _unwrap(result, f"info({community_id})")

    async def energy_balance(
        self,
        community_id: str,
        *,
        start: str | None = None,
        end: str | None = None,
    ) -> dict[str, Any]:
        """Get the energy balance for a community.

        Args:
            community_id: Community entity ID.
            start: ISO timestamp for period start (optional).
            end: ISO timestamp for period end (optional).

        Returns:
            Energy balance dict with production, consumption, self-consumption.
        """
        client = await self._dt._get_client()
        result = await _energy_balance.asyncio(
            community_id=community_id,
            client=client,
            start=start if start else UNSET,
            end=end if end else UNSET,
        )
        data = _unwrap(result, f"energy_balance({community_id})")
        # Generated model → dict for convenience
        if hasattr(data, "to_dict"):
            return data.to_dict()
        return data

    async def summary(self, community_id: str) -> dict[str, Any]:
        """Get a community summary."""
        client = await self._dt._get_client()
        result = await _summary.asyncio(community_id=community_id, client=client)
        data = _unwrap(result, f"summary({community_id})")
        if hasattr(data, "to_dict"):
            return data.to_dict()
        return data

    async def list_values(self, community_id: str) -> list[dict[str, Any]]:
        """List available value fetchers for a community."""
        client = await self._dt._get_client()
        result = await _list_values.asyncio(community_id=community_id, client=client)
        return _unwrap(result, f"list_values({community_id})")

    async def get_value(
        self,
        community_id: str,
        fetcher_id: str,
        **params: Any,
    ) -> dict[str, Any]:
        """Fetch a value using query-string parameters.

        Args:
            community_id: Community entity ID.
            fetcher_id: Value fetcher identifier.
            **params: Query parameters passed to the fetcher.
        """
        client = await self._dt._get_client()
        result = await _get_value.asyncio(
            community_id=community_id,
            fetcher_id=fetcher_id,
            client=client,
        )
        return _unwrap(result, f"get_value({community_id}, {fetcher_id})")

    async def post_value(
        self,
        community_id: str,
        fetcher_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Fetch a value using a JSON payload (POST).

        Args:
            community_id: Community entity ID.
            fetcher_id: Value fetcher identifier.
            payload: Request payload dict.
        """
        client = await self._dt._get_client()
        body = ValuesRequest(payload=Payload.from_dict(payload))
        result = await _post_value.asyncio(
            community_id=community_id,
            fetcher_id=fetcher_id,
            client=client,
            body=body,
        )
        return _unwrap(result, f"post_value({community_id}, {fetcher_id})")

    async def describe_value(
        self,
        community_id: str,
        fetcher_id: str,
    ) -> dict[str, Any]:
        """Describe a value fetcher's schema and metadata."""
        client = await self._dt._get_client()
        result = await _describe_value.asyncio(
            community_id=community_id,
            fetcher_id=fetcher_id,
            client=client,
        )
        return _unwrap(result, f"describe_value({community_id}, {fetcher_id})")

    async def list_simulations(self, community_id: str) -> list[dict[str, Any]]:
        """List available simulations for a community."""
        client = await self._dt._get_client()
        result = await _list_sims.asyncio(community_id=community_id, client=client)
        return _unwrap(result, f"list_simulations({community_id})")

    async def describe_simulation(
        self,
        community_id: str,
        sim_key: str,
    ) -> dict[str, Any]:
        """Describe a simulation's parameters and configuration."""
        client = await self._dt._get_client()
        result = await _describe_sim.asyncio(
            community_id=community_id,
            sim_key=sim_key,
            client=client,
        )
        return _unwrap(result, f"describe_simulation({community_id}, {sim_key})")
