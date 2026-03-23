from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    participant_id: str,
    spec_id: str,
    *,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_limit: int | None | Unset
    if isinstance(limit, Unset):
        json_limit = UNSET
    else:
        json_limit = limit
    params["limit"] = json_limit

    json_offset: int | None | Unset
    if isinstance(offset, Unset):
        json_offset = UNSET
    else:
        json_offset = offset
    params["offset"] = json_offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/participants/{participant_id}/ontology/{spec_id}".format(
            participant_id=quote(str(participant_id), safe=""),
            spec_id=quote(str(spec_id), safe=""),
        ),
        "params": params,
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
    participant_id: str,
    spec_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Fetch Ontology Get

     Fetch an ontology concept view as a JSON-LD document.

    Query parameters (other than ``limit`` and ``offset``) are forwarded
    as payload to each underlying value fetcher.

    Args:
        participant_id (str):
        spec_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        spec_id=spec_id,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    participant_id: str,
    spec_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Fetch Ontology Get

     Fetch an ontology concept view as a JSON-LD document.

    Query parameters (other than ``limit`` and ``offset``) are forwarded
    as payload to each underlying value fetcher.

    Args:
        participant_id (str):
        spec_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        participant_id=participant_id,
        spec_id=spec_id,
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    participant_id: str,
    spec_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Fetch Ontology Get

     Fetch an ontology concept view as a JSON-LD document.

    Query parameters (other than ``limit`` and ``offset``) are forwarded
    as payload to each underlying value fetcher.

    Args:
        participant_id (str):
        spec_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        spec_id=spec_id,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    participant_id: str,
    spec_id: str,
    *,
    client: AuthenticatedClient | Client,
    limit: int | None | Unset = UNSET,
    offset: int | None | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Fetch Ontology Get

     Fetch an ontology concept view as a JSON-LD document.

    Query parameters (other than ``limit`` and ``offset``) are forwarded
    as payload to each underlying value fetcher.

    Args:
        participant_id (str):
        spec_id (str):
        limit (int | None | Unset):
        offset (int | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            participant_id=participant_id,
            spec_id=spec_id,
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
