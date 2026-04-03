# celine/sdk/dt/participant.py
"""
ParticipantClient — curated async wrapper for the it_participant domain.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

from celine.sdk.dt.community import unwrap

from celine.sdk.dt.util import DTApiError
from celine.sdk.openapi.dt.types import UNSET

from celine.sdk.openapi.dt.models import (
    UserMeResponseSchema,
    ValueDescriptorSchema,
    HTTPValidationError,
    FetchResultSchema,
    ValuesRequestSchema,
    GenericPayload,
    SimulationDescriptorSchema,
    UserAssetsResponseSchema,
    OntologySpecDescriptor,
    OntologyRequest,
    Payload,
    FlexibilityCommittedRequest,
)
from celine.sdk.openapi.dt.api.it_participant import (
    it_participant_profile as _profile,
    it_participant_assets as _assets,
    it_participant_list_values as _list_values,
    it_participant_fetch_values_post as _post_value,
    it_participant_describe_value as _describe_value,
    it_participant_list_simulations as _list_simulations,
    it_participant_list_ontology_specs as _list_ontology_specs,
    it_participant_fetch_ontology_get as _fetch_ontology_get,
    it_participant_fetch_ontology_post as _fetch_ontology_post,
    it_participant_flexibility_committed as _flexibility_committed,
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

    async def list_ontology_specs(
        self, participant_id: str
    ) -> list[OntologySpecDescriptor]:
        """List available ontology concept views for a participant."""
        client = await self._dt._get_client()
        result = await _list_ontology_specs.asyncio_detailed(
            participant_id=participant_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def flexibility_committed(
        self,
        participant_id: str,
        *,
        commitment_id: str,
        community_id: str,
        device_id: str,
        window_start: datetime,
        window_end: datetime,
        reward_points_estimated: int,
    ) -> None:
        """Publish a flexibility commitment event to the DT.

        The DT publishes the event to MQTT; the on_event handler settles it
        asynchronously using rec_virtual_consumption_per_device data.

        Returns when the DT has accepted the event (HTTP 202).
        """
        client = await self._dt._get_client()
        body = FlexibilityCommittedRequest(
            commitment_id=commitment_id,
            community_id=community_id,
            device_id=device_id,
            window_start=window_start,
            window_end=window_end,
            reward_points_estimated=reward_points_estimated,
        )
        result = await _flexibility_committed.asyncio_detailed(
            participant_id=participant_id,
            client=client,
            body=body,
        )
        unwrap(result)

    async def fetch_ontology(
        self,
        participant_id: str,
        spec_id: str,
        payload: dict[str, Any] | None = None,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> dict[str, Any]:
        """Fetch an ontology concept view as a JSON-LD document.

        Uses POST when a payload is provided, GET otherwise.

        Args:
            participant_id: Participant entity ID.
            spec_id: Ontology spec ID (e.g. ``"meters"``).
            payload: Optional parameters forwarded to the underlying fetchers.
            limit: Optional result limit per fetcher.
            offset: Optional pagination offset.

        Returns:
            JSON-LD document with ``@context`` and ``@graph``.
        """
        client = await self._dt._get_client()

        if payload:
            if limit is not None:
                payload["limit"] = limit
            if offset is not None:
                payload["offset"] = offset
            body = OntologyRequest(payload=Payload.from_dict(payload))
            result = await _fetch_ontology_post.asyncio_detailed(
                participant_id=participant_id,
                spec_id=spec_id,
                client=client,
                body=body,
            )
        else:
            result = await _fetch_ontology_get.asyncio_detailed(
                participant_id=participant_id,
                spec_id=spec_id,
                client=client,
                limit=limit if limit is not None else UNSET,
                offset=offset if offset is not None else UNSET,
            )

        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data
