from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.participant_response import ParticipantResponse
from ...models.participant_upsert import ParticipantUpsert
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community: str,
    key: str,
    *,
    body: ParticipantUpsert,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "put",
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
) -> HTTPValidationError | ParticipantResponse | None:
    if response.status_code == 200:
        response_200 = ParticipantResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ParticipantResponse]:
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
    body: ParticipantUpsert,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ParticipantResponse]:
    """Ensure a participant's account, organization and org group

     Find or create the account, and file it in the REC.

    Synchronous rather than a signal, because the caller needs the `username`
    back: it becomes the registry's `Member.user_id`, and it is read from
    Keycloak rather than computed — an account that already existed may
    authenticate under a convention nobody here chose.

    Always `200`. A create and a no-op are the same request with the same
    meaning, and `created` in the body says which happened; a `201` on one and a
    `200` on the other would make a retry look like a different outcome.

    **`invite` does not change that.** A disabled account, an address outside
    the dev list or an account that already has a password is still a `200`,
    with the reason in `invitation`, so an approval is never blocked by its
    email.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpsert): The body of `PUT /participants/{community}/{key}`.

            **The email transits and is stored nowhere.** Not here — this service keeps
            no state at all — and not in the registry, which has no email column and is
            gaining none. It is on the account in Keycloak, which is where the address a
            person logs in with belongs.

            It is required because it is the only thing that can find an account this
            platform did not name. A participant who already has a login authenticates
            under whatever convention created it, and the address is the one identifier
            every writer agrees on.

            **A plain string, not `EmailStr`.** The address belongs to the submission
            `../onboarding` already validated and accepted; re-deciding here whether it
            is well formed would mean a person who has been approved cannot be given a
            login because two libraries disagree about their address. Non-empty is the
            whole check, and it exists so a missing value fails here rather than
            creating an account named the empty string.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ParticipantResponse]
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
    body: ParticipantUpsert,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | ParticipantResponse | None:
    """Ensure a participant's account, organization and org group

     Find or create the account, and file it in the REC.

    Synchronous rather than a signal, because the caller needs the `username`
    back: it becomes the registry's `Member.user_id`, and it is read from
    Keycloak rather than computed — an account that already existed may
    authenticate under a convention nobody here chose.

    Always `200`. A create and a no-op are the same request with the same
    meaning, and `created` in the body says which happened; a `201` on one and a
    `200` on the other would make a retry look like a different outcome.

    **`invite` does not change that.** A disabled account, an address outside
    the dev list or an account that already has a password is still a `200`,
    with the reason in `invitation`, so an approval is never blocked by its
    email.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpsert): The body of `PUT /participants/{community}/{key}`.

            **The email transits and is stored nowhere.** Not here — this service keeps
            no state at all — and not in the registry, which has no email column and is
            gaining none. It is on the account in Keycloak, which is where the address a
            person logs in with belongs.

            It is required because it is the only thing that can find an account this
            platform did not name. A participant who already has a login authenticates
            under whatever convention created it, and the address is the one identifier
            every writer agrees on.

            **A plain string, not `EmailStr`.** The address belongs to the submission
            `../onboarding` already validated and accepted; re-deciding here whether it
            is well formed would mean a person who has been approved cannot be given a
            login because two libraries disagree about their address. Non-empty is the
            whole check, and it exists so a missing value fails here rather than
            creating an account named the empty string.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ParticipantResponse
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
    body: ParticipantUpsert,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ParticipantResponse]:
    """Ensure a participant's account, organization and org group

     Find or create the account, and file it in the REC.

    Synchronous rather than a signal, because the caller needs the `username`
    back: it becomes the registry's `Member.user_id`, and it is read from
    Keycloak rather than computed — an account that already existed may
    authenticate under a convention nobody here chose.

    Always `200`. A create and a no-op are the same request with the same
    meaning, and `created` in the body says which happened; a `201` on one and a
    `200` on the other would make a retry look like a different outcome.

    **`invite` does not change that.** A disabled account, an address outside
    the dev list or an account that already has a password is still a `200`,
    with the reason in `invitation`, so an approval is never blocked by its
    email.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpsert): The body of `PUT /participants/{community}/{key}`.

            **The email transits and is stored nowhere.** Not here — this service keeps
            no state at all — and not in the registry, which has no email column and is
            gaining none. It is on the account in Keycloak, which is where the address a
            person logs in with belongs.

            It is required because it is the only thing that can find an account this
            platform did not name. A participant who already has a login authenticates
            under whatever convention created it, and the address is the one identifier
            every writer agrees on.

            **A plain string, not `EmailStr`.** The address belongs to the submission
            `../onboarding` already validated and accepted; re-deciding here whether it
            is well formed would mean a person who has been approved cannot be given a
            login because two libraries disagree about their address. Non-empty is the
            whole check, and it exists so a missing value fails here rather than
            creating an account named the empty string.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ParticipantResponse]
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
    body: ParticipantUpsert,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | ParticipantResponse | None:
    """Ensure a participant's account, organization and org group

     Find or create the account, and file it in the REC.

    Synchronous rather than a signal, because the caller needs the `username`
    back: it becomes the registry's `Member.user_id`, and it is read from
    Keycloak rather than computed — an account that already existed may
    authenticate under a convention nobody here chose.

    Always `200`. A create and a no-op are the same request with the same
    meaning, and `created` in the body says which happened; a `201` on one and a
    `200` on the other would make a retry look like a different outcome.

    **`invite` does not change that.** A disabled account, an address outside
    the dev list or an account that already has a password is still a `200`,
    with the reason in `invitation`, so an approval is never blocked by its
    email.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):
        body (ParticipantUpsert): The body of `PUT /participants/{community}/{key}`.

            **The email transits and is stored nowhere.** Not here — this service keeps
            no state at all — and not in the registry, which has no email column and is
            gaining none. It is on the account in Keycloak, which is where the address a
            person logs in with belongs.

            It is required because it is the only thing that can find an account this
            platform did not name. A participant who already has a login authenticates
            under whatever convention created it, and the address is the one identifier
            every writer agrees on.

            **A plain string, not `EmailStr`.** The address belongs to the submission
            `../onboarding` already validated and accepted; re-deciding here whether it
            is well formed would mean a person who has been approved cannot be given a
            login because two libraries disagree about their address. Non-empty is the
            whole check, and it exists so a missing value fails here rather than
            creating an account named the empty string.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ParticipantResponse
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
