from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.app_run_request import AppRunRequest
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    app_key: str,
    *,
    body: AppRunRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/apps/{app_key}/run".format(
            app_key=quote(str(app_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AppRunRequest,
) -> Response[Any | HTTPValidationError]:
    """Run App

     Execute a DT app.

    The API layer is a thin gate:
      - creates a per-request RunContext from the app-scoped DT
      - delegates to the DT runner

    Args:
        app_key (str):
        body (AppRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        app_key=app_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AppRunRequest,
) -> Any | HTTPValidationError | None:
    """Run App

     Execute a DT app.

    The API layer is a thin gate:
      - creates a per-request RunContext from the app-scoped DT
      - delegates to the DT runner

    Args:
        app_key (str):
        body (AppRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        app_key=app_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AppRunRequest,
) -> Response[Any | HTTPValidationError]:
    """Run App

     Execute a DT app.

    The API layer is a thin gate:
      - creates a per-request RunContext from the app-scoped DT
      - delegates to the DT runner

    Args:
        app_key (str):
        body (AppRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        app_key=app_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AppRunRequest,
) -> Any | HTTPValidationError | None:
    """Run App

     Execute a DT app.

    The API layer is a thin gate:
      - creates a per-request RunContext from the app-scoped DT
      - delegates to the DT runner

    Args:
        app_key (str):
        body (AppRunRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            app_key=app_key,
            client=client,
            body=body,
        )
    ).parsed
