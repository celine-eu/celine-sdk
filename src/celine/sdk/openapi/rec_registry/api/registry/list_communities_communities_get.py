from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_communities_communities_get_format import ListCommunitiesCommunitiesGetFormat
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    key: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListCommunitiesCommunitiesGetFormat | Unset = ListCommunitiesCommunitiesGetFormat.JSON,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_key: None | str | Unset
    if isinstance(key, Unset):
        json_key = UNSET
    else:
        json_key = key
    params["key"] = json_key

    params["limit"] = limit

    json_cursor: None | str | Unset
    if isinstance(cursor, Unset):
        json_cursor = UNSET
    else:
        json_cursor = cursor
    params["cursor"] = json_cursor

    json_format_: str | Unset = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/communities",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    key: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListCommunitiesCommunitiesGetFormat | Unset = ListCommunitiesCommunitiesGetFormat.JSON,
) -> Response[Any | HTTPValidationError]:
    """List Communities

    Args:
        key (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListCommunitiesCommunitiesGetFormat | Unset):  Default:
            ListCommunitiesCommunitiesGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        key=key,
        limit=limit,
        cursor=cursor,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    key: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListCommunitiesCommunitiesGetFormat | Unset = ListCommunitiesCommunitiesGetFormat.JSON,
) -> Any | HTTPValidationError | None:
    """List Communities

    Args:
        key (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListCommunitiesCommunitiesGetFormat | Unset):  Default:
            ListCommunitiesCommunitiesGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        key=key,
        limit=limit,
        cursor=cursor,
        format_=format_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    key: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListCommunitiesCommunitiesGetFormat | Unset = ListCommunitiesCommunitiesGetFormat.JSON,
) -> Response[Any | HTTPValidationError]:
    """List Communities

    Args:
        key (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListCommunitiesCommunitiesGetFormat | Unset):  Default:
            ListCommunitiesCommunitiesGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        key=key,
        limit=limit,
        cursor=cursor,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    key: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListCommunitiesCommunitiesGetFormat | Unset = ListCommunitiesCommunitiesGetFormat.JSON,
) -> Any | HTTPValidationError | None:
    """List Communities

    Args:
        key (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListCommunitiesCommunitiesGetFormat | Unset):  Default:
            ListCommunitiesCommunitiesGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            key=key,
            limit=limit,
            cursor=cursor,
            format_=format_,
        )
    ).parsed
