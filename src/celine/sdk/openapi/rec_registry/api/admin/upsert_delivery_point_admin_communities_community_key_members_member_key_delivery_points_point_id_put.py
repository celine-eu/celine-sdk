from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delivery_point_in import DeliveryPointIn
from ...models.delivery_points_response import DeliveryPointsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    member_key: str,
    point_id: str,
    *,
    body: DeliveryPointIn,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/members/{member_key}/delivery-points/{point_id}".format(
            community_key=quote(str(community_key), safe=""),
            member_key=quote(str(member_key), safe=""),
            point_id=quote(str(point_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeliveryPointsResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DeliveryPointsResponse.from_dict(response.json())

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
) -> Response[DeliveryPointsResponse | HTTPValidationError]:
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
) -> Response[DeliveryPointsResponse | HTTPValidationError]:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryPointsResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        point_id=point_id,
        body=body,
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
) -> DeliveryPointsResponse | HTTPValidationError | None:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryPointsResponse | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        member_key=member_key,
        point_id=point_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    member_key: str,
    point_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: DeliveryPointIn,
) -> Response[DeliveryPointsResponse | HTTPValidationError]:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeliveryPointsResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        point_id=point_id,
        body=body,
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
) -> DeliveryPointsResponse | HTTPValidationError | None:
    """Upsert Delivery Point

     Add or replace one supply point, keeping the others.

    A sub-resource rather than a field on the member, because `delivery_points`
    is a JSONB list: a member gaining a second supply point must not lose the
    first, which is exactly what a naive whole-field update does.

    Args:
        community_key (str):
        member_key (str):
        point_id (str):
        body (DeliveryPointIn): Physical delivery point (POD, CUPS, PRM, etc.).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeliveryPointsResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            point_id=point_id,
            client=client,
            body=body,
        )
    ).parsed
