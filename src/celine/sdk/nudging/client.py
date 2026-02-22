"""Nudging API wrapper.

Reusable client design for multi-tenant/per-request scenarios.
Initialize once, pass tokens per-call - no client recreation overhead.
"""

from __future__ import annotations

from typing import Optional

import httpx

from celine.sdk.auth import TokenProvider
from celine.sdk.openapi.nudging import AuthenticatedClient, Client
from celine.sdk.openapi.nudging.api.notifications import (
    list_notifications_notifications_get,
    mark_read_notifications_notification_id_put,
    soft_delete_notification_notifications_notification_id_delete,
)
from celine.sdk.openapi.nudging.api.webpush import (
    subscribe_webpush_subscribe_post,
    unsubscribe_webpush_unsubscribe_post,
    vapid_public_key_webpush_vapid_public_key_get,
)
from celine.sdk.openapi.nudging.api.admin import (
    admin_list_notifications_admin_notifications_get,
    ingest_event_admin_ingest_event_post,
    send_test_admin_webpush_send_test_post,
)
from celine.sdk.openapi.nudging.models import (
    DigitalTwinEvent,
    SendTestRequest,
    SubscribeRequest,
    UnsubscribeRequest,
)
from celine.sdk.openapi.nudging.models.http_validation_error import HTTPValidationError
from celine.sdk.openapi.nudging.schemas import (
    AdminNotificationOutSchema,
    IngestAcceptedResponseSchema,
    IngestOkResponseSchema,
    IngestErrorDetailSchema,
    NotificationOutSchema,
    SendTestResponseSchema,
    StatusResponseSchema,
    VapidPublicKeyResponseSchema,
)
from celine.sdk.openapi.nudging.types import UNSET, Unset
from celine.sdk.utils.convert import to_client, to_schema

__all__ = [
    "NudgingClient",
    "NudgingAdminClient",
]


class NudgingClient:
    """User-facing nudging client.

    Covers:
    - GET  /notifications               - list caller's notifications
    - PUT  /notifications/{id}          - mark a notification as read
    - DELETE /notifications/{id}        - soft-delete a notification
    - GET  /webpush/vapid-public-key    - fetch VAPID public key (unauthenticated)
    - POST /webpush/subscribe           - register a push subscription
    - POST /webpush/unsubscribe         - remove a push subscription
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
        self._base_client = Client(
            base_url=base_url,
            timeout=self._timeout,
            verify_ssl=verify_ssl,
            raise_on_unexpected_status=True,
        )

    def _get_client(self, token: Optional[str]) -> AuthenticatedClient:
        """Return an authenticated client for this request."""
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

    # ------------------------------------------------------------------ #
    # Notifications                                                        #
    # ------------------------------------------------------------------ #

    async def list_notifications(
        self,
        *,
        limit: int | Unset = 50,
        offset: int | Unset = 0,
        unread_only: bool | Unset = False,
        token: Optional[str] = None,
    ) -> list[NotificationOutSchema]:
        """Return the caller's notifications, newest-first."""
        client = self._get_client(token)
        res = await list_notifications_notifications_get.asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            unread_only=unread_only,
        )

        if isinstance(res.parsed, HTTPValidationError):
            raise Exception(HTTPValidationError)

        items = res.parsed or []
        return [to_schema(item, NotificationOutSchema) for item in items]

    async def mark_read(
        self,
        notification_id: str,
        *,
        token: Optional[str] = None,
    ) -> NotificationOutSchema | None:
        """Mark a notification as read. Idempotent."""
        client = self._get_client(token)
        res = await mark_read_notifications_notification_id_put.asyncio_detailed(
            notification_id=notification_id,
            client=client,
        )
        return to_schema(res.parsed, NotificationOutSchema)

    async def delete_notification(
        self,
        notification_id: str,
        *,
        token: Optional[str] = None,
    ) -> None:
        """Soft-delete a notification. Idempotent - safe to call multiple times."""
        client = self._get_client(token)
        await soft_delete_notification_notifications_notification_id_delete.asyncio_detailed(
            notification_id=notification_id,
            client=client,
        )

    # ------------------------------------------------------------------ #
    # Web Push                                                             #
    # ------------------------------------------------------------------ #

    async def get_vapid_public_key(
        self, token: Optional[str] = None
    ) -> VapidPublicKeyResponseSchema | None:
        """Fetch the VAPID public key (no auth required)."""
        client = self._get_client(token)
        res = await vapid_public_key_webpush_vapid_public_key_get.asyncio_detailed(
            client=client,
        )
        return to_schema(res.parsed, VapidPublicKeyResponseSchema)

    async def subscribe(
        self,
        body: SubscribeRequest,
        *,
        token: Optional[str] = None,
    ) -> StatusResponseSchema | None:
        """Register or refresh a Web Push subscription for the authenticated user."""
        client = self._get_client(token)
        res = await subscribe_webpush_subscribe_post.asyncio_detailed(
            client=client,
            body=body,
        )
        return to_schema(res.parsed, StatusResponseSchema)

    async def unsubscribe(
        self,
        body: UnsubscribeRequest,
        *,
        token: Optional[str] = None,
    ) -> StatusResponseSchema | None:
        """Remove a Web Push subscription for the authenticated user."""
        client = self._get_client(token)
        res = await unsubscribe_webpush_unsubscribe_post.asyncio_detailed(
            client=client,
            body=body,
        )
        return to_schema(res.parsed, StatusResponseSchema)


class NudgingAdminClient:
    """Admin nudging client. Requires nudging.admin scope or admin group.

    Covers:
    - GET  /admin/notifications         - list all notifications (filterable)
    - POST /admin/ingest-event          - ingest a Digital Twin event
    - POST /admin/webpush/send-test     - send a test push notification to any user
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
        """Return an authenticated client. Priority: explicit > default > provider."""
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

    # ------------------------------------------------------------------ #
    # Admin - Notifications                                                #
    # ------------------------------------------------------------------ #

    async def list_notifications(
        self,
        *,
        user_id: None | str | Unset = UNSET,
        family: None | str | Unset = UNSET,
        severity: None | str | Unset = UNSET,
        include_deleted: bool | Unset = False,
        unread_only: bool | Unset = False,
        limit: int | Unset = 100,
        offset: int | Unset = 0,
        token: Optional[str] = None,
    ) -> list[AdminNotificationOutSchema]:
        """Admin view of all notifications. Filterable by user_id, family, severity."""
        client = await self._get_client(token)
        res = await admin_list_notifications_admin_notifications_get.asyncio_detailed(
            client=client,
            user_id=user_id,
            family=family,
            severity=severity,
            include_deleted=include_deleted,
            unread_only=unread_only,
            limit=limit,
            offset=offset,
        )

        if isinstance(res.parsed, HTTPValidationError):
            raise Exception(HTTPValidationError)

        items = res.parsed or []
        return [to_schema(item, AdminNotificationOutSchema) for item in items]

    # ------------------------------------------------------------------ #
    # Admin - Event Ingestion                                              #
    # ------------------------------------------------------------------ #

    async def ingest_event(
        self,
        body: DigitalTwinEvent,
        *,
        token: Optional[str] = None,
    ) -> (
        IngestOkResponseSchema
        | IngestAcceptedResponseSchema
        | IngestErrorDetailSchema
        | None
    ):
        """Ingest an enriched Digital Twin event.

        Evaluates nudging rules and dispatches deliveries for any triggered nudges.

        Returns:
            IngestOkResponseSchema       on 200 (nudges created synchronously)
            IngestAcceptedResponseSchema on 202 (accepted for async processing)
            IngestErrorDetailSchema      on 400 / 409 / 422 / 500
            None                         on 204 (no nudges triggered)
        """
        client = await self._get_client(token)
        res = await ingest_event_admin_ingest_event_post.asyncio_detailed(
            client=client,
            body=body,
        )
        from celine.sdk.openapi.nudging.models import (
            IngestOkResponse,
            IngestAcceptedResponse,
            IngestErrorDetail,
        )

        if isinstance(res.parsed, IngestOkResponse):
            return to_schema(res.parsed, IngestOkResponseSchema)
        if isinstance(res.parsed, IngestAcceptedResponse):
            return to_schema(res.parsed, IngestAcceptedResponseSchema)
        if isinstance(res.parsed, IngestErrorDetail):
            return to_schema(res.parsed, IngestErrorDetailSchema)
        return None  # 204 - no nudges triggered

    # ------------------------------------------------------------------ #
    # Admin - Web Push                                                     #
    # ------------------------------------------------------------------ #

    async def send_test_push(
        self,
        body: SendTestRequest,
        *,
        token: Optional[str] = None,
    ) -> SendTestResponseSchema | None:
        """Send a test Web Push notification to all active subscriptions for a user."""
        client = await self._get_client(token)
        res = await send_test_admin_webpush_send_test_post.asyncio_detailed(
            client=client,
            body=body,
        )
        return to_schema(res.parsed, SendTestResponseSchema)
