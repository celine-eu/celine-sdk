"""REC Registry API wrapper.

Reusable client design for multi-tenant/per-request scenarios.
Initialize once, pass tokens per-call - no client recreation overhead.
"""

from __future__ import annotations

from typing import Any, Optional

import httpx

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
    lookup_assets_by_sensor_ids,
    lookup_assets_by_user_ids,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    change_member_status_admin_communities_community_key_members_member_key_status_post as _change_member_status,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    create_member_admin_communities_community_key_members_post as _create_member,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    delete_member_admin_communities_community_key_members_member_key_delete as _delete_member,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    patch_member_admin_communities_community_key_members_member_key_patch as _patch_member,
)
from celine.sdk.openapi.rec_registry.api.admin import (
    upsert_asset_admin_communities_community_key_members_member_key_assets_asset_key_put as _upsert_asset,
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
    AssetUpsert,
    DeletionReport,
    DeliveryPointIn,
    HTTPValidationError,
    MemberCreate,
    MemberDetail,
    MemberPatch,
    MemberStatusChange,
    MultiImportReport,
    UserAssetsResponse,
    UserCommunityDetail,
    UserMeResponse,
    UserMemberDetail,
    UserDeliveryPointsResponse,
    UserAssetDetail,
    SensorIdsBatchRequest,
    UserIdsBatchRequest,
)

from celine.sdk.openapi.rec_registry.models.global_asset_lookup import GlobalAssetLookup
from celine.sdk.openapi.rec_registry.models.global_member_lookup import GlobalMemberLookup
from celine.sdk.utils.convert import to_schema

from celine.sdk.openapi.rec_registry.schemas import (
    DeliveryPointLookupSchema,
    DeliveryPointsResponseSchema,
    GlobalAssetLookupSchema,
    GlobalMemberLookupSchema,
    HTTPValidationErrorSchema,
    LookupByDeliveryPointResponseSchema,
    LookupBySensorIdResponseSchema,
    LookupByUserIdResponseSchema,
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
]


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

    async def get_my_community(
        self, *, token: Optional[str] = None
    ) -> UserCommunityDetailSchema | None:
        """Get user's community details."""
        client = self._get_client(token)
        res = await get_my_community_user_community_get.asyncio_detailed(client=client)
        return to_schema(res.parsed, UserCommunityDetailSchema)

    async def get_my_member(
        self, *, token: Optional[str] = None
    ) -> UserMemberDetailSchema | None:
        """Get user's member details."""
        client = self._get_client(token)
        res = await get_my_member_user_member_get.asyncio_detailed(client=client)
        return to_schema(res.parsed, UserMemberDetailSchema)

    async def get_my_assets(
        self, *, token: Optional[str] = None
    ) -> UserAssetsResponseSchema | None:
        """List all assets owned by the user."""
        client = self._get_client(token)
        res = await get_my_assets_user_assets_get.asyncio_detailed(client=client)
        if isinstance(res.parsed, HTTPValidationError):
            raise Exception(res.parsed)
        return to_schema(res.parsed, UserAssetsResponseSchema)

    async def get_my_asset(
        self, asset_key: str, *, token: Optional[str] = None
    ) -> UserAssetDetailSchema | None:
        """Get specific asset owned by the user."""
        client = self._get_client(token)
        res = await get_my_asset_user_assets_asset_key_get.asyncio_detailed(
            client=client,
            asset_key=asset_key,
        )

        if isinstance(res.parsed, HTTPValidationError):
            raise Exception(res.parsed)

        return to_schema(res.parsed, UserAssetDetailSchema)

    async def get_my_delivery_points(
        self, *, token: Optional[str] = None
    ) -> UserDeliveryPointsResponseSchema | None:
        """Get user's delivery points."""
        client = self._get_client(token)

        res = await get_my_delivery_points_user_delivery_points_get.asyncio_detailed(
            client=client
        )

        return to_schema(res.parsed, UserDeliveryPointsResponseSchema)


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
        if isinstance(res.parsed, HTTPValidationError):
            raise Exception(res.parsed)
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
    
    async def lookup_asset_by_sensor_ids(
        self, sensor_ids: list[str], *, token: Optional[str] = None
    ) -> list[GlobalAssetLookupSchema]:
        """Find assets by multiple sensor IDs."""
        client = await self._get_client(token)
        res = await lookup_assets_by_sensor_ids.asyncio_detailed(
            client=client,
            body=SensorIdsBatchRequest(sensor_ids=sensor_ids),
        )
        if not isinstance(res.parsed, list):
            return []
        return [
            GlobalAssetLookupSchema.model_validate(item.to_dict())
            for item in res.parsed
        ]

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
        """Create or replace one asset, keeping the member's others."""
        client = await self._get_client(token)
        return await _upsert_asset.asyncio_detailed(
            community_key=community_key,
            member_key=member_key,
            asset_key=asset_key,
            client=client,
            body=body,
        )

    async def lookup_assets_by_user_ids(
        self,
        user_ids: list[str],
        *,
        token: Optional[str] = None,
    ) -> list[GlobalAssetLookupSchema]:
        """Find assets owned by multiple members, across all communities.

        The mirror of :meth:`lookup_assets_by_sensor_ids`: that starts from a
        device and finds its owner, this starts from owners and finds their
        devices.

        Used where access is granted for a *set of people* rather than for the
        caller — a dataspace query authorised by the subjects who consented. The
        self-service route (``get_my_assets``) cannot answer that, because it
        resolves the member from the caller's own token.

        Requires ``rec-registry.lookup``. Returns an empty list for members that
        do not exist or own nothing; the two are deliberately indistinguishable.
        """
        client = await self._get_client(token)
        res = await lookup_assets_by_user_ids.asyncio_detailed(
            client=client,
            body=UserIdsBatchRequest(user_ids=user_ids),
        )
        if not isinstance(res.parsed, list):
            return []
        return [
            GlobalAssetLookupSchema.model_validate(item.to_dict())
            for item in res.parsed
        ]