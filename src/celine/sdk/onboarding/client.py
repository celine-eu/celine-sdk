"""Onboarding API wrapper.

Reusable client design for multi-tenant/per-request scenarios.
Initialize once, pass tokens per-call - no client recreation overhead.

**This wraps onboarding's member surface only.** `/api/me/*` is authorised by the
member's own token and nothing else: no capability, no operator, no service
account. Onboarding's funnel and admin surfaces are in the generated client for
whoever needs them next, and are deliberately not given a method here — a
convenience method that let an operator decide on somebody's behalf is the one
thing that would make a recorded consent worthless.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import httpx

from celine.sdk.onboarding.errors import OnboardingApiError
from celine.sdk.openapi.onboarding import AuthenticatedClient
from celine.sdk.openapi.onboarding.api.me import (
    get_data_sharing_api_me_data_sharing_get,
    get_data_sharing_history_api_me_data_sharing_history_get,
    set_data_sharing_api_me_data_sharing_offer_id_post,
)
from celine.sdk.openapi.onboarding.models import DataSharingDecisionRequest
from celine.sdk.openapi.onboarding.schemas import (
    DataSharingHistoryResponseSchema,
    DataSharingStatusResponseSchema,
)
from celine.sdk.utils.convert import to_schema

__all__ = ["OnboardingClient"]


class OnboardingClient:
    """A member's own onboarding surface, acted on as themselves.

    Covers:
    - GET  /api/me/data-sharing               - offers, merged with their decisions
    - POST /api/me/data-sharing/{offer_id}    - grant or withdraw one offer
    - GET  /api/me/data-sharing/history       - their own record of what happened
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
        """Return an authenticated client for this request.

        `raise_on_unexpected_status` is **off**, which is where this wrapper
        parts company with its siblings. Onboarding declares only `200` and
        `422`, so its meaningful refusals — `409` for a decision that does not
        exist to be made, `503` for an unreachable dataspace — arrive as
        "unexpected" and would be raised as a generic error with the status
        buried. Every non-200 is turned into `OnboardingApiError` below instead,
        carrying the code and the service's own sentence.
        """
        actual_token = token or self._default_token
        if actual_token is None:
            raise ValueError("No token provided and no default_token set")
        return AuthenticatedClient(
            base_url=self._base_url,
            token=actual_token,
            timeout=self._timeout,
            verify_ssl=self._verify_ssl,
            raise_on_unexpected_status=False,
        )

    @staticmethod
    def _detail(content: bytes) -> str | None:
        """Onboarding's own explanation, which names the offer or the state."""
        try:
            body = json.loads(content)
        except (ValueError, TypeError):
            return None
        if isinstance(body, dict) and "detail" in body:
            return str(body["detail"])
        return None

    def _check(self, res: Any, what: str) -> Any:
        """Return the parsed answer, or raise with what onboarding said."""
        if res.status_code != 200:
            detail = self._detail(res.content)
            raise OnboardingApiError(
                f"{what} failed: onboarding answered {res.status_code}"
                + (f" ({detail})" if detail else ""),
                status_code=res.status_code,
                detail=detail,
                body=res.content,
            )
        if res.parsed is None:
            raise OnboardingApiError(
                f"{what} failed: onboarding answered 200 with nothing readable",
                status_code=res.status_code,
                body=res.content,
            )
        return res.parsed

    # ------------------------------------------------------------------ #
    # Data sharing                                                         #
    # ------------------------------------------------------------------ #

    async def get_data_sharing(
        self, *, token: Optional[str] = None
    ) -> DataSharingStatusResponseSchema:
        """Every offer this member's community publishes, with their decision.

        `has_identity` false is a normal state rather than an error, and `state`
        says which: a community that does not take part, a member not yet
        provisioned, and an identity conflict only an operator can clear each
        need a different sentence.
        """
        client = self._get_client(token)
        res = await get_data_sharing_api_me_data_sharing_get.asyncio_detailed(
            client=client
        )
        return to_schema(self._check(res, "get_data_sharing"), DataSharingStatusResponseSchema)

    async def set_data_sharing(
        self,
        offer_id: str,
        *,
        enabled: bool,
        token: Optional[str] = None,
    ) -> DataSharingStatusResponseSchema:
        """Grant or withdraw one offer, as the member.

        Withdrawal is the reason this route exists: the onboarding wizard can
        only grant, and GDPR Art. 7(3) requires taking consent back to be as
        easy as giving it.

        A `409` carried by :class:`OnboardingApiError` means the decision does
        not exist to be made — an offer this community does not publish, one
        disclosed under a contract rather than consented to, or a member with no
        dataspace identity yet.
        """
        client = self._get_client(token)
        res = await set_data_sharing_api_me_data_sharing_offer_id_post.asyncio_detailed(
            offer_id=offer_id,
            client=client,
            body=DataSharingDecisionRequest(enabled=enabled),
        )
        return to_schema(self._check(res, "set_data_sharing"), DataSharingStatusResponseSchema)

    async def get_data_sharing_history(
        self, *, token: Optional[str] = None
    ) -> DataSharingHistoryResponseSchema:
        """What has happened with this member's data, from their own record.

        Absent provenance is an empty list rather than a failure, decided in
        onboarding where the credential is.
        """
        client = self._get_client(token)
        res = await get_data_sharing_history_api_me_data_sharing_history_get.asyncio_detailed(
            client=client
        )
        return to_schema(
            self._check(res, "get_data_sharing_history"), DataSharingHistoryResponseSchema
        )
