from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.shared_delivery_points_read import SharedDeliveryPointsRead
from ...types import UNSET, Response, Unset


def _get_kwargs(
    rec_slug: str,
    *,
    reveal: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["reveal"] = reveal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/{rec_slug}/delivery-points/shared".format(
            rec_slug=quote(str(rec_slug), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SharedDeliveryPointsRead | None:
    if response.status_code == 200:
        response_200 = SharedDeliveryPointsRead.from_dict(response.json())

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
) -> Response[HTTPValidationError | SharedDeliveryPointsRead]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    reveal: bool | Unset = False,
) -> Response[HTTPValidationError | SharedDeliveryPointsRead]:
    """Shared Delivery Points

     PODs that more than one active member holds, this community's holders first.

    409 when this community has no registry to ask; 404 when the registry holds no
    community for it; 502 for another registry refusal; 503 when it cannot be
    reached.

    Args:
        rec_slug (str):
        reveal (bool | Unset): Unmask the PODs. Requires `submissions.reveal`, and is recorded in
            the audit trail. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SharedDeliveryPointsRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        reveal=reveal,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    reveal: bool | Unset = False,
) -> HTTPValidationError | SharedDeliveryPointsRead | None:
    """Shared Delivery Points

     PODs that more than one active member holds, this community's holders first.

    409 when this community has no registry to ask; 404 when the registry holds no
    community for it; 502 for another registry refusal; 503 when it cannot be
    reached.

    Args:
        rec_slug (str):
        reveal (bool | Unset): Unmask the PODs. Requires `submissions.reveal`, and is recorded in
            the audit trail. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SharedDeliveryPointsRead
    """

    return sync_detailed(
        rec_slug=rec_slug,
        client=client,
        reveal=reveal,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    reveal: bool | Unset = False,
) -> Response[HTTPValidationError | SharedDeliveryPointsRead]:
    """Shared Delivery Points

     PODs that more than one active member holds, this community's holders first.

    409 when this community has no registry to ask; 404 when the registry holds no
    community for it; 502 for another registry refusal; 503 when it cannot be
    reached.

    Args:
        rec_slug (str):
        reveal (bool | Unset): Unmask the PODs. Requires `submissions.reveal`, and is recorded in
            the audit trail. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SharedDeliveryPointsRead]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        reveal=reveal,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    reveal: bool | Unset = False,
) -> HTTPValidationError | SharedDeliveryPointsRead | None:
    """Shared Delivery Points

     PODs that more than one active member holds, this community's holders first.

    409 when this community has no registry to ask; 404 when the registry holds no
    community for it; 502 for another registry refusal; 503 when it cannot be
    reached.

    Args:
        rec_slug (str):
        reveal (bool | Unset): Unmask the PODs. Requires `submissions.reveal`, and is recorded in
            the audit trail. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SharedDeliveryPointsRead
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            client=client,
            reveal=reveal,
        )
    ).parsed
