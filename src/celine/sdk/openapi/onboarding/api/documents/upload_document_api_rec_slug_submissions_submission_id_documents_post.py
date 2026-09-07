from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_upload_document_api_rec_slug_submissions_submission_id_documents_post import (
    BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost,
)
from ...models.document_read import DocumentRead
from ...models.document_type import DocumentType
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    *,
    body: BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost,
    doc_type: DocumentType | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_doc_type: str | Unset = UNSET
    if not isinstance(doc_type, Unset):
        json_doc_type = doc_type.value

    params["doc_type"] = json_doc_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/{rec_slug}/submissions/{submission_id}/documents".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DocumentRead | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = DocumentRead.from_dict(response.json())

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
) -> Response[DocumentRead | HTTPValidationError]:
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
    body: BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost,
    doc_type: DocumentType | Unset = UNSET,
) -> Response[DocumentRead | HTTPValidationError]:
    """Upload Document

    Args:
        rec_slug (str):
        submission_id (UUID):
        doc_type (DocumentType | Unset):
        body (BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentRead | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        body=body,
        doc_type=doc_type,
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
    body: BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost,
    doc_type: DocumentType | Unset = UNSET,
) -> DocumentRead | HTTPValidationError | None:
    """Upload Document

    Args:
        rec_slug (str):
        submission_id (UUID):
        doc_type (DocumentType | Unset):
        body (BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentRead | HTTPValidationError
    """

    return sync_detailed(
        rec_slug=rec_slug,
        submission_id=submission_id,
        client=client,
        body=body,
        doc_type=doc_type,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost,
    doc_type: DocumentType | Unset = UNSET,
) -> Response[DocumentRead | HTTPValidationError]:
    """Upload Document

    Args:
        rec_slug (str):
        submission_id (UUID):
        doc_type (DocumentType | Unset):
        body (BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DocumentRead | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        body=body,
        doc_type=doc_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    submission_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost,
    doc_type: DocumentType | Unset = UNSET,
) -> DocumentRead | HTTPValidationError | None:
    """Upload Document

    Args:
        rec_slug (str):
        submission_id (UUID):
        doc_type (DocumentType | Unset):
        body (BodyUploadDocumentApiRecSlugSubmissionsSubmissionIdDocumentsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DocumentRead | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            submission_id=submission_id,
            client=client,
            body=body,
            doc_type=doc_type,
        )
    ).parsed
