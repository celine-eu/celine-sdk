from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.send_test_request import SendTestRequest
from ...models.send_test_response import SendTestResponse
from ...types import Response


def _get_kwargs(
    *,
    body: SendTestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/webpush/send-test",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SendTestResponse | None:
    if response.status_code == 200:
        response_200 = SendTestResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | SendTestResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SendTestRequest,
) -> Response[HTTPValidationError | SendTestResponse]:
    """Send a test push notification

     Sends a test Web Push notification to all active subscriptions for a given user. Requires
    nudging.admin scope or admin group. user_id is explicit in the body because an admin targets any
    user.

    Args:
        body (SendTestRequest): Admin-only: user_id is explicit because an admin targets any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SendTestResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: SendTestRequest,
) -> HTTPValidationError | SendTestResponse | None:
    """Send a test push notification

     Sends a test Web Push notification to all active subscriptions for a given user. Requires
    nudging.admin scope or admin group. user_id is explicit in the body because an admin targets any
    user.

    Args:
        body (SendTestRequest): Admin-only: user_id is explicit because an admin targets any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SendTestResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SendTestRequest,
) -> Response[HTTPValidationError | SendTestResponse]:
    """Send a test push notification

     Sends a test Web Push notification to all active subscriptions for a given user. Requires
    nudging.admin scope or admin group. user_id is explicit in the body because an admin targets any
    user.

    Args:
        body (SendTestRequest): Admin-only: user_id is explicit because an admin targets any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SendTestResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: SendTestRequest,
) -> HTTPValidationError | SendTestResponse | None:
    """Send a test push notification

     Sends a test Web Push notification to all active subscriptions for a given user. Requires
    nudging.admin scope or admin group. user_id is explicit in the body because an admin targets any
    user.

    Args:
        body (SendTestRequest): Admin-only: user_id is explicit because an admin targets any user.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SendTestResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
