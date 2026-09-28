from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.registry_sync_out import RegistrySyncOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    rec_slug: str,
    *,
    dry_run: bool | Unset = False,
    prune: bool | Unset = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["dry_run"] = dry_run

    params["prune"] = prune

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/recs/{rec_slug}/registry-sync".format(
            rec_slug=quote(str(rec_slug), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RegistrySyncOut | None:
    if response.status_code == 200:
        response_200 = RegistrySyncOut.from_dict(response.json())

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
) -> Response[HTTPValidationError | RegistrySyncOut]:
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
    dry_run: bool | Unset = False,
    prune: bool | Unset = False,
) -> Response[HTTPValidationError | RegistrySyncOut]:
    """Registry Sync Route

     Push this REC's template areas to its registry community.

    Realm-level `admins` only (`recs.write`); no service account holds it. A dry
    run writes nothing — not to the registry, not to the provisioning service —
    and answers the plan. A real run first sets the community up through the
    provisioning reconcile, whose failure is reported and does not stop the
    area writes. The status is `200` whenever the sync ran; `ok` and each item's
    `outcome` say what happened.

    Args:
        rec_slug (str):
        dry_run (bool | Unset):  Default: False.
        prune (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RegistrySyncOut]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        dry_run=dry_run,
        prune=prune,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    dry_run: bool | Unset = False,
    prune: bool | Unset = False,
) -> HTTPValidationError | RegistrySyncOut | None:
    """Registry Sync Route

     Push this REC's template areas to its registry community.

    Realm-level `admins` only (`recs.write`); no service account holds it. A dry
    run writes nothing — not to the registry, not to the provisioning service —
    and answers the plan. A real run first sets the community up through the
    provisioning reconcile, whose failure is reported and does not stop the
    area writes. The status is `200` whenever the sync ran; `ok` and each item's
    `outcome` say what happened.

    Args:
        rec_slug (str):
        dry_run (bool | Unset):  Default: False.
        prune (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RegistrySyncOut
    """

    return sync_detailed(
        rec_slug=rec_slug,
        client=client,
        dry_run=dry_run,
        prune=prune,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    dry_run: bool | Unset = False,
    prune: bool | Unset = False,
) -> Response[HTTPValidationError | RegistrySyncOut]:
    """Registry Sync Route

     Push this REC's template areas to its registry community.

    Realm-level `admins` only (`recs.write`); no service account holds it. A dry
    run writes nothing — not to the registry, not to the provisioning service —
    and answers the plan. A real run first sets the community up through the
    provisioning reconcile, whose failure is reported and does not stop the
    area writes. The status is `200` whenever the sync ran; `ok` and each item's
    `outcome` say what happened.

    Args:
        rec_slug (str):
        dry_run (bool | Unset):  Default: False.
        prune (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RegistrySyncOut]
    """

    kwargs = _get_kwargs(
        rec_slug=rec_slug,
        dry_run=dry_run,
        prune=prune,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
    dry_run: bool | Unset = False,
    prune: bool | Unset = False,
) -> HTTPValidationError | RegistrySyncOut | None:
    """Registry Sync Route

     Push this REC's template areas to its registry community.

    Realm-level `admins` only (`recs.write`); no service account holds it. A dry
    run writes nothing — not to the registry, not to the provisioning service —
    and answers the plan. A real run first sets the community up through the
    provisioning reconcile, whose failure is reported and does not stop the
    area writes. The status is `200` whenever the sync ran; `ok` and each item's
    `outcome` say what happened.

    Args:
        rec_slug (str):
        dry_run (bool | Unset):  Default: False.
        prune (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RegistrySyncOut
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            client=client,
            dry_run=dry_run,
            prune=prune,
        )
    ).parsed
