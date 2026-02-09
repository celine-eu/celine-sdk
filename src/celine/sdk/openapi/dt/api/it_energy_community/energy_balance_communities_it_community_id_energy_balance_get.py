from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_energy_balance_communities_it_community_id_energy_balance_get import (
    ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community_id: str,
    *,
    start: None | str | Unset = UNSET,
    end: None | str | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start: None | str | Unset
    if isinstance(start, Unset):
        json_start = UNSET
    else:
        json_start = start
    params["start"] = json_start

    json_end: None | str | Unset
    if isinstance(end, Unset):
        json_end = UNSET
    else:
        json_end = end
    params["end"] = json_end

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/communities/it/{community_id}/energy-balance".format(
            community_id=quote(str(community_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet | None:
    if response.status_code == 200:
        response_200 = ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
    start: None | str | Unset = UNSET,
    end: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet]:
    """Energy Balance

     Compute current energy balance for the community.

    This is a sample custom endpoint. A real implementation would
    fetch consumption + generation timeseries and compute metrics.

    Args:
        community_id (str):
        start (None | str | Unset):
        end (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
        start=start,
        end=end,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
    start: None | str | Unset = UNSET,
    end: None | str | Unset = UNSET,
) -> HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet | None:
    """Energy Balance

     Compute current energy balance for the community.

    This is a sample custom endpoint. A real implementation would
    fetch consumption + generation timeseries and compute metrics.

    Args:
        community_id (str):
        start (None | str | Unset):
        end (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet
    """

    return sync_detailed(
        community_id=community_id,
        client=client,
        start=start,
        end=end,
    ).parsed


async def asyncio_detailed(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
    start: None | str | Unset = UNSET,
    end: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet]:
    """Energy Balance

     Compute current energy balance for the community.

    This is a sample custom endpoint. A real implementation would
    fetch consumption + generation timeseries and compute metrics.

    Args:
        community_id (str):
        start (None | str | Unset):
        end (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
        start=start,
        end=end,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_id: str,
    *,
    client: AuthenticatedClient | Client,
    start: None | str | Unset = UNSET,
    end: None | str | Unset = UNSET,
) -> HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet | None:
    """Energy Balance

     Compute current energy balance for the community.

    This is a sample custom endpoint. A real implementation would
    fetch consumption + generation timeseries and compute metrics.

    Args:
        community_id (str):
        start (None | str | Unset):
        end (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseEnergyBalanceCommunitiesItCommunityIdEnergyBalanceGet
    """

    return (
        await asyncio_detailed(
            community_id=community_id,
            client=client,
            start=start,
            end=end,
        )
    ).parsed
