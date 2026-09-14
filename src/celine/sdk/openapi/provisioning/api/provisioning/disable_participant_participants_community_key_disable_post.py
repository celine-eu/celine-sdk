from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.disable_response import DisableResponse
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community: str,
    key: str,
    *,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/participants/{community}/{key}/disable".format(
            community=quote(str(community), safe=""),
            key=quote(str(key), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DisableResponse | ErrorResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DisableResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DisableResponse | ErrorResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> Response[DisableResponse | ErrorResponse | HTTPValidationError]:
    """Revoke a member's access

     Disables the account. Nothing is deleted and re-enabling is one call —
    what is being revoked is somebody's access to their own energy community.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DisableResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community=community,
        key=key,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> DisableResponse | ErrorResponse | HTTPValidationError | None:
    """Revoke a member's access

     Disables the account. Nothing is deleted and re-enabling is one call —
    what is being revoked is somebody's access to their own energy community.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DisableResponse | ErrorResponse | HTTPValidationError
    """

    return sync_detailed(
        community=community,
        key=key,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> Response[DisableResponse | ErrorResponse | HTTPValidationError]:
    """Revoke a member's access

     Disables the account. Nothing is deleted and re-enabling is one call —
    what is being revoked is somebody's access to their own energy community.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DisableResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community=community,
        key=key,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community: str,
    key: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> DisableResponse | ErrorResponse | HTTPValidationError | None:
    """Revoke a member's access

     Disables the account. Nothing is deleted and re-enabling is one call —
    what is being revoked is somebody's access to their own energy community.

    Args:
        community (str):
        key (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DisableResponse | ErrorResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community=community,
            key=key,
            client=client,
            authorization=authorization,
        )
    ).parsed
