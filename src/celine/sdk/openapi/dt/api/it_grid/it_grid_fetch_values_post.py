from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.fetch_result_schema import FetchResultSchema
from ...models.http_validation_error import HTTPValidationError
from ...models.values_request_schema import ValuesRequestSchema
from ...types import Response


def _get_kwargs(
    network_id: str,
    fetcher_id: str,
    *,
    body: ValuesRequestSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/grid/{network_id}/values/{fetcher_id}".format(
            network_id=quote(str(network_id), safe=""),
            fetcher_id=quote(str(fetcher_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    network_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequestSchema,
) -> Response[FetchResultSchema | HTTPValidationError]:
    """Fetch Values Post

    Args:
        network_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FetchResultSchema | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        network_id=network_id,
        fetcher_id=fetcher_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    network_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequestSchema,
) -> FetchResultSchema | HTTPValidationError | None:
    """Fetch Values Post

    Args:
        network_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FetchResultSchema | HTTPValidationError
    """

    return sync_detailed(
        network_id=network_id,
        fetcher_id=fetcher_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    network_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequestSchema,
) -> Response[FetchResultSchema | HTTPValidationError]:
    """Fetch Values Post

    Args:
        network_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FetchResultSchema | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        network_id=network_id,
        fetcher_id=fetcher_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    network_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequestSchema,
) -> FetchResultSchema | HTTPValidationError | None:
    """Fetch Values Post

    Args:
        network_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FetchResultSchema | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            network_id=network_id,
            fetcher_id=fetcher_id,
            client=client,
            body=body,
        )
    ).parsed
