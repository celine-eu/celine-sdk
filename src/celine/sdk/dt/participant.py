# celine/sdk/dt/participant.py
"""
ParticipantClient — curated async wrapper for the it_participant domain.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from celine.sdk.dt.community import unwrap

from celine.sdk.dt.util import DTApiError
from celine.sdk.openapi.dt.types import UNSET

from celine.sdk.openapi.dt.models import (
    UserMeResponseSchema,
    ValueDescriptorSchema,
    HTTPValidationError,
    DescribeResponseSchema,
    FetchResultSchema,
    ValuesRequestSchema,
    GenericPayload,
    SimulationDescriptorSchema,
    UserAssetsResponseSchema,
)
from celine.sdk.openapi.dt.api.it_participant import (
    it_participant_profile as _profile,
    it_participant_assets as _assets,
    it_participant_list_values as _list_values,
    it_participant_fetch_values_post as _post_value,
    it_participant_describe_value as _describe_value,
    it_participant_list_simulations as _list_simulations,
    it_participant_describe_simulation as _describe_simulations,
)

if TYPE_CHECKING:
    from celine.sdk.dt.client import DTClient

logger = logging.getLogger(__name__)


class ParticipantClient:
    """Async client for the Italian Participant DT domain.

    Not instantiated directly — use ``DTClient.participants``.
    """

    def __init__(self, dt: DTClient) -> None:
        self._dt = dt

    async def profile(self, participant_id: str) -> UserMeResponseSchema:
        """Get the participant profile."""
        client = await self._dt._get_client()
        result = await _profile.asyncio_detailed(
            participant_id=participant_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def assets(self, participant_id: str) -> UserAssetsResponseSchema:
        """Get the participant assets."""
        client = await self._dt._get_client()
        result = await _assets.asyncio_detailed(
            participant_id=participant_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def list_values(self, participant_id: str) -> list[ValueDescriptorSchema]:
        """List available value fetchers for a participant."""
        client = await self._dt._get_client()
        result = await _list_values.asyncio_detailed(
            participant_id=participant_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def fetch_values(
        self,
        participant_id: str,
        fetcher_id: str,
        payload: dict[str, Any] = {},
        limit: int | None = None,
        offset: int = 0,
    ) -> FetchResultSchema:
        """Fetch a value using a JSON payload (POST)."""
        client = await self._dt._get_client()

        if limit is not None:
            payload["limit"] = limit
        if offset is not None:
            payload["offset"] = offset

        body = ValuesRequestSchema(payload=GenericPayload.from_dict(payload))
        result = await _post_value.asyncio_detailed(
            participant_id=participant_id,
            fetcher_id=fetcher_id,
            client=client,
            body=body,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def describe_value(
        self,
        participant_id: str,
        fetcher_id: str,
    ) -> ValueDescriptorSchema:
        """Describe a value fetcher's schema and metadata."""
        client = await self._dt._get_client()
        result = await _describe_value.asyncio_detailed(
            participant_id=participant_id,
            fetcher_id=fetcher_id,
            client=client,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def list_simulations(
        self, participant_id: str
    ) -> list[SimulationDescriptorSchema]:
        """List available simulations for a participant."""
        client = await self._dt._get_client()
        result = await _list_simulations.asyncio_detailed(
            participant_id=participant_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def describe_simulation(
        self,
        participant_id: str,
        sim_key: str,
    ) -> DescribeResponseSchema:
        """Describe a simulation's parameters and configuration."""
        client = await self._dt._get_client()
        result = await _describe_simulations.asyncio_detailed(
            participant_id=participant_id,
            sim_key=sim_key,
            client=client,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data
