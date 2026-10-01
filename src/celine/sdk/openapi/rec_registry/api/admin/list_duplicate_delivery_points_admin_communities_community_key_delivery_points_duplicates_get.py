from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery_point_duplicates import DeliveryPointDuplicates
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/communities/{community_key}/delivery-points/duplicates".format(
            community_key=quote(str(community_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeliveryPointDuplicates | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DeliveryPointDuplicates.from_dict(response.json())

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
) -> Response[DeliveryPointDuplicates | HTTPValidationError]:
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
) -> Response[DeliveryPointDuplicates | HTTPValidationError]:
    """List Duplicate Delivery Points

     The community's delivery points that more than one active member holds (REQ-0087).

    For each point an active member of this community holds and another
    active member — here or in any other community — also holds: the point in
    its compared form (trimmed, lower-cased), this community's holders by
    member key with the spelling each stored, how many active members of
    other communities hold it, and the total. Holders in other communities are
    a count only: never their member, never their community (REQ-0085).
    Members who are not `active` hold nothing.

    The per-community view of `celine-rec-registry duplicate-delivery-points`
    (REQ-0086), for an operator console: these are the points the registry
    will refuse to give, re-give or reactivate (`delivery_point_held`) until
    resolved. A read: `rec-registry.read`. Not paginated.

    Args:
        community_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryPointDuplicates | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> DeliveryPointDuplicates | HTTPValidationError | None:
    """List Duplicate Delivery Points

     The community's delivery points that more than one active member holds (REQ-0087).

    For each point an active member of this community holds and another
    active member — here or in any other community — also holds: the point in
    its compared form (trimmed, lower-cased), this community's holders by
    member key with the spelling each stored, how many active members of
    other communities hold it, and the total. Holders in other communities are
    a count only: never their member, never their community (REQ-0085).
    Members who are not `active` hold nothing.

    The per-community view of `celine-rec-registry duplicate-delivery-points`
    (REQ-0086), for an operator console: these are the points the registry
    will refuse to give, re-give or reactivate (`delivery_point_held`) until
    resolved. A read: `rec-registry.read`. Not paginated.

    Args:
        community_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryPointDuplicates | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[DeliveryPointDuplicates | HTTPValidationError]:
    """List Duplicate Delivery Points

     The community's delivery points that more than one active member holds (REQ-0087).

    For each point an active member of this community holds and another
    active member — here or in any other community — also holds: the point in
    its compared form (trimmed, lower-cased), this community's holders by
    member key with the spelling each stored, how many active members of
    other communities hold it, and the total. Holders in other communities are
    a count only: never their member, never their community (REQ-0085).
    Members who are not `active` hold nothing.

    The per-community view of `celine-rec-registry duplicate-delivery-points`
    (REQ-0086), for an operator console: these are the points the registry
    will refuse to give, re-give or reactivate (`delivery_point_held`) until
    resolved. A read: `rec-registry.read`. Not paginated.

    Args:
        community_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryPointDuplicates | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> DeliveryPointDuplicates | HTTPValidationError | None:
    """List Duplicate Delivery Points

     The community's delivery points that more than one active member holds (REQ-0087).

    For each point an active member of this community holds and another
    active member — here or in any other community — also holds: the point in
    its compared form (trimmed, lower-cased), this community's holders by
    member key with the spelling each stored, how many active members of
    other communities hold it, and the total. Holders in other communities are
    a count only: never their member, never their community (REQ-0085).
    Members who are not `active` hold nothing.

    The per-community view of `celine-rec-registry duplicate-delivery-points`
    (REQ-0086), for an operator console: these are the points the registry
    will refuse to give, re-give or reactivate (`delivery_point_held`) until
    resolved. A read: `rec-registry.read`. Not paginated.

    Args:
        community_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryPointDuplicates | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            client=client,
        )
    ).parsed
