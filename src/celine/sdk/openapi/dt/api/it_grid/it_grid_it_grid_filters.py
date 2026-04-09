from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_it_grid_it_grid_filters import ResponseItGridItGridFilters
from ...types import Response


def _get_kwargs(
    network_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/grid/{network_id}/filters".format(
            network_id=quote(str(network_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseItGridItGridFilters | None:
    if response.status_code == 200:
        response_200 = ResponseItGridItGridFilters.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseItGridItGridFilters]:
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
) -> Response[HTTPValidationError | ResponseItGridItGridFilters]:
    """Get Filters

     Distinct topology values for UI filter autocomplete.

    Returns one object with four arrays — a single DB round-trip for all
    filter dimensions. Values come from silver_grid_ac_line_segment (via
    grid_network_topology), so filter options are always complete regardless
    of weather data availability.

    Args:
        network_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseItGridItGridFilters]
    """

    kwargs = _get_kwargs(
        network_id=network_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    network_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseItGridItGridFilters | None:
    """Get Filters

     Distinct topology values for UI filter autocomplete.

    Returns one object with four arrays — a single DB round-trip for all
    filter dimensions. Values come from silver_grid_ac_line_segment (via
    grid_network_topology), so filter options are always complete regardless
    of weather data availability.

    Args:
        network_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseItGridItGridFilters
    """

    return sync_detailed(
        network_id=network_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    network_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseItGridItGridFilters]:
    """Get Filters

     Distinct topology values for UI filter autocomplete.

    Returns one object with four arrays — a single DB round-trip for all
    filter dimensions. Values come from silver_grid_ac_line_segment (via
    grid_network_topology), so filter options are always complete regardless
    of weather data availability.

    Args:
        network_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseItGridItGridFilters]
    """

    kwargs = _get_kwargs(
        network_id=network_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    network_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseItGridItGridFilters | None:
    """Get Filters

     Distinct topology values for UI filter autocomplete.

    Returns one object with four arrays — a single DB round-trip for all
    filter dimensions. Values come from silver_grid_ac_line_segment (via
    grid_network_topology), so filter options are always complete regardless
    of weather data availability.

    Args:
        network_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseItGridItGridFilters
    """

    return (
        await asyncio_detailed(
            network_id=network_id,
            client=client,
        )
    ).parsed
