from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.value_response_schema import ValueResponseSchema
from ...models.values_request_schema import ValuesRequestSchema
from ...types import Response


def _get_kwargs(
    participant_id: str,
    fetcher_id: str,
    *,
    body: ValuesRequestSchema,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/participants/{participant_id}/values/{fetcher_id}".format(
            participant_id=quote(str(participant_id), safe=""),
            fetcher_id=quote(str(fetcher_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ValueResponseSchema | None:
    if response.status_code == 200:
        response_200 = ValueResponseSchema.from_dict(response.json())

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
) -> Response[HTTPValidationError | ValueResponseSchema]:
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
    body: ValuesRequestSchema,
) -> Response[HTTPValidationError | ValueResponseSchema]:
    """Post Value

    Args:
        participant_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ValueResponseSchema]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        fetcher_id=fetcher_id,
        body=body,
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
    body: ValuesRequestSchema,
) -> HTTPValidationError | ValueResponseSchema | None:
    """Post Value

    Args:
        participant_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ValueResponseSchema
    """

    return sync_detailed(
        participant_id=participant_id,
        fetcher_id=fetcher_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    participant_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequestSchema,
) -> Response[HTTPValidationError | ValueResponseSchema]:
    """Post Value

    Args:
        participant_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ValueResponseSchema]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        fetcher_id=fetcher_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    participant_id: str,
    fetcher_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: ValuesRequestSchema,
) -> HTTPValidationError | ValueResponseSchema | None:
    """Post Value

    Args:
        participant_id (str):
        fetcher_id (str):
        body (ValuesRequestSchema):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ValueResponseSchema
    """

    return (
        await asyncio_detailed(
            participant_id=participant_id,
            fetcher_id=fetcher_id,
            client=client,
            body=body,
        )
    ).parsed
