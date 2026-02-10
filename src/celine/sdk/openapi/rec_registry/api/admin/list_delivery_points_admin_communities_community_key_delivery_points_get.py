from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_response_delivery_point_with_owner import PaginatedResponseDeliveryPointWithOwner
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community_key: str,
    *,
    type_: None | str | Unset = UNSET,
    active: bool | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_type_: None | str | Unset
    if isinstance(type_, Unset):
        json_type_ = UNSET
    else:
        json_type_ = type_
    params["type"] = json_type_

    json_active: bool | None | Unset
    if isinstance(active, Unset):
        json_active = UNSET
    else:
        json_active = active
    params["active"] = json_active

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
        "url": "/admin/communities/{community_key}/delivery-points".format(
            community_key=quote(str(community_key), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginatedResponseDeliveryPointWithOwner | None:
    if response.status_code == 200:
        response_200 = PaginatedResponseDeliveryPointWithOwner.from_dict(response.json())

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
) -> Response[HTTPValidationError | PaginatedResponseDeliveryPointWithOwner]:
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
    type_: None | str | Unset = UNSET,
    active: bool | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseDeliveryPointWithOwner]:
    """List Delivery Points

     List all delivery points in a community.

    Args:
        community_key (str):
        type_ (None | str | Unset): Filter by type
        active (bool | None | Unset): Filter by active status
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseDeliveryPointWithOwner]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        type_=type_,
        active=active,
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
    type_: None | str | Unset = UNSET,
    active: bool | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseDeliveryPointWithOwner | None:
    """List Delivery Points

     List all delivery points in a community.

    Args:
        community_key (str):
        type_ (None | str | Unset): Filter by type
        active (bool | None | Unset): Filter by active status
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseDeliveryPointWithOwner
    """

    return sync_detailed(
        community_key=community_key,
        client=client,
        type_=type_,
        active=active,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    type_: None | str | Unset = UNSET,
    active: bool | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginatedResponseDeliveryPointWithOwner]:
    """List Delivery Points

     List all delivery points in a community.

    Args:
        community_key (str):
        type_ (None | str | Unset): Filter by type
        active (bool | None | Unset): Filter by active status
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginatedResponseDeliveryPointWithOwner]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        type_=type_,
        active=active,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    type_: None | str | Unset = UNSET,
    active: bool | None | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginatedResponseDeliveryPointWithOwner | None:
    """List Delivery Points

     List all delivery points in a community.

    Args:
        community_key (str):
        type_ (None | str | Unset): Filter by type
        active (bool | None | Unset): Filter by active status
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset): Pagination cursor

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginatedResponseDeliveryPointWithOwner
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            client=client,
            type_=type_,
            active=active,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
