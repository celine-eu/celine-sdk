from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
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
) -> ErrorResponse | HTTPValidationError | ImportReport | None:
    if response.status_code == 200:
        response_200 = ImportReport.from_dict(response.json())

        return response_200

    if response.status_code == 422:

        def _parse_response_422(data: object) -> ErrorResponse | HTTPValidationError:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_422_type_0 = ErrorResponse.from_dict(data)

                return response_422_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_422_type_1 = HTTPValidationError.from_dict(data)

            return response_422_type_1

        response_422 = _parse_response_422(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | HTTPValidationError | ImportReport]:
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
) -> Response[ErrorResponse | HTTPValidationError | ImportReport]:
    """Admin Import

     Replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    **This is destructive.** Members now arrive at runtime through the member
    API, so re-importing a stale export is the most likely way to lose them.
    Overwriting an existing community therefore requires `force=true`, and
    answers `409` without it, naming what would have been deleted.

    Use `dry_run=true` to see the effect first — that is the intended way to
    decide whether `force` is warranted.

    **A bundle that breaks an invariant is refused whole**, before anything is
    deleted: `422` with the invariant's `code` — `sensor_held`, one sensor held
    by two active members of the bundle, or by one of them and an active member
    of another community (REQ-0069); `asset_key_too_long`, an asset key over
    128 characters (REQ-0028); `invalid_role`, `invalid_status`,
    `unknown_area`, a member whose role or status is outside its set or whose
    area is not a key of the bundle's `community.areas` (REQ-0066);
    `invalid_area_boundary`, an area that is not one primary substation — one
    boundary, one `primary_substation` topology node with the boundary's id,
    no two areas on one boundary id (REQ-0067); a bundle written before schema
    v0.7 that has areas is refused so. A dry run
    lists every such refusal in `refusals` instead. A body that fails validation is a `422` too, with
    FastAPI's list `detail`; the OpenAPI document declares both bodies.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | ImportReport]
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
) -> ErrorResponse | HTTPValidationError | ImportReport | None:
    """Admin Import

     Replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    **This is destructive.** Members now arrive at runtime through the member
    API, so re-importing a stale export is the most likely way to lose them.
    Overwriting an existing community therefore requires `force=true`, and
    answers `409` without it, naming what would have been deleted.

    Use `dry_run=true` to see the effect first — that is the intended way to
    decide whether `force` is warranted.

    **A bundle that breaks an invariant is refused whole**, before anything is
    deleted: `422` with the invariant's `code` — `sensor_held`, one sensor held
    by two active members of the bundle, or by one of them and an active member
    of another community (REQ-0069); `asset_key_too_long`, an asset key over
    128 characters (REQ-0028); `invalid_role`, `invalid_status`,
    `unknown_area`, a member whose role or status is outside its set or whose
    area is not a key of the bundle's `community.areas` (REQ-0066);
    `invalid_area_boundary`, an area that is not one primary substation — one
    boundary, one `primary_substation` topology node with the boundary's id,
    no two areas on one boundary id (REQ-0067); a bundle written before schema
    v0.7 that has areas is refused so. A dry run
    lists every such refusal in `refusals` instead. A body that fails validation is a `422` too, with
    FastAPI's list `detail`; the OpenAPI document declares both bodies.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | ImportReport
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: ImportRequest,
) -> Response[ErrorResponse | HTTPValidationError | ImportReport]:
    """Admin Import

     Replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    **This is destructive.** Members now arrive at runtime through the member
    API, so re-importing a stale export is the most likely way to lose them.
    Overwriting an existing community therefore requires `force=true`, and
    answers `409` without it, naming what would have been deleted.

    Use `dry_run=true` to see the effect first — that is the intended way to
    decide whether `force` is warranted.

    **A bundle that breaks an invariant is refused whole**, before anything is
    deleted: `422` with the invariant's `code` — `sensor_held`, one sensor held
    by two active members of the bundle, or by one of them and an active member
    of another community (REQ-0069); `asset_key_too_long`, an asset key over
    128 characters (REQ-0028); `invalid_role`, `invalid_status`,
    `unknown_area`, a member whose role or status is outside its set or whose
    area is not a key of the bundle's `community.areas` (REQ-0066);
    `invalid_area_boundary`, an area that is not one primary substation — one
    boundary, one `primary_substation` topology node with the boundary's id,
    no two areas on one boundary id (REQ-0067); a bundle written before schema
    v0.7 that has areas is refused so. A dry run
    lists every such refusal in `refusals` instead. A body that fails validation is a `422` too, with
    FastAPI's list `detail`; the OpenAPI document declares both bodies.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | HTTPValidationError | ImportReport]
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
) -> ErrorResponse | HTTPValidationError | ImportReport | None:
    """Admin Import

     Replacement import of a REC registry bundle.

    - Deletes existing community (by community.id/key) with all related data
    - Creates new community with members and assets atomically
    - Returns counts of deleted and inserted entities

    **This is destructive.** Members now arrive at runtime through the member
    API, so re-importing a stale export is the most likely way to lose them.
    Overwriting an existing community therefore requires `force=true`, and
    answers `409` without it, naming what would have been deleted.

    Use `dry_run=true` to see the effect first — that is the intended way to
    decide whether `force` is warranted.

    **A bundle that breaks an invariant is refused whole**, before anything is
    deleted: `422` with the invariant's `code` — `sensor_held`, one sensor held
    by two active members of the bundle, or by one of them and an active member
    of another community (REQ-0069); `asset_key_too_long`, an asset key over
    128 characters (REQ-0028); `invalid_role`, `invalid_status`,
    `unknown_area`, a member whose role or status is outside its set or whose
    area is not a key of the bundle's `community.areas` (REQ-0066);
    `invalid_area_boundary`, an area that is not one primary substation — one
    boundary, one `primary_substation` topology node with the boundary's id,
    no two areas on one boundary id (REQ-0067); a bundle written before schema
    v0.7 that has areas is refused so. A dry run
    lists every such refusal in `refusals` instead. A body that fails validation is a `422` too, with
    FastAPI's list `detail`; the OpenAPI document declares both bodies.

    Args:
        body (ImportRequest): Import request payload.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | HTTPValidationError | ImportReport
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
