from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.commitment_out import CommitmentOut
from ...models.commitment_settle import CommitmentSettle
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    commitment_id: UUID,
    *,
    body: CommitmentSettle,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/commitments/{commitment_id}/settle".format(
            commitment_id=quote(str(commitment_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommitmentOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CommitmentOut.from_dict(response.json())

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
) -> Response[CommitmentOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    commitment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CommitmentSettle,
) -> Response[CommitmentOut | HTTPValidationError]:
    """Settle Commitment

     Settle a commitment with actual kWh and reward points.  Service only.

    Args:
        commitment_id (UUID):
        body (CommitmentSettle):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommitmentOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        commitment_id=commitment_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    commitment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CommitmentSettle,
) -> CommitmentOut | HTTPValidationError | None:
    """Settle Commitment

     Settle a commitment with actual kWh and reward points.  Service only.

    Args:
        commitment_id (UUID):
        body (CommitmentSettle):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommitmentOut | HTTPValidationError
    """

    return sync_detailed(
        commitment_id=commitment_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    commitment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CommitmentSettle,
) -> Response[CommitmentOut | HTTPValidationError]:
    """Settle Commitment

     Settle a commitment with actual kWh and reward points.  Service only.

    Args:
        commitment_id (UUID):
        body (CommitmentSettle):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommitmentOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        commitment_id=commitment_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    commitment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: CommitmentSettle,
) -> CommitmentOut | HTTPValidationError | None:
    """Settle Commitment

     Settle a commitment with actual kWh and reward points.  Service only.

    Args:
        commitment_id (UUID):
        body (CommitmentSettle):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommitmentOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            commitment_id=commitment_id,
            client=client,
            body=body,
        )
    ).parsed
