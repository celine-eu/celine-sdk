from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_participants_communities_community_key_participants_get_format import (
    ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community_key: str,
    *,
    kind: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat
    | Unset = ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_kind: None | str | Unset
    if isinstance(kind, Unset):
        json_kind = UNSET
    else:
        json_kind = kind
    params["kind"] = json_kind

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
        "url": "/communities/{community_key}/participants".format(
            community_key=quote(str(community_key), safe=""),
        ),
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
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    kind: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat
    | Unset = ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON,
) -> Response[Any | HTTPValidationError]:
    """List Participants

    Args:
        community_key (str):
        kind (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat | Unset):  Default:
            ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        kind=kind,
        limit=limit,
        cursor=cursor,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    kind: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat
    | Unset = ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON,
) -> Any | HTTPValidationError | None:
    """List Participants

    Args:
        community_key (str):
        kind (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat | Unset):  Default:
            ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        client=client,
        kind=kind,
        limit=limit,
        cursor=cursor,
        format_=format_,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    kind: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat
    | Unset = ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON,
) -> Response[Any | HTTPValidationError]:
    """List Participants

    Args:
        community_key (str):
        kind (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat | Unset):  Default:
            ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        kind=kind,
        limit=limit,
        cursor=cursor,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    kind: None | str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: None | str | Unset = UNSET,
    format_: ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat
    | Unset = ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON,
) -> Any | HTTPValidationError | None:
    """List Participants

    Args:
        community_key (str):
        kind (None | str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (None | str | Unset):
        format_ (ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat | Unset):  Default:
            ListParticipantsCommunitiesCommunityKeyParticipantsGetFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            client=client,
            kind=kind,
            limit=limit,
            cursor=cursor,
            format_=format_,
        )
    ).parsed
