# celine/sdk/dt/grid.py
"""
GridClient — curated async wrapper for the it_grid domain.

Covers the grid resilience endpoints: substations_map, filters, the value fetchers
(tile_index, shapes, risks, risks_now, trendline, and fetch_values for the others),
summary and get_info. Every call is about one network: the DT answers only the rows
of the distribution operator whose organisation alias is ``network_id``.
"""
from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

from celine.sdk.dt.util import unwrap, DTApiError, log_refusal

from celine.sdk.openapi.dt.models import (
    HTTPValidationError,
    ValuesRequestSchema,
    GenericPayload,
    FetchResultSchema,
)
from celine.sdk.openapi.dt.models.summary_response_schema import SummaryResponseSchema
from celine.sdk.openapi.dt.models.response_it_grid_it_grid_substations_map import (
    ResponseItGridItGridSubstationsMap,
)
from celine.sdk.openapi.dt.api.it_grid import (
    it_grid_get_summary as _summary,
    it_grid_get_info as _info,
    it_grid_it_grid_substations_map as _substations_map,
    # Generated after `task gen` once DT ValueFetcherSpecs are deployed:
    it_grid_fetch_values_post as _post_value,
    it_grid_list_values as _list_values,
)

if TYPE_CHECKING:
    from celine.sdk.dt.client import DTClient

logger = logging.getLogger(__name__)


class GridClient:
    """Async client for the IT Grid resilience DT domain.

    Not instantiated directly — use ``DTClient.grid``.

    Usage::

        shapes = await dt.grid.shapes("example-dso")
        risks = await dt.grid.risks("example-dso", dates=["2026-04-08"])
    """

    def __init__(self, dt: DTClient) -> None:
        self._dt = dt

    # ------------------------------------------------------------------
    # Substations (CIM: Substation — secondary substations)
    # ------------------------------------------------------------------

    async def substations_map(self, network_id: str) -> dict[str, Any]:
        """GeoJSON FeatureCollection of all secondary substations."""
        client = await self._dt._get_client()
        result = await _substations_map.asyncio_detailed(
            network_id=network_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return data.to_dict()

    # ------------------------------------------------------------------
    # Filter metadata
    # ------------------------------------------------------------------

    async def filters(self, network_id: str) -> dict[str, Any]:
        """Distinct topology values + network bounding box for UI initialisation.

        Returns parent_substations, lines, operational_units, municipalities
        and extent_min/max_lng/lat sourced from grid_shapes.
        """
        result = await self.fetch_values(network_id, "filters", limit=1)
        return result.items[0].to_dict() if result.items else {
            "parent_substations": [],
            "lines": [],
            "operational_units": [],
            "municipalities": [],
            "extent_min_lng": None,
            "extent_min_lat": None,
            "extent_max_lng": None,
            "extent_max_lat": None,
        }

    # ------------------------------------------------------------------
    # ValueFetcherSpec — shapes / risks / trendline
    # ------------------------------------------------------------------

    async def fetch_values(
        self,
        network_id: str,
        fetcher_id: str,
        payload: dict[str, Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> FetchResultSchema:
        """Generic values fetcher — delegates to POST /values/{fetcher_id}."""
        client = await self._dt._get_client()
        p: dict[str, Any] = dict(payload or {})
        if limit is not None:
            p["limit"] = limit
        if offset is not None:
            p["offset"] = offset
        body = ValuesRequestSchema(payload=GenericPayload.from_dict(p))
        result = await _post_value.asyncio_detailed(
            network_id=network_id,
            fetcher_id=fetcher_id,
            client=client,
            body=body,
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            log_refusal(logger, f"fetcher {fetcher_id}", result, data)
            raise DTApiError("Validation error", 500)
        return data

    async def tile_index(self, network_id: str) -> FetchResultSchema:
        """Tile catalog for progressive shape loading.

        Returns one row per 5 km tile with bbox polygon and segment count.
        """
        return await self.fetch_values(network_id, "tile_index", limit=500)

    async def shapes(
        self,
        network_id: str,
        *,
        asset_type: list[str] | None = None,
        tile_ids: list[str] | None = None,
    ) -> FetchResultSchema:
        """Static CIM asset topology — geometry only, no risk properties.

        Load once per session; topology changes on monthly cadence only.
        Pass tile_ids for progressive loading (e.g. ["tile_0_3", "tile_1_3"]).
        """
        payload: dict[str, Any] = {}
        if asset_type:
            payload["asset_type"] = asset_type
        if tile_ids:
            payload["tile_ids"] = tile_ids
        return await self.fetch_values(network_id, "shapes", payload, limit=10000)

    async def risks(
        self,
        network_id: str,
        *,
        dates: list[str],
        risk_vector: list[str] | None = None,
    ) -> FetchResultSchema:
        """WARNING/ALERT risk rows for the given dates.

        Returns segment_id + risk metadata only — no geometry.
        Frontend joins against cached shapes by segment_id.
        """
        payload: dict[str, Any] = {"dates": dates}
        if risk_vector:
            payload["risk_vector"] = risk_vector
        return await self.fetch_values(network_id, "risks", payload, limit=10000)

    async def risks_now(
        self,
        network_id: str,
        *,
        risk_vector: list[str] | None = None,
    ) -> FetchResultSchema:
        """Nowcasting risk rows — current observations, no date filter.

        Same schema as risks() but sourced from the nowcasting table.
        """
        payload: dict[str, Any] = {}
        if risk_vector:
            payload["risk_vector"] = risk_vector
        return await self.fetch_values(network_id, "risks_now", payload, limit=10000)

    async def trendline(
        self,
        network_id: str,
        *,
        date_from: str,
        date_to: str,
        risk_vector: list[str] | None = None,
    ) -> FetchResultSchema:
        """Daily risk percentage indicator per vector.

        Powers sparkline charts and the day-level risk badge.
        """
        payload: dict[str, Any] = {"date_from": date_from, "date_to": date_to}
        if risk_vector:
            payload["risk_vector"] = risk_vector
        return await self.fetch_values(network_id, "trendline", payload)

    # ------------------------------------------------------------------
    # Summary / info
    # ------------------------------------------------------------------

    async def summary(self, network_id: str) -> dict[str, Any]:
        """Network-level summary (risk counts, last update timestamp)."""
        client = await self._dt._get_client()
        result = await _summary.asyncio_detailed(network_id=network_id, client=client)
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return data.to_dict()
