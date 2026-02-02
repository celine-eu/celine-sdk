from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_post_value_values_fetcher_id_post import ResponsePostValueValuesFetcherIdPost
from ...models.values_request import ValuesRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    fetcher_id: str,
    *,
    body: ValuesRequest,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

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
        "method": "post",
        "url": "/values/{fetcher_id}".format(
            fetcher_id=quote(str(fetcher_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponsePostValueValuesFetcherIdPost | None:
    if response.status_code == 200:
        response_200 = ResponsePostValueValuesFetcherIdPost.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponsePostValueValuesFetcherIdPost]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Response[HTTPValidationError | ResponsePostValueValuesFetcherIdPost]:
    """Post Value

     Fetch values using JSON payload.

    Args:
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):
        body (ValuesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponsePostValueValuesFetcherIdPost]
    """

    kwargs = _get_kwargs(
        fetcher_id=fetcher_id,
        body=body,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> HTTPValidationError | ResponsePostValueValuesFetcherIdPost | None:
    """Post Value

     Fetch values using JSON payload.

    Args:
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):
        body (ValuesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponsePostValueValuesFetcherIdPost
    """

    return sync_detailed(
        fetcher_id=fetcher_id,
        client=client,
        body=body,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Response[HTTPValidationError | ResponsePostValueValuesFetcherIdPost]:
    """Post Value

     Fetch values using JSON payload.

    Args:
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):
        body (ValuesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponsePostValueValuesFetcherIdPost]
    """

    kwargs = _get_kwargs(
        fetcher_id=fetcher_id,
        body=body,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequest,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> HTTPValidationError | ResponsePostValueValuesFetcherIdPost | None:
    """Post Value

     Fetch values using JSON payload.

    Args:
        fetcher_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):
        body (ValuesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponsePostValueValuesFetcherIdPost
    """

    return (
        await asyncio_detailed(
            fetcher_id=fetcher_id,
            client=client,
            body=body,
            limit=limit,
            offset=offset,
        )
    ).parsed
