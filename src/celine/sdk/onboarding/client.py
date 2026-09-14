"""Onboarding API wrapper.

Reusable client design for multi-tenant/per-request scenarios.
Initialize once, pass tokens per-call - no client recreation overhead.

Two clients, for two ways of being authorised:

- :class:`OnboardingClient` wraps the **member surface**. `/api/me/*` is
  authorised by the member's own token and nothing else: no capability, no
  operator, no service account. It deliberately has no method that decides on
  somebody's behalf, because that is the one thing that would make a recorded
  consent worthless.
- :class:`OnboardingAdminClient` wraps the **delegated member emails**: a service
  holding `onboarding.members.invite` asks onboarding to send a registry member an
  invitation or a password reset, and forwards the manager whose press it is.
  Onboarding verifies both tokens, and refuses a call with no person behind it.

The rest of onboarding's admin surface is in the generated client for whoever
needs it next.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import httpx

from celine.sdk.auth import TokenProvider
from celine.sdk.onboarding.errors import OnboardingApiError
from celine.sdk.openapi.onboarding import AuthenticatedClient
from celine.sdk.openapi.onboarding.api.admin import (
    send_member_invitation_api_admin_communities_community_members_member_key_invitation_post as _send_invitation,
)
from celine.sdk.openapi.onboarding.api.admin import (
    send_member_password_reset_api_admin_communities_community_members_member_key_password_reset_post as _send_password_reset,
)
from celine.sdk.openapi.onboarding.api.me import (
    get_data_sharing_api_me_data_sharing_get,
    get_data_sharing_history_api_me_data_sharing_history_get,
    set_data_sharing_api_me_data_sharing_offer_id_post,
)
from celine.sdk.openapi.onboarding.models import DataSharingDecisionRequest
from celine.sdk.openapi.onboarding.schemas import (
    DataSharingHistoryResponseSchema,
    DataSharingStatusResponseSchema,
    MemberEmailSentSchema,
)
from celine.sdk.utils.convert import to_schema

__all__ = ["OnboardingClient", "OnboardingAdminClient", "ACTING_USER_HEADER"]

#: The header onboarding reads the acting manager's access token from, on the
#: delegated admin routes. Never `x-auth-request-access-token`: onboarding refuses
#: a delegated call carrying that one, because it means the public ingress.
ACTING_USER_HEADER = "X-Acting-User-Token"


def _body(content: bytes) -> Any:
    try:
        return json.loads(content)
    except (ValueError, TypeError):
        return None


def _retry_after(res: Any, detail: Any) -> int | None:
    value = detail.get("retryAfterSeconds") if isinstance(detail, dict) else None
    if value is None:
        value = res.headers.get("retry-after")
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _checked(res: Any, what: str) -> Any:
    """Return the parsed `200`, or raise with what onboarding said.

    `detail` is either a sentence (the member surface) or `{"code", "message"}`
    (the admin member routes). Both survive: the sentence as `detail`, the code as
    `code`.
    """
    if res.status_code != 200:
        body = _body(res.content)
        raw = body.get("detail") if isinstance(body, dict) else None
        code = raw.get("code") if isinstance(raw, dict) else None
        if isinstance(raw, dict):
            detail = str(raw["message"]) if raw.get("message") is not None else None
        else:
            detail = str(raw) if raw is not None else None
        explanation = " ".join(part for part in (code, detail and f"({detail})") if part)
        raise OnboardingApiError(
            f"{what} failed: onboarding answered {res.status_code}"
            + (f" {explanation}" if explanation else ""),
            status_code=res.status_code,
            detail=detail,
            body=res.content,
            code=str(code) if code is not None else None,
            retry_after_seconds=_retry_after(res, raw),
        )
    if res.parsed is None:
        raise OnboardingApiError(
            f"{what} failed: onboarding answered 200 with nothing readable",
            status_code=res.status_code,
            body=res.content,
        )
    return res.parsed


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

    def _check(self, res: Any, what: str) -> Any:
        """Return the parsed answer, or raise with what onboarding said."""
        return _checked(res, what)

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


class OnboardingAdminClient:
    """Onboarding's delegated member emails: a service acting for a manager.

    Covers:
    - POST /api/admin/communities/{community}/members/{member_key}/invitation
    - POST /api/admin/communities/{community}/members/{member_key}/password-reset

    Two tokens on every call. The service's own (`Authorization`, from the token
    provider, carrying `onboarding.members.invite`) and the manager's
    (`X-Acting-User-Token`, passed per call). There is no default for the second:
    each send follows one person's press, and a client that remembered a manager
    would send as them for whoever called next.

    `community` is the REC registry's community key, which on this platform is
    also the manager's organization alias. Every non-`200` is raised as
    :class:`OnboardingApiError` with its `code`; `cooldown` also carries
    `retry_after_seconds`. Nothing is retried: sending again is the manager's
    decision.
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

    async def _get_client(self, token: Optional[str], acting_token: str) -> AuthenticatedClient:
        """An authenticated client carrying both tokens.

        Priority for the service token: explicit > default > provider. As on the
        member client, `raise_on_unexpected_status` is off and every non-`200`
        becomes :class:`OnboardingApiError`.
        """
        if not acting_token or not acting_token.strip():
            raise ValueError("acting_token is required: a member email follows a person's press")
        if token is not None:
            actual_token = token
        elif self._default_token is not None:
            actual_token = self._default_token
        elif self._token_provider is not None:
            actual_token = (await self._token_provider.get_token()).access_token
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
            raise_on_unexpected_status=False,
            headers={ACTING_USER_HEADER: acting_token},
        )

    async def send_member_invitation(
        self,
        community: str,
        member_key: str,
        *,
        acting_token: str,
        token: Optional[str] = None,
    ) -> MemberEmailSentSchema:
        """Email the member an invitation to set their first password.

        `code` is `sent`, or `not_on_dev_list` when dev email mode held it back.
        Refused `409 has_password` when the account already has one.
        """
        client = await self._get_client(token, acting_token)
        res = await _send_invitation.asyncio_detailed(
            community=community,
            member_key=member_key,
            client=client,
        )
        return to_schema(_checked(res, "send_member_invitation"), MemberEmailSentSchema)

    async def send_member_password_reset(
        self,
        community: str,
        member_key: str,
        *,
        acting_token: str,
        token: Optional[str] = None,
    ) -> MemberEmailSentSchema:
        """Email the member a link to reset their password.

        Refused `409 no_password` when the account has none. It is never turned
        into an invitation.
        """
        client = await self._get_client(token, acting_token)
        res = await _send_password_reset.asyncio_detailed(
            community=community,
            member_key=member_key,
            client=client,
        )
        return to_schema(_checked(res, "send_member_password_reset"), MemberEmailSentSchema)
