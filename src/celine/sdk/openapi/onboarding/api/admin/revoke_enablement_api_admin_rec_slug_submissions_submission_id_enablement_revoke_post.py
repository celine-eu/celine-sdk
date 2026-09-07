from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.enablement_read import EnablementRead
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    submission_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/{rec_slug}/submissions/{submission_id}/enablement/revoke".format(
            rec_slug=quote(str(rec_slug), safe=""),
            submission_id=quote(str(submission_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EnablementRead | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = EnablementRead.from_dict(response.json())

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
) -> Response[EnablementRead | HTTPValidationError]:
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
) -> Response[EnablementRead | HTTPValidationError]:
    """Revoke Enablement

     Undo enablement in reverse: credential, membership, registry, login.

    Best-effort per step and recorded per step. A revocation that fails half way
    must leave a record of what is still out there — that record is the only way
    anybody finds the rest.

    The standing sharing consent is deliberately **not** revoked here: withdrawal
    is the data subject's own act, authenticated with their own credential, and
    onboarding holds no credential to make it on their behalf.

    Args:
        rec_slug (str):
        submission_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnablementRead | HTTPValidationError]
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
) -> EnablementRead | HTTPValidationError | None:
    """Revoke Enablement

     Undo enablement in reverse: credential, membership, registry, login.

    Best-effort per step and recorded per step. A revocation that fails half way
    must leave a record of what is still out there — that record is the only way
    anybody finds the rest.

    The standing sharing consent is deliberately **not** revoked here: withdrawal
    is the data subject's own act, authenticated with their own credential, and
    onboarding holds no credential to make it on their behalf.

    Args:
        rec_slug (str):
        submission_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnablementRead | HTTPValidationError
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
) -> Response[EnablementRead | HTTPValidationError]:
    """Revoke Enablement

     Undo enablement in reverse: credential, membership, registry, login.

    Best-effort per step and recorded per step. A revocation that fails half way
    must leave a record of what is still out there — that record is the only way
    anybody finds the rest.

    The standing sharing consent is deliberately **not** revoked here: withdrawal
    is the data subject's own act, authenticated with their own credential, and
    onboarding holds no credential to make it on their behalf.

    Args:
        rec_slug (str):
        submission_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EnablementRead | HTTPValidationError]
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
) -> EnablementRead | HTTPValidationError | None:
    """Revoke Enablement

     Undo enablement in reverse: credential, membership, registry, login.

    Best-effort per step and recorded per step. A revocation that fails half way
    must leave a record of what is still out there — that record is the only way
    anybody finds the rest.

    The standing sharing consent is deliberately **not** revoked here: withdrawal
    is the data subject's own act, authenticated with their own credential, and
    onboarding holds no credential to make it on their behalf.

    Args:
        rec_slug (str):
        submission_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EnablementRead | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            submission_id=submission_id,
            client=client,
        )
    ).parsed
