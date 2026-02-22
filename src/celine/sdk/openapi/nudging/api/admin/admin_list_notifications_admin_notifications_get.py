from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_notification_out import AdminNotificationOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    user_id: None | str | Unset = UNSET,
    family: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
    include_deleted: bool | Unset = False,
    unread_only: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_user_id: None | str | Unset
    if isinstance(user_id, Unset):
        json_user_id = UNSET
    else:
        json_user_id = user_id
    params["user_id"] = json_user_id

    json_family: None | str | Unset
    if isinstance(family, Unset):
        json_family = UNSET
    else:
        json_family = family
    params["family"] = json_family

    json_severity: None | str | Unset
    if isinstance(severity, Unset):
        json_severity = UNSET
    else:
        json_severity = severity
    params["severity"] = json_severity

    params["include_deleted"] = include_deleted

    params["unread_only"] = unread_only

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/notifications",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[AdminNotificationOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AdminNotificationOut.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[AdminNotificationOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    user_id: None | str | Unset = UNSET,
    family: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
    include_deleted: bool | Unset = False,
    unread_only: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[AdminNotificationOut]]:
    """List notifications (admin)

     Admin view of all notifications. Filterable by user_id, family, severity. Requires nudging.admin
    scope or admin group.

    Args:
        user_id (None | str | Unset): Filter by user ID
        family (None | str | Unset): Filter by family (energy, onboarding, …)
        severity (None | str | Unset): Filter by severity (info, warning, critical)
        include_deleted (bool | Unset): Include soft-deleted notifications Default: False.
        unread_only (bool | Unset): Return only unread notifications Default: False.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AdminNotificationOut]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        family=family,
        severity=severity,
        include_deleted=include_deleted,
        unread_only=unread_only,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    user_id: None | str | Unset = UNSET,
    family: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
    include_deleted: bool | Unset = False,
    unread_only: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[AdminNotificationOut] | None:
    """List notifications (admin)

     Admin view of all notifications. Filterable by user_id, family, severity. Requires nudging.admin
    scope or admin group.

    Args:
        user_id (None | str | Unset): Filter by user ID
        family (None | str | Unset): Filter by family (energy, onboarding, …)
        severity (None | str | Unset): Filter by severity (info, warning, critical)
        include_deleted (bool | Unset): Include soft-deleted notifications Default: False.
        unread_only (bool | Unset): Return only unread notifications Default: False.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AdminNotificationOut]
    """

    return sync_detailed(
        client=client,
        user_id=user_id,
        family=family,
        severity=severity,
        include_deleted=include_deleted,
        unread_only=unread_only,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    user_id: None | str | Unset = UNSET,
    family: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
    include_deleted: bool | Unset = False,
    unread_only: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> Response[HTTPValidationError | list[AdminNotificationOut]]:
    """List notifications (admin)

     Admin view of all notifications. Filterable by user_id, family, severity. Requires nudging.admin
    scope or admin group.

    Args:
        user_id (None | str | Unset): Filter by user ID
        family (None | str | Unset): Filter by family (energy, onboarding, …)
        severity (None | str | Unset): Filter by severity (info, warning, critical)
        include_deleted (bool | Unset): Include soft-deleted notifications Default: False.
        unread_only (bool | Unset): Return only unread notifications Default: False.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AdminNotificationOut]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        family=family,
        severity=severity,
        include_deleted=include_deleted,
        unread_only=unread_only,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    user_id: None | str | Unset = UNSET,
    family: None | str | Unset = UNSET,
    severity: None | str | Unset = UNSET,
    include_deleted: bool | Unset = False,
    unread_only: bool | Unset = False,
    limit: int | Unset = 100,
    offset: int | Unset = 0,
) -> HTTPValidationError | list[AdminNotificationOut] | None:
    """List notifications (admin)

     Admin view of all notifications. Filterable by user_id, family, severity. Requires nudging.admin
    scope or admin group.

    Args:
        user_id (None | str | Unset): Filter by user ID
        family (None | str | Unset): Filter by family (energy, onboarding, …)
        severity (None | str | Unset): Filter by severity (info, warning, critical)
        include_deleted (bool | Unset): Include soft-deleted notifications Default: False.
        unread_only (bool | Unset): Return only unread notifications Default: False.
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AdminNotificationOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            user_id=user_id,
            family=family,
            severity=severity,
            include_deleted=include_deleted,
            unread_only=unread_only,
            limit=limit,
            offset=offset,
        )
    ).parsed
