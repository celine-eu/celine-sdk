from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.authorize_request import AuthorizeRequest
from ...models.authorize_response import AuthorizeResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AuthorizeRequest,
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
        "url": "/authorize",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AuthorizeResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = AuthorizeResponse.from_dict(response.json())

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
) -> Response[AuthorizeResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuthorizeRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> Response[AuthorizeResponse | HTTPValidationError]:
    """Authorize

     Authorize a resource action.

    Policy routing:
    - Specialized policies are tried first (celine.{resource.type})
    - Falls back to generic policy (celine.authz) if not found

    Scope derivation (in generic policy):
        {resource.type}.{resource.attributes.resource_type}.{action.name}

    Examples:
        - type=dataset → celine.dataset (specialized, has access_level logic)
        - type=dt, resource_type=simulation, action=read → celine.authz → dt.simulation.read
        - type=pipeline, resource_type=status, action=write → celine.authz → pipeline.status.write

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (AuthorizeRequest): Generic authorization request.

            The JWT token should be passed in the Authorization header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthorizeResponse | HTTPValidationError]
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
    body: AuthorizeRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> AuthorizeResponse | HTTPValidationError | None:
    """Authorize

     Authorize a resource action.

    Policy routing:
    - Specialized policies are tried first (celine.{resource.type})
    - Falls back to generic policy (celine.authz) if not found

    Scope derivation (in generic policy):
        {resource.type}.{resource.attributes.resource_type}.{action.name}

    Examples:
        - type=dataset → celine.dataset (specialized, has access_level logic)
        - type=dt, resource_type=simulation, action=read → celine.authz → dt.simulation.read
        - type=pipeline, resource_type=status, action=write → celine.authz → pipeline.status.write

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (AuthorizeRequest): Generic authorization request.

            The JWT token should be passed in the Authorization header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthorizeResponse | HTTPValidationError
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
    body: AuthorizeRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> Response[AuthorizeResponse | HTTPValidationError]:
    """Authorize

     Authorize a resource action.

    Policy routing:
    - Specialized policies are tried first (celine.{resource.type})
    - Falls back to generic policy (celine.authz) if not found

    Scope derivation (in generic policy):
        {resource.type}.{resource.attributes.resource_type}.{action.name}

    Examples:
        - type=dataset → celine.dataset (specialized, has access_level logic)
        - type=dt, resource_type=simulation, action=read → celine.authz → dt.simulation.read
        - type=pipeline, resource_type=status, action=write → celine.authz → pipeline.status.write

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (AuthorizeRequest): Generic authorization request.

            The JWT token should be passed in the Authorization header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthorizeResponse | HTTPValidationError]
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
    body: AuthorizeRequest,
    x_request_id: None | str | Unset = UNSET,
    x_source_service: None | str | Unset = UNSET,
    authorization: None | str | Unset = UNSET,
) -> AuthorizeResponse | HTTPValidationError | None:
    """Authorize

     Authorize a resource action.

    Policy routing:
    - Specialized policies are tried first (celine.{resource.type})
    - Falls back to generic policy (celine.authz) if not found

    Scope derivation (in generic policy):
        {resource.type}.{resource.attributes.resource_type}.{action.name}

    Examples:
        - type=dataset → celine.dataset (specialized, has access_level logic)
        - type=dt, resource_type=simulation, action=read → celine.authz → dt.simulation.read
        - type=pipeline, resource_type=status, action=write → celine.authz → pipeline.status.write

    Args:
        x_request_id (None | str | Unset):
        x_source_service (None | str | Unset):
        authorization (None | str | Unset):
        body (AuthorizeRequest): Generic authorization request.

            The JWT token should be passed in the Authorization header.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthorizeResponse | HTTPValidationError
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
