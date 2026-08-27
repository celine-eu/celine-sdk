from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dids_batch_request import DidsBatchRequest
from ...models.global_member_lookup import GlobalMemberLookup
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: DidsBatchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/lookup/members-by-dids",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[GlobalMemberLookup] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GlobalMemberLookup.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[GlobalMemberLookup]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DidsBatchRequest,
) -> Response[HTTPValidationError | list[GlobalMemberLookup]]:
    """Lookup Members By Dids

     Find the members holding a set of dataspace DIDs, across all communities.

    **Why it exists.** The connector answers *who consents* in DIDs; this
    registry knows *what they hold*; nothing joined the two. Resolving a DID
    through the identity registry to a Keycloak user id does not close the gap,
    because `Member.user_id` holds a Keycloak *username* and the identifier that
    hop returns matches no row here. So the DID is stored on the member and this
    is the join.

    **Members, not assets** — and that is the part it would be easy to get
    wrong. Mirroring `assets-by-user-ids` exactly would lose the supply point in
    the common case: ../onboarding writes the declared POD into
    `Member.delivery_points` and registers **no assets**, because a meter's
    `sensor_id` is assigned at physical installation, long after onboarding. An
    asset-shaped answer is therefore empty for every participant whose meter has
    not been commissioned yet. `GlobalMemberLookup` already carries
    `delivery_points`; a commissioned meter stays reachable through the
    `user_id` in the same row and the existing `assets-by-user-ids`.

    **Bounded**, at the same 500 as the other two batch routes and from the same
    constant.

    **No enumeration oracle.** A DID that belongs to nobody and a member holding
    no supply points are indistinguishable — an unknown DID contributes no row
    and is not a `404`. The caller supplies the DIDs, so any difference between
    those answers would make this a way to discover who is registered.

    Every row carries its `did`, which is what lets the caller attribute the row
    back to the DID it asked about.

    Args:
        body (DidsBatchRequest): Members to resolve by their dataspace DID.

            Bounded by the same constant as its two siblings, for the same reason: a
            caller naming ten thousand DIDs in one request has a dump of the registry
            rather than a lookup.

            A DID is the identifier a consent record is written in, so the set the
            caller holds is the set of people who consented — and this endpoint turns
            that into the supply points they hold. Which makes the bound the same
            security decision it is on the other two.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[GlobalMemberLookup]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: DidsBatchRequest,
) -> HTTPValidationError | list[GlobalMemberLookup] | None:
    """Lookup Members By Dids

     Find the members holding a set of dataspace DIDs, across all communities.

    **Why it exists.** The connector answers *who consents* in DIDs; this
    registry knows *what they hold*; nothing joined the two. Resolving a DID
    through the identity registry to a Keycloak user id does not close the gap,
    because `Member.user_id` holds a Keycloak *username* and the identifier that
    hop returns matches no row here. So the DID is stored on the member and this
    is the join.

    **Members, not assets** — and that is the part it would be easy to get
    wrong. Mirroring `assets-by-user-ids` exactly would lose the supply point in
    the common case: ../onboarding writes the declared POD into
    `Member.delivery_points` and registers **no assets**, because a meter's
    `sensor_id` is assigned at physical installation, long after onboarding. An
    asset-shaped answer is therefore empty for every participant whose meter has
    not been commissioned yet. `GlobalMemberLookup` already carries
    `delivery_points`; a commissioned meter stays reachable through the
    `user_id` in the same row and the existing `assets-by-user-ids`.

    **Bounded**, at the same 500 as the other two batch routes and from the same
    constant.

    **No enumeration oracle.** A DID that belongs to nobody and a member holding
    no supply points are indistinguishable — an unknown DID contributes no row
    and is not a `404`. The caller supplies the DIDs, so any difference between
    those answers would make this a way to discover who is registered.

    Every row carries its `did`, which is what lets the caller attribute the row
    back to the DID it asked about.

    Args:
        body (DidsBatchRequest): Members to resolve by their dataspace DID.

            Bounded by the same constant as its two siblings, for the same reason: a
            caller naming ten thousand DIDs in one request has a dump of the registry
            rather than a lookup.

            A DID is the identifier a consent record is written in, so the set the
            caller holds is the set of people who consented — and this endpoint turns
            that into the supply points they hold. Which makes the bound the same
            security decision it is on the other two.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[GlobalMemberLookup]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DidsBatchRequest,
) -> Response[HTTPValidationError | list[GlobalMemberLookup]]:
    """Lookup Members By Dids

     Find the members holding a set of dataspace DIDs, across all communities.

    **Why it exists.** The connector answers *who consents* in DIDs; this
    registry knows *what they hold*; nothing joined the two. Resolving a DID
    through the identity registry to a Keycloak user id does not close the gap,
    because `Member.user_id` holds a Keycloak *username* and the identifier that
    hop returns matches no row here. So the DID is stored on the member and this
    is the join.

    **Members, not assets** — and that is the part it would be easy to get
    wrong. Mirroring `assets-by-user-ids` exactly would lose the supply point in
    the common case: ../onboarding writes the declared POD into
    `Member.delivery_points` and registers **no assets**, because a meter's
    `sensor_id` is assigned at physical installation, long after onboarding. An
    asset-shaped answer is therefore empty for every participant whose meter has
    not been commissioned yet. `GlobalMemberLookup` already carries
    `delivery_points`; a commissioned meter stays reachable through the
    `user_id` in the same row and the existing `assets-by-user-ids`.

    **Bounded**, at the same 500 as the other two batch routes and from the same
    constant.

    **No enumeration oracle.** A DID that belongs to nobody and a member holding
    no supply points are indistinguishable — an unknown DID contributes no row
    and is not a `404`. The caller supplies the DIDs, so any difference between
    those answers would make this a way to discover who is registered.

    Every row carries its `did`, which is what lets the caller attribute the row
    back to the DID it asked about.

    Args:
        body (DidsBatchRequest): Members to resolve by their dataspace DID.

            Bounded by the same constant as its two siblings, for the same reason: a
            caller naming ten thousand DIDs in one request has a dump of the registry
            rather than a lookup.

            A DID is the identifier a consent record is written in, so the set the
            caller holds is the set of people who consented — and this endpoint turns
            that into the supply points they hold. Which makes the bound the same
            security decision it is on the other two.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[GlobalMemberLookup]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: DidsBatchRequest,
) -> HTTPValidationError | list[GlobalMemberLookup] | None:
    """Lookup Members By Dids

     Find the members holding a set of dataspace DIDs, across all communities.

    **Why it exists.** The connector answers *who consents* in DIDs; this
    registry knows *what they hold*; nothing joined the two. Resolving a DID
    through the identity registry to a Keycloak user id does not close the gap,
    because `Member.user_id` holds a Keycloak *username* and the identifier that
    hop returns matches no row here. So the DID is stored on the member and this
    is the join.

    **Members, not assets** — and that is the part it would be easy to get
    wrong. Mirroring `assets-by-user-ids` exactly would lose the supply point in
    the common case: ../onboarding writes the declared POD into
    `Member.delivery_points` and registers **no assets**, because a meter's
    `sensor_id` is assigned at physical installation, long after onboarding. An
    asset-shaped answer is therefore empty for every participant whose meter has
    not been commissioned yet. `GlobalMemberLookup` already carries
    `delivery_points`; a commissioned meter stays reachable through the
    `user_id` in the same row and the existing `assets-by-user-ids`.

    **Bounded**, at the same 500 as the other two batch routes and from the same
    constant.

    **No enumeration oracle.** A DID that belongs to nobody and a member holding
    no supply points are indistinguishable — an unknown DID contributes no row
    and is not a `404`. The caller supplies the DIDs, so any difference between
    those answers would make this a way to discover who is registered.

    Every row carries its `did`, which is what lets the caller attribute the row
    back to the DID it asked about.

    Args:
        body (DidsBatchRequest): Members to resolve by their dataspace DID.

            Bounded by the same constant as its two siblings, for the same reason: a
            caller naming ten thousand DIDs in one request has a dump of the registry
            rather than a lookup.

            A DID is the identifier a consent record is written in, so the set the
            caller holds is the set of people who consented — and this endpoint turns
            that into the supply points they hold. Which makes the bound the same
            security decision it is on the other two.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[GlobalMemberLookup]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
