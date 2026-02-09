# celine/sdk/dt/participant.py
"""
ParticipantClient — curated async wrapper for the it_participant domain.
"""
from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

from celine.sdk.openapi.dt.api.it_participant import (
    it_participant_get_value as _get_value,
    it_participant_post_value as _post_value,
    it_participant_info as _info,
    it_participant_list_values as _list_values,
    it_participant_list_simulations as _list_sims,
    it_participant_describe_value as _describe_value,
    it_participant_describe_simulation as _describe_sim,
    participant_profile_participants_participant_id_profile_get as _profile,
    flexibility_participants_participant_id_flexibility_get as _flexibility,
)
from celine.sdk.openapi.dt.models import ValuesRequest, Payload
from celine.sdk.openapi.dt.models.http_validation_error import HTTPValidationError
from celine.sdk.openapi.dt.types import UNSET

from celine.sdk.dt.community import DTApiError, _unwrap

if TYPE_CHECKING:
    from celine.sdk.dt.client import DTClient

logger = logging.getLogger(__name__)


class ParticipantClient:
    """Async client for the Italian Participant DT domain.

    Not instantiated directly — use ``DTClient.participants``.
    """

    def __init__(self, dt: DTClient) -> None:
        self._dt = dt

    async def info(self, participant_id: str) -> dict[str, Any]:
        client = await self._dt._get_client()
        result = await _info.asyncio(participant_id=participant_id, client=client)
        return _unwrap(result, f"info({participant_id})")

    async def profile(self, participant_id: str) -> dict[str, Any]:
        """Get the participant profile."""
        client = await self._dt._get_client()
        result = await _profile.asyncio(participant_id=participant_id, client=client)
        data = _unwrap(result, f"profile({participant_id})")
        if hasattr(data, "to_dict"):
            return data.to_dict()
        return data

    async def flexibility(self, participant_id: str) -> dict[str, Any]:
        """Get the participant flexibility status."""
        client = await self._dt._get_client()
        result = await _flexibility.asyncio(
            participant_id=participant_id, client=client
        )
        data = _unwrap(result, f"flexibility({participant_id})")
        if hasattr(data, "to_dict"):
            return data.to_dict()
        return data

    async def list_values(self, participant_id: str) -> list[dict[str, Any]]:
        """List available value fetchers for a participant."""
        client = await self._dt._get_client()
        result = await _list_values.asyncio(
            participant_id=participant_id, client=client
        )
        return _unwrap(result, f"list_values({participant_id})")

    async def get_value(
        self,
        participant_id: str,
        fetcher_id: str,
        **params: Any,
    ) -> dict[str, Any]:
        """Fetch a value using query-string parameters.

        Args:
            participant_id: Participant entity ID.
            fetcher_id: Value fetcher identifier.
            **params: Query parameters passed to the fetcher.
        """
        client = await self._dt._get_client()
        result = await _get_value.asyncio(
            participant_id=participant_id,
            fetcher_id=fetcher_id,
            client=client,
        )
        return _unwrap(result, f"get_value({participant_id}, {fetcher_id})")

    async def post_value(
        self,
        participant_id: str,
        fetcher_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Fetch a value using a JSON payload (POST)."""
        client = await self._dt._get_client()
        body = ValuesRequest(payload=Payload.from_dict(payload))
        result = await _post_value.asyncio(
            participant_id=participant_id,
            fetcher_id=fetcher_id,
            client=client,
            body=body,
        )
        return _unwrap(result, f"post_value({participant_id}, {fetcher_id})")

    async def describe_value(
        self,
        participant_id: str,
        fetcher_id: str,
    ) -> dict[str, Any]:
        """Describe a value fetcher's schema and metadata."""
        client = await self._dt._get_client()
        result = await _describe_value.asyncio(
            participant_id=participant_id,
            fetcher_id=fetcher_id,
            client=client,
        )
        return _unwrap(result, f"describe_value({participant_id}, {fetcher_id})")

    async def list_simulations(self, participant_id: str) -> list[dict[str, Any]]:
        """List available simulations for a participant."""
        client = await self._dt._get_client()
        result = await _list_sims.asyncio(participant_id=participant_id, client=client)
        return _unwrap(result, f"list_simulations({participant_id})")

    async def describe_simulation(
        self,
        participant_id: str,
        sim_key: str,
    ) -> dict[str, Any]:
        """Describe a simulation's parameters and configuration."""
        client = await self._dt._get_client()
        result = await _describe_sim.asyncio(
            participant_id=participant_id,
            sim_key=sim_key,
            client=client,
        )
        return _unwrap(result, f"describe_simulation({participant_id}, {sim_key})")
