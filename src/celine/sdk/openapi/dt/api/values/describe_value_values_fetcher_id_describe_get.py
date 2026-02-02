from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_describe_value_values_fetcher_id_describe_get import (
    ResponseDescribeValueValuesFetcherIdDescribeGet,
)
from ...types import Response


def _get_kwargs(
    fetcher_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/values/{fetcher_id}/describe".format(
            fetcher_id=quote(str(fetcher_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet | None:
    if response.status_code == 200:
        response_200 = ResponseDescribeValueValuesFetcherIdDescribeGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet]:
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
) -> Response[HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet]:
    """Describe Value

     Describe a value fetcher: metadata + payload schema.

    Args:
        fetcher_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet]
    """

    kwargs = _get_kwargs(
        fetcher_id=fetcher_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet | None:
    """Describe Value

     Describe a value fetcher: metadata + payload schema.

    Args:
        fetcher_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet
    """

    return sync_detailed(
        fetcher_id=fetcher_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet]:
    """Describe Value

     Describe a value fetcher: metadata + payload schema.

    Args:
        fetcher_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet]
    """

    kwargs = _get_kwargs(
        fetcher_id=fetcher_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet | None:
    """Describe Value

     Describe a value fetcher: metadata + payload schema.

    Args:
        fetcher_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseDescribeValueValuesFetcherIdDescribeGet
    """

    return (
        await asyncio_detailed(
            fetcher_id=fetcher_id,
            client=client,
        )
    ).parsed
