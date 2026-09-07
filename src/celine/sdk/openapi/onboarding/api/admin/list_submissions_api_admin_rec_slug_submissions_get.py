import datetime
from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.submission_admin_read import SubmissionAdminRead
from ...models.submission_status import SubmissionStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    rec_slug: str,
    *,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    status: None | SubmissionStatus | Unset = UNSET,
    ref: None | str | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["skip"] = skip

    params["limit"] = limit

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    elif isinstance(status, SubmissionStatus):
        json_status = status.value
    else:
        json_status = status
    params["status"] = json_status

    json_ref: None | str | Unset
    if isinstance(ref, Unset):
        json_ref = UNSET
    else:
        json_ref = ref
    params["ref"] = json_ref

    json_created_from: None | str | Unset
    if isinstance(created_from, Unset):
        json_created_from = UNSET
    elif isinstance(created_from, datetime.datetime):
        json_created_from = created_from.isoformat()
    else:
        json_created_from = created_from
    params["created_from"] = json_created_from

    json_created_to: None | str | Unset
    if isinstance(created_to, Unset):
        json_created_to = UNSET
    elif isinstance(created_to, datetime.datetime):
        json_created_to = created_to.isoformat()
    else:
        json_created_to = created_to
    params["created_to"] = json_created_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/{rec_slug}/submissions".format(
            rec_slug=quote(str(rec_slug), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[SubmissionAdminRead] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SubmissionAdminRead.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[SubmissionAdminRead]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    status: None | SubmissionStatus | Unset = UNSET,
    ref: None | str | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[SubmissionAdminRead]]:
    """List Submissions

     One page of the queue, always masked.

    Reveal is a per-record act on the detail endpoint, not something a list can
    do wholesale.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        status (None | SubmissionStatus | Unset):
        ref (None | str | Unset): Substring of the submission reference. Deliberately the only
            searchable field: everything else is encrypted with a non-deterministic IV, so there is no
            ciphertext to match against.
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[SubmissionAdminRead]]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        skip=skip,
        limit=limit,
        status=status,
        ref=ref,
        created_from=created_from,
        created_to=created_to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    status: None | SubmissionStatus | Unset = UNSET,
    ref: None | str | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
) -> HTTPValidationError | list[SubmissionAdminRead] | None:
    """List Submissions

     One page of the queue, always masked.

    Reveal is a per-record act on the detail endpoint, not something a list can
    do wholesale.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        status (None | SubmissionStatus | Unset):
        ref (None | str | Unset): Substring of the submission reference. Deliberately the only
            searchable field: everything else is encrypted with a non-deterministic IV, so there is no
            ciphertext to match against.
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[SubmissionAdminRead]
    """

    return sync_detailed(
        rec_slug=rec_slug,
        client=client,
        skip=skip,
        limit=limit,
        status=status,
        ref=ref,
        created_from=created_from,
        created_to=created_to,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    status: None | SubmissionStatus | Unset = UNSET,
    ref: None | str | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
) -> Response[HTTPValidationError | list[SubmissionAdminRead]]:
    """List Submissions

     One page of the queue, always masked.

    Reveal is a per-record act on the detail endpoint, not something a list can
    do wholesale.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        status (None | SubmissionStatus | Unset):
        ref (None | str | Unset): Substring of the submission reference. Deliberately the only
            searchable field: everything else is encrypted with a non-deterministic IV, so there is no
            ciphertext to match against.
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[SubmissionAdminRead]]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        skip=skip,
        limit=limit,
        status=status,
        ref=ref,
        created_from=created_from,
        created_to=created_to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    skip: int | Unset = 0,
    limit: int | Unset = 50,
    status: None | SubmissionStatus | Unset = UNSET,
    ref: None | str | Unset = UNSET,
    created_from: datetime.datetime | None | Unset = UNSET,
    created_to: datetime.datetime | None | Unset = UNSET,
) -> HTTPValidationError | list[SubmissionAdminRead] | None:
    """List Submissions

     One page of the queue, always masked.

    Reveal is a per-record act on the detail endpoint, not something a list can
    do wholesale.

    Args:
        rec_slug (str):
        skip (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 50.
        status (None | SubmissionStatus | Unset):
        ref (None | str | Unset): Substring of the submission reference. Deliberately the only
            searchable field: everything else is encrypted with a non-deterministic IV, so there is no
            ciphertext to match against.
        created_from (datetime.datetime | None | Unset):
        created_to (datetime.datetime | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[SubmissionAdminRead]
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            client=client,
            skip=skip,
            limit=limit,
            status=status,
            ref=ref,
            created_from=created_from,
            created_to=created_to,
        )
    ).parsed
