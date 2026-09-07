from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.admin_me import AdminMe
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/me",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AdminMe | None:
    if response.status_code == 200:
        response_200 = AdminMe.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AdminMe]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminMe]:
    """Me

     The caller's identity and per-community capabilities.

    403 when they administer nothing. A valid token that grants nothing is not an
    authentication problem, and answering 200-with-an-empty-list would send the
    console to a login screen it has already passed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminMe]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> AdminMe | None:
    """Me

     The caller's identity and per-community capabilities.

    403 when they administer nothing. A valid token that grants nothing is not an
    authentication problem, and answering 200-with-an-empty-list would send the
    console to a login screen it has already passed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminMe
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[AdminMe]:
    """Me

     The caller's identity and per-community capabilities.

    403 when they administer nothing. A valid token that grants nothing is not an
    authentication problem, and answering 200-with-an-empty-list would send the
    console to a login screen it has already passed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdminMe]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> AdminMe | None:
    """Me

     The caller's identity and per-community capabilities.

    403 when they administer nothing. A valid token that grants nothing is not an
    authentication problem, and answering 200-with-an-empty-list would send the
    console to a login screen it has already passed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdminMe
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
