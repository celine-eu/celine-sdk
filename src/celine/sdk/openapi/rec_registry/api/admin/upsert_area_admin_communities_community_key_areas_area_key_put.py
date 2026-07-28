from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.area_upsert import AreaUpsert
from ...models.community_detail import CommunityDetail
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    area_key: str,
    *,
    body: AreaUpsert,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/areas/{area_key}".format(
            community_key=quote(str(community_key), safe=""),
            area_key=quote(str(area_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommunityDetail | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CommunityDetail.from_dict(response.json())

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
) -> Response[CommunityDetail | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> Response[CommunityDetail | HTTPValidationError]:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        area_key=area_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> CommunityDetail | HTTPValidationError | None:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        area_key=area_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> Response[CommunityDetail | HTTPValidationError]:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        area_key=area_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> CommunityDetail | HTTPValidationError | None:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            area_key=area_key,
            client=client,
            body=body,
        )
    ).parsed
