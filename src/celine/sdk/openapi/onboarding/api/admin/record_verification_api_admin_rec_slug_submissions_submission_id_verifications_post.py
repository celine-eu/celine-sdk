from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.verification_create import VerificationCreate
from ...models.verification_read import VerificationRead
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    *,
    body: VerificationCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/verifications".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | VerificationRead | None:
    if response.status_code == 201:
        response_201 = VerificationRead.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | VerificationRead]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: VerificationCreate,
) -> Response[HTTPValidationError | VerificationRead]:
    """Record Verification

     Record how the REC verified the person; supersedes any earlier one.

    409 once the submission is approved or rejected; 422 for a document that is
    missing, not on this submission, or given with `offline`.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (VerificationCreate): How the REC verified the participant's identity and that they
            hold the POD.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | VerificationRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: VerificationCreate,
) -> HTTPValidationError | VerificationRead | None:
    """Record Verification

     Record how the REC verified the person; supersedes any earlier one.

    409 once the submission is approved or rejected; 422 for a document that is
    missing, not on this submission, or given with `offline`.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (VerificationCreate): How the REC verified the participant's identity and that they
            hold the POD.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | VerificationRead
    """

    return sync_detailed(
        rec_slug=rec_slug,
        submission_id=submission_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: VerificationCreate,
) -> Response[HTTPValidationError | VerificationRead]:
    """Record Verification

     Record how the REC verified the person; supersedes any earlier one.

    409 once the submission is approved or rejected; 422 for a document that is
    missing, not on this submission, or given with `offline`.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (VerificationCreate): How the REC verified the participant's identity and that they
            hold the POD.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | VerificationRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: VerificationCreate,
) -> HTTPValidationError | VerificationRead | None:
    """Record Verification

     Record how the REC verified the person; supersedes any earlier one.

    409 once the submission is approved or rejected; 422 for a document that is
    missing, not on this submission, or given with `offline`.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (VerificationCreate): How the REC verified the participant's identity and that they
            hold the POD.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | VerificationRead
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            submission_id=submission_id,
            client=client,
            body=body,
        )
    ).parsed
