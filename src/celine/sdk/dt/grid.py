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

from celine.sdk.openapi.dt.models import HTTPValidationError
from celine.sdk.openapi.dt.models.response_it_grid_wind_map import ResponseItGridWindMap
from celine.sdk.openapi.dt.models.response_it_grid_wind_bosco import ResponseItGridWindBosco
from celine.sdk.openapi.dt.models.response_it_grid_heat_map import ResponseItGridHeatMap
from celine.sdk.openapi.dt.models.it_grid_wind_trend_response_200_item import ItGridWindTrendResponse200Item
from celine.sdk.openapi.dt.models.it_grid_heat_trend_response_200_item import ItGridHeatTrendResponse200Item
from celine.sdk.openapi.dt.models.it_grid_wind_alert_distribution_response_200_item import ItGridWindAlertDistributionResponse200Item
from celine.sdk.openapi.dt.models.it_grid_heat_alert_distribution_response_200_item import ItGridHeatAlertDistributionResponse200Item
from celine.sdk.openapi.dt.models.summary_response_schema import SummaryResponseSchema
from celine.sdk.openapi.dt.models.response_it_grid_it_grid_substations_map import ResponseItGridItGridSubstationsMap
from celine.sdk.openapi.dt.models.response_it_grid_it_grid_filters import ResponseItGridItGridFilters

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
    it_grid_it_grid_filters as _filters,
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
        result = await _wind_trend.asyncio_detailed(network_id=network_id, client=client)
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
        result = await _heat_trend.asyncio_detailed(network_id=network_id, client=client)
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
        result = await _substations_map.asyncio_detailed(network_id=network_id, client=client)
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return data.to_dict()

    # ------------------------------------------------------------------
    # Filter metadata
    # ------------------------------------------------------------------

    async def filters(self, network_id: str) -> dict[str, list[str]]:
        """Distinct topology values for UI filter autocomplete.

        Returns parent_substations, lines, operational_units, municipalities.
        Sourced from grid_network_topology (monthly cadence) — always complete
        regardless of weather data availability.
        """
        client = await self._dt._get_client()
        result = await _filters.asyncio_detailed(network_id=network_id, client=client)
        data = unwrap(result)
        if isinstance(data, HTTPValidationError):
            raise DTApiError("Validation error from DT", 422)
        return data.to_dict()

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
