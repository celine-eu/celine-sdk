"""Flexibility API wrapper.

Reusable client design matching the RecRegistryAdminClient pattern:
- FlexibilityClient       — user-scoped (pass token per-call)
- FlexibilityAdminClient  — service-scoped (token_provider for auto-refresh)

Initialize once, reuse for all requests.

Example — per-request usage (FastAPI):
    # At startup
    flexibility_client = FlexibilityClient(base_url="http://flexibility-api:8000")

    # In a route
    @app.get("/api/suggestions")
    async def get_suggestions(token: str = Depends(get_token)):
        return await flexibility_client.list_suggestions(token=token)

Example — service account:
    from celine.sdk.auth import OidcClientCredentialsProvider

    provider = OidcClientCredentialsProvider(...)
    admin = FlexibilityAdminClient(base_url="http://flexibility-api:8000", token_provider=provider)
    pending = await admin.get_pending_commitments()
"""

from __future__ import annotations

from datetime import datetime
from http import HTTPStatus
from typing import Optional
from uuid import UUID

import httpx

from celine.sdk.auth import TokenProvider
from celine.sdk.flexibility.errors import FlexibilityApiError
from celine.sdk.openapi.flexibility import AuthenticatedClient
from celine.sdk.openapi.flexibility.api.commitments import (
    cancel_commitment_api_commitments_commitment_id_delete,
    export_commitments_api_commitments_export_get,  # generated after openapi regen
    get_pending_api_commitments_pending_get,
    list_commitments_api_commitments_get,
    settle_commitment_api_commitments_commitment_id_settle_patch,
)
from celine.sdk.openapi.flexibility.api.suggestions import (
    list_suggestions_api_suggestions_get,
    respond_to_suggestion_api_suggestions_suggestion_id_respond_post,
)
from celine.sdk.openapi.flexibility.models import (
    CommitmentSettle,
    SuggestionRespondRequest,
)
from celine.sdk.openapi.flexibility.models.suggestion_respond_request_response import (
    SuggestionRespondRequestResponse,
)
from celine.sdk.openapi.flexibility.schemas import (
    CommitmentListResponseSchema,
    CommitmentOutSchema,
    SuggestionItemSchema,
    SuggestionRespondResponseSchema,
)
from celine.sdk.openapi.flexibility.types import UNSET

__all__ = ["FlexibilityClient", "FlexibilityAdminClient", "FlexibilityApiError"]


def _commitments(response: httpx.Response, what: str) -> list[CommitmentOutSchema]:
    """A `200` list of commitments as schemas; anything else raises.

    On the export route an empty list is a meaningful answer, so a refusal or an
    unreadable body must not degrade to one: a mirror would complete having
    fetched nothing. The error names the call and the status only; the body
    stays on `FlexibilityApiError.body` and out of the message.
    """
    if response.status_code != HTTPStatus.OK:
        raise FlexibilityApiError(
            f"{what} refused: flexibility-api answered {response.status_code}",
            status_code=response.status_code,
            body=response.content,
        )
    unreadable = FlexibilityApiError(
        f"{what}: flexibility-api answered 200 with no readable commitment list",
        status_code=response.status_code,
        body=response.content,
    )
    try:
        payload = response.json()
    except ValueError:
        # `from None`: the decode error would repeat the body.
        raise unreadable from None
    if not isinstance(payload, list):
        raise unreadable
    try:
        return [CommitmentOutSchema.model_validate(item) for item in payload]
    except ValueError:
        # `from None`: the validation error would repeat the body's values.
        raise unreadable from None


class FlexibilityClient:
    """User-scoped Flexibility API client.

    Covers user-facing endpoints: suggestions, commitments.
    Pass the user JWT on each call via token= for per-request usage.

    Args:
        base_url: Base URL of the Flexibility API
        default_token: Default token to use when none provided per-call
        timeout: Request timeout in seconds (default: 30.0)
        verify_ssl: Verify SSL certificates (default: True)
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

    def _get_client(self, token: Optional[str]) -> AuthenticatedClient:
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

    # ── Suggestions ──────────────────────────────────────────────────────────

    async def list_suggestions(
        self, *, token: Optional[str] = None
    ) -> list[SuggestionItemSchema]:
        """List load-shift window suggestions for the authenticated user."""
        client = self._get_client(token)
        res = await list_suggestions_api_suggestions_get.asyncio_detailed(client=client)
        if not res.parsed:
            return []
        return [SuggestionItemSchema.model_validate(item.to_dict()) for item in res.parsed]

    async def respond_to_suggestion(
        self,
        suggestion_id: str,
        response: str,
        *,
        reward_points: Optional[int] = None,
        period_start: Optional[str] = None,
        period_end: Optional[str] = None,
        token: Optional[str] = None,
    ) -> SuggestionRespondResponseSchema:
        """Accept or decline a flexibility suggestion.

        On acceptance, creates a commitment in the flexibility-api and publishes
        the flexibility.committed MQTT event.

        Args:
            suggestion_id: The suggestion window ID
            response: "accepted" or "declined"
            reward_points: Override the estimated reward points
            period_start: ISO datetime of window start (required on accepted)
            period_end: ISO datetime of window end (required on accepted)
        """
        client = self._get_client(token)
        body = SuggestionRespondRequest(
            response=SuggestionRespondRequestResponse(response),
            reward_points=reward_points if reward_points is not None else UNSET,
            period_start=period_start if period_start is not None else UNSET,
            period_end=period_end if period_end is not None else UNSET,
        )
        res = await respond_to_suggestion_api_suggestions_suggestion_id_respond_post.asyncio_detailed(
            suggestion_id=suggestion_id,
            client=client,
            body=body,
        )
        from celine.sdk.openapi.flexibility.models.suggestion_respond_response import SuggestionRespondResponse as _SuggestionRespondResponse
        if not isinstance(res.parsed, _SuggestionRespondResponse):
            raise ValueError(f"Unexpected response: status={res.status_code} parsed={res.parsed!r}")
        return SuggestionRespondResponseSchema.model_validate(res.parsed.to_dict())

    # ── Commitments ──────────────────────────────────────────────────────────

    async def list_commitments(
        self,
        *,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        token: Optional[str] = None,
    ) -> CommitmentListResponseSchema:
        """List commitments for the authenticated user."""
        client = self._get_client(token)
        res = await list_commitments_api_commitments_get.asyncio_detailed(
            client=client,
            status=status if status is not None else UNSET,
            limit=limit,
            offset=offset,
        )
        if res.parsed is None:
            return CommitmentListResponseSchema(items=[], total=0)
        return CommitmentListResponseSchema.model_validate(res.parsed.to_dict())

    async def cancel_commitment(
        self, commitment_id: UUID, *, token: Optional[str] = None
    ) -> None:
        """Cancel a pending commitment."""
        client = self._get_client(token)
        await cancel_commitment_api_commitments_commitment_id_delete.asyncio_detailed(
            client=client,
            commitment_id=commitment_id,
        )


class FlexibilityAdminClient:
    """Service-scoped Flexibility API client.

    Covers admin/service endpoints: pending commitments, settlement.
    Uses a token_provider (OidcClientCredentialsProvider) for automatic
    token refresh.

    Args:
        base_url: Base URL of the Flexibility API
        default_token: Default token (for testing / static tokens)
        token_provider: Token provider for automatic token management
        timeout: Request timeout in seconds (default: 30.0)
        verify_ssl: Verify SSL certificates (default: True)
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

    async def _get_client(self, token: Optional[str]) -> AuthenticatedClient:
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

    async def export_commitments(
        self,
        *,
        created_after: Optional[datetime] = None,
        token: Optional[str] = None,
    ) -> list[CommitmentOutSchema]:
        """Bulk export all commitments for pipeline mirroring.

        Requires flexibility.commitments.export scope on the service account.
        Returns all statuses across all users, ordered by committed_at asc.

        Args:
            created_after: Only return commitments created at or after this datetime.
                           Pass now() - 90 days for the standard mirror window.

        Returns:
            The commitments, possibly none: `[]` means only that the service
            answered `200` with an empty list.

        Raises:
            FlexibilityApiError: on any status but `200`, and on a `200` whose
                body is not a list of commitments. The message carries the
                status code only, never the token or the body (REQ-0210).
        """
        client = await self._get_client(token)
        # The request is built by the generated module (`_get_kwargs`), so path
        # and query stay generated; the answer is read here. The generated
        # parser raises `UnexpectedStatus` with the whole body in its message
        # and fails with a decode error on a proxy's HTML page.
        kwargs = export_commitments_api_commitments_export_get._get_kwargs(
            created_after=created_after if created_after is not None else UNSET,
        )
        response = await client.get_async_httpx_client().request(**kwargs)
        return _commitments(response, "export_commitments")

    async def get_pending_commitments(
        self, *, token: Optional[str] = None
    ) -> list[CommitmentOutSchema]:
        """Return commitments whose window has opened and have not yet been reminded."""
        client = await self._get_client(token)
        res = await get_pending_api_commitments_pending_get.asyncio_detailed(client=client)
        if not res.parsed:
            return []
        return [CommitmentOutSchema.model_validate(item.to_dict()) for item in res.parsed]

    async def settle_commitment(
        self,
        commitment_id: UUID,
        reward_points_actual: int,
        *,
        actual_kwh: Optional[float] = None,
        token: Optional[str] = None,
    ) -> CommitmentOutSchema:
        """Settle a commitment with actual reward points."""
        client = await self._get_client(token)
        body = CommitmentSettle(
            reward_points_actual=reward_points_actual,
            actual_kwh=actual_kwh if actual_kwh is not None else UNSET,
        )
        res = await settle_commitment_api_commitments_commitment_id_settle_patch.asyncio_detailed(
            client=client,
            commitment_id=commitment_id,
            body=body,
        )
        return CommitmentOutSchema.model_validate(res.parsed.to_dict())
