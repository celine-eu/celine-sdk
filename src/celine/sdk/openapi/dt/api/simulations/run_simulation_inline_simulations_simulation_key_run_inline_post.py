from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_run_simulation_inline_simulations_simulation_key_run_inline_post import (
    ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost,
)
from ...models.run_inline_request import RunInlineRequest
from ...types import Response


def _get_kwargs(
    simulation_key: str,
    *,
    body: RunInlineRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/simulations/{simulation_key}/run-inline".format(
            simulation_key=quote(str(simulation_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost | None:
    if response.status_code == 200:
        response_200 = ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost]:
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
    body: RunInlineRequest,
) -> Response[HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost]:
    """Run Simulation Inline

    Args:
        simulation_key (str):
        body (RunInlineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost]
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
    body: RunInlineRequest,
) -> HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost | None:
    """Run Simulation Inline

    Args:
        simulation_key (str):
        body (RunInlineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost
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
    body: RunInlineRequest,
) -> Response[HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost]:
    """Run Simulation Inline

    Args:
        simulation_key (str):
        body (RunInlineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost]
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
    body: RunInlineRequest,
) -> HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost | None:
    """Run Simulation Inline

    Args:
        simulation_key (str):
        body (RunInlineRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseRunSimulationInlineSimulationsSimulationKeyRunInlinePost
    """

    return (
        await asyncio_detailed(
            simulation_key=simulation_key,
            client=client,
            body=body,
        )
    ).parsed
