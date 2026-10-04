from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.revision_create import RevisionCreate
from ...models.revision_read import RevisionRead
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    *,
    body: RevisionCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/revisions".format(
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
) -> HTTPValidationError | RevisionRead | None:
    if response.status_code == 201:
        response_201 = RevisionRead.from_dict(response.json())

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
    *,
    client: AuthenticatedClient | Client,
    body: RevisionCreate,
) -> Response[HTTPValidationError | RevisionRead]:
    """Record Revision

     Correct one field; the submission's column takes the new value.

    409 unless the submission is submitted, under review or approved; 422 for a
    value the field refuses, a missing note, the value already held, or a document
    that is missing, not on this submission, or given with `offline`. The POD is
    masked in the answer, like everywhere else.

    After approval the corrected value is then propagated (`services/propagation`);
    each step's state is in the answer's `steps`, a failure included. The revision
    stands whatever they do.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (RevisionCreate): An operator's correction of one declared field, from `submitted`
            on.

            `value` is checked per field by `services.revision.normalise`. The supply
            address is its text, as the eligibility step saves it, and is revisable only
            before approval (REQ-0026).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RevisionRead]
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
    body: RevisionCreate,
) -> HTTPValidationError | RevisionRead | None:
    """Record Revision

     Correct one field; the submission's column takes the new value.

    409 unless the submission is submitted, under review or approved; 422 for a
    value the field refuses, a missing note, the value already held, or a document
    that is missing, not on this submission, or given with `offline`. The POD is
    masked in the answer, like everywhere else.

    After approval the corrected value is then propagated (`services/propagation`);
    each step's state is in the answer's `steps`, a failure included. The revision
    stands whatever they do.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (RevisionCreate): An operator's correction of one declared field, from `submitted`
            on.

            `value` is checked per field by `services.revision.normalise`. The supply
            address is its text, as the eligibility step saves it, and is revisable only
            before approval (REQ-0026).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RevisionRead
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
    body: RevisionCreate,
) -> Response[HTTPValidationError | RevisionRead]:
    """Record Revision

     Correct one field; the submission's column takes the new value.

    409 unless the submission is submitted, under review or approved; 422 for a
    value the field refuses, a missing note, the value already held, or a document
    that is missing, not on this submission, or given with `offline`. The POD is
    masked in the answer, like everywhere else.

    After approval the corrected value is then propagated (`services/propagation`);
    each step's state is in the answer's `steps`, a failure included. The revision
    stands whatever they do.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (RevisionCreate): An operator's correction of one declared field, from `submitted`
            on.

            `value` is checked per field by `services.revision.normalise`. The supply
            address is its text, as the eligibility step saves it, and is revisable only
            before approval (REQ-0026).

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RevisionRead]
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
    body: RevisionCreate,
) -> HTTPValidationError | RevisionRead | None:
    """Record Revision

     Correct one field; the submission's column takes the new value.

    409 unless the submission is submitted, under review or approved; 422 for a
    value the field refuses, a missing note, the value already held, or a document
    that is missing, not on this submission, or given with `offline`. The POD is
    masked in the answer, like everywhere else.

    After approval the corrected value is then propagated (`services/propagation`);
    each step's state is in the answer's `steps`, a failure included. The revision
    stands whatever they do.

    Args:
        rec_slug (str):
        submission_id (UUID):
        body (RevisionCreate): An operator's correction of one declared field, from `submitted`
            on.

            `value` is checked per field by `services.revision.normalise`. The supply
            address is its text, as the eligibility step saves it, and is revisable only
            before approval (REQ-0026).

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
            client=client,
            body=body,
        )
    ).parsed
