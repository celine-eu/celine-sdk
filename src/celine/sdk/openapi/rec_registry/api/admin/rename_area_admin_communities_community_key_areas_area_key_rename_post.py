from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.area_rename import AreaRename
from ...models.area_renamed import AreaRenamed
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    area_key: str,
    *,
    body: AreaRename,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/communities/{community_key}/areas/{area_key}/rename".format(
            community_key=quote(str(community_key), safe=""),
            area_key=quote(str(area_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = AreaRenamed.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

    if response.status_code == 422:

        def _parse_response_422(data: object) -> ErrorResponse | HTTPValidationError:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_422_type_0 = ErrorResponse.from_dict(data)

                return response_422_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_422_type_1 = HTTPValidationError.from_dict(data)

            return response_422_type_1

        response_422 = _parse_response_422(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaRename,
) -> Response[AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Rename Area

     Move an area to a new key, with its members, in one write (REQ-0079).

    The area — name, boundary, topology, as stored — is written under
    `new_key`, every member of the community whose `area` is `area_key`
    (active or not) is moved to `new_key`, and `area_key` is removed: one
    transaction, under the community's row taken exclusively, so no reader
    sees both keys, or a member in an area that does not exist, or two areas
    on one boundary (REQ-0067). Nothing else changes — not the other areas,
    not the members' other fields, not their assets.

    This is how an onboarding template sync renames an area whose substation
    the registry already holds under another key: an area `PUT` under the new
    key would be refused (one area per boundary), and the old key cannot be
    deleted while members hold it.

    Refused, changing nothing: `422 invalid_area_key` for a `new_key` that is
    not an area key; `404 area_not_found` for an `area_key` the community does
    not have; `409 area_key_taken` for a `new_key` it already has. Derives
    `community.write`.

    Args:
        community_key (str):
        area_key (str):
        body (AreaRename): Move an area to a new key, with its members (REQ-0079).

            `new_key` only; any other key is `422`. A key that is not an area key —
            letters, digits, `-` and `_`, starting with a letter or digit, at most 128
            characters — is refused `422 invalid_area_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        area_key=area_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaRename,
) -> AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Rename Area

     Move an area to a new key, with its members, in one write (REQ-0079).

    The area — name, boundary, topology, as stored — is written under
    `new_key`, every member of the community whose `area` is `area_key`
    (active or not) is moved to `new_key`, and `area_key` is removed: one
    transaction, under the community's row taken exclusively, so no reader
    sees both keys, or a member in an area that does not exist, or two areas
    on one boundary (REQ-0067). Nothing else changes — not the other areas,
    not the members' other fields, not their assets.

    This is how an onboarding template sync renames an area whose substation
    the registry already holds under another key: an area `PUT` under the new
    key would be refused (one area per boundary), and the old key cannot be
    deleted while members hold it.

    Refused, changing nothing: `422 invalid_area_key` for a `new_key` that is
    not an area key; `404 area_not_found` for an `area_key` the community does
    not have; `409 area_key_taken` for a `new_key` it already has. Derives
    `community.write`.

    Args:
        community_key (str):
        area_key (str):
        body (AreaRename): Move an area to a new key, with its members (REQ-0079).

            `new_key` only; any other key is `422`. A key that is not an area key —
            letters, digits, `-` and `_`, starting with a letter or digit, at most 128
            characters — is refused `422 invalid_area_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        area_key=area_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaRename,
) -> Response[AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Rename Area

     Move an area to a new key, with its members, in one write (REQ-0079).

    The area — name, boundary, topology, as stored — is written under
    `new_key`, every member of the community whose `area` is `area_key`
    (active or not) is moved to `new_key`, and `area_key` is removed: one
    transaction, under the community's row taken exclusively, so no reader
    sees both keys, or a member in an area that does not exist, or two areas
    on one boundary (REQ-0067). Nothing else changes — not the other areas,
    not the members' other fields, not their assets.

    This is how an onboarding template sync renames an area whose substation
    the registry already holds under another key: an area `PUT` under the new
    key would be refused (one area per boundary), and the old key cannot be
    deleted while members hold it.

    Refused, changing nothing: `422 invalid_area_key` for a `new_key` that is
    not an area key; `404 area_not_found` for an `area_key` the community does
    not have; `409 area_key_taken` for a `new_key` it already has. Derives
    `community.write`.

    Args:
        community_key (str):
        area_key (str):
        body (AreaRename): Move an area to a new key, with its members (REQ-0079).

            `new_key` only; any other key is `422`. A key that is not an area key —
            letters, digits, `-` and `_`, starting with a letter or digit, at most 128
            characters — is refused `422 invalid_area_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        area_key=area_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaRename,
) -> AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Rename Area

     Move an area to a new key, with its members, in one write (REQ-0079).

    The area — name, boundary, topology, as stored — is written under
    `new_key`, every member of the community whose `area` is `area_key`
    (active or not) is moved to `new_key`, and `area_key` is removed: one
    transaction, under the community's row taken exclusively, so no reader
    sees both keys, or a member in an area that does not exist, or two areas
    on one boundary (REQ-0067). Nothing else changes — not the other areas,
    not the members' other fields, not their assets.

    This is how an onboarding template sync renames an area whose substation
    the registry already holds under another key: an area `PUT` under the new
    key would be refused (one area per boundary), and the old key cannot be
    deleted while members hold it.

    Refused, changing nothing: `422 invalid_area_key` for a `new_key` that is
    not an area key; `404 area_not_found` for an `area_key` the community does
    not have; `409 area_key_taken` for a `new_key` it already has. Derives
    `community.write`.

    Args:
        community_key (str):
        area_key (str):
        body (AreaRename): Move an area to a new key, with its members (REQ-0079).

            `new_key` only; any other key is `422`. A key that is not an area key —
            letters, digits, `-` and `_`, starting with a letter or digit, at most 128
            characters — is refused `422 invalid_area_key`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AreaRenamed | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            area_key=area_key,
            client=client,
            body=body,
        )
    ).parsed
