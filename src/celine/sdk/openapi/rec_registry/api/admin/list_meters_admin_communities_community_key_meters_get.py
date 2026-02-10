from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_meter_list_item import PaginatedResponseMeterListItem
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community_key: str,
    *,
    owner: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_owner: None | str | Unset
    if isinstance(owner, Unset):
        json_owner = UNSET
    else:
        json_owner = owner
    params["owner"] = json_owner

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/communities/{community_key}/meters".format(
            community_key=quote(str(community_key), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponseMeterListItem | None:
    if response.status_code == 200:
        response_200 = PaginatedResponseMeterListItem.from_dict(response.json())

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
) -> Response[HTTPValidationError | PaginatedResponseMeterListItem]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    owner: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseMeterListItem]:
    """List Meters

     List meters in a community.

    Args:
        community_key (str):
        owner (None | str | Unset): Filter by owner member key
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseMeterListItem]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        owner=owner,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    owner: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseMeterListItem | None:
    """List Meters

     List meters in a community.

    Args:
        community_key (str):
        owner (None | str | Unset): Filter by owner member key
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseMeterListItem
    """

    return sync_detailed(
        community_key=community_key,
        client=client,
        owner=owner,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    owner: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseMeterListItem]:
    """List Meters

     List meters in a community.

    Args:
        community_key (str):
        owner (None | str | Unset): Filter by owner member key
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseMeterListItem]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        owner=owner,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    owner: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseMeterListItem | None:
    """List Meters

     List meters in a community.

    Args:
        community_key (str):
        owner (None | str | Unset): Filter by owner member key
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseMeterListItem
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            client=client,
            owner=owner,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
