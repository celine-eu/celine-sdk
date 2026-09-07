from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.submission_admin_read import SubmissionAdminRead
from ...models.transition_request import TransitionRequest
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    *,
    body: TransitionRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/transition".format(
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
) -> HTTPValidationError | SubmissionAdminRead | None:
    if response.status_code == 200:
        response_200 = SubmissionAdminRead.from_dict(response.json())

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
) -> Response[HTTPValidationError | SubmissionAdminRead]:
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
    body: TransitionRequest,
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Transition Submission

     Drive the review state machine.

    Split out of `PATCH` because the state machine is not a field: it has its own
    capability, its own preconditions, and a reason that a field update has
    nowhere to put.

    On approval the enablement pipeline runs first. A fail-closed step failing
    returns 422 and leaves the submission in review — but everything the pipeline
    *did* manage is committed, so the retry finishes the job instead of starting
    it again.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (TransitionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SubmissionAdminRead]
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
    body: TransitionRequest,
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Transition Submission

     Drive the review state machine.

    Split out of `PATCH` because the state machine is not a field: it has its own
    capability, its own preconditions, and a reason that a field update has
    nowhere to put.

    On approval the enablement pipeline runs first. A fail-closed step failing
    returns 422 and leaves the submission in review — but everything the pipeline
    *did* manage is committed, so the retry finishes the job instead of starting
    it again.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (TransitionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SubmissionAdminRead
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
    body: TransitionRequest,
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Transition Submission

     Drive the review state machine.

    Split out of `PATCH` because the state machine is not a field: it has its own
    capability, its own preconditions, and a reason that a field update has
    nowhere to put.

    On approval the enablement pipeline runs first. A fail-closed step failing
    returns 422 and leaves the submission in review — but everything the pipeline
    *did* manage is committed, so the retry finishes the job instead of starting
    it again.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (TransitionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SubmissionAdminRead]
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
    body: TransitionRequest,
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Transition Submission

     Drive the review state machine.

    Split out of `PATCH` because the state machine is not a field: it has its own
    capability, its own preconditions, and a reason that a field update has
    nowhere to put.

    On approval the enablement pipeline runs first. A fail-closed step failing
    returns 422 and leaves the submission in review — but everything the pipeline
    *did* manage is committed, so the retry finishes the job instead of starting
    it again.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (TransitionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SubmissionAdminRead
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            submission_id=submission_id,
            client=client,
            body=body,
        )
    ).parsed
