from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_scenarios_simulations_simulation_key_scenarios_get_response_200_item import (
    ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    simulation_key: str,
    *,
    include_expired: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_expired"] = include_expired

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/simulations/{simulation_key}/scenarios".format(
            simulation_key=quote(str(simulation_key), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item.from_dict(
                response_200_item_data
            )

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
    include_expired: bool | Unset = False,
) -> Response[HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item]]:
    """List Scenarios

    Args:
        simulation_key (str):
        include_expired (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item]]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
        include_expired=include_expired,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
    include_expired: bool | Unset = False,
) -> HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item] | None:
    """List Scenarios

    Args:
        simulation_key (str):
        include_expired (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item]
    """

    return sync_detailed(
        simulation_key=simulation_key,
        client=client,
        include_expired=include_expired,
    ).parsed


async def asyncio_detailed(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
    include_expired: bool | Unset = False,
) -> Response[HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item]]:
    """List Scenarios

    Args:
        simulation_key (str):
        include_expired (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item]]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
        include_expired=include_expired,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
    include_expired: bool | Unset = False,
) -> HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item] | None:
    """List Scenarios

    Args:
        simulation_key (str):
        include_expired (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ListScenariosSimulationsSimulationKeyScenariosGetResponse200Item]
    """

    return (
        await asyncio_detailed(
            simulation_key=simulation_key,
            client=client,
            include_expired=include_expired,
        )
    ).parsed
