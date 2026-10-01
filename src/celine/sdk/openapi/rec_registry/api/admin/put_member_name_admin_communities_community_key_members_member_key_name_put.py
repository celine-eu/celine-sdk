from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.member_detail import MemberDetail
from ...models.member_name_put import MemberNamePut
from ...types import Response


def _get_kwargs(
    community_key: str,
    member_key: str,
    *,
    body: MemberNamePut,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/members/{member_key}/name".format(
            community_key=quote(str(community_key), safe=""),
            member_key=quote(str(member_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | HTTPValidationError | MemberDetail | None:
    if response.status_code == 200:
        response_200 = MemberDetail.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | HTTPValidationError | MemberDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberNamePut,
) -> Response[ErrorResponse | HTTPValidationError | MemberDetail]:
    """Put Member Name

     Set a member's name, and nothing else (REQ-0083).

    The body is `{name}`: the one key, not `null`, and no other — anything
    else is `422` (FastAPI's validation body) and changes nothing. Derives
    `members.name.write` (REQ-0081), which `rec-registry.members.name.write`,
    `rec-registry.members.write` and `rec-registry.admin` satisfy (REQ-0082).

    Args:
        community_key (str):
        member_key (str):
        body (MemberNamePut): A member's name, and nothing else (`PUT …/members/{key}/name`,
            REQ-0083).

            The one key is required and may not be `null`; any other key is `422`, so
            the narrow `members.name.write` grant cannot carry an identity rewrite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | MemberDetail]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberNamePut,
) -> ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Put Member Name

     Set a member's name, and nothing else (REQ-0083).

    The body is `{name}`: the one key, not `null`, and no other — anything
    else is `422` (FastAPI's validation body) and changes nothing. Derives
    `members.name.write` (REQ-0081), which `rec-registry.members.name.write`,
    `rec-registry.members.write` and `rec-registry.admin` satisfy (REQ-0082).

    Args:
        community_key (str):
        member_key (str):
        body (MemberNamePut): A member's name, and nothing else (`PUT …/members/{key}/name`,
            REQ-0083).

            The one key is required and may not be `null`; any other key is `422`, so
            the narrow `members.name.write` grant cannot carry an identity rewrite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | MemberDetail
    """

    return sync_detailed(
        community_key=community_key,
        member_key=member_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberNamePut,
) -> Response[ErrorResponse | HTTPValidationError | MemberDetail]:
    """Put Member Name

     Set a member's name, and nothing else (REQ-0083).

    The body is `{name}`: the one key, not `null`, and no other — anything
    else is `422` (FastAPI's validation body) and changes nothing. Derives
    `members.name.write` (REQ-0081), which `rec-registry.members.name.write`,
    `rec-registry.members.write` and `rec-registry.admin` satisfy (REQ-0082).

    Args:
        community_key (str):
        member_key (str):
        body (MemberNamePut): A member's name, and nothing else (`PUT …/members/{key}/name`,
            REQ-0083).

            The one key is required and may not be `null`; any other key is `422`, so
            the narrow `members.name.write` grant cannot carry an identity rewrite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | MemberDetail]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberNamePut,
) -> ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Put Member Name

     Set a member's name, and nothing else (REQ-0083).

    The body is `{name}`: the one key, not `null`, and no other — anything
    else is `422` (FastAPI's validation body) and changes nothing. Derives
    `members.name.write` (REQ-0081), which `rec-registry.members.name.write`,
    `rec-registry.members.write` and `rec-registry.admin` satisfy (REQ-0082).

    Args:
        community_key (str):
        member_key (str):
        body (MemberNamePut): A member's name, and nothing else (`PUT …/members/{key}/name`,
            REQ-0083).

            The one key is required and may not be `null`; any other key is `422`, so
            the narrow `members.name.write` grant cannot carry an identity rewrite.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | MemberDetail
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            client=client,
            body=body,
        )
    ).parsed
