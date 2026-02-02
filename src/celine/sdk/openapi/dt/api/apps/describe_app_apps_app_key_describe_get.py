from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_describe_app_apps_app_key_describe_get import ResponseDescribeAppAppsAppKeyDescribeGet
from ...types import Response


def _get_kwargs(
    app_key: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/apps/{app_key}/describe".format(
            app_key=quote(str(app_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet | None:
    if response.status_code == 200:
        response_200 = ResponseDescribeAppAppsAppKeyDescribeGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet]:
    """Describe App

     Describe a DT app: metadata + input/output schemas.

    Args:
        app_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet]
    """

    kwargs = _get_kwargs(
        app_key=app_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet | None:
    """Describe App

     Describe a DT app: metadata + input/output schemas.

    Args:
        app_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet
    """

    return sync_detailed(
        app_key=app_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet]:
    """Describe App

     Describe a DT app: metadata + input/output schemas.

    Args:
        app_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet]
    """

    kwargs = _get_kwargs(
        app_key=app_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet | None:
    """Describe App

     Describe a DT app: metadata + input/output schemas.

    Args:
        app_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseDescribeAppAppsAppKeyDescribeGet
    """

    return (
        await asyncio_detailed(
            app_key=app_key,
            client=client,
        )
    ).parsed
