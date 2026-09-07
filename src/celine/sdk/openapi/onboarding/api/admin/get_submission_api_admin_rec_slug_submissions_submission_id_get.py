from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.submission_admin_read import SubmissionAdminRead
from ...types import UNSET, Response, Unset


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    *,
    reveal: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["reveal"] = reveal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
        ),
        "params": params,
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
    reveal: bool | Unset = False,
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Get Submission

     One submission, with the identifiers masked unless `reveal` is asked for.

    The point of the reveal capability is not that an operator must never see a
    fiscal code — sometimes they must, to resolve exactly the kind of mismatch
    review exists to catch — but that doing so is a deliberate act with their name
    on it.

    Args:
        rec_slug (str):
        submission_id (UUID):
        reveal (bool | Unset): Unmask the fiscal code and POD. Requires `submissions.reveal`, and
            is recorded in the audit trail. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SubmissionAdminRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        reveal=reveal,
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
    reveal: bool | Unset = False,
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Get Submission

     One submission, with the identifiers masked unless `reveal` is asked for.

    The point of the reveal capability is not that an operator must never see a
    fiscal code — sometimes they must, to resolve exactly the kind of mismatch
    review exists to catch — but that doing so is a deliberate act with their name
    on it.

    Args:
        rec_slug (str):
        submission_id (UUID):
        reveal (bool | Unset): Unmask the fiscal code and POD. Requires `submissions.reveal`, and
            is recorded in the audit trail. Default: False.

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
        reveal=reveal,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    reveal: bool | Unset = False,
) -> Response[HTTPValidationError | SubmissionAdminRead]:
    """Get Submission

     One submission, with the identifiers masked unless `reveal` is asked for.

    The point of the reveal capability is not that an operator must never see a
    fiscal code — sometimes they must, to resolve exactly the kind of mismatch
    review exists to catch — but that doing so is a deliberate act with their name
    on it.

    Args:
        rec_slug (str):
        submission_id (UUID):
        reveal (bool | Unset): Unmask the fiscal code and POD. Requires `submissions.reveal`, and
            is recorded in the audit trail. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SubmissionAdminRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        reveal=reveal,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    reveal: bool | Unset = False,
) -> HTTPValidationError | SubmissionAdminRead | None:
    """Get Submission

     One submission, with the identifiers masked unless `reveal` is asked for.

    The point of the reveal capability is not that an operator must never see a
    fiscal code — sometimes they must, to resolve exactly the kind of mismatch
    review exists to catch — but that doing so is a deliberate act with their name
    on it.

    Args:
        rec_slug (str):
        submission_id (UUID):
        reveal (bool | Unset): Unmask the fiscal code and POD. Requires `submissions.reveal`, and
            is recorded in the audit trail. Default: False.

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
            reveal=reveal,
        )
    ).parsed
