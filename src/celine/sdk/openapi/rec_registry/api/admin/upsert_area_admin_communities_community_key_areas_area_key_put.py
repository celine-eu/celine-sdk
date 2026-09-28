from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.area_upsert import AreaUpsert
from ...models.community_detail import CommunityDetail
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    area_key: str,
    *,
    body: AreaUpsert,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/areas/{area_key}".format(
            community_key=quote(str(community_key), safe=""),
            area_key=quote(str(area_key), safe=""),
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
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    **An area is one primary substation** (REQ-0067): `boundary: {source, id}`
    with `source` `gse_cabine_primarie`, and `topology` listing exactly one node
    id — `boundary.id`, a node of the community's topology whose `type` is
    `primary_substation`. No other area of the community may carry the same
    `boundary.id`. Anything else is `422 invalid_area_boundary` and changes
    nothing — including a node the community's topology does not hold yet,
    which has to be written first. Areas stored before the rule are not
    re-judged, except that the written area may not share their boundary id.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

            One primary substation (REQ-0067): `boundary` references it and `topology`
            lists exactly one node id, `boundary.id`, a `primary_substation` node of
            the community's topology. Anything else — no boundary, a list of them or a
            malformed one included — is `422 invalid_area_boundary`; `boundary`
            accepts anything in the model only so that each of those is refused with
            that code rather than as a validation error.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        area_key=area_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    **An area is one primary substation** (REQ-0067): `boundary: {source, id}`
    with `source` `gse_cabine_primarie`, and `topology` listing exactly one node
    id — `boundary.id`, a node of the community's topology whose `type` is
    `primary_substation`. No other area of the community may carry the same
    `boundary.id`. Anything else is `422 invalid_area_boundary` and changes
    nothing — including a node the community's topology does not hold yet,
    which has to be written first. Areas stored before the rule are not
    re-judged, except that the written area may not share their boundary id.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

            One primary substation (REQ-0067): `boundary` references it and `topology`
            lists exactly one node id, `boundary.id`, a `primary_substation` node of
            the community's topology. Anything else — no boundary, a list of them or a
            malformed one included — is `422 invalid_area_boundary`; `boundary`
            accepts anything in the model only so that each of those is refused with
            that code rather than as a validation error.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        area_key=area_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    **An area is one primary substation** (REQ-0067): `boundary: {source, id}`
    with `source` `gse_cabine_primarie`, and `topology` listing exactly one node
    id — `boundary.id`, a node of the community's topology whose `type` is
    `primary_substation`. No other area of the community may carry the same
    `boundary.id`. Anything else is `422 invalid_area_boundary` and changes
    nothing — including a node the community's topology does not hold yet,
    which has to be written first. Areas stored before the rule are not
    re-judged, except that the written area may not share their boundary id.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

            One primary substation (REQ-0067): `boundary` references it and `topology`
            lists exactly one node id, `boundary.id`, a `primary_substation` node of
            the community's topology. Anything else — no boundary, a list of them or a
            malformed one included — is `422 invalid_area_boundary`; `boundary`
            accepts anything in the model only so that each of those is refused with
            that code rather than as a validation error.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        area_key=area_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    area_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AreaUpsert,
) -> CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Area

     Add or replace one area, keeping the others.

    Topology assignments change more often than the community does, so this is a
    sub-resource rather than part of the community patch.

    **An area is one primary substation** (REQ-0067): `boundary: {source, id}`
    with `source` `gse_cabine_primarie`, and `topology` listing exactly one node
    id — `boundary.id`, a node of the community's topology whose `type` is
    `primary_substation`. No other area of the community may carry the same
    `boundary.id`. Anything else is `422 invalid_area_boundary` and changes
    nothing — including a node the community's topology does not hold yet,
    which has to be written first. Areas stored before the rule are not
    re-judged, except that the written area may not share their boundary id.

    Args:
        community_key (str):
        area_key (str):
        body (AreaUpsert): Create or replace one area of a community.

            One primary substation (REQ-0067): `boundary` references it and `topology`
            lists exactly one node id, `boundary.id`, a `primary_substation` node of
            the community's topology. Anything else — no boundary, a list of them or a
            malformed one included — is `422 invalid_area_boundary`; `boundary`
            accepts anything in the model only so that each of those is refused with
            that code rather than as a validation error.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CommunityDetail | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            area_key=area_key,
            client=client,
            body=body,
        )
    ).parsed
