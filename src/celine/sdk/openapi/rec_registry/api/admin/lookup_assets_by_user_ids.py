from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.global_asset_lookup import GlobalAssetLookup
from ...models.http_validation_error import HTTPValidationError
from ...models.user_ids_batch_request import UserIdsBatchRequest
from ...types import Response


def _get_kwargs(
    *,
    body: UserIdsBatchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/lookup/assets-by-user-ids",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[GlobalAssetLookup] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GlobalAssetLookup.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[HTTPValidationError | list[GlobalAssetLookup]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: UserIdsBatchRequest,
) -> Response[HTTPValidationError | list[GlobalAssetLookup]]:
    r"""Lookup Assets By User Ids

     Find assets owned by multiple members, across all communities.

    The mirror of ``assets-by-sensor-ids``: that one starts from a device and
    finds its owner, this one starts from owners and finds their devices.

    **Why it exists.** A dataspace query is authorised for a *set of people* —
    the subjects who consented — not for the caller. The existing self-service
    path (``GET /user/assets``) can only answer \"mine\", because it resolves the
    member from the caller's own token. Widening *that* endpoint to take a list
    would turn a self-service route into a directory with no scope check in
    front of it, so the batch form belongs here, behind the admin policy.

    **No enumeration oracle.** A ``user_id`` that does not exist and a member
    who owns nothing are indistinguishable — both contribute no rows. The caller
    supplies the ids, so any difference in the answer would make this a way to
    discover who is registered.

    Args:
        body (UserIdsBatchRequest): Members to resolve assets for.

            Bounded on purpose. A caller that can name ten thousand people in one
            request has a dump of the registry, not a lookup, and the endpoint is
            reachable by anything holding `rec-registry.lookup`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[GlobalAssetLookup]]
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
    body: UserIdsBatchRequest,
) -> HTTPValidationError | list[GlobalAssetLookup] | None:
    r"""Lookup Assets By User Ids

     Find assets owned by multiple members, across all communities.

    The mirror of ``assets-by-sensor-ids``: that one starts from a device and
    finds its owner, this one starts from owners and finds their devices.

    **Why it exists.** A dataspace query is authorised for a *set of people* —
    the subjects who consented — not for the caller. The existing self-service
    path (``GET /user/assets``) can only answer \"mine\", because it resolves the
    member from the caller's own token. Widening *that* endpoint to take a list
    would turn a self-service route into a directory with no scope check in
    front of it, so the batch form belongs here, behind the admin policy.

    **No enumeration oracle.** A ``user_id`` that does not exist and a member
    who owns nothing are indistinguishable — both contribute no rows. The caller
    supplies the ids, so any difference in the answer would make this a way to
    discover who is registered.

    Args:
        body (UserIdsBatchRequest): Members to resolve assets for.

            Bounded on purpose. A caller that can name ten thousand people in one
            request has a dump of the registry, not a lookup, and the endpoint is
            reachable by anything holding `rec-registry.lookup`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[GlobalAssetLookup]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: UserIdsBatchRequest,
) -> Response[HTTPValidationError | list[GlobalAssetLookup]]:
    r"""Lookup Assets By User Ids

     Find assets owned by multiple members, across all communities.

    The mirror of ``assets-by-sensor-ids``: that one starts from a device and
    finds its owner, this one starts from owners and finds their devices.

    **Why it exists.** A dataspace query is authorised for a *set of people* —
    the subjects who consented — not for the caller. The existing self-service
    path (``GET /user/assets``) can only answer \"mine\", because it resolves the
    member from the caller's own token. Widening *that* endpoint to take a list
    would turn a self-service route into a directory with no scope check in
    front of it, so the batch form belongs here, behind the admin policy.

    **No enumeration oracle.** A ``user_id`` that does not exist and a member
    who owns nothing are indistinguishable — both contribute no rows. The caller
    supplies the ids, so any difference in the answer would make this a way to
    discover who is registered.

    Args:
        body (UserIdsBatchRequest): Members to resolve assets for.

            Bounded on purpose. A caller that can name ten thousand people in one
            request has a dump of the registry, not a lookup, and the endpoint is
            reachable by anything holding `rec-registry.lookup`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[GlobalAssetLookup]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: UserIdsBatchRequest,
) -> HTTPValidationError | list[GlobalAssetLookup] | None:
    r"""Lookup Assets By User Ids

     Find assets owned by multiple members, across all communities.

    The mirror of ``assets-by-sensor-ids``: that one starts from a device and
    finds its owner, this one starts from owners and finds their devices.

    **Why it exists.** A dataspace query is authorised for a *set of people* —
    the subjects who consented — not for the caller. The existing self-service
    path (``GET /user/assets``) can only answer \"mine\", because it resolves the
    member from the caller's own token. Widening *that* endpoint to take a list
    would turn a self-service route into a directory with no scope check in
    front of it, so the batch form belongs here, behind the admin policy.

    **No enumeration oracle.** A ``user_id`` that does not exist and a member
    who owns nothing are indistinguishable — both contribute no rows. The caller
    supplies the ids, so any difference in the answer would make this a way to
    discover who is registered.

    Args:
        body (UserIdsBatchRequest): Members to resolve assets for.

            Bounded on purpose. A caller that can name ten thousand people in one
            request has a dump of the registry, not a lookup, and the endpoint is
            reachable by anything holding `rec-registry.lookup`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[GlobalAssetLookup]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
