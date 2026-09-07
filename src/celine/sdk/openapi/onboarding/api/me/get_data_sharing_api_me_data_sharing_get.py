from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.data_sharing_status_response import DataSharingStatusResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/me/data-sharing",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DataSharingStatusResponse | None:
    if response.status_code == 200:
        response_200 = DataSharingStatusResponse.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DataSharingStatusResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[DataSharingStatusResponse]:
    """Get Data Sharing

     What this member is sharing, and what they could share.

    Offers come from the published vocabulary through the REC's allow-list, and
    decisions from the connector under the member's own credential, so what is
    shown here and what the dataspace enforces cannot drift.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSharingStatusResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> DataSharingStatusResponse | None:
    """Get Data Sharing

     What this member is sharing, and what they could share.

    Offers come from the published vocabulary through the REC's allow-list, and
    decisions from the connector under the member's own credential, so what is
    shown here and what the dataspace enforces cannot drift.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSharingStatusResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[DataSharingStatusResponse]:
    """Get Data Sharing

     What this member is sharing, and what they could share.

    Offers come from the published vocabulary through the REC's allow-list, and
    decisions from the connector under the member's own credential, so what is
    shown here and what the dataspace enforces cannot drift.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DataSharingStatusResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> DataSharingStatusResponse | None:
    """Get Data Sharing

     What this member is sharing, and what they could share.

    Offers come from the published vocabulary through the REC's allow-list, and
    decisions from the connector under the member's own credential, so what is
    shown here and what the dataspace enforces cannot drift.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DataSharingStatusResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
