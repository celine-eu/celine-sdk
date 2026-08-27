from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.member_create import MemberCreate
from ...models.member_detail import MemberDetail
from ...types import Response


def _get_kwargs(
    community_key: str,
    *,
    body: MemberCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/communities/{community_key}/members".format(
            community_key=quote(str(community_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | MemberDetail | None:
    if response.status_code == 201:
        response_201 = MemberDetail.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | MemberDetail]:
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
    body: MemberCreate,
) -> Response[HTTPValidationError | MemberDetail]:
    """Create Member

     Create one member.

    Answers `409` when the key or `user_id` is already taken, naming the
    existing key so a caller can switch to `PATCH`. It does not overwrite: the
    caller asked to create, and silently updating somebody else's row is how a
    retry with a changed payload rewrites the wrong person.

    A concurrent create answers `409` too — the unique index refuses it, and the
    service translates that back into the same conflict.

    Args:
        community_key (str):
        body (MemberCreate): Create one member. `key` is minted from the community's own numbering
            when omitted, so a caller with no opinion still gets `gl-00007` rather than
            something that reads as foreign in an exported bundle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MemberDetail]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberCreate,
) -> HTTPValidationError | MemberDetail | None:
    """Create Member

     Create one member.

    Answers `409` when the key or `user_id` is already taken, naming the
    existing key so a caller can switch to `PATCH`. It does not overwrite: the
    caller asked to create, and silently updating somebody else's row is how a
    retry with a changed payload rewrites the wrong person.

    A concurrent create answers `409` too — the unique index refuses it, and the
    service translates that back into the same conflict.

    Args:
        community_key (str):
        body (MemberCreate): Create one member. `key` is minted from the community's own numbering
            when omitted, so a caller with no opinion still gets `gl-00007` rather than
            something that reads as foreign in an exported bundle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MemberDetail
    """

    return sync_detailed(
        community_key=community_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberCreate,
) -> Response[HTTPValidationError | MemberDetail]:
    """Create Member

     Create one member.

    Answers `409` when the key or `user_id` is already taken, naming the
    existing key so a caller can switch to `PATCH`. It does not overwrite: the
    caller asked to create, and silently updating somebody else's row is how a
    retry with a changed payload rewrites the wrong person.

    A concurrent create answers `409` too — the unique index refuses it, and the
    service translates that back into the same conflict.

    Args:
        community_key (str):
        body (MemberCreate): Create one member. `key` is minted from the community's own numbering
            when omitted, so a caller with no opinion still gets `gl-00007` rather than
            something that reads as foreign in an exported bundle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MemberDetail]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberCreate,
) -> HTTPValidationError | MemberDetail | None:
    """Create Member

     Create one member.

    Answers `409` when the key or `user_id` is already taken, naming the
    existing key so a caller can switch to `PATCH`. It does not overwrite: the
    caller asked to create, and silently updating somebody else's row is how a
    retry with a changed payload rewrites the wrong person.

    A concurrent create answers `409` too — the unique index refuses it, and the
    service translates that back into the same conflict.

    Args:
        community_key (str):
        body (MemberCreate): Create one member. `key` is minted from the community's own numbering
            when omitted, so a caller with no opinion still gets `gl-00007` rather than
            something that reads as foreign in an exported bundle.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MemberDetail
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            client=client,
            body=body,
        )
    ).parsed
