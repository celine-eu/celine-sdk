from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.describe_response_schema import DescribeResponseSchema
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_id: str,
    sim_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/communities/it/{community_id}/simulations/{sim_key}/describe".format(
            community_id=quote(str(community_id), safe=""),
            sim_key=quote(str(sim_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DescribeResponseSchema | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DescribeResponseSchema.from_dict(response.json())

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
) -> Response[DescribeResponseSchema | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_id: str,
    sim_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DescribeResponseSchema | HTTPValidationError]:
    """Describe Simulation

    Args:
        community_id (str):
        sim_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DescribeResponseSchema | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
        sim_key=sim_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_id: str,
    sim_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> DescribeResponseSchema | HTTPValidationError | None:
    """Describe Simulation

    Args:
        community_id (str):
        sim_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DescribeResponseSchema | HTTPValidationError
    """

    return sync_detailed(
        community_id=community_id,
        sim_key=sim_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    community_id: str,
    sim_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DescribeResponseSchema | HTTPValidationError]:
    """Describe Simulation

    Args:
        community_id (str):
        sim_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DescribeResponseSchema | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
        sim_key=sim_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_id: str,
    sim_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> DescribeResponseSchema | HTTPValidationError | None:
    """Describe Simulation

    Args:
        community_id (str):
        sim_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DescribeResponseSchema | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_id=community_id,
            sim_key=sim_key,
            client=client,
        )
    ).parsed
