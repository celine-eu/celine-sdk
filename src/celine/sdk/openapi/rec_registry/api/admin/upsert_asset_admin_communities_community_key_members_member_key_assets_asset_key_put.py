from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_upsert import AssetUpsert
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    body: AssetUpsert,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/members/{member_key}/assets/{asset_key}".format(
            community_key=quote(str(community_key), safe=""),
            member_key=quote(str(member_key), safe=""),
            asset_key=quote(str(asset_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> Response[Any | HTTPValidationError]:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        asset_key=asset_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> Any | HTTPValidationError | None:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        member_key=member_key,
        asset_key=asset_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> Response[Any | HTTPValidationError]:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        asset_key=asset_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> Any | HTTPValidationError | None:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            asset_key=asset_key,
            client=client,
            body=body,
        )
    ).parsed
