from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.user_asset_detail import UserAssetDetail
from ...types import Response


def _get_kwargs(
    asset_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user/assets/{asset_key}".format(
            asset_key=quote(str(asset_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UserAssetDetail | None:
    if response.status_code == 200:
        response_200 = UserAssetDetail.from_dict(response.json())

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
) -> Response[HTTPValidationError | UserAssetDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | UserAssetDetail]:
    """Get My Asset

     Get a specific asset owned by the current user.

    Args:
        asset_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UserAssetDetail]
    """

    kwargs = _get_kwargs(
        asset_key=asset_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | UserAssetDetail | None:
    """Get My Asset

     Get a specific asset owned by the current user.

    Args:
        asset_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UserAssetDetail
    """

    return sync_detailed(
        asset_key=asset_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | UserAssetDetail]:
    """Get My Asset

     Get a specific asset owned by the current user.

    Args:
        asset_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UserAssetDetail]
    """

    kwargs = _get_kwargs(
        asset_key=asset_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | UserAssetDetail | None:
    """Get My Asset

     Get a specific asset owned by the current user.

    Args:
        asset_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UserAssetDetail
    """

    return (
        await asyncio_detailed(
            asset_key=asset_key,
            client=client,
        )
    ).parsed
