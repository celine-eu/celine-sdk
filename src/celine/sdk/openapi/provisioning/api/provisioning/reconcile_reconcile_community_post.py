from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
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
) -> Any | ErrorResponse | HTTPValidationError | ReconcileResponse | None:
    if response.status_code == 200:
        response_200 = ReconcileResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if response.status_code == 502:
        response_502 = ErrorResponse.from_dict(response.json())

        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorResponse | HTTPValidationError | ReconcileResponse]:
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
) -> Response[Any | ErrorResponse | HTTPValidationError | ReconcileResponse]:
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
        Response[Any | ErrorResponse | HTTPValidationError | ReconcileResponse]
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
) -> Any | ErrorResponse | HTTPValidationError | ReconcileResponse | None:
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
        Any | ErrorResponse | HTTPValidationError | ReconcileResponse
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
) -> Response[Any | ErrorResponse | HTTPValidationError | ReconcileResponse]:
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
        Response[Any | ErrorResponse | HTTPValidationError | ReconcileResponse]
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
) -> Any | ErrorResponse | HTTPValidationError | ReconcileResponse | None:
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
        Any | ErrorResponse | HTTPValidationError | ReconcileResponse
    """

    return (
        await asyncio_detailed(
            community=community,
            client=client,
            authorization=authorization,
        )
    ).parsed
