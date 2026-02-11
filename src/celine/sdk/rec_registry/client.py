"""REC Registry API wrapper.

Reusable client design for multi-tenant/per-request scenarios.
Initialize once, pass tokens per-call - no client recreation overhead.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import httpx

from celine.sdk.auth import TokenProvider
from celine.sdk.openapi.rec_registry import AuthenticatedClient, Client
from celine.sdk.openapi.rec_registry.api.admin import (
    admin_export_admin_export_get,
    admin_import_admin_import_post,
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
    lookup_asset_by_sensor_id_admin_lookup_asset_by_sensor_id_sensor_id_get,
    lookup_community_by_delivery_point_admin_lookup_community_by_delivery_point_dp_id_get,
    lookup_community_by_sensor_id_admin_lookup_community_by_sensor_id_sensor_id_get,
    lookup_community_by_user_id_admin_lookup_community_by_user_id_user_id_get,
    lookup_member_by_user_id_admin_lookup_member_by_user_id_user_id_get,
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
    HTTPValidationError,
    UserAssetsResponse,
    UserCommunityDetail,
    UserMeResponse,
    UserMemberDetail,
    ImportRequest,
    UserDeliveryPointsResponse,
    UserAssetDetail,
)

from celine.sdk.utils.convert import to_schema

from celine.sdk.openapi.rec_registry.schemas import (
    HTTPValidationErrorSchema,
    UserAssetsResponseSchema,
    UserCommunityDetailSchema,
    UserMeResponseSchema,
    UserMemberDetailSchema,
    ImportRequestSchema,
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
    async def export_community(
        self, community_key: str, *, token: Optional[str] = None
    ) -> str:
        """Export community data as YAML."""
        client = await self._get_client(token)
        res = await admin_export_admin_export_get.asyncio_detailed(
            client=client,
            community=community_key,
        )
        if isinstance(res.parsed, HTTPValidationError):
            raise Exception(res.parsed)
        return str(res.parsed)

    async def import_community(
        self, yaml_data: str, *, token: Optional[str] = None
    ) -> Any:
        """Import community data from YAML."""
        client = await self._get_client(token)
        return await admin_import_admin_import_post.asyncio_detailed(
            client=client,
            body=ImportRequest(bundle=json.loads(yaml_data)),
        )

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
    ) -> Any:
        """Get member's delivery points."""
        client = await self._get_client(token)
        return await get_member_delivery_points_admin_communities_community_key_members_member_key_delivery_points_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            member_key=member_key,
        )

    async def get_delivery_point_by_id(
        self, community_key: str, dp_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Get delivery point by ID."""
        client = await self._get_client(token)
        return await get_delivery_point_by_id_admin_communities_community_key_delivery_points_by_id_dp_id_get.asyncio_detailed(
            client=client,
            community_key=community_key,
            dp_id=dp_id,
        )

    # Lookup operations (cross-community queries)
    async def lookup_community_by_user_id(
        self, user_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Find community for a user ID."""
        client = await self._get_client(token)
        return await lookup_community_by_user_id_admin_lookup_community_by_user_id_user_id_get.asyncio_detailed(
            client=client,
            user_id=user_id,
        )

    async def lookup_community_by_sensor_id(
        self, sensor_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Find community for a sensor ID."""
        client = await self._get_client(token)
        return await lookup_community_by_sensor_id_admin_lookup_community_by_sensor_id_sensor_id_get.asyncio_detailed(
            client=client,
            sensor_id=sensor_id,
        )

    async def lookup_community_by_delivery_point(
        self, dp_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Find community for a delivery point ID."""
        client = await self._get_client(token)
        return await lookup_community_by_delivery_point_admin_lookup_community_by_delivery_point_dp_id_get.asyncio_detailed(
            client=client,
            dp_id=dp_id,
        )

    async def lookup_asset_by_sensor_id(
        self, sensor_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Find asset for a sensor ID."""
        client = await self._get_client(token)
        return await lookup_asset_by_sensor_id_admin_lookup_asset_by_sensor_id_sensor_id_get.asyncio_detailed(
            client=client,
            sensor_id=sensor_id,
        )

    async def lookup_member_by_user_id(
        self, user_id: str, *, token: Optional[str] = None
    ) -> Any:
        """Find member for a user ID."""
        client = await self._get_client(token)
        return await lookup_member_by_user_id_admin_lookup_member_by_user_id_user_id_get.asyncio_detailed(
            client=client,
            user_id=user_id,
        )
