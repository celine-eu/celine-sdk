from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.asset_detail import AssetDetail
from ...models.asset_upsert import AssetUpsert
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    body: AssetUpsert,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/admin/communities/{community_key}/members/{member_key}/assets/{asset_key}".format(
            community_key=quote(str(community_key), safe=""),
            member_key=quote(str(member_key), safe=""),
            asset_key=quote(str(asset_key), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = AssetDetail.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 409:
        response_409 = ErrorResponse.from_dict(response.json())

        return response_409

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
) -> Response[AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> Response[AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Answers `409` when the key already belongs to another member of the
    community — asset keys are unique per community, not per member, so a key
    that looks free to this member may not be.

    A concurrent upsert of the same key by the same member is **not** a
    conflict: the service applies it to the row the other writer created and
    answers `200`, because a create-or-replace is idempotent and a race means
    only that the two arrived in an order neither cared about.

    **A meter is attached here** — by convention at `meter-<sensor id>`, the id
    trimmed (REQ-0071). The outcomes a caller tells apart by `code`:

    * `200` — attached, or already attached to this member (a no-op replace);
    * `409 sensor_held` — another active member, in any community, holds the
      sensor (REQ-0069); a holder outside this community is not named;
    * `409 asset_key_taken` — another member of this community holds the key
      (with the convention: an inactive member still holding the asset).

    The sensor id is stored trimmed; one blank after trimming is `422`. An
    asset key longer than 128 characters is `422 asset_key_too_long` — with the
    convention, a sensor id longer than 122 (REQ-0028).

    Answers the stored asset.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        asset_key=asset_key,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Answers `409` when the key already belongs to another member of the
    community — asset keys are unique per community, not per member, so a key
    that looks free to this member may not be.

    A concurrent upsert of the same key by the same member is **not** a
    conflict: the service applies it to the row the other writer created and
    answers `200`, because a create-or-replace is idempotent and a race means
    only that the two arrived in an order neither cared about.

    **A meter is attached here** — by convention at `meter-<sensor id>`, the id
    trimmed (REQ-0071). The outcomes a caller tells apart by `code`:

    * `200` — attached, or already attached to this member (a no-op replace);
    * `409 sensor_held` — another active member, in any community, holds the
      sensor (REQ-0069); a holder outside this community is not named;
    * `409 asset_key_taken` — another member of this community holds the key
      (with the convention: an inactive member still holding the asset).

    The sensor id is stored trimmed; one blank after trimming is `422`. An
    asset key longer than 128 characters is `422 asset_key_too_long` — with the
    convention, a sensor id longer than 122 (REQ-0028).

    Answers the stored asset.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return sync_detailed(
        community_key=community_key,
        member_key=member_key,
        asset_key=asset_key,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> Response[AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError]:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Answers `409` when the key already belongs to another member of the
    community — asset keys are unique per community, not per member, so a key
    that looks free to this member may not be.

    A concurrent upsert of the same key by the same member is **not** a
    conflict: the service applies it to the row the other writer created and
    answers `200`, because a create-or-replace is idempotent and a race means
    only that the two arrived in an order neither cared about.

    **A meter is attached here** — by convention at `meter-<sensor id>`, the id
    trimmed (REQ-0071). The outcomes a caller tells apart by `code`:

    * `200` — attached, or already attached to this member (a no-op replace);
    * `409 sensor_held` — another active member, in any community, holds the
      sensor (REQ-0069); a holder outside this community is not named;
    * `409 asset_key_taken` — another member of this community holds the key
      (with the convention: an inactive member still holding the asset).

    The sensor id is stored trimmed; one blank after trimming is `422`. An
    asset key longer than 128 characters is `422 asset_key_too_long` — with the
    convention, a sensor id longer than 122 (REQ-0028).

    Answers the stored asset.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        community_key=community_key,
        member_key=member_key,
        asset_key=asset_key,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    community_key: str,
    member_key: str,
    asset_key: str,
    *,
    client: AuthenticatedClient | Client,
    body: AssetUpsert,
) -> AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError | None:
    """Upsert Asset

     Create or replace one asset, leaving the member's other assets alone.

    Answers `409` when the key already belongs to another member of the
    community — asset keys are unique per community, not per member, so a key
    that looks free to this member may not be.

    A concurrent upsert of the same key by the same member is **not** a
    conflict: the service applies it to the row the other writer created and
    answers `200`, because a create-or-replace is idempotent and a race means
    only that the two arrived in an order neither cared about.

    **A meter is attached here** — by convention at `meter-<sensor id>`, the id
    trimmed (REQ-0071). The outcomes a caller tells apart by `code`:

    * `200` — attached, or already attached to this member (a no-op replace);
    * `409 sensor_held` — another active member, in any community, holds the
      sensor (REQ-0069); a holder outside this community is not named;
    * `409 asset_key_taken` — another member of this community holds the key
      (with the convention: an inactive member still holding the asset).

    The sensor id is stored trimmed; one blank after trimming is `422`. An
    asset key longer than 128 characters is `422 asset_key_too_long` — with the
    convention, a sensor id longer than 122 (REQ-0028).

    Answers the stored asset.

    Args:
        community_key (str):
        member_key (str):
        asset_key (str):
        body (AssetUpsert): Create or replace one asset of a member.

            `properties` is validated against the model for `asset_type`, so an EV
            charger cannot be stored with a heat pump's fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetDetail | ErrorResponse | ErrorResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            asset_key=asset_key,
            client=client,
            body=body,
        )
    ).parsed
