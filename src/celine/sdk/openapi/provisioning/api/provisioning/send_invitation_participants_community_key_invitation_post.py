from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.invitation_request import InvitationRequest
from ...models.invitation_response import InvitationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community: str,
    key: str,
    *,
    body: InvitationRequest,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/participants/{community}/{key}/invitation".format(
            community=quote(str(community), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | HTTPValidationError | InvitationResponse | None:
    if response.status_code == 200:
        response_200 = InvitationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | HTTPValidationError | InvitationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: InvitationRequest,
    authorization: None | str | Unset = UNSET,
) -> Response[ErrorResponse | HTTPValidationError | InvitationResponse]:
    """Email a member an invitation, or a password reset, as the caller names

     Keycloak emails the link; no credential is generated or returned.

    The body names the email: `invitation` for an account with no password,
    `password_reset` (short lifespan) for one that has one. A mismatch is `409`
    `has_password` or `no_password`, before any send or cooldown, and the
    service never picks the other email instead. `404` for a community, member
    or account that does not exist (the code says which), `409` for a disabled
    account or one with no email address (`no_email`), `429` within the
    cooldown of the last email to that account — sent by this route or by an
    upsert — and `502` `send_failed` when Keycloak did not send it, which starts
    no cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (InvitationRequest): The body of `POST /participants/{community}/{key}/invitation`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | InvitationResponse]
    """

    kwargs = _get_kwargs(
        community=community,
        key=key,
        body=body,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: InvitationRequest,
    authorization: None | str | Unset = UNSET,
) -> ErrorResponse | HTTPValidationError | InvitationResponse | None:
    """Email a member an invitation, or a password reset, as the caller names

     Keycloak emails the link; no credential is generated or returned.

    The body names the email: `invitation` for an account with no password,
    `password_reset` (short lifespan) for one that has one. A mismatch is `409`
    `has_password` or `no_password`, before any send or cooldown, and the
    service never picks the other email instead. `404` for a community, member
    or account that does not exist (the code says which), `409` for a disabled
    account or one with no email address (`no_email`), `429` within the
    cooldown of the last email to that account — sent by this route or by an
    upsert — and `502` `send_failed` when Keycloak did not send it, which starts
    no cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (InvitationRequest): The body of `POST /participants/{community}/{key}/invitation`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | InvitationResponse
    """

    return sync_detailed(
        community=community,
        key=key,
        client=client,
        body=body,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: InvitationRequest,
    authorization: None | str | Unset = UNSET,
) -> Response[ErrorResponse | HTTPValidationError | InvitationResponse]:
    """Email a member an invitation, or a password reset, as the caller names

     Keycloak emails the link; no credential is generated or returned.

    The body names the email: `invitation` for an account with no password,
    `password_reset` (short lifespan) for one that has one. A mismatch is `409`
    `has_password` or `no_password`, before any send or cooldown, and the
    service never picks the other email instead. `404` for a community, member
    or account that does not exist (the code says which), `409` for a disabled
    account or one with no email address (`no_email`), `429` within the
    cooldown of the last email to that account — sent by this route or by an
    upsert — and `502` `send_failed` when Keycloak did not send it, which starts
    no cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (InvitationRequest): The body of `POST /participants/{community}/{key}/invitation`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | InvitationResponse]
    """

    kwargs = _get_kwargs(
        community=community,
        key=key,
        body=body,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    body: InvitationRequest,
    authorization: None | str | Unset = UNSET,
) -> ErrorResponse | HTTPValidationError | InvitationResponse | None:
    """Email a member an invitation, or a password reset, as the caller names

     Keycloak emails the link; no credential is generated or returned.

    The body names the email: `invitation` for an account with no password,
    `password_reset` (short lifespan) for one that has one. A mismatch is `409`
    `has_password` or `no_password`, before any send or cooldown, and the
    service never picks the other email instead. `404` for a community, member
    or account that does not exist (the code says which), `409` for a disabled
    account or one with no email address (`no_email`), `429` within the
    cooldown of the last email to that account — sent by this route or by an
    upsert — and `502` `send_failed` when Keycloak did not send it, which starts
    no cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (InvitationRequest): The body of `POST /participants/{community}/{key}/invitation`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | InvitationResponse
    """

    return (
        await asyncio_detailed(
            community=community,
            key=key,
            client=client,
            body=body,
            authorization=authorization,
        )
    ).parsed
