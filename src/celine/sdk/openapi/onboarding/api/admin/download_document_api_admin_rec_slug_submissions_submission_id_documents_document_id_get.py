from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
    document_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/documents/{document_id}".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
            document_id=quote(str(document_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rec_slug: str,
    submission_id: UUID,
    document_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    """Download Document

     Stream one document, decrypted.

    Audited, unlike the document *list*: the bill itself carries the address,
    supply point and consumption history, so opening one is an act worth
    attributing. Listing filenames is not.

    Ownership is checked on both the submission and the document — a document id
    from another community must not be reachable by pairing it with a submission
    id from this one.

    Args:
        rec_slug (str):
        submission_id (UUID):
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        document_id=document_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    submission_id: UUID,
    document_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    """Download Document

     Stream one document, decrypted.

    Audited, unlike the document *list*: the bill itself carries the address,
    supply point and consumption history, so opening one is an act worth
    attributing. Listing filenames is not.

    Ownership is checked on both the submission and the document — a document id
    from another community must not be reachable by pairing it with a submission
    id from this one.

    Args:
        rec_slug (str):
        submission_id (UUID):
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        rec_slug=rec_slug,
        submission_id=submission_id,
        document_id=document_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    submission_id: UUID,
    document_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    """Download Document

     Stream one document, decrypted.

    Audited, unlike the document *list*: the bill itself carries the address,
    supply point and consumption history, so opening one is an act worth
    attributing. Listing filenames is not.

    Ownership is checked on both the submission and the document — a document id
    from another community must not be reachable by pairing it with a submission
    id from this one.

    Args:
        rec_slug (str):
        submission_id (UUID):
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        submission_id=submission_id,
        document_id=document_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    submission_id: UUID,
    document_id: UUID,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    """Download Document

     Stream one document, decrypted.

    Audited, unlike the document *list*: the bill itself carries the address,
    supply point and consumption history, so opening one is an act worth
    attributing. Listing filenames is not.

    Ownership is checked on both the submission and the document — a document id
    from another community must not be reachable by pairing it with a submission
    id from this one.

    Args:
        rec_slug (str):
        submission_id (UUID):
        document_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            submission_id=submission_id,
            document_id=document_id,
            client=client,
        )
    ).parsed
