from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.response_reload_templates_api_admin_recs_reload_post import ResponseReloadTemplatesApiAdminRecsReloadPost
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/recs/reload",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ResponseReloadTemplatesApiAdminRecsReloadPost | None:
    if response.status_code == 200:
        response_200 = ResponseReloadTemplatesApiAdminRecsReloadPost.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ResponseReloadTemplatesApiAdminRecsReloadPost]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ResponseReloadTemplatesApiAdminRecsReloadPost]:
    """Reload Templates

     Force a manifest cache refresh.

    Deployment-wide, so it belongs to no community — only a realm-level operator
    (or a scoped service account) satisfies it. Gated on `recs.read` rather than a
    write capability because the cache refreshes itself on a 5-second TTL anyway;
    this only makes an operator stop waiting.

    Moved here from the public `/api/recs` router, which protected it with the
    shared admin token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseReloadTemplatesApiAdminRecsReloadPost]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
) -> ResponseReloadTemplatesApiAdminRecsReloadPost | None:
    """Reload Templates

     Force a manifest cache refresh.

    Deployment-wide, so it belongs to no community — only a realm-level operator
    (or a scoped service account) satisfies it. Gated on `recs.read` rather than a
    write capability because the cache refreshes itself on a 5-second TTL anyway;
    this only makes an operator stop waiting.

    Moved here from the public `/api/recs` router, which protected it with the
    shared admin token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseReloadTemplatesApiAdminRecsReloadPost
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
) -> Response[ResponseReloadTemplatesApiAdminRecsReloadPost]:
    """Reload Templates

     Force a manifest cache refresh.

    Deployment-wide, so it belongs to no community — only a realm-level operator
    (or a scoped service account) satisfies it. Gated on `recs.read` rather than a
    write capability because the cache refreshes itself on a 5-second TTL anyway;
    this only makes an operator stop waiting.

    Moved here from the public `/api/recs` router, which protected it with the
    shared admin token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResponseReloadTemplatesApiAdminRecsReloadPost]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
) -> ResponseReloadTemplatesApiAdminRecsReloadPost | None:
    """Reload Templates

     Force a manifest cache refresh.

    Deployment-wide, so it belongs to no community — only a realm-level operator
    (or a scoped service account) satisfies it. Gated on `recs.read` rather than a
    write capability because the cache refreshes itself on a 5-second TTL anyway;
    this only makes an operator stop waiting.

    Moved here from the public `/api/recs` router, which protected it with the
    shared admin token.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResponseReloadTemplatesApiAdminRecsReloadPost
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
