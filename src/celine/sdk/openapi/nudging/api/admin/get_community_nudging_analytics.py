import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.community_nudging_analytics_out import CommunityNudgingAnalyticsOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    community_id: str,
    *,
    start: datetime.date,
    end: datetime.date,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_start = start.isoformat()
    params["start"] = json_start

    json_end = end.isoformat()
    params["end"] = json_end

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/admin/analytics/communities/{community_id}/conversion".format(
            community_id=quote(str(community_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommunityNudgingAnalyticsOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CommunityNudgingAnalyticsOut.from_dict(response.json())

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
) -> Response[CommunityNudgingAnalyticsOut | HTTPValidationError]:
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
    start: datetime.date,
    end: datetime.date,
) -> Response[CommunityNudgingAnalyticsOut | HTTPValidationError]:
    """Get aggregate nudging analytics for one REC

     Returns funnel, rule, failure and reachability aggregates only. No participant identity, destination
    or message content is returned.

    Args:
        community_id (str):
        start (datetime.date): First UTC calendar day, inclusive
        end (datetime.date): Last UTC calendar day, inclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityNudgingAnalyticsOut | HTTPValidationError]
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
    start: datetime.date,
    end: datetime.date,
) -> CommunityNudgingAnalyticsOut | HTTPValidationError | None:
    """Get aggregate nudging analytics for one REC

     Returns funnel, rule, failure and reachability aggregates only. No participant identity, destination
    or message content is returned.

    Args:
        community_id (str):
        start (datetime.date): First UTC calendar day, inclusive
        end (datetime.date): Last UTC calendar day, inclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityNudgingAnalyticsOut | HTTPValidationError
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
    start: datetime.date,
    end: datetime.date,
) -> Response[CommunityNudgingAnalyticsOut | HTTPValidationError]:
    """Get aggregate nudging analytics for one REC

     Returns funnel, rule, failure and reachability aggregates only. No participant identity, destination
    or message content is returned.

    Args:
        community_id (str):
        start (datetime.date): First UTC calendar day, inclusive
        end (datetime.date): Last UTC calendar day, inclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityNudgingAnalyticsOut | HTTPValidationError]
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
    start: datetime.date,
    end: datetime.date,
) -> CommunityNudgingAnalyticsOut | HTTPValidationError | None:
    """Get aggregate nudging analytics for one REC

     Returns funnel, rule, failure and reachability aggregates only. No participant identity, destination
    or message content is returned.

    Args:
        community_id (str):
        start (datetime.date): First UTC calendar day, inclusive
        end (datetime.date): Last UTC calendar day, inclusive

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityNudgingAnalyticsOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_id=community_id,
            client=client,
            start=start,
            end=end,
        )
    ).parsed
