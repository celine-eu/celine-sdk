from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.revision_read import RevisionRead
from ...models.revision_retry_request import RevisionRetryRequest
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    revision_id: UUID,
    *,
    body: RevisionRetryRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/revisions/{revision_id}/retry".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
            revision_id=quote(str(revision_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RevisionRead | None:
    if response.status_code == 200:
        response_200 = RevisionRead.from_dict(response.json())

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
) -> Response[HTTPValidationError | RevisionRead]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rec_slug: str,
    submission_id: UUID,
    revision_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: RevisionRetryRequest,
) -> Response[HTTPValidationError | RevisionRead]:
    """Retry Revision

     Re-run a revision's unfinished propagation steps, or one named step.

    404 for a revision that is not this submission's; 409 for one recorded before
    approval, which has nothing to propagate.

    Args:
        rec_slug (str):
        submission_id (UUID):
        revision_id (UUID):
        body (RevisionRetryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RevisionRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        revision_id=revision_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    submission_id: UUID,
    revision_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: RevisionRetryRequest,
) -> HTTPValidationError | RevisionRead | None:
    """Retry Revision

     Re-run a revision's unfinished propagation steps, or one named step.

    404 for a revision that is not this submission's; 409 for one recorded before
    approval, which has nothing to propagate.

    Args:
        rec_slug (str):
        submission_id (UUID):
        revision_id (UUID):
        body (RevisionRetryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RevisionRead
    """

    return sync_detailed(
        rec_slug=rec_slug,
        submission_id=submission_id,
        revision_id=revision_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    submission_id: UUID,
    revision_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: RevisionRetryRequest,
) -> Response[HTTPValidationError | RevisionRead]:
    """Retry Revision

     Re-run a revision's unfinished propagation steps, or one named step.

    404 for a revision that is not this submission's; 409 for one recorded before
    approval, which has nothing to propagate.

    Args:
        rec_slug (str):
        submission_id (UUID):
        revision_id (UUID):
        body (RevisionRetryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RevisionRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        revision_id=revision_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    submission_id: UUID,
    revision_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: RevisionRetryRequest,
) -> HTTPValidationError | RevisionRead | None:
    """Retry Revision

     Re-run a revision's unfinished propagation steps, or one named step.

    404 for a revision that is not this submission's; 409 for one recorded before
    approval, which has nothing to propagate.

    Args:
        rec_slug (str):
        submission_id (UUID):
        revision_id (UUID):
        body (RevisionRetryRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RevisionRead
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            submission_id=submission_id,
            revision_id=revision_id,
            client=client,
            body=body,
        )
    ).parsed
