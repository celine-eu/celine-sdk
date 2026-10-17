from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.member_released import MemberReleased
from ...types import Response


def _get_kwargs(
    community: str,
    member_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/communities/{community}/members/{member_key}/release".format(
            community=quote(str(community), safe=""),
            member_key=quote(str(member_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | MemberReleased | None:
    if response.status_code == 200:
        response_200 = MemberReleased.from_dict(response.json())

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
) -> Response[Any | HTTPValidationError | MemberReleased]:
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
) -> Response[Any | HTTPValidationError | MemberReleased]:
    """Release Member

     Release the member from the REC, on a REC admin's behalf.

    Withdraws every standing grant the community collected, deletes the identity
    registry membership and revokes the credential, releases the login (disabled,
    out of the REC's Keycloak organization and its groups, sessions ended) and
    sets the registry member inactive. Nothing is deleted. The next community's
    approval enables the same login again.

    `200` whenever the release ran, failed steps included: `state` is `partial`
    and calling again is the retry. Every step is idempotent. Keyed on the
    registry's pair, so a member imported into the registry, with no submission,
    is released like one onboarded here.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | MemberReleased]
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
) -> Any | HTTPValidationError | MemberReleased | None:
    """Release Member

     Release the member from the REC, on a REC admin's behalf.

    Withdraws every standing grant the community collected, deletes the identity
    registry membership and revokes the credential, releases the login (disabled,
    out of the REC's Keycloak organization and its groups, sessions ended) and
    sets the registry member inactive. Nothing is deleted. The next community's
    approval enables the same login again.

    `200` whenever the release ran, failed steps included: `state` is `partial`
    and calling again is the retry. Every step is idempotent. Keyed on the
    registry's pair, so a member imported into the registry, with no submission,
    is released like one onboarded here.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | MemberReleased
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
) -> Response[Any | HTTPValidationError | MemberReleased]:
    """Release Member

     Release the member from the REC, on a REC admin's behalf.

    Withdraws every standing grant the community collected, deletes the identity
    registry membership and revokes the credential, releases the login (disabled,
    out of the REC's Keycloak organization and its groups, sessions ended) and
    sets the registry member inactive. Nothing is deleted. The next community's
    approval enables the same login again.

    `200` whenever the release ran, failed steps included: `state` is `partial`
    and calling again is the retry. Every step is idempotent. Keyed on the
    registry's pair, so a member imported into the registry, with no submission,
    is released like one onboarded here.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError | MemberReleased]
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
) -> Any | HTTPValidationError | MemberReleased | None:
    """Release Member

     Release the member from the REC, on a REC admin's behalf.

    Withdraws every standing grant the community collected, deletes the identity
    registry membership and revokes the credential, releases the login (disabled,
    out of the REC's Keycloak organization and its groups, sessions ended) and
    sets the registry member inactive. Nothing is deleted. The next community's
    approval enables the same login again.

    `200` whenever the release ran, failed steps included: `state` is `partial`
    and calling again is the retry. Every step is idempotent. Keyed on the
    registry's pair, so a member imported into the registry, with no submission,
    is released like one onboarded here.

    Args:
        community (str):
        member_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError | MemberReleased
    """

    return (
        await asyncio_detailed(
            community=community,
            member_key=member_key,
            client=client,
        )
    ).parsed
