from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.dataset_access_request import DatasetAccessRequest
from ...models.dataset_access_response import DatasetAccessResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: DatasetAccessRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_request_id, Unset):
        headers["x-request-id"] = x_request_id

    if not isinstance(x_source_service, Unset):
        headers["x-source-service"] = x_source_service

    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/dataset/access",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DatasetAccessResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DatasetAccessResponse.from_dict(response.json())

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
) -> Response[DatasetAccessResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DatasetAccessRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> Response[DatasetAccessResponse | HTTPValidationError]:
    """Check Dataset Access

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (DatasetAccessRequest): Request to check dataset access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetAccessResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        x_request_id=x_request_id,
        x_source_service=x_source_service,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: DatasetAccessRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> DatasetAccessResponse | HTTPValidationError | None:
    """Check Dataset Access

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (DatasetAccessRequest): Request to check dataset access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetAccessResponse | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        x_request_id=x_request_id,
        x_source_service=x_source_service,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DatasetAccessRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> Response[DatasetAccessResponse | HTTPValidationError]:
    """Check Dataset Access

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (DatasetAccessRequest): Request to check dataset access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatasetAccessResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        x_request_id=x_request_id,
        x_source_service=x_source_service,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: DatasetAccessRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> DatasetAccessResponse | HTTPValidationError | None:
    """Check Dataset Access

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (DatasetAccessRequest): Request to check dataset access.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatasetAccessResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_request_id=x_request_id,
            x_source_service=x_source_service,
            authorization=authorization,
        )
    ).parsed
