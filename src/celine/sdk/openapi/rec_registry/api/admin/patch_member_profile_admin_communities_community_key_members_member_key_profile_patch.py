from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.member_detail import MemberDetail
from ...models.member_profile_patch import MemberProfilePatch
from ...types import Response


def _get_kwargs(
    community_key: str,
    member_key: str,
    *,
    body: MemberProfilePatch,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/admin/communities/{community_key}/members/{member_key}/profile".format(
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
    body: MemberProfilePatch,
) -> Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]:
    """Patch Member Profile

     Correct a member's role and area, and nothing else (REQ-0070).

    The body is `{role?, area?}`: at least one of the two, and no other key —
    an empty body, an unknown key, `null`, or a key the general `PATCH`
    accepts (`user_id`, `did`, `status`, `name`, `extra`) is `422` and changes
    nothing. Absent fields are left alone.

    Derives `members.profile.write` (REQ-0063), which
    `rec-registry.members.profile.write`, `rec-registry.members.write` and
    `rec-registry.admin` satisfy (REQ-0064): a community dashboard can be
    given this and nothing more.

    `role` outside its set is `422 invalid_role`; an `area` that is not a key
    of the community's areas is `422 unknown_area` (REQ-0066). A role change
    leaves the member's assets as they are; the member's status is not
    looked at.

    Args:
        community_key (str):
        member_key (str):
        body (MemberProfilePatch): A member's role and area, and nothing else (REQ-0070).

            At least one of the two, and no other key: a body that could carry a
            `user_id` would hand the narrower `members.profile.write` grant the identity
            rewrite REQ-0022 exists to stop. Absent fields are left alone; neither may
            be sent as `null`, since a member always has both.

            The values are checked against their sets by the route, with a coded `422`
            (`invalid_role`, `unknown_area`; REQ-0066), not here — a validation error
            here has no `code`.

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
    body: MemberProfilePatch,
) -> ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Patch Member Profile

     Correct a member's role and area, and nothing else (REQ-0070).

    The body is `{role?, area?}`: at least one of the two, and no other key —
    an empty body, an unknown key, `null`, or a key the general `PATCH`
    accepts (`user_id`, `did`, `status`, `name`, `extra`) is `422` and changes
    nothing. Absent fields are left alone.

    Derives `members.profile.write` (REQ-0063), which
    `rec-registry.members.profile.write`, `rec-registry.members.write` and
    `rec-registry.admin` satisfy (REQ-0064): a community dashboard can be
    given this and nothing more.

    `role` outside its set is `422 invalid_role`; an `area` that is not a key
    of the community's areas is `422 unknown_area` (REQ-0066). A role change
    leaves the member's assets as they are; the member's status is not
    looked at.

    Args:
        community_key (str):
        member_key (str):
        body (MemberProfilePatch): A member's role and area, and nothing else (REQ-0070).

            At least one of the two, and no other key: a body that could carry a
            `user_id` would hand the narrower `members.profile.write` grant the identity
            rewrite REQ-0022 exists to stop. Absent fields are left alone; neither may
            be sent as `null`, since a member always has both.

            The values are checked against their sets by the route, with a coded `422`
            (`invalid_role`, `unknown_area`; REQ-0066), not here — a validation error
            here has no `code`.

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
    body: MemberProfilePatch,
) -> Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]:
    """Patch Member Profile

     Correct a member's role and area, and nothing else (REQ-0070).

    The body is `{role?, area?}`: at least one of the two, and no other key —
    an empty body, an unknown key, `null`, or a key the general `PATCH`
    accepts (`user_id`, `did`, `status`, `name`, `extra`) is `422` and changes
    nothing. Absent fields are left alone.

    Derives `members.profile.write` (REQ-0063), which
    `rec-registry.members.profile.write`, `rec-registry.members.write` and
    `rec-registry.admin` satisfy (REQ-0064): a community dashboard can be
    given this and nothing more.

    `role` outside its set is `422 invalid_role`; an `area` that is not a key
    of the community's areas is `422 unknown_area` (REQ-0066). A role change
    leaves the member's assets as they are; the member's status is not
    looked at.

    Args:
        community_key (str):
        member_key (str):
        body (MemberProfilePatch): A member's role and area, and nothing else (REQ-0070).

            At least one of the two, and no other key: a body that could carry a
            `user_id` would hand the narrower `members.profile.write` grant the identity
            rewrite REQ-0022 exists to stop. Absent fields are left alone; neither may
            be sent as `null`, since a member always has both.

            The values are checked against their sets by the route, with a coded `422`
            (`invalid_role`, `unknown_area`; REQ-0066), not here — a validation error
            here has no `code`.

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
    body: MemberProfilePatch,
) -> ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Patch Member Profile

     Correct a member's role and area, and nothing else (REQ-0070).

    The body is `{role?, area?}`: at least one of the two, and no other key —
    an empty body, an unknown key, `null`, or a key the general `PATCH`
    accepts (`user_id`, `did`, `status`, `name`, `extra`) is `422` and changes
    nothing. Absent fields are left alone.

    Derives `members.profile.write` (REQ-0063), which
    `rec-registry.members.profile.write`, `rec-registry.members.write` and
    `rec-registry.admin` satisfy (REQ-0064): a community dashboard can be
    given this and nothing more.

    `role` outside its set is `422 invalid_role`; an `area` that is not a key
    of the community's areas is `422 unknown_area` (REQ-0066). A role change
    leaves the member's assets as they are; the member's status is not
    looked at.

    Args:
        community_key (str):
        member_key (str):
        body (MemberProfilePatch): A member's role and area, and nothing else (REQ-0070).

            At least one of the two, and no other key: a body that could carry a
            `user_id` would hand the narrower `members.profile.write` grant the identity
            rewrite REQ-0022 exists to stop. Absent fields are left alone; neither may
            be sent as `null`, since a member always has both.

            The values are checked against their sets by the route, with a coded `422`
            (`invalid_role`, `unknown_area`; REQ-0066), not here — a validation error
            here has no `code`.

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
