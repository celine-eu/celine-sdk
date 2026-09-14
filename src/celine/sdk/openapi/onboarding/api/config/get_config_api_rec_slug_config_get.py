from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    rec_slug: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/{rec_slug}/config".format(
            rec_slug=quote(str(rec_slug), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
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
) -> Response[Any | HTTPValidationError]:
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
) -> Response[Any | HTTPValidationError]:
    """Get Config

     The manifest's public allow-list, and whether approval brings a login.

    ``login_invitation`` is what lets the wizard tell the person that approval
    comes with an email to set a password — and not tell them when it does not.
    Approval sends that invitation only where a login is provisioned at all: a
    deployment with no provisioning service, or a REC declaring no
    ``rec_registry`` block, gets no account and therefore no email. A promise
    the platform then breaks is worse than saying nothing.

    ``features`` is what the deployment allows, which the manifest cannot know.
    The wizard renders upload and scanning only where these say so, rather than
    offering a control the API would refuse. Upload and scan are separate
    fields that follow one switch today, so that upload without scanning can be
    enabled later without changing this response. ``phone_verification`` says
    whether a ``phone_verify`` step can run; off, the wizard leaves it out.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
) -> Any | HTTPValidationError | None:
    """Get Config

     The manifest's public allow-list, and whether approval brings a login.

    ``login_invitation`` is what lets the wizard tell the person that approval
    comes with an email to set a password — and not tell them when it does not.
    Approval sends that invitation only where a login is provisioned at all: a
    deployment with no provisioning service, or a REC declaring no
    ``rec_registry`` block, gets no account and therefore no email. A promise
    the platform then breaks is worse than saying nothing.

    ``features`` is what the deployment allows, which the manifest cannot know.
    The wizard renders upload and scanning only where these say so, rather than
    offering a control the API would refuse. Upload and scan are separate
    fields that follow one switch today, so that upload without scanning can be
    enabled later without changing this response. ``phone_verification`` says
    whether a ``phone_verify`` step can run; off, the wizard leaves it out.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        rec_slug=rec_slug,
        client=client,
    ).parsed


async def asyncio_detailed(
    rec_slug: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    """Get Config

     The manifest's public allow-list, and whether approval brings a login.

    ``login_invitation`` is what lets the wizard tell the person that approval
    comes with an email to set a password — and not tell them when it does not.
    Approval sends that invitation only where a login is provisioned at all: a
    deployment with no provisioning service, or a REC declaring no
    ``rec_registry`` block, gets no account and therefore no email. A promise
    the platform then breaks is worse than saying nothing.

    ``features`` is what the deployment allows, which the manifest cannot know.
    The wizard renders upload and scanning only where these say so, rather than
    offering a control the API would refuse. Upload and scan are separate
    fields that follow one switch today, so that upload without scanning can be
    enabled later without changing this response. ``phone_verification`` says
    whether a ``phone_verify`` step can run; off, the wizard leaves it out.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
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
) -> Any | HTTPValidationError | None:
    """Get Config

     The manifest's public allow-list, and whether approval brings a login.

    ``login_invitation`` is what lets the wizard tell the person that approval
    comes with an email to set a password — and not tell them when it does not.
    Approval sends that invitation only where a login is provisioned at all: a
    deployment with no provisioning service, or a REC declaring no
    ``rec_registry`` block, gets no account and therefore no email. A promise
    the platform then breaks is worse than saying nothing.

    ``features`` is what the deployment allows, which the manifest cannot know.
    The wizard renders upload and scanning only where these say so, rather than
    offering a control the API would refuse. Upload and scan are separate
    fields that follow one switch today, so that upload without scanning can be
    enabled later without changing this response. ``phone_verification`` says
    whether a ``phone_verify`` step can run; off, the wizard leaves it out.

    Args:
        rec_slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            rec_slug=rec_slug,
            client=client,
        )
    ).parsed
