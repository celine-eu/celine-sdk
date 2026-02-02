from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_describe_simulation_simulations_simulation_key_describe_get import (
    ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet,
)
from ...types import Response


def _get_kwargs(
    simulation_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/simulations/{simulation_key}/describe".format(
            simulation_key=quote(str(simulation_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet | None:
    if response.status_code == 200:
        response_200 = ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet]:
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
) -> Response[HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet]:
    """Describe Simulation

    Args:
        simulation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet | None:
    """Describe Simulation

    Args:
        simulation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet
    """

    return sync_detailed(
        simulation_key=simulation_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet]:
    """Describe Simulation

    Args:
        simulation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet | None:
    """Describe Simulation

    Args:
        simulation_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseDescribeSimulationSimulationsSimulationKeyDescribeGet
    """

    return (
        await asyncio_detailed(
            simulation_key=simulation_key,
            client=client,
        )
    ).parsed
