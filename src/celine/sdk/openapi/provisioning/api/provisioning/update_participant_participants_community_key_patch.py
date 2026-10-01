from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.participant_update import ParticipantUpdate
from ...models.participant_update_response import ParticipantUpdateResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community: str,
    key: str,
    *,
    body: ParticipantUpdate,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/participants/{community}/{key}".format(
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
) -> ErrorResponse | HTTPValidationError | ParticipantUpdateResponse | None:
    if response.status_code == 200:
        response_200 = ParticipantUpdateResponse.from_dict(response.json())

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

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | HTTPValidationError | ParticipantUpdateResponse]:
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
    body: ParticipantUpdate,
    authorization: None | str | Unset = UNSET,
) -> Response[ErrorResponse | HTTPValidationError | ParticipantUpdateResponse]:
    """Correct a member's names or email address on their existing account

     Write `first_name`, `last_name` and `email` on the account the registry
    names for `(community, key)`. Never creates an account and never changes
    the username.

    An address change resets `email_verified` and emails a `VERIFY_EMAIL` link
    to the **new** address only; the same address is not a change and sends
    nothing. `404` for a community, member or account that does not exist (the
    code says which), `409 account_disabled`, `409 email_taken` when another
    account holds the address, `502 send_failed` when Keycloak did not send the
    link — the account is then put back as it was, so a retry sends.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpdate): The body of `PATCH /participants/{community}/{key}`.

            At least one field; an empty body, or one with only `null`s, is `422`.
            **No `username`**: the account keeps the one it has, and a body naming one
            (or any other field) is refused `422` rather than silently ignored.

            The address is a plain string, for the reason `ParticipantUpsert` gives.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | ParticipantUpdateResponse]
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
    body: ParticipantUpdate,
    authorization: None | str | Unset = UNSET,
) -> ErrorResponse | HTTPValidationError | ParticipantUpdateResponse | None:
    """Correct a member's names or email address on their existing account

     Write `first_name`, `last_name` and `email` on the account the registry
    names for `(community, key)`. Never creates an account and never changes
    the username.

    An address change resets `email_verified` and emails a `VERIFY_EMAIL` link
    to the **new** address only; the same address is not a change and sends
    nothing. `404` for a community, member or account that does not exist (the
    code says which), `409 account_disabled`, `409 email_taken` when another
    account holds the address, `502 send_failed` when Keycloak did not send the
    link — the account is then put back as it was, so a retry sends.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpdate): The body of `PATCH /participants/{community}/{key}`.

            At least one field; an empty body, or one with only `null`s, is `422`.
            **No `username`**: the account keeps the one it has, and a body naming one
            (or any other field) is refused `422` rather than silently ignored.

            The address is a plain string, for the reason `ParticipantUpsert` gives.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | ParticipantUpdateResponse
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
    body: ParticipantUpdate,
    authorization: None | str | Unset = UNSET,
) -> Response[ErrorResponse | HTTPValidationError | ParticipantUpdateResponse]:
    """Correct a member's names or email address on their existing account

     Write `first_name`, `last_name` and `email` on the account the registry
    names for `(community, key)`. Never creates an account and never changes
    the username.

    An address change resets `email_verified` and emails a `VERIFY_EMAIL` link
    to the **new** address only; the same address is not a change and sends
    nothing. `404` for a community, member or account that does not exist (the
    code says which), `409 account_disabled`, `409 email_taken` when another
    account holds the address, `502 send_failed` when Keycloak did not send the
    link — the account is then put back as it was, so a retry sends.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpdate): The body of `PATCH /participants/{community}/{key}`.

            At least one field; an empty body, or one with only `null`s, is `422`.
            **No `username`**: the account keeps the one it has, and a body naming one
            (or any other field) is refused `422` rather than silently ignored.

            The address is a plain string, for the reason `ParticipantUpsert` gives.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | ParticipantUpdateResponse]
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
    body: ParticipantUpdate,
    authorization: None | str | Unset = UNSET,
) -> ErrorResponse | HTTPValidationError | ParticipantUpdateResponse | None:
    """Correct a member's names or email address on their existing account

     Write `first_name`, `last_name` and `email` on the account the registry
    names for `(community, key)`. Never creates an account and never changes
    the username.

    An address change resets `email_verified` and emails a `VERIFY_EMAIL` link
    to the **new** address only; the same address is not a change and sends
    nothing. `404` for a community, member or account that does not exist (the
    code says which), `409 account_disabled`, `409 email_taken` when another
    account holds the address, `502 send_failed` when Keycloak did not send the
    link — the account is then put back as it was, so a retry sends.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpdate): The body of `PATCH /participants/{community}/{key}`.

            At least one field; an empty body, or one with only `null`s, is `422`.
            **No `username`**: the account keeps the one it has, and a body naming one
            (or any other field) is refused `422` rather than silently ignored.

            The address is a plain string, for the reason `ParticipantUpsert` gives.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | ParticipantUpdateResponse
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
