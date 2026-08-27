from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.global_asset_lookup import GlobalAssetLookup
from ...models.http_validation_error import HTTPValidationError
from ...models.sensor_ids_batch_request import SensorIdsBatchRequest
from ...types import Response


def _get_kwargs(
    *,
    body: SensorIdsBatchRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/lookup/assets-by-sensor-ids",
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
    body: SensorIdsBatchRequest,
) -> Response[HTTPValidationError | list[GlobalAssetLookup]]:
    """Lookup Assets By Sensor Ids

     Find assets by multiple sensor_ids across all communities.

    The mirror of ``assets-by-user-ids``: this one starts from a device and
    finds its owner, that one starts from owners and finds their devices.

    **Bounded**, at the same 500 as its sibling. Both are reachable by anything
    holding ``rec-registry.lookup``, and a caller that can name ten thousand
    sensors in one request has a dump of the registry rather than a lookup.

    **A sensor id that matches nothing contributes no row** rather than failing
    the request: the caller asked about a set, and one absent member of it does
    not make the rest unanswerable.

    Args:
        body (SensorIdsBatchRequest): Sensors to resolve owners for.

            Bounded for the same reason as its sibling below, and by the same number.
            Sensor ids are less guessable than usernames, which makes this the weaker
            enumeration path — but not the weaker *bulk extraction* one: a caller
            holding a list of them resolves every owner and community in one request.

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
    body: SensorIdsBatchRequest,
) -> HTTPValidationError | list[GlobalAssetLookup] | None:
    """Lookup Assets By Sensor Ids

     Find assets by multiple sensor_ids across all communities.

    The mirror of ``assets-by-user-ids``: this one starts from a device and
    finds its owner, that one starts from owners and finds their devices.

    **Bounded**, at the same 500 as its sibling. Both are reachable by anything
    holding ``rec-registry.lookup``, and a caller that can name ten thousand
    sensors in one request has a dump of the registry rather than a lookup.

    **A sensor id that matches nothing contributes no row** rather than failing
    the request: the caller asked about a set, and one absent member of it does
    not make the rest unanswerable.

    Args:
        body (SensorIdsBatchRequest): Sensors to resolve owners for.

            Bounded for the same reason as its sibling below, and by the same number.
            Sensor ids are less guessable than usernames, which makes this the weaker
            enumeration path — but not the weaker *bulk extraction* one: a caller
            holding a list of them resolves every owner and community in one request.

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
    body: SensorIdsBatchRequest,
) -> Response[HTTPValidationError | list[GlobalAssetLookup]]:
    """Lookup Assets By Sensor Ids

     Find assets by multiple sensor_ids across all communities.

    The mirror of ``assets-by-user-ids``: this one starts from a device and
    finds its owner, that one starts from owners and finds their devices.

    **Bounded**, at the same 500 as its sibling. Both are reachable by anything
    holding ``rec-registry.lookup``, and a caller that can name ten thousand
    sensors in one request has a dump of the registry rather than a lookup.

    **A sensor id that matches nothing contributes no row** rather than failing
    the request: the caller asked about a set, and one absent member of it does
    not make the rest unanswerable.

    Args:
        body (SensorIdsBatchRequest): Sensors to resolve owners for.

            Bounded for the same reason as its sibling below, and by the same number.
            Sensor ids are less guessable than usernames, which makes this the weaker
            enumeration path — but not the weaker *bulk extraction* one: a caller
            holding a list of them resolves every owner and community in one request.

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
    body: SensorIdsBatchRequest,
) -> HTTPValidationError | list[GlobalAssetLookup] | None:
    """Lookup Assets By Sensor Ids

     Find assets by multiple sensor_ids across all communities.

    The mirror of ``assets-by-user-ids``: this one starts from a device and
    finds its owner, that one starts from owners and finds their devices.

    **Bounded**, at the same 500 as its sibling. Both are reachable by anything
    holding ``rec-registry.lookup``, and a caller that can name ten thousand
    sensors in one request has a dump of the registry rather than a lookup.

    **A sensor id that matches nothing contributes no row** rather than failing
    the request: the caller asked about a set, and one absent member of it does
    not make the rest unanswerable.

    Args:
        body (SensorIdsBatchRequest): Sensors to resolve owners for.

            Bounded for the same reason as its sibling below, and by the same number.
            Sensor ids are less guessable than usernames, which makes this the weaker
            enumeration path — but not the weaker *bulk extraction* one: a caller
            holding a list of them resolves every owner and community in one request.

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
