from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.import_report import ImportReport
from ...models.import_request import ImportRequest
from ...types import Response


def _get_kwargs(
    *,
    body: ImportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/import",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ImportReport | None:
    if response.status_code == 200:
        response_200 = ImportReport.from_dict(response.json())

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
) -> Response[HTTPValidationError | ImportReport]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ImportRequest,
) -> Response[HTTPValidationError | ImportReport]:
    """Admin Import

     Idempotent replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    Use `dry_run=true` to validate without making changes.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ImportReport]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: ImportRequest,
) -> HTTPValidationError | ImportReport | None:
    """Admin Import

     Idempotent replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    Use `dry_run=true` to validate without making changes.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ImportReport
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ImportRequest,
) -> Response[HTTPValidationError | ImportReport]:
    """Admin Import

     Idempotent replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    Use `dry_run=true` to validate without making changes.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ImportReport]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: ImportRequest,
) -> HTTPValidationError | ImportReport | None:
    """Admin Import

     Idempotent replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    Use `dry_run=true` to validate without making changes.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ImportReport
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
