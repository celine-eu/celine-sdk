from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.member_detail import MemberDetail
from ...models.member_patch import MemberPatch
from ...types import Response


def _get_kwargs(
    community_key: str,
    member_key: str,
    *,
    body: MemberPatch,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/admin/communities/{community_key}/members/{member_key}".format(
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
    body: MemberPatch,
) -> Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]:
    """Patch Member

     Partially update a member. Absent fields are left alone.

    Reassigning a `user_id` that belongs to somebody else is `409`, whether the
    clash was already committed or arrives concurrently.

    **This is also how a member's dataspace DID is written**, because the DID is
    minted a step after the member is registered — there is no separate route
    for it, since a dedicated write would have to be added to
    `TestNoWriteReducesASibling` to earn nothing `PATCH` does not already do.
    Its clash check differs from the `user_id` one beside it in two ways, and
    both matter:

    * **It is registry-wide.** `ix_member_did` is global, so the check cannot be
      scoped to the community in the path.
    * **It names the holder only inside the addressed community.** Saying which
      member of *another* community holds a DID would answer a question the
      caller did not ask about people they were not addressing — the same
      enumeration reasoning as REQ-0045.

    Re-sending a member the DID it already holds is a no-op success: onboarding
    writes it from a retriable step, so the same write arriving twice must not
    be a conflict.

    Setting `status: active` on a member that was not active re-checks its
    sensors, and the whole patch is refused `409 sensor_held` when another
    active member holds one (REQ-0069).

    `role` and `area` are still accepted here, for `members.write` holders,
    and held to the same sets as on `PATCH …/profile`: `422 invalid_role`,
    `invalid_status`, `unknown_area` (REQ-0066). A role change leaves the
    member's assets as they are.

    Args:
        community_key (str):
        member_key (str):
        body (MemberPatch): Partial update. Absent fields are left alone, never cleared.

            `delivery_points` is deliberately absent: it is a JSONB list, and a patch
            that happened to omit it would otherwise read as "this member now has none".
            It has its own sub-resource.

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
    body: MemberPatch,
) -> ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Patch Member

     Partially update a member. Absent fields are left alone.

    Reassigning a `user_id` that belongs to somebody else is `409`, whether the
    clash was already committed or arrives concurrently.

    **This is also how a member's dataspace DID is written**, because the DID is
    minted a step after the member is registered — there is no separate route
    for it, since a dedicated write would have to be added to
    `TestNoWriteReducesASibling` to earn nothing `PATCH` does not already do.
    Its clash check differs from the `user_id` one beside it in two ways, and
    both matter:

    * **It is registry-wide.** `ix_member_did` is global, so the check cannot be
      scoped to the community in the path.
    * **It names the holder only inside the addressed community.** Saying which
      member of *another* community holds a DID would answer a question the
      caller did not ask about people they were not addressing — the same
      enumeration reasoning as REQ-0045.

    Re-sending a member the DID it already holds is a no-op success: onboarding
    writes it from a retriable step, so the same write arriving twice must not
    be a conflict.

    Setting `status: active` on a member that was not active re-checks its
    sensors, and the whole patch is refused `409 sensor_held` when another
    active member holds one (REQ-0069).

    `role` and `area` are still accepted here, for `members.write` holders,
    and held to the same sets as on `PATCH …/profile`: `422 invalid_role`,
    `invalid_status`, `unknown_area` (REQ-0066). A role change leaves the
    member's assets as they are.

    Args:
        community_key (str):
        member_key (str):
        body (MemberPatch): Partial update. Absent fields are left alone, never cleared.

            `delivery_points` is deliberately absent: it is a JSONB list, and a patch
            that happened to omit it would otherwise read as "this member now has none".
            It has its own sub-resource.

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
    body: MemberPatch,
) -> Response[ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail]:
    """Patch Member

     Partially update a member. Absent fields are left alone.

    Reassigning a `user_id` that belongs to somebody else is `409`, whether the
    clash was already committed or arrives concurrently.

    **This is also how a member's dataspace DID is written**, because the DID is
    minted a step after the member is registered — there is no separate route
    for it, since a dedicated write would have to be added to
    `TestNoWriteReducesASibling` to earn nothing `PATCH` does not already do.
    Its clash check differs from the `user_id` one beside it in two ways, and
    both matter:

    * **It is registry-wide.** `ix_member_did` is global, so the check cannot be
      scoped to the community in the path.
    * **It names the holder only inside the addressed community.** Saying which
      member of *another* community holds a DID would answer a question the
      caller did not ask about people they were not addressing — the same
      enumeration reasoning as REQ-0045.

    Re-sending a member the DID it already holds is a no-op success: onboarding
    writes it from a retriable step, so the same write arriving twice must not
    be a conflict.

    Setting `status: active` on a member that was not active re-checks its
    sensors, and the whole patch is refused `409 sensor_held` when another
    active member holds one (REQ-0069).

    `role` and `area` are still accepted here, for `members.write` holders,
    and held to the same sets as on `PATCH …/profile`: `422 invalid_role`,
    `invalid_status`, `unknown_area` (REQ-0066). A role change leaves the
    member's assets as they are.

    Args:
        community_key (str):
        member_key (str):
        body (MemberPatch): Partial update. Absent fields are left alone, never cleared.

            `delivery_points` is deliberately absent: it is a JSONB list, and a patch
            that happened to omit it would otherwise read as "this member now has none".
            It has its own sub-resource.

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
    body: MemberPatch,
) -> ErrorResponse | ErrorResponse | HTTPValidationError | MemberDetail | None:
    """Patch Member

     Partially update a member. Absent fields are left alone.

    Reassigning a `user_id` that belongs to somebody else is `409`, whether the
    clash was already committed or arrives concurrently.

    **This is also how a member's dataspace DID is written**, because the DID is
    minted a step after the member is registered — there is no separate route
    for it, since a dedicated write would have to be added to
    `TestNoWriteReducesASibling` to earn nothing `PATCH` does not already do.
    Its clash check differs from the `user_id` one beside it in two ways, and
    both matter:

    * **It is registry-wide.** `ix_member_did` is global, so the check cannot be
      scoped to the community in the path.
    * **It names the holder only inside the addressed community.** Saying which
      member of *another* community holds a DID would answer a question the
      caller did not ask about people they were not addressing — the same
      enumeration reasoning as REQ-0045.

    Re-sending a member the DID it already holds is a no-op success: onboarding
    writes it from a retriable step, so the same write arriving twice must not
    be a conflict.

    Setting `status: active` on a member that was not active re-checks its
    sensors, and the whole patch is refused `409 sensor_held` when another
    active member holds one (REQ-0069).

    `role` and `area` are still accepted here, for `members.write` holders,
    and held to the same sets as on `PATCH …/profile`: `422 invalid_role`,
    `invalid_status`, `unknown_area` (REQ-0066). A role change leaves the
    member's assets as they are.

    Args:
        community_key (str):
        member_key (str):
        body (MemberPatch): Partial update. Absent fields are left alone, never cleared.

            `delivery_points` is deliberately absent: it is a JSONB list, and a patch
            that happened to omit it would otherwise read as "this member now has none".
            It has its own sub-resource.

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
