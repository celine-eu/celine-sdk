from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.member_email_sent import MemberEmailSent
from ...types import Response


def _get_kwargs(
    community: str,
    member_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/communities/{community}/members/{member_key}/password-reset".format(
            community=quote(str(community), safe=""),
            member_key=quote(str(member_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | MemberEmailSent | None:
    if response.status_code == 200:
        response_200 = MemberEmailSent.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if response.status_code == 502:
        response_502 = cast(Any, None)
        return response_502

    if response.status_code == 503:
        response_503 = cast(Any, None)
        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError | MemberEmailSent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError | MemberEmailSent]:
    """Send Member Password Reset

     Email the member a link to reset their password.

    Refused with `409 no_password` when the account has none; the invitation route
    is then the one to call.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | MemberEmailSent]
    """

    kwargs = _get_kwargs(
        community=community,
        member_key=member_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | MemberEmailSent | None:
    """Send Member Password Reset

     Email the member a link to reset their password.

    Refused with `409 no_password` when the account has none; the invitation route
    is then the one to call.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | MemberEmailSent
    """

    return sync_detailed(
        community=community,
        member_key=member_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    community: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError | MemberEmailSent]:
    """Send Member Password Reset

     Email the member a link to reset their password.

    Refused with `409 no_password` when the account has none; the invitation route
    is then the one to call.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | MemberEmailSent]
    """

    kwargs = _get_kwargs(
        community=community,
        member_key=member_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | MemberEmailSent | None:
    """Send Member Password Reset

     Email the member a link to reset their password.

    Refused with `409 no_password` when the account has none; the invitation route
    is then the one to call.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | MemberEmailSent
    """

    return (
        await asyncio_detailed(
            community=community,
            member_key=member_key,
            client=client,
        )
    ).parsed
