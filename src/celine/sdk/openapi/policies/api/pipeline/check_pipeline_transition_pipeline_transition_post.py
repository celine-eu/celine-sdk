from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.pipeline_transition_request import PipelineTransitionRequest
from ...models.pipeline_transition_response import PipelineTransitionResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: PipelineTransitionRequest,
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
        "url": "/pipeline/transition",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PipelineTransitionResponse | None:
    if response.status_code == 200:
        response_200 = PipelineTransitionResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | PipelineTransitionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PipelineTransitionRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PipelineTransitionResponse]:
    """Check Pipeline Transition

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (PipelineTransitionRequest): Request to validate a pipeline state transition.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PipelineTransitionResponse]
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
    body: PipelineTransitionRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | PipelineTransitionResponse | None:
    """Check Pipeline Transition

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (PipelineTransitionRequest): Request to validate a pipeline state transition.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PipelineTransitionResponse
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
    body: PipelineTransitionRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PipelineTransitionResponse]:
    """Check Pipeline Transition

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (PipelineTransitionRequest): Request to validate a pipeline state transition.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PipelineTransitionResponse]
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
    body: PipelineTransitionRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | PipelineTransitionResponse | None:
    """Check Pipeline Transition

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (PipelineTransitionRequest): Request to validate a pipeline state transition.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PipelineTransitionResponse
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
