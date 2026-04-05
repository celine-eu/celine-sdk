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

from typing import Optional
from uuid import UUID

import httpx

from celine.sdk.auth import TokenProvider
from celine.sdk.openapi.flexibility import AuthenticatedClient
from celine.sdk.openapi.flexibility.api.commitments import (
    cancel_commitment_api_commitments_commitment_id_delete,
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

__all__ = ["FlexibilityClient", "FlexibilityAdminClient"]


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
