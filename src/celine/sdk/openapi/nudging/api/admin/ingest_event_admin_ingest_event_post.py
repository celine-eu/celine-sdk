from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.digital_twin_event import DigitalTwinEvent
from ...models.ingest_accepted_response import IngestAcceptedResponse
from ...models.ingest_error_detail import IngestErrorDetail
from ...models.ingest_ok_response import IngestOkResponse
from ...types import Response


def _get_kwargs(
    *,
    body: DigitalTwinEvent,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/admin/ingest-event",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse | None:
    if response.status_code == 200:
        response_200 = IngestOkResponse.from_dict(response.json())

        return response_200

    if response.status_code == 202:
        response_202 = IngestAcceptedResponse.from_dict(response.json())

        return response_202

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = IngestErrorDetail.from_dict(response.json())

        return response_400

    if response.status_code == 409:
        response_409 = IngestErrorDetail.from_dict(response.json())

        return response_409

    if response.status_code == 422:
        response_422 = IngestErrorDetail.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = IngestErrorDetail.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DigitalTwinEvent,
) -> Response[Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse]:
    """Ingest a Digital Twin event

     Accepts an enriched Digital Twin event, evaluates nudging rules, and dispatches deliveries for any
    triggered nudges.

    Args:
        body (DigitalTwinEvent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse]
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
    body: DigitalTwinEvent,
) -> Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse | None:
    """Ingest a Digital Twin event

     Accepts an enriched Digital Twin event, evaluates nudging rules, and dispatches deliveries for any
    triggered nudges.

    Args:
        body (DigitalTwinEvent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: DigitalTwinEvent,
) -> Response[Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse]:
    """Ingest a Digital Twin event

     Accepts an enriched Digital Twin event, evaluates nudging rules, and dispatches deliveries for any
    triggered nudges.

    Args:
        body (DigitalTwinEvent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: DigitalTwinEvent,
) -> Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse | None:
    """Ingest a Digital Twin event

     Accepts an enriched Digital Twin event, evaluates nudging rules, and dispatches deliveries for any
    triggered nudges.

    Args:
        body (DigitalTwinEvent):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | IngestAcceptedResponse | IngestErrorDetail | IngestOkResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
