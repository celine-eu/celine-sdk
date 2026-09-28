from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.community_detail import CommunityDetail
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    node_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/admin/communities/{community_key}/topology/{node_id}".format(
            community_key=quote(str(community_key), safe=""),
            node_id=quote(str(node_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommunityDetail | ErrorResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CommunityDetail.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CommunityDetail | ErrorResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CommunityDetail | ErrorResponse | HTTPValidationError]:
    """Delete Topology Node

     Remove one topology node, unless something still references it (REQ-0072).

    A node an area lists is `409 topology_node_in_use`, naming the areas —
    whether or not those areas keep the one-substation rule — so the areas are
    changed or deleted first. So is a node another node names as its
    `parent`, naming those nodes by id, so they are re-parented or deleted
    first. A node the community does not have is `404`.

    Args:
        community_key (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        node_id=node_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CommunityDetail | ErrorResponse | HTTPValidationError | None:
    """Delete Topology Node

     Remove one topology node, unless something still references it (REQ-0072).

    A node an area lists is `409 topology_node_in_use`, naming the areas —
    whether or not those areas keep the one-substation rule — so the areas are
    changed or deleted first. So is a node another node names as its
    `parent`, naming those nodes by id, so they are re-parented or deleted
    first. A node the community does not have is `404`.

    Args:
        community_key (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | ErrorResponse | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        node_id=node_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CommunityDetail | ErrorResponse | HTTPValidationError]:
    """Delete Topology Node

     Remove one topology node, unless something still references it (REQ-0072).

    A node an area lists is `409 topology_node_in_use`, naming the areas —
    whether or not those areas keep the one-substation rule — so the areas are
    changed or deleted first. So is a node another node names as its
    `parent`, naming those nodes by id, so they are re-parented or deleted
    first. A node the community does not have is `404`.

    Args:
        community_key (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        node_id=node_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> CommunityDetail | ErrorResponse | HTTPValidationError | None:
    """Delete Topology Node

     Remove one topology node, unless something still references it (REQ-0072).

    A node an area lists is `409 topology_node_in_use`, naming the areas —
    whether or not those areas keep the one-substation rule — so the areas are
    changed or deleted first. So is a node another node names as its
    `parent`, naming those nodes by id, so they are re-parented or deleted
    first. A node the community does not have is `404`.

    Args:
        community_key (str):
        node_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | ErrorResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            node_id=node_id,
            client=client,
        )
    ).parsed
