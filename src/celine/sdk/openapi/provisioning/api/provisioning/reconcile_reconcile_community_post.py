from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.reconcile_response import ReconcileResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    community: str,
    *,
    authorization: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(authorization, Unset):
        headers["authorization"] = authorization

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/reconcile/{community}".format(
            community=quote(str(community), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ReconcileResponse | None:
    if response.status_code == 200:
        response_200 = ReconcileResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ReconcileResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReconcileResponse]:
    """Sweep one community from the registry

     Provision every active member the registry holds, then assert that each
    is in the REC's organization.

    **A sweep that ends with a divergence answers `500`**, with the divergences
    in the body. Everything checked is something this same call claimed to have
    done, so a finding is a provisioning call that reported success and had not
    succeeded — a `200` with a list nobody reads is how 10 of 45 members ended
    up outside their own organization with nothing saying so.

    What calls this on a schedule is a deployment concern. The route is the
    entry point and nothing here is a scheduler.

    Args:
        community (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReconcileResponse]
    """

    kwargs = _get_kwargs(
        community=community,
        authorization=authorization,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | ReconcileResponse | None:
    """Sweep one community from the registry

     Provision every active member the registry holds, then assert that each
    is in the REC's organization.

    **A sweep that ends with a divergence answers `500`**, with the divergences
    in the body. Everything checked is something this same call claimed to have
    done, so a finding is a provisioning call that reported success and had not
    succeeded — a `200` with a list nobody reads is how 10 of 45 members ended
    up outside their own organization with nothing saying so.

    What calls this on a schedule is a deployment concern. The route is the
    entry point and nothing here is a scheduler.

    Args:
        community (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReconcileResponse
    """

    return sync_detailed(
        community=community,
        client=client,
        authorization=authorization,
    ).parsed


async def asyncio_detailed(
    community: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReconcileResponse]:
    """Sweep one community from the registry

     Provision every active member the registry holds, then assert that each
    is in the REC's organization.

    **A sweep that ends with a divergence answers `500`**, with the divergences
    in the body. Everything checked is something this same call claimed to have
    done, so a finding is a provisioning call that reported success and had not
    succeeded — a `200` with a list nobody reads is how 10 of 45 members ended
    up outside their own organization with nothing saying so.

    What calls this on a schedule is a deployment concern. The route is the
    entry point and nothing here is a scheduler.

    Args:
        community (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReconcileResponse]
    """

    kwargs = _get_kwargs(
        community=community,
        authorization=authorization,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community: str,
    *,
    client: AuthenticatedClient | Client,
    authorization: None | str | Unset = UNSET,
) -> HTTPValidationError | ReconcileResponse | None:
    """Sweep one community from the registry

     Provision every active member the registry holds, then assert that each
    is in the REC's organization.

    **A sweep that ends with a divergence answers `500`**, with the divergences
    in the body. Everything checked is something this same call claimed to have
    done, so a finding is a provisioning call that reported success and had not
    succeeded — a `200` with a list nobody reads is how 10 of 45 members ended
    up outside their own organization with nothing saying so.

    What calls this on a schedule is a deployment concern. The route is the
    entry point and nothing here is a scheduler.

    Args:
        community (str):
        authorization (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReconcileResponse
    """

    return (
        await asyncio_detailed(
            community=community,
            client=client,
            authorization=authorization,
        )
    ).parsed
