from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery_point_in import DeliveryPointIn
from ...models.delivery_points_response import DeliveryPointsResponse
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community_key: str,
    member_key: str,
    point_id: str,
    *,
    body: DeliveryPointIn,
    replaces: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_replaces: None | str | Unset
    if isinstance(replaces, Unset):
        json_replaces = UNSET
    else:
        json_replaces = replaces
    params["replaces"] = json_replaces

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/members/{member_key}/delivery-points/{point_id}".format(
            community_key=quote(str(community_key), safe=""),
            member_key=quote(str(member_key), safe=""),
            point_id=quote(str(point_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeliveryPointsResponse | ErrorResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DeliveryPointsResponse.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DeliveryPointsResponse | ErrorResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    member_key: str,
    point_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeliveryPointIn,
    replaces: None | str | Unset = UNSET,
) -> Response[DeliveryPointsResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    **`?replaces={old}` corrects a point in one write** (REQ-0084): the new
    point is added, `old` (trimmed, case-insensitive) is removed, and the
    member's meters whose `properties.pod` named `old` are relinked to the
    new id, as the path spells it — all in one transaction, so a failure
    leaves both points and every link as they were. `404` when `old` is not
    this member's point. The query never changes the action: this route
    derives `members.delivery_points.write` either way (REQ-0081).

    An `active` member taking a point another active member holds, in any
    community, is `409 delivery_point_held` (REQ-0085), and nothing changes.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        replaces (None | str | Unset): Correct a delivery point: the id of the member's point this
            one replaces. In one transaction the new point is added, this one removed, and the
            member's meters whose `pod` named it are relinked to the new id. `404` when the member has
            no such point.
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryPointsResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        point_id=point_id,
        body=body,
        replaces=replaces,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    member_key: str,
    point_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeliveryPointIn,
    replaces: None | str | Unset = UNSET,
) -> DeliveryPointsResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    **`?replaces={old}` corrects a point in one write** (REQ-0084): the new
    point is added, `old` (trimmed, case-insensitive) is removed, and the
    member's meters whose `properties.pod` named `old` are relinked to the
    new id, as the path spells it — all in one transaction, so a failure
    leaves both points and every link as they were. `404` when `old` is not
    this member's point. The query never changes the action: this route
    derives `members.delivery_points.write` either way (REQ-0081).

    An `active` member taking a point another active member holds, in any
    community, is `409 delivery_point_held` (REQ-0085), and nothing changes.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        replaces (None | str | Unset): Correct a delivery point: the id of the member's point this
            one replaces. In one transaction the new point is added, this one removed, and the
            member's meters whose `pod` named it are relinked to the new id. `404` when the member has
            no such point.
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryPointsResponse | ErrorResponse | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        member_key=member_key,
        point_id=point_id,
        client=client,
        body=body,
        replaces=replaces,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    member_key: str,
    point_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeliveryPointIn,
    replaces: None | str | Unset = UNSET,
) -> Response[DeliveryPointsResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    **`?replaces={old}` corrects a point in one write** (REQ-0084): the new
    point is added, `old` (trimmed, case-insensitive) is removed, and the
    member's meters whose `properties.pod` named `old` are relinked to the
    new id, as the path spells it — all in one transaction, so a failure
    leaves both points and every link as they were. `404` when `old` is not
    this member's point. The query never changes the action: this route
    derives `members.delivery_points.write` either way (REQ-0081).

    An `active` member taking a point another active member holds, in any
    community, is `409 delivery_point_held` (REQ-0085), and nothing changes.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        replaces (None | str | Unset): Correct a delivery point: the id of the member's point this
            one replaces. In one transaction the new point is added, this one removed, and the
            member's meters whose `pod` named it are relinked to the new id. `404` when the member has
            no such point.
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryPointsResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        point_id=point_id,
        body=body,
        replaces=replaces,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    member_key: str,
    point_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeliveryPointIn,
    replaces: None | str | Unset = UNSET,
) -> DeliveryPointsResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    **`?replaces={old}` corrects a point in one write** (REQ-0084): the new
    point is added, `old` (trimmed, case-insensitive) is removed, and the
    member's meters whose `properties.pod` named `old` are relinked to the
    new id, as the path spells it — all in one transaction, so a failure
    leaves both points and every link as they were. `404` when `old` is not
    this member's point. The query never changes the action: this route
    derives `members.delivery_points.write` either way (REQ-0081).

    An `active` member taking a point another active member holds, in any
    community, is `409 delivery_point_held` (REQ-0085), and nothing changes.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        replaces (None | str | Unset): Correct a delivery point: the id of the member's point this
            one replaces. In one transaction the new point is added, this one removed, and the
            member's meters whose `pod` named it are relinked to the new id. `404` when the member has
            no such point.
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryPointsResponse | ErrorResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            point_id=point_id,
            client=client,
            body=body,
            replaces=replaces,
        )
    ).parsed
