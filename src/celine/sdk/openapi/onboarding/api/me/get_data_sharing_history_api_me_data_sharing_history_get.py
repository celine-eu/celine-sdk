from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data_sharing_history_response import DataSharingHistoryResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/me/data-sharing/history",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DataSharingHistoryResponse | None:
    if response.status_code == 200:
        response_200 = DataSharingHistoryResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DataSharingHistoryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[DataSharingHistoryResponse]:
    """Get Data Sharing History

     What has happened with this member's data, from their own record.

    Absent provenance returns an empty list rather than failing: the decisions
    stand without their history, and refusing the whole page for a detail is
    worse than showing it without one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSharingHistoryResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> DataSharingHistoryResponse | None:
    """Get Data Sharing History

     What has happened with this member's data, from their own record.

    Absent provenance returns an empty list rather than failing: the decisions
    stand without their history, and refusing the whole page for a detail is
    worse than showing it without one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSharingHistoryResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[DataSharingHistoryResponse]:
    """Get Data Sharing History

     What has happened with this member's data, from their own record.

    Absent provenance returns an empty list rather than failing: the decisions
    stand without their history, and refusing the whole page for a detail is
    worse than showing it without one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSharingHistoryResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> DataSharingHistoryResponse | None:
    """Get Data Sharing History

     What has happened with this member's data, from their own record.

    Absent provenance returns an empty list rather than failing: the decisions
    stand without their history, and refusing the whole page for a detail is
    worse than showing it without one.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSharingHistoryResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
