from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.eligibility_request import EligibilityRequest
from ...models.eligibility_response import EligibilityResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    rec_slug: str,
    *,
    body: EligibilityRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/{rec_slug}/eligibility".format(
            rec_slug=quote(str(rec_slug), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> EligibilityResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = EligibilityResponse.from_dict(response.json())

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
) -> Response[EligibilityResponse | HTTPValidationError]:
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
    body: EligibilityRequest,
) -> Response[EligibilityResponse | HTTPValidationError]:
    """Check Eligibility

    Args:
        rec_slug (str):
        body (EligibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EligibilityResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    body: EligibilityRequest,
) -> EligibilityResponse | HTTPValidationError | None:
    """Check Eligibility

    Args:
        rec_slug (str):
        body (EligibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EligibilityResponse | HTTPValidationError
    """

    return sync_detailed(
        rec_slug=rec_slug,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    body: EligibilityRequest,
) -> Response[EligibilityResponse | HTTPValidationError]:
    """Check Eligibility

    Args:
        rec_slug (str):
        body (EligibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[EligibilityResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    body: EligibilityRequest,
) -> EligibilityResponse | HTTPValidationError | None:
    """Check Eligibility

    Args:
        rec_slug (str):
        body (EligibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        EligibilityResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            client=client,
            body=body,
        )
    ).parsed
