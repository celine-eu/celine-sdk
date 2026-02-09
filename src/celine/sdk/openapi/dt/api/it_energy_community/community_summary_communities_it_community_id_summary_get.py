from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_community_summary_communities_it_community_id_summary_get import (
    ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet,
)
from ...types import Response


def _get_kwargs(
    community_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/communities/it/{community_id}/summary".format(
            community_id=quote(str(community_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet | None:
    if response.status_code == 200:
        response_200 = ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet]:
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
) -> Response[HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet]:
    """Community Summary

     High-level community summary.

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet]
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
) -> HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet | None:
    """Community Summary

     High-level community summary.

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet
    """

    return sync_detailed(
        community_id=community_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet]:
    """Community Summary

     High-level community summary.

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet]
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
) -> HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet | None:
    """Community Summary

     High-level community summary.

    Args:
        community_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseCommunitySummaryCommunitiesItCommunityIdSummaryGet
    """

    return (
        await asyncio_detailed(
            community_id=community_id,
            client=client,
        )
    ).parsed
