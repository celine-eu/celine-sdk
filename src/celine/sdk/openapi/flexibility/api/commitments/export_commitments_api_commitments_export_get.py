import datetime
from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.commitment_out import CommitmentOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    created_after: datetime.datetime | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_created_after: None | str | Unset
    if isinstance(created_after, Unset):
        json_created_after = UNSET
    elif isinstance(created_after, datetime.datetime):
        json_created_after = created_after.isoformat()
    else:
        json_created_after = created_after
    params["created_after"] = json_created_after

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/commitments/export",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[CommitmentOut] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = CommitmentOut.from_dict(response_200_item_data)

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
) -> Response[HTTPValidationError | list[CommitmentOut]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    created_after: datetime.datetime | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[CommitmentOut]]:
    """Export Commitments

     Bulk export all commitments for pipeline mirroring.

    Service only. Requires flexibility.commitments.export scope.
    Returns all statuses (committed, settled, rejected, cancelled).
    created_after filters by committed_at (ISO datetime, UTC).

    Args:
        created_after (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[CommitmentOut]]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    created_after: datetime.datetime | None | Unset = UNSET,
) -> HTTPValidationError | list[CommitmentOut] | None:
    """Export Commitments

     Bulk export all commitments for pipeline mirroring.

    Service only. Requires flexibility.commitments.export scope.
    Returns all statuses (committed, settled, rejected, cancelled).
    created_after filters by committed_at (ISO datetime, UTC).

    Args:
        created_after (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[CommitmentOut]
    """

    return sync_detailed(
        client=client,
        created_after=created_after,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    created_after: datetime.datetime | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[CommitmentOut]]:
    """Export Commitments

     Bulk export all commitments for pipeline mirroring.

    Service only. Requires flexibility.commitments.export scope.
    Returns all statuses (committed, settled, rejected, cancelled).
    created_after filters by committed_at (ISO datetime, UTC).

    Args:
        created_after (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[CommitmentOut]]
    """

    kwargs = _get_kwargs(
        created_after=created_after,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    created_after: datetime.datetime | None | Unset = UNSET,
) -> HTTPValidationError | list[CommitmentOut] | None:
    """Export Commitments

     Bulk export all commitments for pipeline mirroring.

    Service only. Requires flexibility.commitments.export scope.
    Returns all statuses (committed, settled, rejected, cancelled).
    created_after filters by committed_at (ISO datetime, UTC).

    Args:
        created_after (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[CommitmentOut]
    """

    return (
        await asyncio_detailed(
            client=client,
            created_after=created_after,
        )
    ).parsed
