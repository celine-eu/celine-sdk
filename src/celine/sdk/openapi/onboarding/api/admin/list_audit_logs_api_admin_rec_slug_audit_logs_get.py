from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.audit_log_read import AuditLogRead
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    rec_slug: str,
    *,
    skip: int | Unset = 0,
    limit: int | Unset = 100,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/{rec_slug}/audit-logs".format(
            rec_slug=quote(str(rec_slug), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[AuditLogRead] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AuditLogRead.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[AuditLogRead]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[HTTPValidationError | list[AuditLogRead]]:
    """List Audit Logs

     Scoped to the community in the path.

    The previous endpoint sat under `/api/{rec}/admin` but ignored the slug, so
    any token holder read the whole deployment's history. Rows written before
    `rec_slug` existed and not recovered by the 0009 backfill are excluded: they
    name no community, and showing them under an arbitrary one would invent the
    fact.

    Reading the trail is deliberately *not* itself audited. It is a read granted
    to every tier, and logging each view would bury the actions worth finding
    under the act of looking for them.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AuditLogRead]]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        skip=skip,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 100,
) -> HTTPValidationError | list[AuditLogRead] | None:
    """List Audit Logs

     Scoped to the community in the path.

    The previous endpoint sat under `/api/{rec}/admin` but ignored the slug, so
    any token holder read the whole deployment's history. Rows written before
    `rec_slug` existed and not recovered by the 0009 backfill are excluded: they
    name no community, and showing them under an arbitrary one would invent the
    fact.

    Reading the trail is deliberately *not* itself audited. It is a read granted
    to every tier, and logging each view would bury the actions worth finding
    under the act of looking for them.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AuditLogRead]
    """

    return sync_detailed(
        rec_slug=rec_slug,
        client=client,
        skip=skip,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 100,
) -> Response[HTTPValidationError | list[AuditLogRead]]:
    """List Audit Logs

     Scoped to the community in the path.

    The previous endpoint sat under `/api/{rec}/admin` but ignored the slug, so
    any token holder read the whole deployment's history. Rows written before
    `rec_slug` existed and not recovered by the 0009 backfill are excluded: they
    name no community, and showing them under an arbitrary one would invent the
    fact.

    Reading the trail is deliberately *not* itself audited. It is a read granted
    to every tier, and logging each view would bury the actions worth finding
    under the act of looking for them.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[AuditLogRead]]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        skip=skip,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 100,
) -> HTTPValidationError | list[AuditLogRead] | None:
    """List Audit Logs

     Scoped to the community in the path.

    The previous endpoint sat under `/api/{rec}/admin` but ignored the slug, so
    any token holder read the whole deployment's history. Rows written before
    `rec_slug` existed and not recovered by the 0009 backfill are excluded: they
    name no community, and showing them under an arbitrary one would invent the
    fact.

    Reading the trail is deliberately *not* itself audited. It is a read granted
    to every tier, and logging each view would bury the actions worth finding
    under the act of looking for them.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[AuditLogRead]
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            client=client,
            skip=skip,
            limit=limit,
        )
    ).parsed
