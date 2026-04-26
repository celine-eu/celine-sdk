# celine/sdk/dt/grid.py
"""
GridClient — curated async wrapper for the it_grid domain.

Covers all grid resilience endpoints:
  wind_map, wind_bosco, wind_alert_distribution, wind_trend
  heat_map, heat_alert_distribution, heat_trend
  summary, get_info
"""
from __future__ import annotations

import logging
from typing import Any, TYPE_CHECKING

from celine.sdk.dt.util import unwrap, DTApiError
from celine.sdk.openapi.dt.types import UNSET

from celine.sdk.openapi.dt.models import (
    HTTPValidationError,
    ValuesRequestSchema,
    GenericPayload,
    FetchResultSchema,
)
from celine.sdk.openapi.dt.models.response_it_grid_wind_map import ResponseItGridWindMap
from celine.sdk.openapi.dt.models.response_it_grid_wind_bosco import (
    ResponseItGridWindBosco,
)
from celine.sdk.openapi.dt.models.response_it_grid_heat_map import ResponseItGridHeatMap
from celine.sdk.openapi.dt.models.it_grid_wind_trend_response_200_item import (
    ItGridWindTrendResponse200Item,
)
from celine.sdk.openapi.dt.models.it_grid_heat_trend_response_200_item import (
    ItGridHeatTrendResponse200Item,
)
from celine.sdk.openapi.dt.models.it_grid_wind_alert_distribution_response_200_item import (
    ItGridWindAlertDistributionResponse200Item,
)
from celine.sdk.openapi.dt.models.it_grid_heat_alert_distribution_response_200_item import (
    ItGridHeatAlertDistributionResponse200Item,
)
from celine.sdk.openapi.dt.models.summary_response_schema import SummaryResponseSchema
from celine.sdk.openapi.dt.models.response_it_grid_it_grid_substations_map import (
    ResponseItGridItGridSubstationsMap,
)
from celine.sdk.openapi.dt.api.it_grid import (
    it_grid_wind_map as _wind_map,
    it_grid_wind_bosco as _wind_bosco,
    it_grid_wind_alert_distribution as _wind_alert_dist,
    it_grid_wind_trend as _wind_trend,
    it_grid_heat_map as _heat_map,
    it_grid_heat_alert_distribution as _heat_alert_dist,
    it_grid_heat_trend as _heat_trend,
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


def _opt(v: list[str] | None):
    """Convert None to UNSET for generated client params."""
    return UNSET if v is None else v


class GridClient:
    """Async client for the IT Grid resilience DT domain.

    Not instantiated directly — use ``DTClient.grid``.

    Usage::

        fc = await dt.grid.wind_map("default", dates=["2026-04-08"])
        trend = await dt.grid.wind_trend("default")
    """

    def __init__(self, dt: DTClient) -> None:
        self._dt = dt

    # ------------------------------------------------------------------
    # Wind
    # ------------------------------------------------------------------

    async def wind_map(
        self,
        network_id: str,
        *,
        dates: list[str] | None = None,
        operational_unit: list[str] | None = None,
        line_name: list[str] | None = None,
        substation_name: list[str] | None = None,
        risk_level: list[str] | None = None,
    ) -> dict[str, Any]:
        """GeoJSON FeatureCollection of overhead MT lines coloured by wind risk."""
        client = await self._dt._get_client()
        result = await _wind_map.asyncio_detailed(
            network_id=network_id,
            client=client,
            dates=_opt(dates),
            operational_unit=_opt(operational_unit),
            line_name=_opt(line_name),
            substation_name=_opt(substation_name),
            risk_level=_opt(risk_level),
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return data.to_dict()

    async def wind_bosco(
        self,
        network_id: str,
        *,
        dates: list[str] | None = None,
        operational_unit: list[str] | None = None,
        line_name: list[str] | None = None,
        substation_name: list[str] | None = None,
    ) -> dict[str, Any]:
        """GeoJSON FeatureCollection of vegetated route wind risk segments."""
        client = await self._dt._get_client()
        result = await _wind_bosco.asyncio_detailed(
            network_id=network_id,
            client=client,
            dates=_opt(dates),
            operational_unit=_opt(operational_unit),
            line_name=_opt(line_name),
            substation_name=_opt(substation_name),
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return data.to_dict()

    async def wind_alert_distribution(
        self,
        network_id: str,
        *,
        dates: list[str] | None = None,
        operational_unit: list[str] | None = None,
        line_name: list[str] | None = None,
        substation_name: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """COUNT of line-segment events per risk_level for wind."""
        client = await self._dt._get_client()
        result = await _wind_alert_dist.asyncio_detailed(
            network_id=network_id,
            client=client,
            dates=_opt(dates),
            operational_unit=_opt(operational_unit),
            line_name=_opt(line_name),
            substation_name=_opt(substation_name),
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return [item.to_dict() for item in data]

    async def wind_trend(self, network_id: str) -> list[dict[str, Any]]:
        """Daily MAX(gust_excess) over the rolling window now−1d → now+2d."""
        client = await self._dt._get_client()
        result = await _wind_trend.asyncio_detailed(
            network_id=network_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return [item.to_dict() for item in data]

    # ------------------------------------------------------------------
    # Heat
    # ------------------------------------------------------------------

    async def heat_map(
        self,
        network_id: str,
        *,
        dates: list[str] | None = None,
        operational_unit: list[str] | None = None,
        line_name: list[str] | None = None,
        substation_name: list[str] | None = None,
        risk_level: list[str] | None = None,
    ) -> dict[str, Any]:
        """GeoJSON FeatureCollection of underground MT cables coloured by heat risk."""
        client = await self._dt._get_client()
        result = await _heat_map.asyncio_detailed(
            network_id=network_id,
            client=client,
            dates=_opt(dates),
            operational_unit=_opt(operational_unit),
            line_name=_opt(line_name),
            substation_name=_opt(substation_name),
            risk_level=_opt(risk_level),
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return data.to_dict()

    async def heat_alert_distribution(
        self,
        network_id: str,
        *,
        dates: list[str] | None = None,
        operational_unit: list[str] | None = None,
        line_name: list[str] | None = None,
        substation_name: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """COUNT of line-segment events per risk_level for heat."""
        client = await self._dt._get_client()
        result = await _heat_alert_dist.asyncio_detailed(
            network_id=network_id,
            client=client,
            dates=_opt(dates),
            operational_unit=_opt(operational_unit),
            line_name=_opt(line_name),
            substation_name=_opt(substation_name),
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return [item.to_dict() for item in data]

    async def heat_trend(self, network_id: str) -> list[dict[str, Any]]:
        """Daily MAX(temp_max_c) over the rolling window now−3d → now+2d."""
        client = await self._dt._get_client()
        result = await _heat_trend.asyncio_detailed(
            network_id=network_id, client=client
        )
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return [item.to_dict() for item in data]

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
            logger.warning(data.detail)
            raise DTApiError("Validation error", 500)
        return data

    async def shapes(
        self,
        network_id: str,
        *,
        asset_type: list[str] | None = None,
    ) -> FetchResultSchema:
        """Static CIM asset topology — geometry only, no risk properties.

        Load once per session; topology changes on monthly cadence only.
        """
        payload: dict[str, Any] = {}
        if asset_type:
            payload["asset_type"] = asset_type
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
