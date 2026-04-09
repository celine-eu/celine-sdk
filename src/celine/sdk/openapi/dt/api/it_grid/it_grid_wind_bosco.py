from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_it_grid_wind_bosco import ResponseItGridWindBosco
from ...types import UNSET, Response, Unset


def _get_kwargs(
    network_id: str,
    *,
    dates: list[str] | None | Unset = UNSET,
    operational_unit: list[str] | None | Unset = UNSET,
    line_name: list[str] | None | Unset = UNSET,
    substation_name: list[str] | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_dates: list[str] | None | Unset
    if isinstance(dates, Unset):
        json_dates = UNSET
    elif isinstance(dates, list):
        json_dates = dates

    else:
        json_dates = dates
    params["dates"] = json_dates

    json_operational_unit: list[str] | None | Unset
    if isinstance(operational_unit, Unset):
        json_operational_unit = UNSET
    elif isinstance(operational_unit, list):
        json_operational_unit = operational_unit

    else:
        json_operational_unit = operational_unit
    params["operational_unit"] = json_operational_unit

    json_line_name: list[str] | None | Unset
    if isinstance(line_name, Unset):
        json_line_name = UNSET
    elif isinstance(line_name, list):
        json_line_name = line_name

    else:
        json_line_name = line_name
    params["line_name"] = json_line_name

    json_substation_name: list[str] | None | Unset
    if isinstance(substation_name, Unset):
        json_substation_name = UNSET
    elif isinstance(substation_name, list):
        json_substation_name = substation_name

    else:
        json_substation_name = substation_name
    params["substation_name"] = json_substation_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid/{network_id}/wind/bosco".format(
            network_id=quote(str(network_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseItGridWindBosco | None:
    if response.status_code == 200:
        response_200 = ResponseItGridWindBosco.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ResponseItGridWindBosco]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    network_id: str,
    *,
    client: AuthenticatedClient | Client,
    dates: list[str] | None | Unset = UNSET,
    operational_unit: list[str] | None | Unset = UNSET,
    line_name: list[str] | None | Unset = UNSET,
    substation_name: list[str] | None | Unset = UNSET,
) -> Response[HTTPValidationError | ResponseItGridWindBosco]:
    """Wind Bosco

     GeoJSON FeatureCollection of overhead segments in vegetated zones, coloured by wind risk.

    Args:
        network_id (str):
        dates (list[str] | None | Unset):
        operational_unit (list[str] | None | Unset):
        line_name (list[str] | None | Unset):
        substation_name (list[str] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseItGridWindBosco]
    """

    kwargs = _get_kwargs(
        network_id=network_id,
        dates=dates,
        operational_unit=operational_unit,
        line_name=line_name,
        substation_name=substation_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    network_id: str,
    *,
    client: AuthenticatedClient | Client,
    dates: list[str] | None | Unset = UNSET,
    operational_unit: list[str] | None | Unset = UNSET,
    line_name: list[str] | None | Unset = UNSET,
    substation_name: list[str] | None | Unset = UNSET,
) -> HTTPValidationError | ResponseItGridWindBosco | None:
    """Wind Bosco

     GeoJSON FeatureCollection of overhead segments in vegetated zones, coloured by wind risk.

    Args:
        network_id (str):
        dates (list[str] | None | Unset):
        operational_unit (list[str] | None | Unset):
        line_name (list[str] | None | Unset):
        substation_name (list[str] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseItGridWindBosco
    """

    return sync_detailed(
        network_id=network_id,
        client=client,
        dates=dates,
        operational_unit=operational_unit,
        line_name=line_name,
        substation_name=substation_name,
    ).parsed


async def asyncio_detailed(
    network_id: str,
    *,
    client: AuthenticatedClient | Client,
    dates: list[str] | None | Unset = UNSET,
    operational_unit: list[str] | None | Unset = UNSET,
    line_name: list[str] | None | Unset = UNSET,
    substation_name: list[str] | None | Unset = UNSET,
) -> Response[HTTPValidationError | ResponseItGridWindBosco]:
    """Wind Bosco

     GeoJSON FeatureCollection of overhead segments in vegetated zones, coloured by wind risk.

    Args:
        network_id (str):
        dates (list[str] | None | Unset):
        operational_unit (list[str] | None | Unset):
        line_name (list[str] | None | Unset):
        substation_name (list[str] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseItGridWindBosco]
    """

    kwargs = _get_kwargs(
        network_id=network_id,
        dates=dates,
        operational_unit=operational_unit,
        line_name=line_name,
        substation_name=substation_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    network_id: str,
    *,
    client: AuthenticatedClient | Client,
    dates: list[str] | None | Unset = UNSET,
    operational_unit: list[str] | None | Unset = UNSET,
    line_name: list[str] | None | Unset = UNSET,
    substation_name: list[str] | None | Unset = UNSET,
) -> HTTPValidationError | ResponseItGridWindBosco | None:
    """Wind Bosco

     GeoJSON FeatureCollection of overhead segments in vegetated zones, coloured by wind risk.

    Args:
        network_id (str):
        dates (list[str] | None | Unset):
        operational_unit (list[str] | None | Unset):
        line_name (list[str] | None | Unset):
        substation_name (list[str] | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseItGridWindBosco
    """

    return (
        await asyncio_detailed(
            network_id=network_id,
            client=client,
            dates=dates,
            operational_unit=operational_unit,
            line_name=line_name,
            substation_name=substation_name,
        )
    ).parsed
