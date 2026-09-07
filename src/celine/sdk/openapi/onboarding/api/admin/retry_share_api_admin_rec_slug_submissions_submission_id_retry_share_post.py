from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.submission_admin_read import SubmissionAdminRead
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/retry-share".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
        ),
    }

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
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Retry Share

     Deprecated alias for `enablement/retry?step=dataspace_share`.

    Kept for one release because it is the only admin endpoint that existed before
    the console did. The enablement endpoint supersedes it: it records the attempt
    on the step row, so a repeated failure is visible as a count rather than as a
    422 the operator sees and nothing remembers.

    Args:
        rec_slug (str):
        submission_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SubmissionAdminRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
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
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Retry Share

     Deprecated alias for `enablement/retry?step=dataspace_share`.

    Kept for one release because it is the only admin endpoint that existed before
    the console did. The enablement endpoint supersedes it: it records the attempt
    on the step row, so a repeated failure is visible as a count rather than as a
    422 the operator sees and nothing remembers.

    Args:
        rec_slug (str):
        submission_id (UUID):

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
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Retry Share

     Deprecated alias for `enablement/retry?step=dataspace_share`.

    Kept for one release because it is the only admin endpoint that existed before
    the console did. The enablement endpoint supersedes it: it records the attempt
    on the step row, so a repeated failure is visible as a count rather than as a
    422 the operator sees and nothing remembers.

    Args:
        rec_slug (str):
        submission_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SubmissionAdminRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Retry Share

     Deprecated alias for `enablement/retry?step=dataspace_share`.

    Kept for one release because it is the only admin endpoint that existed before
    the console did. The enablement endpoint supersedes it: it records the attempt
    on the step row, so a repeated failure is visible as a count rather than as a
    422 the operator sees and nothing remembers.

    Args:
        rec_slug (str):
        submission_id (UUID):

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
        )
    ).parsed
