from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_run_sweep_simulations_simulation_key_sweep_post import (
    ResponseRunSweepSimulationsSimulationKeySweepPost,
)
from ...models.sweep_request import SweepRequest
from ...types import Response


def _get_kwargs(
    simulation_key: str,
    *,
    body: SweepRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/simulations/{simulation_key}/sweep".format(
            simulation_key=quote(str(simulation_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost | None:
    if response.status_code == 200:
        response_200 = ResponseRunSweepSimulationsSimulationKeySweepPost.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost]:
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
    body: SweepRequest,
) -> Response[HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost]:
    """Run Sweep

    Args:
        simulation_key (str):
        body (SweepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SweepRequest,
) -> HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost | None:
    """Run Sweep

    Args:
        simulation_key (str):
        body (SweepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost
    """

    return sync_detailed(
        simulation_key=simulation_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SweepRequest,
) -> Response[HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost]:
    """Run Sweep

    Args:
        simulation_key (str):
        body (SweepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost]
    """

    kwargs = _get_kwargs(
        simulation_key=simulation_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    simulation_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: SweepRequest,
) -> HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost | None:
    """Run Sweep

    Args:
        simulation_key (str):
        body (SweepRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseRunSweepSimulationsSimulationKeySweepPost
    """

    return (
        await asyncio_detailed(
            simulation_key=simulation_key,
            client=client,
            body=body,
        )
    ).parsed
