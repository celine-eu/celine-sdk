"""REC Registry API wrapper.

Reusable client design for multi-tenant/per-request scenarios.
Initialize once, pass tokens per-call - no client recreation overhead.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Awaitable, Callable, Mapping, Optional, TypeVar

import httpx
from pydantic import BaseModel

from celine.sdk.auth import TokenProvider
from celine.sdk.openapi.rec_registry import AuthenticatedClient, Client
from celine.sdk.openapi.rec_registry.api.admin import (
    admin_export_admin_export_get,
    admin_import_yaml_admin_import_yaml_post,
    get_asset_admin_communities_community_key_assets_asset_key_get,
    get_asset_by_sensor_id_admin_communities_community_key_assets_by_sensor_id_sensor_id_get,
    get_community_admin_communities_community_key_get,
    get_community_topology_admin_communities_community_key_topology_get,
    get_delivery_point_by_id_admin_communities_community_key_delivery_points_by_id_dp_id_get,
    get_member_admin_communities_community_key_members_member_key_get,
    get_member_by_user_id_admin_communities_community_key_members_by_user_id_user_id_get,
    get_member_delivery_points_admin_communities_community_key_members_member_key_delivery_points_get,
    list_assets_admin_communities_community_key_assets_get,
    list_communities_admin_communities_get,
    list_delivery_points_admin_communities_community_key_delivery_points_get,
    list_members_admin_communities_community_key_members_get,
    list_meters_admin_communities_community_key_meters_get,
    lookup_asset_by_sensor_id,
    lookup_community_by_delivery_point,
    lookup_community_by_sensor_id,
    lookup_community_by_user_id,
    lookup_member_by_user_id,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    change_member_status_admin_communities_community_key_members_member_key_status_post as _change_member_status,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    create_member_admin_communities_community_key_members_post as _create_member,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    delete_asset_admin_communities_community_key_members_member_key_assets_asset_key_delete as _delete_asset,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    delete_member_admin_communities_community_key_members_member_key_delete as _delete_member,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    lookup_assets_by_sensor_ids as _lookup_assets_by_sensor_ids,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    lookup_assets_by_user_ids as _lookup_assets_by_user_ids,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    lookup_members_by_dids as _lookup_members_by_dids,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    patch_member_admin_communities_community_key_members_member_key_patch as _patch_member,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    patch_member_profile_admin_communities_community_key_members_member_key_profile_patch as _patch_member_profile,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    upsert_asset_admin_communities_community_key_members_member_key_assets_asset_key_put as _upsert_asset,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    upsert_area_admin_communities_community_key_areas_area_key_put as _upsert_area,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    delete_area_admin_communities_community_key_areas_area_key_delete as _delete_area,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    rename_area_admin_communities_community_key_areas_area_key_rename_post as _rename_area,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    upsert_topology_node_admin_communities_community_key_topology_node_id_put as _upsert_topology_node,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    delete_topology_node_admin_communities_community_key_topology_node_id_delete as _delete_topology_node,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    upsert_delivery_point_admin_communities_community_key_members_member_key_delivery_points_point_id_put as _upsert_delivery_point,
)
from celine.sdk.openapi.rec_registry.api.me import (
    get_me_user_get,
    get_my_asset_user_assets_asset_key_get,
    get_my_assets_user_assets_get,
    get_my_community_user_community_get,
    get_my_delivery_points_user_delivery_points_get,
    get_my_member_user_member_get,
)
from celine.sdk.openapi.rec_registry.models import (
    AreaRename,
    AreaUpsert,
    AssetUpsert,
    DeletionReport,
    DeliveryPointIn,
    ErrorResponse,
    HTTPValidationError,
    MemberCreate,
    MemberDetail,
    MemberPatch,
    MemberProfilePatch,
    MemberStatusChange,
    MultiImportReport,
    UserAssetsResponse,
    UserCommunityDetail,
    UserMeResponse,
    UserMemberDetail,
    UserDeliveryPointsResponse,
    UserAssetDetail,
    SensorIdsBatchRequest,
    TopologyNodeIn,
    UserIdsBatchRequest,
    DidsBatchRequest,
)

from celine.sdk.openapi.rec_registry.models.global_asset_lookup import GlobalAssetLookup
from celine.sdk.openapi.rec_registry.models.global_member_lookup import GlobalMemberLookup
from celine.sdk.rec_registry.errors import RecRegistryApiError
from celine.sdk.utils.convert import to_schema

from celine.sdk.openapi.rec_registry.schemas import (
    AreaRenamedSchema,
    AssetDetailSchema,
    CommunityDetailSchema,
    DeliveryPointLookupSchema,
    DeliveryPointsResponseSchema,
    GlobalAssetLookupSchema,
    GlobalMemberLookupSchema,
    HTTPValidationErrorSchema,
    LookupByDeliveryPointResponseSchema,
    LookupBySensorIdResponseSchema,
    LookupByUserIdResponseSchema,
    MemberDetailSchema,
    UserAssetsResponseSchema,
    UserCommunityDetailSchema,
    UserMeResponseSchema,
    UserMemberDetailSchema,
    UserDeliveryPointsResponseSchema,
    UserAssetDetailSchema,
)

from celine.sdk.openapi.rec_registry.types import UNSET

__all__ = [
    "RecRegistryUserClient",
    "RecRegistryAdminClient",
    "RecRegistryApiError",
    "AreaRenamedSchema",
    "AssetDetailSchema",
    "CommunityDetailSchema",
    "MemberDetailSchema",
    "MAX_BATCH_LOOKUP_IDS",
]

#: The largest batch any of the three batch-lookup routes accepts.
#:
#: Mirrored from `rec-registry`, where REQ-0043, REQ-0045 and REQ-0061 bound all
#: three batch lookups at one shared constant of the same name — 501 ids is a
#: `422`, 500 is accepted. It is mirrored rather than read from the specification because
#: there is nothing there to read: the generated request models are plain
#: `attrs` classes and validate nothing. The last time this number was written
#: twice the two copies disagreed for months (rec-registry#37), which is why it
#: is named here rather than typed into the two call sites.
MAX_BATCH_LOOKUP_IDS = 500

SchemaT = TypeVar("SchemaT", bound=BaseModel)


def _refused(response: httpx.Response, what: str) -> RecRegistryApiError:
    """The wrapper's error for a registry answer the helper does not take as success.

    Carries the status, the raw body and, when the registry named one, its
    refusal `code` read from the top level of the body (REQ-0127). A body that
    is not JSON leaves `code` and `detail` at `None`; nothing is parsed out of
    the sentence.
    """
    code, detail = RecRegistryApiError.refusal_of(response.content)
    sentence = detail if isinstance(detail, str) else None
    return RecRegistryApiError(
        f"{what} refused: rec-registry answered {response.status_code}"
        + (f" {code}" if code else "")
        + (f" ({sentence})" if sentence else ""),
        status_code=response.status_code,
        body=response.content,
        code=code,
        detail=detail,
    )


def _answer(response: httpx.Response, schema: type[SchemaT], what: str) -> SchemaT:
    """`200` parsed into `schema`; anything else raises `RecRegistryApiError`.

    The response is read here, never by the generated `_parse_response`, which
    calls `response.json()` on every status it declares and so fails with a
    decode error on a proxy's HTML `403`, and maps `code` onto a generated enum.
    An unreadable `200` raises too, rather than answering nothing.
    """
    if response.status_code != HTTPStatus.OK:
        raise _refused(response, what)
    try:
        return schema.model_validate(response.json())
    except ValueError as exc:
        raise RecRegistryApiError(
            f"{what}: rec-registry answered 200 with nothing readable",
            status_code=response.status_code,
            body=response.content,
        ) from exc


class RecRegistryUserClient:
    """User-scoped REC Registry client (/user endpoints).

    Designed for per-request token usage. Initialize once, reuse for all requests.
    Pass token on each call - no client recreation overhead.

    Args:
        base_url: Base URL of the REC Registry API
        timeout: Request timeout in seconds (default: 30.0)
        verify_ssl: Verify SSL certificates (default: True)

    Example - Per-request usage (FastAPI/Flask):
        # Initialize once (application startup)
        registry_client = RecRegistryUserClient(base_url="https://registry.example.com")

        # Use in request handler
        @app.get("/api/me")
        async def get_current_user(token: str = Depends(get_token)):
            me = await registry_client.get_me(token=token)
            return me

    Example - With default token:
        # For single-tenant or testing
        client = RecRegistryUserClient(
            base_url="https://registry.example.com",
            default_token="my-token"
        )
        me = await client.get_me()  # Uses default_token
    """

    def __init__(
        self,
        base_url: str,
        *,
        default_token: Optional[str] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ):
        self._base_url = base_url
        self._default_token = default_token
        self._timeout = httpx.Timeout(timeout)
        self._verify_ssl = verify_ssl
        # Shared unauthenticated client for creating authenticated ones
        self._base_client = Client(
            base_url=base_url,
            timeout=self._timeout,
            verify_ssl=verify_ssl,
            raise_on_unexpected_status=True,
        )

    def _get_client(self, token: Optional[str]) -> AuthenticatedClient:
        """Get authenticated client for this request."""
        actual_token = token or self._default_token
        if actual_token is None:
            raise ValueError("No token provided and no default_token set")

        return AuthenticatedClient(
            base_url=self._base_url,
            token=actual_token,
            timeout=self._timeout,
            verify_ssl=self._verify_ssl,
            raise_on_unexpected_status=True,
        )

    async def get_me(
        self, *, token: Optional[str] = None
    ) -> UserMeResponseSchema | None:
        """Get current user profile and membership information."""
        client = self._get_client(token)
        res = await get_me_user_get.asyncio_detailed(client=client)
        return to_schema(res.parsed, UserMeResponseSchema)

    # The self-service reads below send through the generated request builder
    # (`_get_kwargs`), so path and quoting stay generated, and read the
    # response themselves (REQ-0132): anything but `200` raises
    # `RecRegistryApiError` with the registry's `code` — `not_a_member` on the
    # `403` a caller who is no member gets — and a body that is not JSON (a
    # proxy's page on a status the route declares) raises the same error with
    # no code, never a decode error from the generated parse.

    async def _read_mine(
        self,
        kwargs: dict[str, Any],
        schema: type[SchemaT],
        what: str,
        token: Optional[str],
    ) -> SchemaT:
        client = self._get_client(token)
        response = await client.get_async_httpx_client().request(**kwargs)
        return _answer(response, schema, what)

    async def get_my_community(
        self, *, token: Optional[str] = None
    ) -> UserCommunityDetailSchema:
        """Get the caller's community.

        Raises :class:`RecRegistryApiError` on anything but `200`; a caller
        who is no member gets `status_code` 403 and `code` `not_a_member`.
        """
        return await self._read_mine(
            get_my_community_user_community_get._get_kwargs(),
            UserCommunityDetailSchema,
            "get-my-community",
            token,
        )

    async def get_my_member(
        self, *, token: Optional[str] = None
    ) -> UserMemberDetailSchema:
        """Get the caller's member record.

        Raises :class:`RecRegistryApiError` on anything but `200`; a caller
        who is no member gets `status_code` 403 and `code` `not_a_member`.
        """
        return await self._read_mine(
            get_my_member_user_member_get._get_kwargs(),
            UserMemberDetailSchema,
            "get-my-member",
            token,
        )

    async def get_my_assets(
        self, *, token: Optional[str] = None
    ) -> UserAssetsResponseSchema:
        """List the assets the caller owns.

        Raises :class:`RecRegistryApiError` on anything but `200`; a caller
        who is no member gets `status_code` 403 and `code` `not_a_member` —
        which is not the same answer as a member owning nothing (`200`, no
        items).
        """
        return await self._read_mine(
            get_my_assets_user_assets_get._get_kwargs(),
            UserAssetsResponseSchema,
            "get-my-assets",
            token,
        )

    async def get_my_asset(
        self, asset_key: str, *, token: Optional[str] = None
    ) -> UserAssetDetailSchema:
        """Get one asset the caller owns.

        Raises :class:`RecRegistryApiError` on anything but `200`: `403`
        `not_a_member` for a caller who is no member, `404` for an asset the
        caller does not own.
        """
        return await self._read_mine(
            get_my_asset_user_assets_asset_key_get._get_kwargs(asset_key=asset_key),
            UserAssetDetailSchema,
            "get-my-asset",
            token,
        )

    async def get_my_delivery_points(
        self, *, token: Optional[str] = None
    ) -> UserDeliveryPointsResponseSchema:
        """Get the caller's delivery points.

        Raises :class:`RecRegistryApiError` on anything but `200`; a caller
        who is no member gets `status_code` 403 and `code` `not_a_member`.
        """
        return await self._read_mine(
            get_my_delivery_points_user_delivery_points_get._get_kwargs(),
            UserDeliveryPointsResponseSchema,
            "get-my-delivery-points",
            token,
        )


class RecRegistryAdminClient:
    """Admin-scoped REC Registry client (/admin endpoints).

    Designed for flexible token usage:
    1. Per-request tokens (multi-tenant)
    2. Default token (single-tenant)
    3. Token provider (service accounts)

    Initialize once, reuse for all requests.

    Args:
        base_url: Base URL of the REC Registry API
        default_token: Default token to use when none provided per-call
        token_provider: Token provider for automatic token management
        timeout: Request timeout in seconds (default: 30.0)
        verify_ssl: Verify SSL certificates (default: True)

    Example - Per-request tokens (multi-tenant):
        # Initialize once
        admin = RecRegistryAdminClient(base_url="https://registry.example.com")

        # Use in request handler
        @app.post("/api/admin/export")
        async def export_community(
            community_key: str,
            admin_token: str = Depends(get_admin_token)
        ):
            yaml = await admin.export_community(community_key, token=admin_token)
            return yaml

    Example - Default token (single-tenant):
        admin = RecRegistryAdminClient(
            base_url="https://registry.example.com",
            default_token="admin-token"
        )
        yaml = await admin.export_community("key")  # Uses default_token

    Example - Token provider (service account):
        from celine.sdk.auth import OidcClientCredentialsProvider

        provider = OidcClientCredentialsProvider(...)
        admin = RecRegistryAdminClient(
            base_url="https://registry.example.com",
            token_provider=provider
        )
        yaml = await admin.export_community("key")  # Uses provider
    """

    def __init__(
        self,
        base_url: str,
        *,
        default_token: Optional[str] = None,
        token_provider: Optional[TokenProvider] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ):
        self._base_url = base_url
        self._default_token = default_token
        self._token_provider = token_provider
        self._timeout = httpx.Timeout(timeout)
        self._verify_ssl = verify_ssl
        self._base_client = Client(
            base_url=base_url,
            timeout=self._timeout,
            verify_ssl=verify_ssl,
            raise_on_unexpected_status=True,
        )

    async def _get_client(self, token: Optional[str]) -> AuthenticatedClient:
        """Get authenticated client for this request."""
        # Priority: explicit token > default_token > token_provider
        if token is not None:
            actual_token = token
        elif self._default_token is not None:
            actual_token = self._default_token
        elif self._token_provider is not None:
            access_token = await self._token_provider.get_token()
            actual_token = access_token.access_token
        else:
            raise ValueError(
                "No token provided. Pass token= parameter, set default_token, "
                "or provide token_provider"
            )

        return AuthenticatedClient(
            base_url=self._base_url,
            token=actual_token,
            timeout=self._timeout,
            verify_ssl=self._verify_ssl,
            raise_on_unexpected_status=True,
        )

    # Export/Import operations
    async def export_communities(
        self,
        community_keys: list[str] | None = None,
        *,
        token: Optional[str] = None,
    ) -> str:
        """Export one or more communities as YAML.

        Pass community_keys to export specific communities.
        Omit (or pass None) to export all communities.
        Multiple communities are returned as a multidocument YAML string.
        """
        client = await self._get_client(token)
        res = await admin_export_admin_export_get.asyncio_detailed(
            client=client,
            community=community_keys if community_keys is not None else UNSET,
        )
        if isinstance(res.parsed, HTTPValidationError):
            raise Exception(res.parsed)
        return str(res.parsed)

    async def export_community(
        self, community_key: str, *, token: Optional[str] = None
    ) -> str:
        """Export a single community as YAML."""
        return await self.export_communities([community_key], token=token)

    async def import_yaml(
        self,
        yaml_content: str,
        *,
        dry_run: bool = False,
        token: Optional[str] = None,
    ) -> MultiImportReport:
        """Import one or more communities from a YAML string.

        Accepts single or multidocument YAML (documents separated by ---).
        Returns a report for each imported bundle.
        """
        client = await self._get_client(token)
        res = await admin_import_yaml_admin_import_yaml_post.asyncio_detailed(
            client=client,
            body=yaml_content,
            dry_run=dry_run,
        )
        # Since registry 1.6.0 the route's `422` is `oneOf` `ErrorResponse` (a
        # bundle breaking an invariant, with its `code`) / `HTTPValidationError`
        # (a body that failed validation). The generated parse tries
        # `ErrorResponse` first and it accepts a validation body too (with no
        # `code`), so which model came back says nothing: the code is read
        # from the raw body. Both are refusals; neither is a report.
        # `RecRegistryApiError` is an `Exception`, so a caller catching the
        # bare `Exception` this used to raise still catches it.
        if isinstance(res.parsed, (ErrorResponse, HTTPValidationError)):
            code, detail = RecRegistryApiError.refusal_of(res.content)
            raise RecRegistryApiError(
                f"import-yaml refused (status={int(res.status_code)})"
                + (f" {code}" if code else ""),
                status_code=int(res.status_code),
                body=res.content,
                code=code,
                detail=detail,
            )
        return res.parsed

    # List operations
    async def list_communities(
        self,
        *,
        key: Optional[str] = None,
        limit: int = 50,
        cursor: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Any:
        """List all communities."""
        client = await self._get_client(token)
        return await list_communities_admin_communities_get.asyncio_detailed(
            client=client,
            key=key if key is not None else UNSET,
            limit=limit,
            cursor=cursor if cursor is not None else UNSET,
        )

    async def list_assets(
        self,
        community_key: str,
        *,
        asset_type: Optional[str] = None,
        owner: Optional[str] = None,
        limit: int = 50,
        cursor: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Any:
        """List assets in a community."""
        client = await self._get_client(token)
        return await list_assets_admin_communities_community_key_assets_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            asset_type=asset_type if asset_type is not None else UNSET,
            owner=owner if owner is not None else UNSET,
            limit=limit,
            cursor=cursor if cursor is not None else UNSET,
        )

    async def list_members(
        self,
        community_key: str,
        *,
        role: Optional[str] = None,
        status: Optional[str] = None,
        area: Optional[str] = None,
        limit: int = 50,
        cursor: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Any:
        """List members in a community."""
        client = await self._get_client(token)
        return await list_members_admin_communities_community_key_members_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            role=role if role is not None else UNSET,
            status=status if status is not None else UNSET,
            area=area if area is not None else UNSET,
            limit=limit,
            cursor=cursor if cursor is not None else UNSET,
        )

    async def list_delivery_points(
        self,
        community_key: str,
        *,
        type_: Optional[str] = None,
        active: Optional[bool] = None,
        limit: int = 50,
        cursor: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Any:
        """List delivery points in a community."""
        client = await self._get_client(token)
        return await list_delivery_points_admin_communities_community_key_delivery_points_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            type_=type_ if type_ is not None else UNSET,
            active=active if active is not None else UNSET,
            limit=limit,
            cursor=cursor if cursor is not None else UNSET,
        )

    async def list_meters(
        self,
        community_key: str,
        *,
        owner: Optional[str] = None,
        limit: int = 50,
        cursor: Optional[str] = None,
        token: Optional[str] = None,
    ) -> Any:
        """List meters in a community."""
        client = await self._get_client(token)
        return await list_meters_admin_communities_community_key_meters_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            owner=owner if owner is not None else UNSET,
            limit=limit,
            cursor=cursor if cursor is not None else UNSET,
        )

    # Get operations
    async def get_community(
        self, community_key: str, *, token: Optional[str] = None
    ) -> Any:
        """Get community details."""
        client = await self._get_client(token)
        return await get_community_admin_communities_community_key_get.asyncio_detailed(
            client=client,
            community_key=community_key,
        )

    async def get_community_topology(
        self, community_key: str, *, token: Optional[str] = None
    ) -> Any:
        """Get community topology (network structure)."""
        client = await self._get_client(token)
        return await get_community_topology_admin_communities_community_key_topology_get.asyncio_detailed(
            client=client,
            community_key=community_key,
        )

    async def get_asset(
        self, community_key: str, asset_key: str, *, token: Optional[str] = None
    ) -> Any:
        """Get asset details."""
        client = await self._get_client(token)
        return await get_asset_admin_communities_community_key_assets_asset_key_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            asset_key=asset_key,
        )

    async def get_asset_by_sensor_id(
        self, community_key: str, sensor_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Get asset by sensor ID."""
        client = await self._get_client(token)
        return await get_asset_by_sensor_id_admin_communities_community_key_assets_by_sensor_id_sensor_id_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            sensor_id=sensor_id,
        )

    async def get_member(
        self, community_key: str, member_key: str, *, token: Optional[str] = None
    ) -> Any:
        """Get member details."""
        client = await self._get_client(token)
        return await get_member_admin_communities_community_key_members_member_key_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            member_key=member_key,
        )

    async def get_member_by_user_id(
        self, community_key: str, user_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Get member by user ID."""
        client = await self._get_client(token)
        return await get_member_by_user_id_admin_communities_community_key_members_by_user_id_user_id_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            user_id=user_id,
        )

    async def get_member_delivery_points(
        self, community_key: str, member_key: str, *, token: Optional[str] = None
    ) -> DeliveryPointsResponseSchema | None:
        """Get member's delivery points."""
        client = await self._get_client(token)
        res = await get_member_delivery_points_admin_communities_community_key_members_member_key_delivery_points_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            member_key=member_key,
        )
        return to_schema(res.parsed, DeliveryPointsResponseSchema)

    async def get_delivery_point_by_id(
        self, community_key: str, dp_id: str, *, token: Optional[str] = None
    ) -> DeliveryPointLookupSchema | None:
        """Get delivery point by ID."""
        client = await self._get_client(token)
        res = await get_delivery_point_by_id_admin_communities_community_key_delivery_points_by_id_dp_id_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            dp_id=dp_id,
        )
        return to_schema(res.parsed, DeliveryPointLookupSchema)

    # Lookup operations (cross-community queries)
    async def lookup_community_by_user_id(
        self, user_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Find community for a user ID."""
        client = await self._get_client(token)
        res = await lookup_community_by_user_id.asyncio_detailed(
            client=client,
            user_id=user_id,
        )
        return to_schema(res.parsed, LookupBySensorIdResponseSchema)

    async def lookup_community_by_sensor_id(
        self, sensor_id: str, *, token: Optional[str] = None
    ) -> LookupByUserIdResponseSchema | None:
        """Find community for a sensor ID."""
        client = await self._get_client(token)
        res = await lookup_community_by_sensor_id.asyncio_detailed(
            client=client,
            sensor_id=sensor_id,
        )
        return to_schema(res.parsed, LookupByUserIdResponseSchema)

    async def lookup_community_by_delivery_point(
        self, dp_id: str, *, token: Optional[str] = None
    ) -> LookupByDeliveryPointResponseSchema | None:
        """Find community for a delivery point ID."""
        client = await self._get_client(token)
        res = await lookup_community_by_delivery_point.asyncio_detailed(
            client=client,
            dp_id=dp_id,
        )
        return to_schema(res.parsed, LookupByDeliveryPointResponseSchema)

    async def lookup_asset_by_sensor_id(
        self, sensor_id: str, *, token: Optional[str] = None
    ) -> GlobalAssetLookupSchema | None:
        """Find asset for a sensor ID."""
        client = await self._get_client(token)
        res = await lookup_asset_by_sensor_id.asyncio_detailed(
            client=client,
            sensor_id=sensor_id,
        )
        return to_schema(res.parsed, GlobalAssetLookupSchema)

    async def lookup_member_by_user_id(
        self, user_id: str, *, token: Optional[str] = None
    ) -> GlobalMemberLookupSchema | None:
        """Find member for a user ID."""
        client = await self._get_client(token)
        res = await lookup_member_by_user_id.asyncio_detailed(
            client=client,
            user_id=user_id,
        )
        return to_schema(res.parsed, GlobalMemberLookupSchema)

    async def _batch_lookup(
        self,
        ids: list[str],
        *,
        route: str,
        request: Callable[[list[str]], Any],
        call: Callable[..., Awaitable[Any]],
        schema: type,
        token: Optional[str],
    ) -> list[Any]:
        """Run one batch lookup, in requests of at most the route's bound.

        Chunking is invisible to the caller: the bound is a property of the
        route rather than something the caller did wrong. Rows arrive in
        request order, and an empty input sends nothing.

        Anything that is not a `200` raises. On all three of these routes an
        empty list is a *meaningful* answer — "none of these ids matched", and,
        deliberately, "that member holds nothing" — so returning `[]` for a
        refusal makes a denial indistinguishable from a result, in the
        direction that loses data quietly.

        `schema` is a parameter rather than a fixed `GlobalAssetLookupSchema`
        because the DID batch answers **members**, not assets: onboarding writes
        a participant's supply point onto the member and registers no asset
        until a meter is physically installed, so an asset-shaped answer would
        be empty for exactly the population a consent-gated export covers.
        """
        found: list[Any] = []
        for start in range(0, len(ids), MAX_BATCH_LOOKUP_IDS):
            chunk = ids[start : start + MAX_BATCH_LOOKUP_IDS]
            client = await self._get_client(token)
            res = await call(client=client, body=request(chunk))
            if not isinstance(res.parsed, list):
                raise RecRegistryApiError(
                    f"{route} refused a batch of {len(chunk)} ids "
                    f"(status={res.status_code})",
                    status_code=res.status_code,
                    body=res.content,
                )
            found.extend(schema.model_validate(item.to_dict()) for item in res.parsed)
        return found

    async def lookup_assets_by_sensor_ids(
        self, sensor_ids: list[str], *, token: Optional[str] = None
    ) -> list[GlobalAssetLookupSchema]:
        """Find the assets behind a set of sensor ids, across all communities.

        The mirror of :meth:`lookup_assets_by_user_ids`: this one starts from a
        device and finds its owner, that one starts from owners and finds their
        devices.

        A sensor id matching nothing contributes no row rather than failing the
        request. More than `MAX_BATCH_LOOKUP_IDS` ids are split across as many
        requests as it takes; a refused request raises `RecRegistryApiError`
        rather than answering an empty list.
        """
        return await self._batch_lookup(
            sensor_ids,
            route="assets-by-sensor-ids",
            request=lambda chunk: SensorIdsBatchRequest(sensor_ids=chunk),
            call=_lookup_assets_by_sensor_ids.asyncio_detailed,
            schema=GlobalAssetLookupSchema,
            token=token,
        )

    async def lookup_asset_by_sensor_ids(
        self, sensor_ids: list[str], *, token: Optional[str] = None
    ) -> list[GlobalAssetLookupSchema]:
        """Deprecated alias for :meth:`lookup_assets_by_sensor_ids`.

        The singular `asset` did not match its mirror and left the
        cross-reference between the two unresolvable. Kept because
        `digital-twin` calls this name: dropping it would have failed there at
        runtime rather than at build time.
        """
        return await self.lookup_assets_by_sensor_ids(sensor_ids, token=token)

    # ── Writes ────────────────────────────────────────────────────────────
    #
    # These call the same endpoints as the CLI and the console. Responses are
    # returned undecoded (`asyncio_detailed`) so a caller can act on the status
    # — a 409 from `create_member` means "already there, switch to patch", which
    # is a normal outcome for a service that retries, not an error.

    async def create_member(
        self,
        community_key: str,
        body: MemberCreate,
        *,
        token: Optional[str] = None,
    ) -> Any:
        """Create one member, with its delivery points and assets.

        `409` when the key or `user_id` is already taken; `404` for an unknown
        community. Requires `rec-registry.members.write`.
        """
        client = await self._get_client(token)
        return await _create_member.asyncio_detailed(
            community_key=community_key, client=client, body=body
        )

    async def patch_member(
        self,
        community_key: str,
        member_key: str,
        body: MemberPatch,
        *,
        token: Optional[str] = None,
    ) -> Any:
        """Partially update a member. Absent fields are left alone."""
        client = await self._get_client(token)
        return await _patch_member.asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            client=client,
            body=body,
        )

    async def change_member_status(
        self,
        community_key: str,
        member_key: str,
        body: MemberStatusChange,
        *,
        token: Optional[str] = None,
    ) -> Any:
        """Move a member through `pending → active → suspended → inactive`."""
        client = await self._get_client(token)
        return await _change_member_status.asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            client=client,
            body=body,
        )

    async def delete_member(
        self,
        community_key: str,
        member_key: str,
        *,
        purge: bool = False,
        token: Optional[str] = None,
    ) -> Any:
        """Deactivate a member, or erase one.

        `purge=True` removes the member and its assets permanently and needs the
        separate `rec-registry.members.purge` grant. The default deactivates,
        which is reversible.
        """
        client = await self._get_client(token)
        return await _delete_member.asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            client=client,
            purge=purge,
        )

    async def upsert_delivery_point(
        self,
        community_key: str,
        member_key: str,
        point_id: str,
        body: DeliveryPointIn,
        *,
        token: Optional[str] = None,
    ) -> Any:
        """Add or replace one supply point, keeping the member's others."""
        client = await self._get_client(token)
        return await _upsert_delivery_point.asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            point_id=point_id,
            client=client,
            body=body,
        )

    async def upsert_asset(
        self,
        community_key: str,
        member_key: str,
        asset_key: str,
        body: AssetUpsert,
        *,
        token: Optional[str] = None,
    ) -> Any:
        """Create or replace one asset, keeping the member's others.

        Returns the undecoded response, `409` included. For a write whose
        refusal is an answer to show someone, use :meth:`put_asset`.
        """
        client = await self._get_client(token)
        return await _upsert_asset.asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            asset_key=asset_key,
            client=client,
            body=body,
        )

    # ── Writes that raise with the registry's code ───────────────────────
    #
    # Unlike the writes above, these parse success into a schema and raise
    # `RecRegistryApiError` on anything else, carrying the registry's refusal
    # `code` (`sensor_held`, `asset_key_taken`, ...). They are for callers to
    # whom a refusal is an answer to show a person — the community dashboard
    # attaching and detaching a member's meter, or correcting a member's role
    # and area — rather than a branch in a retry loop.
    #
    # They send through the generated request builder (`_get_kwargs`), so the
    # path, quoting and body stay generated, and read the response here: the
    # generated `_parse_response` raises `UnexpectedStatus` on an undeclared
    # status (a `403` from the policy middleware) and maps `code` onto a
    # generated enum, and neither may reach the caller.

    @staticmethod
    async def _send(
        client: AuthenticatedClient, kwargs: dict[str, Any]
    ) -> httpx.Response:
        return await client.get_async_httpx_client().request(**kwargs)

    @staticmethod
    def _refused(response: httpx.Response, what: str) -> RecRegistryApiError:
        return _refused(response, what)

    async def put_asset(
        self,
        community_key: str,
        member_key: str,
        asset_key: str,
        body: AssetUpsert | Mapping[str, Any],
        *,
        token: Optional[str] = None,
    ) -> AssetDetailSchema:
        """Write one asset of one member; the way a manager attaches a meter.

        Sends `PUT /admin/communities/{community_key}/members/{member_key}/assets/{asset_key}`
        with exactly the key and body given. Nothing is composed or normalised
        here: the `meter-<sensor_id>` key convention and the trimmed sensor-id
        comparison are the registry's, so the caller passes the asset key and
        the body's `key` as the registry expects them.

        Answers the stored asset as the generated :class:`AssetDetailSchema` —
        the shape the asset `GET` answers (registry 1.6.0 declares it on the
        `PUT` too). A key the registry adds later is ignored, not refused.
        Writing an asset the member already holds, with the same body, answers
        it too — the registry treats that as a no-op, and so does this.

        Anything but `200` raises :class:`RecRegistryApiError`; branch on its
        `code`: `sensor_held` (`409`, another active member in any community
        holds the sensor), `asset_key_taken` (`409`), `member_not_found` or
        `community_not_found` (`404`), `asset_key_too_long` (`422`, a key over
        the registry's 128 characters); `None` for a validation `422` or a
        missing grant (`403`). Needs `rec-registry.assets.write`.
        """
        payload = (
            body if isinstance(body, AssetUpsert) else AssetUpsert.from_dict(body)
        )
        client = await self._get_client(token)
        response = await self._send(
            client,
            _upsert_asset._get_kwargs(
                community_key=community_key,
                member_key=member_key,
                asset_key=asset_key,
                body=payload,
            ),
        )
        if response.status_code != HTTPStatus.OK:
            raise self._refused(response, "put-asset")
        try:
            return AssetDetailSchema.model_validate(response.json())
        except ValueError as exc:
            raise RecRegistryApiError(
                "put-asset: rec-registry answered 200 with nothing readable",
                status_code=response.status_code,
                body=response.content,
            ) from exc

    async def delete_asset(
        self,
        community_key: str,
        member_key: str,
        asset_key: str,
        *,
        token: Optional[str] = None,
    ) -> None:
        """Delete one asset of one member; the way a manager detaches a meter.

        A hard delete of that one asset (the registry keeps no dated holding);
        the member's other assets are untouched. Answers nothing on `204`.

        Anything else raises :class:`RecRegistryApiError` — **including a
        `404` for an asset the member does not hold** (`code`
        `asset_not_found`, or `member_not_found` for the member). The wrapper
        does not read that as "already detached": whether it is success is the
        caller's decision. Needs `rec-registry.assets.write`.
        """
        client = await self._get_client(token)
        response = await self._send(
            client,
            _delete_asset._get_kwargs(
                community_key=community_key,
                member_key=member_key,
                asset_key=asset_key,
            ),
        )
        if response.status_code != HTTPStatus.NO_CONTENT:
            raise self._refused(response, "delete-asset")

    async def patch_member_profile(
        self,
        community_key: str,
        member_key: str,
        *,
        role: Optional[str] = None,
        area: Optional[str] = None,
        token: Optional[str] = None,
    ) -> MemberDetailSchema:
        """Correct one member's role and area; the way a manager edits a member.

        Sends `PATCH /admin/communities/{community_key}/members/{member_key}/profile`
        with a body of only the keys given, out of `role` and `area`. A key left
        at `None` is omitted, never sent as `null`; there is no parameter for
        any other member field, so `user_id`, `did`, `status` and the rest
        cannot be sent from here. It never falls back to the general member
        `PATCH`, which needs `rec-registry.members.write` — a grant that can
        rewrite a member's identity and status.

        Calling it with neither raises :class:`ValueError` without sending
        anything: the registry refuses an empty body, with no code to show.

        Values are passed as given: which roles a caller may set (the
        dashboard allows only consumer and prosumer) is the caller's rule, and
        the role and area sets are the registry's.

        Answers the updated member as the generated :class:`MemberDetailSchema`.
        Anything but `200` raises :class:`RecRegistryApiError`; branch on its
        `code`: `invalid_role` or `unknown_area` (`422`), `member_not_found` or
        `community_not_found` (`404`); `None` for a validation `422` or a
        missing grant (`403`). Needs `rec-registry.members.profile.write`
        (`rec-registry.members.write` and `rec-registry.admin` also satisfy it).
        """
        if role is None and area is None:
            raise ValueError("patch_member_profile needs a role, an area, or both")
        payload = MemberProfilePatch(
            role=UNSET if role is None else role,
            area=UNSET if area is None else area,
        )
        client = await self._get_client(token)
        response = await self._send(
            client,
            _patch_member_profile._get_kwargs(
                community_key=community_key,
                member_key=member_key,
                body=payload,
            ),
        )
        if response.status_code != HTTPStatus.OK:
            raise self._refused(response, "patch-member-profile")
        try:
            return MemberDetailSchema.model_validate(response.json())
        except ValueError as exc:
            raise RecRegistryApiError(
                "patch-member-profile: rec-registry answered 200 with nothing readable",
                status_code=response.status_code,
                body=response.content,
            ) from exc

    # ── Areas and topology: the onboarding template sync ────────────────
    #
    # Onboarding owns a community's areas (its templates) and writes them to
    # the registry: each substation as one topology node, then the area that
    # references it. The sync's refusals are answers it reports to an admin
    # (`invalid_area_boundary`, `area_in_use`, `topology_node_in_use`,
    # `community_not_found`), so these follow the raising helpers above: a
    # schema on success, `RecRegistryApiError` with the registry's `code` on
    # anything else. Every write answers the whole community, as the registry
    # does, so the caller sees the areas and nodes it did not touch.

    @staticmethod
    def _community_answer(
        response: httpx.Response, what: str
    ) -> CommunityDetailSchema:
        return _answer(response, CommunityDetailSchema, what)

    async def read_community(
        self, community_key: str, *, token: Optional[str] = None
    ) -> CommunityDetailSchema:
        """Read one community, its areas and its topology, or raise.

        Sends `GET /admin/communities/{community_key}` and answers the
        generated :class:`CommunityDetailSchema` — `areas` (each with its
        `boundary` and `topology`) and `topology` (each node's `id`, `type`,
        `name`, `operator_id`, `parent`). This is the read a sync compares a
        template against, and the drift check with it.

        Unlike :meth:`get_community`, which answers the undecoded response
        and raises the generated `UnexpectedStatus` on an undeclared status,
        anything but `200` raises :class:`RecRegistryApiError` — a missing
        community included (`404`; this route names no `code` for it and does
        not declare it), so it is never read as a community with no areas.
        Needs the registry's `read` action (`rec-registry.read`).
        """
        client = await self._get_client(token)
        response = await self._send(
            client,
            get_community_admin_communities_community_key_get._get_kwargs(
                community_key=community_key
            ),
        )
        return self._community_answer(response, "read-community")

    async def put_area(
        self,
        community_key: str,
        area_key: str,
        body: AreaUpsert | Mapping[str, Any],
        *,
        token: Optional[str] = None,
    ) -> CommunityDetailSchema:
        """Add or replace one area of a community, keeping the others.

        Sends `PUT /admin/communities/{community_key}/areas/{area_key}` with
        the body as given — `{name, boundary: {source, id}, topology: [id]}` —
        and nothing added: the one-substation rule is the registry's, and it
        is judged there. The node the area lists must already be in the
        community's topology (:meth:`put_topology_node` first).

        Answers the whole community. Anything but `200` raises
        :class:`RecRegistryApiError`; branch on its `code`:
        `invalid_area_boundary` (`422`), `community_not_found` (`404`);
        `None` for a validation `422` or a missing grant (`403`). Needs
        `rec-registry.community.write`.
        """
        payload = body if isinstance(body, AreaUpsert) else AreaUpsert.from_dict(body)
        client = await self._get_client(token)
        response = await self._send(
            client,
            _upsert_area._get_kwargs(
                community_key=community_key, area_key=area_key, body=payload
            ),
        )
        return self._community_answer(response, "put-area")

    async def delete_area(
        self,
        community_key: str,
        area_key: str,
        *,
        token: Optional[str] = None,
    ) -> CommunityDetailSchema:
        """Delete one area of a community, unless members still reference it.

        Sends `DELETE /admin/communities/{community_key}/areas/{area_key}`
        and answers the whole community. A refusal raises
        :class:`RecRegistryApiError`: `area_in_use` (`409`, members reference
        the area — the registry's sentence names how many, and the wrapper
        does not parse it), `community_not_found` (`404`), and a `404` with no
        code for an area the community does not have, which is not read as
        "already deleted": whether that is success is the caller's decision.
        Needs `rec-registry.community.write`.
        """
        client = await self._get_client(token)
        response = await self._send(
            client,
            _delete_area._get_kwargs(community_key=community_key, area_key=area_key),
        )
        return self._community_answer(response, "delete-area")

    async def rename_area(
        self,
        community_key: str,
        area_key: str,
        new_key: str,
        *,
        token: Optional[str] = None,
    ) -> AreaRenamedSchema:
        """Move one area to a new key, with the members that reference it.

        Sends `POST /admin/communities/{community_key}/areas/{area_key}/rename`
        with a body of only `{"new_key": new_key}`. The registry moves the
        area as stored (name, boundary, topology) and every member of the
        community whose `area` is `area_key`, of any status, in one write; the
        wrapper sends nothing else and does not follow up with a `PUT` or a
        `DELETE` of its own. This is how a template sync renames an area whose
        substation the registry holds under another key: a `PUT` under the new
        key is refused (one area per boundary) and the old key cannot be
        deleted while members hold it.

        Answers the generated :class:`AreaRenamedSchema` — `old_key`,
        `new_key`, `members_moved` and the whole community after the rename.
        Anything but `200` raises :class:`RecRegistryApiError`; branch on its
        `code`: `invalid_area_key` (`422`, `new_key` is not an area key),
        `area_not_found` (`404`), `area_key_taken` (`409`, `new_key` already
        exists, the old key included), `community_not_found` (`404`); `None`
        for a validation `422` or a missing grant (`403`). The key pattern is
        the registry's and is not checked here. Needs
        `rec-registry.community.write`.
        """
        client = await self._get_client(token)
        response = await self._send(
            client,
            _rename_area._get_kwargs(
                community_key=community_key,
                area_key=area_key,
                body=AreaRename(new_key=new_key),
            ),
        )
        return _answer(response, AreaRenamedSchema, "rename-area")

    async def put_topology_node(
        self,
        community_key: str,
        node_id: str,
        body: TopologyNodeIn | Mapping[str, Any],
        *,
        token: Optional[str] = None,
    ) -> CommunityDetailSchema:
        """Add or replace one topology node of a community, keeping the others.

        Sends `PUT /admin/communities/{community_key}/topology/{node_id}` with
        the body as given — `{id, type, name?, operator_id?, parent?}`. The
        registry merges by `id` and refuses a body `id` that differs from the
        path; the wrapper does not fill one from the other.

        Answers the whole community. Anything but `200` raises
        :class:`RecRegistryApiError`; branch on its `code`:
        `invalid_area_boundary` (`422`, the write would change the `type` of
        a node an area relies on), `community_not_found` (`404`); `None` for a
        validation `422` (a body `id` that is not the path's, among others) or
        a missing grant (`403`). Needs `rec-registry.community.write`.
        """
        payload = (
            body if isinstance(body, TopologyNodeIn) else TopologyNodeIn.from_dict(body)
        )
        client = await self._get_client(token)
        response = await self._send(
            client,
            _upsert_topology_node._get_kwargs(
                community_key=community_key, node_id=node_id, body=payload
            ),
        )
        return self._community_answer(response, "put-topology-node")

    async def delete_topology_node(
        self,
        community_key: str,
        node_id: str,
        *,
        token: Optional[str] = None,
    ) -> CommunityDetailSchema:
        """Delete one topology node, unless an area still lists it.

        Sends `DELETE /admin/communities/{community_key}/topology/{node_id}`
        and answers the whole community. A refusal raises
        :class:`RecRegistryApiError`: `topology_node_in_use` (`409`, the
        registry's sentence names the areas), `community_not_found` (`404`),
        and a `404` with no code for a node the community does not have —
        not read as "already deleted". Needs `rec-registry.community.write`.
        """
        client = await self._get_client(token)
        response = await self._send(
            client,
            _delete_topology_node._get_kwargs(
                community_key=community_key, node_id=node_id
            ),
        )
        return self._community_answer(response, "delete-topology-node")

    async def lookup_assets_by_user_ids(
        self,
        user_ids: list[str],
        *,
        token: Optional[str] = None,
    ) -> list[GlobalAssetLookupSchema]:
        """Find assets owned by multiple members, across all communities.

        The mirror of :meth:`lookup_assets_by_sensor_ids`: that one starts from
        a device and finds its owner, this one starts from owners and finds
        their devices.

        Used where access is granted for a *set of people* rather than for the
        caller — a dataspace query authorised by the subjects who consented. The
        self-service route (``get_my_assets``) cannot answer that, because it
        resolves the member from the caller's own token.

        Requires ``rec-registry.lookup``. Returns an empty list for members that
        do not exist or own nothing; the two are deliberately indistinguishable.
        A *refused* request is not a third member of that set — it raises
        `RecRegistryApiError`.

        More than `MAX_BATCH_LOOKUP_IDS` ids are split across as many requests
        as it takes, and the rows are concatenated in request order.
        """
        return await self._batch_lookup(
            user_ids,
            route="assets-by-user-ids",
            request=lambda chunk: UserIdsBatchRequest(user_ids=chunk),
            call=_lookup_assets_by_user_ids.asyncio_detailed,
            schema=GlobalAssetLookupSchema,
            token=token,
        )

    async def lookup_members_by_dids(
        self,
        dids: list[str],
        *,
        token: Optional[str] = None,
    ) -> list[GlobalMemberLookupSchema]:
        """Find the members holding a set of dataspace DIDs, across communities.

        The join between the connector's answer to *who consented* — stated in
        DIDs — and the registry's answer to *what they hold*. Resolving a DID
        through the identity registry to a Keycloak user id does not close that
        gap: `Member.user_id` holds a Keycloak *username*, so the identifier
        that hop returns matches no row.

        **Answers members, not assets**, and the difference matters in the
        common case. Onboarding writes a participant's declared supply point
        onto `Member.delivery_points` and registers no asset, because a meter's
        `sensor_id` is assigned at physical installation — so every row carries
        `delivery_points`, and an asset-shaped answer would be empty for every
        participant whose meter is not yet commissioned. A commissioned meter
        stays reachable through :meth:`lookup_assets_by_user_ids` and the
        `user_id` in the same row.

        Every row carries its `did`, which is what lets the caller attribute it
        back to the DID it asked about.

        Requires ``rec-registry.lookup``. A DID belonging to nobody and a member
        holding no supply points are deliberately indistinguishable — both
        contribute no row, and neither is a `404`. A *refused* request is not a
        third member of that set: it raises `RecRegistryApiError`.

        More than `MAX_BATCH_LOOKUP_IDS` dids are split across as many requests
        as it takes, and the rows are concatenated in request order.
        """
        return await self._batch_lookup(
            dids,
            route="members-by-dids",
            request=lambda chunk: DidsBatchRequest(dids=chunk),
            call=_lookup_members_by_dids.asyncio_detailed,
            schema=GlobalMemberLookupSchema,
            token=token,
        )
