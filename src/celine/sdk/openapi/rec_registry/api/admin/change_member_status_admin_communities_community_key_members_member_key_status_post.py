from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.member_detail import MemberDetail
from ...models.member_status_change import MemberStatusChange
from ...types import Response


def _get_kwargs(
    community_key: str,
    member_key: str,
    *,
    body: MemberStatusChange,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/communities/{community_key}/members/{member_key}/status".format(
            community_key=quote(str(community_key), safe=""),
            member_key=quote(str(member_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail | None:
    if response.status_code == 200:
        response_200 = MemberDetail.from_dict(response.json())

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
) -> Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberStatusChange,
) -> Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]:
    """Change Member Status

     Move a member through the lifecycle explicitly.

    Separate from `PATCH` because a status change is the transition an operator
    reasons about — and because it reads clearly in an audit log, which a
    generic field update does not.

    A move to `active` re-checks the member's sensors: when another active
    member took one meanwhile it answers `409 sensor_held` and the status is
    left as it was (REQ-0069).

    Args:
        community_key (str):
        member_key (str):
        body (MemberStatusChange): Move a member through `pending → active → suspended →
            inactive`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberStatusChange,
) -> ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Change Member Status

     Move a member through the lifecycle explicitly.

    Separate from `PATCH` because a status change is the transition an operator
    reasons about — and because it reads clearly in an audit log, which a
    generic field update does not.

    A move to `active` re-checks the member's sensors: when another active
    member took one meanwhile it answers `409 sensor_held` and the status is
    left as it was (REQ-0069).

    Args:
        community_key (str):
        member_key (str):
        body (MemberStatusChange): Move a member through `pending → active → suspended →
            inactive`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail
    """

    return sync_detailed(
        community_key=community_key,
        member_key=member_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberStatusChange,
) -> Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]:
    """Change Member Status

     Move a member through the lifecycle explicitly.

    Separate from `PATCH` because a status change is the transition an operator
    reasons about — and because it reads clearly in an audit log, which a
    generic field update does not.

    A move to `active` re-checks the member's sensors: when another active
    member took one meanwhile it answers `409 sensor_held` and the status is
    left as it was (REQ-0069).

    Args:
        community_key (str):
        member_key (str):
        body (MemberStatusChange): Move a member through `pending → active → suspended →
            inactive`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    member_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: MemberStatusChange,
) -> ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Change Member Status

     Move a member through the lifecycle explicitly.

    Separate from `PATCH` because a status change is the transition an operator
    reasons about — and because it reads clearly in an audit log, which a
    generic field update does not.

    A move to `active` re-checks the member's sensors: when another active
    member took one meanwhile it answers `409 sensor_held` and the status is
    left as it was (REQ-0069).

    Args:
        community_key (str):
        member_key (str):
        body (MemberStatusChange): Move a member through `pending → active → suspended →
            inactive`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            client=client,
            body=body,
        )
    ).parsed
