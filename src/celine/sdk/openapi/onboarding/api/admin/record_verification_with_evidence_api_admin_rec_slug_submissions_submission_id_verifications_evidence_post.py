from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_record_verification_with_evidence_api_admin_rec_slug_submissions_submission_id_verifications_evidence_post import (
    BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.verification_read import VerificationRead
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    *,
    body: BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/verifications/evidence".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
        ),
    }

    _kwargs["files"] = body.to_multipart()

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
    body: BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost,
) -> Response[HTTPValidationError | VerificationRead]:
    """Record Verification With Evidence

     Record an offline check with the evidence it rested on (`offline-with-evidence`).

    Each file is hashed and discarded; only `{kind, sha256}` is recorded.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerification
            sEvidencePost):

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
    body: BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost,
) -> HTTPValidationError | VerificationRead | None:
    """Record Verification With Evidence

     Record an offline check with the evidence it rested on (`offline-with-evidence`).

    Each file is hashed and discarded; only `{kind, sha256}` is recorded.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerification
            sEvidencePost):

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
    body: BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost,
) -> Response[HTTPValidationError | VerificationRead]:
    """Record Verification With Evidence

     Record an offline check with the evidence it rested on (`offline-with-evidence`).

    Each file is hashed and discarded; only `{kind, sha256}` is recorded.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerification
            sEvidencePost):

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
    body: BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost,
) -> HTTPValidationError | VerificationRead | None:
    """Record Verification With Evidence

     Record an offline check with the evidence it rested on (`offline-with-evidence`).

    Each file is hashed and discarded; only `{kind, sha256}` is recorded.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerification
            sEvidencePost):

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
