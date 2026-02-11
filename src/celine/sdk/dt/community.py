# celine/sdk/dt/community.py
"""
CommunityClient — curated async wrapper for the it_energy_community domain.

All methods delegate to the generated ``celine.sdk.openapi.dt.api.it_energy_community``
module functions. Error handling converts generated error types into clean exceptions.
"""
from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

from celine.sdk.dt.util import unwrap, DTApiError
from celine.sdk.openapi.dt.models.describe_response_schema import DescribeResponseSchema
from celine.sdk.openapi.dt.models.generic_payload import GenericPayload
from celine.sdk.openapi.dt.models.simulation_descriptor_schema import (
    SimulationDescriptorSchema,
)
from celine.sdk.openapi.dt.models.value_descriptor_schema import ValueDescriptorSchema
from celine.sdk.openapi.dt.models.value_response_schema import ValueResponseSchema
from celine.sdk.openapi.dt.models.values_request_schema import ValuesRequestSchema
from celine.sdk.openapi.dt.types import UNSET

from celine.sdk.openapi.dt.models import (
    HTTPValidationError,
    ResponseItEnergyCommunityGetInfo,
)
from celine.sdk.openapi.dt.api.it_energy_community import (
    it_energy_community_energy_balance as _energy_balance,
    it_energy_community_energy_balance_hourly as _energy_balance_hourly,
    it_energy_community_get_info as _info,
    it_energy_community_list_values as _list_values,
    it_energy_community_get_value as _get_value,
    it_energy_community_post_value as _post_value,
    it_energy_community_describe_value as _describe_value,
    it_energy_community_list_simulations as _list_simulations,
    it_energy_community_describe_simulation as _describe_simulations,
)


if TYPE_CHECKING:
    from celine.sdk.dt.client import DTClient

logger = logging.getLogger(__name__)


class CommunityClient:
    """Async client for the Italian Energy Community DT domain.

    Not instantiated directly — use ``DTClient.communities``.
    """

    def __init__(self, dt: DTClient) -> None:
        self._dt = dt

    async def info(self, community_id: str) -> ResponseItEnergyCommunityGetInfo:
        """Get domain info and available capabilities for a community."""
        client = await self._dt._get_client()
        result = await _info.asyncio_detailed(community_id=community_id, client=client)
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

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
        result = await _energy_balance.asyncio_detailed(
            community_id=community_id,
            client=client,
            start=start if start else UNSET,
            end=end if end else UNSET,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def list_values(self, community_id: str) -> list[ValueDescriptorSchema]:
        """List available value fetchers for a participant."""
        client = await self._dt._get_client()
        result = await _list_values.asyncio_detailed(
            community_id=community_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def get_value(
        self,
        community_id: str,
        fetcher_id: str,
        **params: Any,
    ) -> ValueResponseSchema:
        """Fetch a value using query-string parameters.

        Args:
            participant_id: Participant entity ID.
            fetcher_id: Value fetcher identifier.
            **params: Query parameters passed to the fetcher.
        """
        client = await self._dt._get_client()
        result = await _get_value.asyncio_detailed(
            community_id=community_id,
            fetcher_id=fetcher_id,
            client=client,
            **params,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def post_value(
        self,
        community_id: str,
        fetcher_id: str,
        payload: dict[str, Any],
    ) -> ValueResponseSchema:
        """Fetch a value using a JSON payload (POST)."""
        client = await self._dt._get_client()
        body = ValuesRequestSchema(payload=GenericPayload.from_dict(payload))
        result = await _post_value.asyncio_detailed(
            community_id=community_id,
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
        community_id: str,
        fetcher_id: str,
    ) -> DescribeResponseSchema:
        """Describe a value fetcher's schema and metadata."""
        client = await self._dt._get_client()
        result = await _describe_value.asyncio_detailed(
            community_id=community_id,
            fetcher_id=fetcher_id,
            client=client,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def list_simulations(
        self, community_id: str
    ) -> list[SimulationDescriptorSchema]:
        """List available simulations for a participant."""
        client = await self._dt._get_client()
        result = await _list_simulations.asyncio_detailed(
            community_id=community_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def describe_simulation(
        self,
        community_id: str,
        sim_key: str,
    ) -> DescribeResponseSchema:
        """Describe a simulation's parameters and configuration."""
        client = await self._dt._get_client()
        result = await _describe_simulations.asyncio_detailed(
            community_id=community_id,
            sim_key=sim_key,
            client=client,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data
