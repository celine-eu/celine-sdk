from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.registry_drift_out import RegistryDriftOut
from ...types import Response


def _get_kwargs(
    rec_slug: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/admin/recs/{rec_slug}/registry-drift".format(
            rec_slug=quote(str(rec_slug), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RegistryDriftOut | None:
    if response.status_code == 200:
        response_200 = RegistryDriftOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | RegistryDriftOut]:
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
) -> Response[HTTPValidationError | RegistryDriftOut]:
    """Registry Drift Route

     Whether the registry's areas and topology match this REC's template.

    `recs.drift`: realm-level `admins`, and that REC's own `managers` and
    `admins` (D55); not its editors or viewers, and no service account.

    Reads the registry community with this service's own `rec-registry.read`;
    writes nothing and asks the Digital Twin nothing.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RegistryDriftOut]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | RegistryDriftOut | None:
    """Registry Drift Route

     Whether the registry's areas and topology match this REC's template.

    `recs.drift`: realm-level `admins`, and that REC's own `managers` and
    `admins` (D55); not its editors or viewers, and no service account.

    Reads the registry community with this service's own `rec-registry.read`;
    writes nothing and asks the Digital Twin nothing.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RegistryDriftOut
    """

    return sync_detailed(
        rec_slug=rec_slug,
        client=client,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | RegistryDriftOut]:
    """Registry Drift Route

     Whether the registry's areas and topology match this REC's template.

    `recs.drift`: realm-level `admins`, and that REC's own `managers` and
    `admins` (D55); not its editors or viewers, and no service account.

    Reads the registry community with this service's own `rec-registry.read`;
    writes nothing and asks the Digital Twin nothing.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RegistryDriftOut]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | RegistryDriftOut | None:
    """Registry Drift Route

     Whether the registry's areas and topology match this REC's template.

    `recs.drift`: realm-level `admins`, and that REC's own `managers` and
    `admins` (D55); not its editors or viewers, and no service account.

    Reads the registry community with this service's own `rec-registry.read`;
    writes nothing and asks the Digital Twin nothing.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RegistryDriftOut
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            client=client,
        )
    ).parsed
