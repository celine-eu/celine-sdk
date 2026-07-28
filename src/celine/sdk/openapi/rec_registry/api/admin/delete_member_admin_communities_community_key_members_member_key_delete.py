from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.deletion_report import DeletionReport
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community_key: str,
    member_key: str,
    *,
    purge: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["purge"] = purge

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/admin/communities/{community_key}/members/{member_key}".format(
            community_key=quote(str(community_key), safe=""),
            member_key=quote(str(member_key), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DeletionReport | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DeletionReport.from_dict(response.json())

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
) -> Response[DeletionReport | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    purge: bool | Unset = False,
) -> Response[DeletionReport | HTTPValidationError]:
    """Delete Member

     Deactivate a member, or erase one.

    Deactivation is the default because a member who leaves still has historical
    metering data, past consents and provenance elsewhere in the platform that
    reference them — and `Asset` cascades on delete, so a real removal silently
    takes their meters too.

    `purge=true` is for an erasure request. It is authorized separately from
    ordinary member writes, so a service that manages members day to day cannot
    perform one.

    Args:
        community_key (str):
        member_key (str):
        purge (bool | Unset): Permanently remove the member and its assets. Requires the rec-
            registry.members.purge grant. Without it the member is deactivated, which is reversible.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletionReport | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        purge=purge,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    purge: bool | Unset = False,
) -> DeletionReport | HTTPValidationError | None:
    """Delete Member

     Deactivate a member, or erase one.

    Deactivation is the default because a member who leaves still has historical
    metering data, past consents and provenance elsewhere in the platform that
    reference them — and `Asset` cascades on delete, so a real removal silently
    takes their meters too.

    `purge=true` is for an erasure request. It is authorized separately from
    ordinary member writes, so a service that manages members day to day cannot
    perform one.

    Args:
        community_key (str):
        member_key (str):
        purge (bool | Unset): Permanently remove the member and its assets. Requires the rec-
            registry.members.purge grant. Without it the member is deactivated, which is reversible.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletionReport | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        member_key=member_key,
        client=client,
        purge=purge,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    purge: bool | Unset = False,
) -> Response[DeletionReport | HTTPValidationError]:
    """Delete Member

     Deactivate a member, or erase one.

    Deactivation is the default because a member who leaves still has historical
    metering data, past consents and provenance elsewhere in the platform that
    reference them — and `Asset` cascades on delete, so a real removal silently
    takes their meters too.

    `purge=true` is for an erasure request. It is authorized separately from
    ordinary member writes, so a service that manages members day to day cannot
    perform one.

    Args:
        community_key (str):
        member_key (str):
        purge (bool | Unset): Permanently remove the member and its assets. Requires the rec-
            registry.members.purge grant. Without it the member is deactivated, which is reversible.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeletionReport | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        purge=purge,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    purge: bool | Unset = False,
) -> DeletionReport | HTTPValidationError | None:
    """Delete Member

     Deactivate a member, or erase one.

    Deactivation is the default because a member who leaves still has historical
    metering data, past consents and provenance elsewhere in the platform that
    reference them — and `Asset` cascades on delete, so a real removal silently
    takes their meters too.

    `purge=true` is for an erasure request. It is authorized separately from
    ordinary member writes, so a service that manages members day to day cannot
    perform one.

    Args:
        community_key (str):
        member_key (str):
        purge (bool | Unset): Permanently remove the member and its assets. Requires the rec-
            registry.members.purge grant. Without it the member is deactivated, which is reversible.
            Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeletionReport | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            client=client,
            purge=purge,
        )
    ).parsed
