from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.invitation_response import InvitationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community: str,
    key: str,
    *,
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

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | InvitationResponse | None:
    if response.status_code == 200:
        response_200 = InvitationResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | InvitationResponse]:
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
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InvitationResponse]:
    """Email a member a link to set, or reset, their password

     Keycloak emails the link; no credential is generated or returned.

    An account with no password gets an invitation, one with a password gets a
    reset with a short lifespan. `404` for a member the registry or the realm
    does not have, `409` for a disabled account, `429` within the cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InvitationResponse]
    """

    kwargs = _get_kwargs(
        community=community,
        key=key,
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
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | InvitationResponse | None:
    """Email a member a link to set, or reset, their password

     Keycloak emails the link; no credential is generated or returned.

    An account with no password gets an invitation, one with a password gets a
    reset with a short lifespan. `404` for a member the registry or the realm
    does not have, `409` for a disabled account, `429` within the cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InvitationResponse
    """

    return sync_detailed(
        community=community,
        key=key,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | InvitationResponse]:
    """Email a member a link to set, or reset, their password

     Keycloak emails the link; no credential is generated or returned.

    An account with no password gets an invitation, one with a password gets a
    reset with a short lifespan. `404` for a member the registry or the realm
    does not have, `409` for a disabled account, `429` within the cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | InvitationResponse]
    """

    kwargs = _get_kwargs(
        community=community,
        key=key,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | InvitationResponse | None:
    """Email a member a link to set, or reset, their password

     Keycloak emails the link; no credential is generated or returned.

    An account with no password gets an invitation, one with a password gets a
    reset with a short lifespan. `404` for a member the registry or the realm
    does not have, `409` for a disabled account, `429` within the cooldown.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | InvitationResponse
    """

    return (
        await asyncio_detailed(
            community=community,
            key=key,
            client=client,
            authorization=authorization,
        )
    ).parsed
