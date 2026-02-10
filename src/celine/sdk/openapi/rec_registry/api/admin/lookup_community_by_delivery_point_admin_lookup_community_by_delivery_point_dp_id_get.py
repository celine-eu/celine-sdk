from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.lookup_by_delivery_point_response import LookupByDeliveryPointResponse
from ...types import Response


def _get_kwargs(
    dp_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/lookup/community-by-delivery-point/{dp_id}".format(
            dp_id=quote(str(dp_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | LookupByDeliveryPointResponse | None:
    if response.status_code == 200:
        response_200 = LookupByDeliveryPointResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | LookupByDeliveryPointResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dp_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | LookupByDeliveryPointResponse]:
    """Lookup Community By Delivery Point

     Find which community a delivery point belongs to.

    Args:
        dp_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LookupByDeliveryPointResponse]
    """

    kwargs = _get_kwargs(
        dp_id=dp_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dp_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | LookupByDeliveryPointResponse | None:
    """Lookup Community By Delivery Point

     Find which community a delivery point belongs to.

    Args:
        dp_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LookupByDeliveryPointResponse
    """

    return sync_detailed(
        dp_id=dp_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    dp_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | LookupByDeliveryPointResponse]:
    """Lookup Community By Delivery Point

     Find which community a delivery point belongs to.

    Args:
        dp_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LookupByDeliveryPointResponse]
    """

    kwargs = _get_kwargs(
        dp_id=dp_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dp_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | LookupByDeliveryPointResponse | None:
    """Lookup Community By Delivery Point

     Find which community a delivery point belongs to.

    Args:
        dp_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LookupByDeliveryPointResponse
    """

    return (
        await asyncio_detailed(
            dp_id=dp_id,
            client=client,
        )
    ).parsed
