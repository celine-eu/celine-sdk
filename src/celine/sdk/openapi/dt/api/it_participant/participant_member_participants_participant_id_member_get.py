from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.response_participant_member_participants_participant_id_member_get import (
    ResponseParticipantMemberParticipantsParticipantIdMemberGet,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    participant_id: str,
    *,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/participants/{participant_id}/member".format(
            participant_id=quote(str(participant_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet | None:
    if response.status_code == 200:
        response_200 = ResponseParticipantMemberParticipantsParticipantIdMemberGet.from_dict(response.json())

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
) -> Response[HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    participant_id: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet]:
    """Participant Member

     Get participant's member details from registry.

    Args:
        participant_id (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    participant_id: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet | None:
    """Participant Member

     Get participant's member details from registry.

    Args:
        participant_id (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet
    """

    return sync_detailed(
        participant_id=participant_id,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    participant_id: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet]:
    """Participant Member

     Get participant's member details from registry.

    Args:
        participant_id (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet]
    """

    kwargs = _get_kwargs(
        participant_id=participant_id,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    participant_id: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet | None:
    """Participant Member

     Get participant's member details from registry.

    Args:
        participant_id (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ResponseParticipantMemberParticipantsParticipantIdMemberGet
    """

    return (
        await asyncio_detailed(
            participant_id=participant_id,
            client=client,
            authorization=authorization,
        )
    ).parsed
