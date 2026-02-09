from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_it_energy_community_post_value import ResponseItEnergyCommunityPostValue
from ...models.values_request import ValuesRequest
from ...types import Response


def _get_kwargs(
    community_id: str,
    fetcher_id: str,
    *,
    body: ValuesRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/communities/it/{community_id}/values/{fetcher_id}".format(
            community_id=quote(str(community_id), safe=""),
            fetcher_id=quote(str(fetcher_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseItEnergyCommunityPostValue | None:
    if response.status_code == 200:
        response_200 = ResponseItEnergyCommunityPostValue.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseItEnergyCommunityPostValue]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
) -> Response[HTTPValidationError | ResponseItEnergyCommunityPostValue]:
    """Post Value

     Fetch a value using a JSON payload.

    Args:
        community_id (str):
        fetcher_id (str):
        body (ValuesRequest): POST body for the values API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseItEnergyCommunityPostValue]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
        fetcher_id=fetcher_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
) -> HTTPValidationError | ResponseItEnergyCommunityPostValue | None:
    """Post Value

     Fetch a value using a JSON payload.

    Args:
        community_id (str):
        fetcher_id (str):
        body (ValuesRequest): POST body for the values API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseItEnergyCommunityPostValue
    """

    return sync_detailed(
        community_id=community_id,
        fetcher_id=fetcher_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
) -> Response[HTTPValidationError | ResponseItEnergyCommunityPostValue]:
    """Post Value

     Fetch a value using a JSON payload.

    Args:
        community_id (str):
        fetcher_id (str):
        body (ValuesRequest): POST body for the values API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseItEnergyCommunityPostValue]
    """

    kwargs = _get_kwargs(
        community_id=community_id,
        fetcher_id=fetcher_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
) -> HTTPValidationError | ResponseItEnergyCommunityPostValue | None:
    """Post Value

     Fetch a value using a JSON payload.

    Args:
        community_id (str):
        fetcher_id (str):
        body (ValuesRequest): POST body for the values API.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseItEnergyCommunityPostValue
    """

    return (
        await asyncio_detailed(
            community_id=community_id,
            fetcher_id=fetcher_id,
            client=client,
            body=body,
        )
    ).parsed
