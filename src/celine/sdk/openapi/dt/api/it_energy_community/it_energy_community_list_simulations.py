from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.simulation_descriptor_schema import SimulationDescriptorSchema
from ...types import Response


def _get_kwargs(
    community_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/communities/it/{community_id}/simulations".format(
            community_id=quote(str(community_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[SimulationDescriptorSchema] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SimulationDescriptorSchema.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[SimulationDescriptorSchema]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[SimulationDescriptorSchema]]:
    """List Simulations

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[SimulationDescriptorSchema]]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[SimulationDescriptorSchema] | None:
    """List Simulations

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[SimulationDescriptorSchema]
    """

    return sync_detailed(
        community_id=community_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | list[SimulationDescriptorSchema]]:
    """List Simulations

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[SimulationDescriptorSchema]]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | list[SimulationDescriptorSchema] | None:
    """List Simulations

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[SimulationDescriptorSchema]
    """

    return (
        await asyncio_detailed(
            community_id=community_id,
            client=client,
        )
    ).parsed
