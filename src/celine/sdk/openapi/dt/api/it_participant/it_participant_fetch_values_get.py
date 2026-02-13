from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.fetch_result_schema import FetchResultSchema
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    participant_id: str,
    fetcher_id: str,
    *,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_limit: int | None | Unset
    if isinstance(limit, Unset):
        json_limit = UNSET
    else:
        json_limit = limit
    params["limit"] = json_limit

    json_offset: int | None | Unset
    if isinstance(offset, Unset):
        json_offset = UNSET
    else:
        json_offset = offset
    params["offset"] = json_offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/participants/{participant_id}/values/{fetcher_id}".format(
            participant_id=quote(str(participant_id), safe=""),
            fetcher_id=quote(str(fetcher_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> FetchResultSchema | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = FetchResultSchema.from_dict(response.json())

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
) -> Response[FetchResultSchema | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    participant_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Response[FetchResultSchema | HTTPValidationError]:
    """Fetch Values Get

    Args:
        participant_id (str):
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FetchResultSchema | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        fetcher_id=fetcher_id,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    participant_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> FetchResultSchema | HTTPValidationError | None:
    """Fetch Values Get

    Args:
        participant_id (str):
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FetchResultSchema | HTTPValidationError
    """

    return sync_detailed(
        participant_id=participant_id,
        fetcher_id=fetcher_id,
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    participant_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Response[FetchResultSchema | HTTPValidationError]:
    """Fetch Values Get

    Args:
        participant_id (str):
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FetchResultSchema | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        fetcher_id=fetcher_id,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    participant_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> FetchResultSchema | HTTPValidationError | None:
    """Fetch Values Get

    Args:
        participant_id (str):
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FetchResultSchema | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            participant_id=participant_id,
            fetcher_id=fetcher_id,
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
