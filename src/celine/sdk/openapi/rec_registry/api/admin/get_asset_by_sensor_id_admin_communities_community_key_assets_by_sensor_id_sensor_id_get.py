from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_detail import AssetDetail
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    sensor_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/communities/{community_key}/assets/by-sensor-id/{sensor_id}".format(
            community_key=quote(str(community_key), safe=""),
            sensor_id=quote(str(sensor_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AssetDetail | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = AssetDetail.from_dict(response.json())

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
) -> Response[AssetDetail | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    sensor_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AssetDetail | HTTPValidationError]:
    """Get Asset By Sensor Id

     Get an asset by its sensor_id.

    Args:
        community_key (str):
        sensor_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetDetail | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        sensor_id=sensor_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    sensor_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> AssetDetail | HTTPValidationError | None:
    """Get Asset By Sensor Id

     Get an asset by its sensor_id.

    Args:
        community_key (str):
        sensor_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetDetail | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        sensor_id=sensor_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    sensor_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[AssetDetail | HTTPValidationError]:
    """Get Asset By Sensor Id

     Get an asset by its sensor_id.

    Args:
        community_key (str):
        sensor_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetDetail | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        sensor_id=sensor_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    sensor_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> AssetDetail | HTTPValidationError | None:
    """Get Asset By Sensor Id

     Get an asset by its sensor_id.

    Args:
        community_key (str):
        sensor_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetDetail | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            sensor_id=sensor_id,
            client=client,
        )
    ).parsed
