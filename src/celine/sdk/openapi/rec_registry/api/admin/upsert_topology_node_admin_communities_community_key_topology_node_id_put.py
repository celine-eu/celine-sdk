from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.community_detail import CommunityDetail
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.topology_node_in import TopologyNodeIn
from ...types import Response


def _get_kwargs(
    community_key: str,
    node_id: str,
    *,
    body: TopologyNodeIn,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/topology/{node_id}".format(
            community_key=quote(str(community_key), safe=""),
            node_id=quote(str(node_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CommunityDetail.from_dict(response.json())

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
) -> Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TopologyNodeIn,
) -> Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Topology Node

     Add or replace one topology node, keeping the others (REQ-0072).

    Nodes merge by `id`, as delivery points do: re-sending an existing id
    replaces that node where it stands, and a new id is appended. The body is
    the bundle's topology node — `id`, `type`, and optionally `name`,
    `operator_id`, `parent`, `area` — under the names every read answers;
    other keys are not stored. The body `id` must match the path, or `422`.

    **A node write never breaks an area that keeps the one-substation rule**
    (REQ-0067): changing the `type` of a node such an area lists away from
    `primary_substation` is `422 invalid_area_boundary` and changes nothing.
    This is the route an onboarding template sync writes a community's
    substations through, before the areas that reference them.

    Answers the whole community, so the caller can see the others are still
    there.

    Args:
        community_key (str):
        node_id (str):
        body (TopologyNodeIn): Grid topology node (substation, transformer, etc.).

            The body of the topology node `PUT` too (REQ-0072), and the names every
            read answers (`TopologyNode`): `operator_id`, `parent`. Keys beyond these
            are accepted and not stored, on the import and on the `PUT` alike.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        node_id=node_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TopologyNodeIn,
) -> CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Topology Node

     Add or replace one topology node, keeping the others (REQ-0072).

    Nodes merge by `id`, as delivery points do: re-sending an existing id
    replaces that node where it stands, and a new id is appended. The body is
    the bundle's topology node — `id`, `type`, and optionally `name`,
    `operator_id`, `parent`, `area` — under the names every read answers;
    other keys are not stored. The body `id` must match the path, or `422`.

    **A node write never breaks an area that keeps the one-substation rule**
    (REQ-0067): changing the `type` of a node such an area lists away from
    `primary_substation` is `422 invalid_area_boundary` and changes nothing.
    This is the route an onboarding template sync writes a community's
    substations through, before the areas that reference them.

    Answers the whole community, so the caller can see the others are still
    there.

    Args:
        community_key (str):
        node_id (str):
        body (TopologyNodeIn): Grid topology node (substation, transformer, etc.).

            The body of the topology node `PUT` too (REQ-0072), and the names every
            read answers (`TopologyNode`): `operator_id`, `parent`. Keys beyond these
            are accepted and not stored, on the import and on the `PUT` alike.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        node_id=node_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TopologyNodeIn,
) -> Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Topology Node

     Add or replace one topology node, keeping the others (REQ-0072).

    Nodes merge by `id`, as delivery points do: re-sending an existing id
    replaces that node where it stands, and a new id is appended. The body is
    the bundle's topology node — `id`, `type`, and optionally `name`,
    `operator_id`, `parent`, `area` — under the names every read answers;
    other keys are not stored. The body `id` must match the path, or `422`.

    **A node write never breaks an area that keeps the one-substation rule**
    (REQ-0067): changing the `type` of a node such an area lists away from
    `primary_substation` is `422 invalid_area_boundary` and changes nothing.
    This is the route an onboarding template sync writes a community's
    substations through, before the areas that reference them.

    Answers the whole community, so the caller can see the others are still
    there.

    Args:
        community_key (str):
        node_id (str):
        body (TopologyNodeIn): Grid topology node (substation, transformer, etc.).

            The body of the topology node `PUT` too (REQ-0072), and the names every
            read answers (`TopologyNode`): `operator_id`, `parent`. Keys beyond these
            are accepted and not stored, on the import and on the `PUT` alike.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        node_id=node_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    node_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: TopologyNodeIn,
) -> CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Topology Node

     Add or replace one topology node, keeping the others (REQ-0072).

    Nodes merge by `id`, as delivery points do: re-sending an existing id
    replaces that node where it stands, and a new id is appended. The body is
    the bundle's topology node — `id`, `type`, and optionally `name`,
    `operator_id`, `parent`, `area` — under the names every read answers;
    other keys are not stored. The body `id` must match the path, or `422`.

    **A node write never breaks an area that keeps the one-substation rule**
    (REQ-0067): changing the `type` of a node such an area lists away from
    `primary_substation` is `422 invalid_area_boundary` and changes nothing.
    This is the route an onboarding template sync writes a community's
    substations through, before the areas that reference them.

    Answers the whole community, so the caller can see the others are still
    there.

    Args:
        community_key (str):
        node_id (str):
        body (TopologyNodeIn): Grid topology node (substation, transformer, etc.).

            The body of the topology node `PUT` too (REQ-0072), and the names every
            read answers (`TopologyNode`): `operator_id`, `parent`. Keys beyond these
            are accepted and not stored, on the import and on the `PUT` alike.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            node_id=node_id,
            client=client,
            body=body,
        )
    ).parsed
