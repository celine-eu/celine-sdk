from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.submission_admin_read import SubmissionAdminRead
from ...models.submission_update import SubmissionUpdate
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    *,
    body: SubmissionUpdate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}".format(
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
    body: SubmissionUpdate,
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Update Submission

     Edit fields, and — for now — drive the state machine.

    A payload carrying `status` additionally requires `submissions.review`: an
    editor may correct a misread fiscal code, but approving somebody provisions a
    login, a registry member and a dataspace identity, which is a different
    decision. The transition moves to its own endpoint in B2, where it can also
    carry a rejection reason; the extra check is here so the distinction is
    enforced now rather than after the restructure.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (SubmissionUpdate):

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
    body: SubmissionUpdate,
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Update Submission

     Edit fields, and — for now — drive the state machine.

    A payload carrying `status` additionally requires `submissions.review`: an
    editor may correct a misread fiscal code, but approving somebody provisions a
    login, a registry member and a dataspace identity, which is a different
    decision. The transition moves to its own endpoint in B2, where it can also
    carry a rejection reason; the extra check is here so the distinction is
    enforced now rather than after the restructure.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (SubmissionUpdate):

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
    body: SubmissionUpdate,
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Update Submission

     Edit fields, and — for now — drive the state machine.

    A payload carrying `status` additionally requires `submissions.review`: an
    editor may correct a misread fiscal code, but approving somebody provisions a
    login, a registry member and a dataspace identity, which is a different
    decision. The transition moves to its own endpoint in B2, where it can also
    carry a rejection reason; the extra check is here so the distinction is
    enforced now rather than after the restructure.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (SubmissionUpdate):

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
    body: SubmissionUpdate,
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Update Submission

     Edit fields, and — for now — drive the state machine.

    A payload carrying `status` additionally requires `submissions.review`: an
    editor may correct a misread fiscal code, but approving somebody provisions a
    login, a registry member and a dataspace identity, which is a different
    decision. The transition moves to its own endpoint in B2, where it can also
    carry a rejection reason; the extra check is here so the distinction is
    enforced now rather than after the restructure.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (SubmissionUpdate):

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
