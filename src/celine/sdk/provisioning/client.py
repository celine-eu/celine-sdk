"""Provisioning API wrapper.

Reusable client design for multi-tenant/per-request scenarios: initialize once,
pass tokens per call — the shape `rec_registry` and `onboarding` already use.

## What this wrapper decides

**`raise_on_unexpected_status` is off**, as in `onboarding` and for the same
reason. FastAPI declares only `200` and `422`, so every answer that actually
carries meaning here — `403` for a missing scope, `404` for a member nobody has,
`500` for a sweep that left divergences, `502` for a dependency that failed —
arrives as "unexpected" and would be raised with the status buried. Each is
turned into :class:`ProvisioningApiError` instead, carrying the code and the
service's own sentence.

**A diverging reconcile gets its own exception.** It is neither a refusal nor an
outage: the sweep provisioned everybody and the realm still disagrees. See
:class:`ReconcileDivergence`.

**`authorization` is never passed to the generated calls.** The service declares
it as an explicit header parameter, so the generated signature offers it — but
`AuthenticatedClient` already sets the header, and passing both is two sources
for one credential. Leaving it `UNSET` omits it.
"""

from __future__ import annotations

import json
from typing import Any, Optional

import httpx

from celine.sdk.auth import TokenProvider
from celine.sdk.openapi.provisioning import AuthenticatedClient
from celine.sdk.openapi.provisioning.api.provisioning import (
    disable_participant_participants_community_key_disable_post as _disable,
)
from celine.sdk.openapi.provisioning.api.provisioning import (
    reconcile_reconcile_community_post as _reconcile,
)
from celine.sdk.openapi.provisioning.api.provisioning import (
    reset_password_participants_community_key_password_reset_post as _reset_password,
)
from celine.sdk.openapi.provisioning.api.provisioning import (
    upsert_participant_participants_community_key_put as _upsert_participant,
)
from celine.sdk.openapi.provisioning.models import ParticipantUpsert
from celine.sdk.openapi.provisioning.schemas import (
    DisableResponseSchema,
    ParticipantResponseSchema,
    PasswordResetResponseSchema,
    ReconcileResponseSchema,
)
from celine.sdk.provisioning.errors import ProvisioningApiError, ReconcileDivergence
from celine.sdk.utils.convert import to_schema

__all__ = ["ProvisioningClient"]


class ProvisioningClient:
    """Participant accounts in the celine realm, written through one service.

    Covers:
    - PUT  /participants/{community}/{key}                 - ensure the account
    - POST /participants/{community}/{key}/password-reset  - one-time credential
    - POST /participants/{community}/{key}/disable         - revoke access
    - POST /reconcile/{community}                          - sweep a community

    Args:
        base_url: Base URL of the provisioning service, on the internal network.
        default_token: Token to use when none is passed per call.
        token_provider: Token provider, for a service account. This is the usual
            one — every caller is another service.
        timeout: Request timeout in seconds.
        verify_ssl: Verify SSL certificates.
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
        """Authenticated client for this request.

        Priority: explicit token > default_token > token_provider.
        """
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
        )

    @staticmethod
    def _detail(content: bytes) -> Any:
        """The service's own explanation, which names the member or the scope.

        Returned whole rather than stringified: a diverging reconcile puts the
        entire report in `detail`, and flattening it would lose the list.
        """
        try:
            body = json.loads(content)
        except (ValueError, TypeError):
            return None
        if isinstance(body, dict) and "detail" in body:
            return body["detail"]
        return None

    def _check(self, res: Any, what: str) -> Any:
        """Return the parsed answer, or raise with what provisioning said."""
        if res.status_code != 200:
            detail = self._detail(res.content)
            hint = detail if isinstance(detail, str) else None
            raise ProvisioningApiError(
                f"{what} failed: provisioning answered {res.status_code}"
                + (f" ({hint})" if hint else ""),
                status_code=res.status_code,
                detail=detail,
                body=res.content,
            )
        if res.parsed is None:
            raise ProvisioningApiError(
                f"{what} failed: provisioning answered 200 with nothing readable",
                status_code=res.status_code,
                body=res.content,
            )
        return res.parsed

    # ------------------------------------------------------------------ #
    # Participants                                                         #
    # ------------------------------------------------------------------ #

    async def ensure_participant(
        self,
        community: str,
        key: str,
        *,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        token: Optional[str] = None,
    ) -> ParticipantResponseSchema:
        """Ensure the account exists, is in the REC organization and its org group.

        Idempotent on `(community, key)`: a retry finds the account the first
        call made, joins nothing twice, and comes back with `created` false.

        **Use the `username` that comes back, never the one you would have
        computed.** It is read from Keycloak, and an account that already existed
        may authenticate under a convention nobody chose here — a participant
        onboarded before this service existed, or seeded from a registry file.
        That value is what a caller stores as the registry's `Member.user_id`;
        `user_id` in the response is the Keycloak uuid, which is a different
        thing with an unfortunately similar name.

        The address transits and is stored in neither this service nor the
        registry. It lands on the Keycloak account, which is where the address
        somebody logs in with belongs.

        **Write the member row after this returns, not before.** The login then
        exists before the row that keys on it, which is the fail-closed order.
        """
        client = await self._get_client(token)
        res = await _upsert_participant.asyncio_detailed(
            community=community,
            key=key,
            client=client,
            body=ParticipantUpsert(
                email=email,
                first_name=first_name,
                last_name=last_name,
            ),
        )
        return to_schema(
            self._check(res, "ensure_participant"), ParticipantResponseSchema
        )

    async def reset_password(
        self,
        community: str,
        key: str,
        *,
        token: Optional[str] = None,
    ) -> PasswordResetResponseSchema:
        """Issue a one-time credential for a member the registry already holds.

        The credential is **temporary**: the participant has to change it at
        next login, so what comes back is a handover and never their password.
        Treat it as one — it should reach the person and nothing else, and it
        should not be logged.

        A `404` carried by :class:`ProvisioningApiError` means the registry has
        no such member, or the realm has no account for one — provision it
        first.
        """
        client = await self._get_client(token)
        res = await _reset_password.asyncio_detailed(
            community=community, key=key, client=client
        )
        return to_schema(
            self._check(res, "reset_password"), PasswordResetResponseSchema
        )

    async def disable(
        self,
        community: str,
        key: str,
        *,
        token: Optional[str] = None,
    ) -> DisableResponseSchema:
        """Revoke a member's access, without destroying anything.

        The account, its memberships and everything keyed on its uuid survive,
        and re-enabling is one call — what is being revoked is somebody's access
        to their own energy community.

        `changed` is false when the revocation was already in force. That is not
        a failure and must not be reported as one.
        """
        client = await self._get_client(token)
        res = await _disable.asyncio_detailed(
            community=community, key=key, client=client
        )
        return to_schema(self._check(res, "disable"), DisableResponseSchema)

    # ------------------------------------------------------------------ #
    # Reconcile                                                            #
    # ------------------------------------------------------------------ #

    async def reconcile(
        self,
        community: str,
        *,
        token: Optional[str] = None,
    ) -> ReconcileResponseSchema:
        """Provision every active member the registry holds for one community.

        Then it checks that each of them is in the REC's organization, and
        **raises :class:`ReconcileDivergence` if any is not**. That is a `500`
        from the service, deliberately: everything checked is something the same
        call claimed to have done, so a finding is a provisioning call that
        reported success and had not succeeded.

        Needs `provisioning.reconcile`, which is a separate scope from the
        per-member write — sweeping a whole community and provisioning one
        member somebody asked about are different grants.

        Members that are not `active` are skipped and **not** disabled: skipping
        provisioning and revoking access are different acts with different
        owners.
        """
        client = await self._get_client(token)
        res = await _reconcile.asyncio_detailed(community=community, client=client)

        if res.status_code == 500:
            detail = self._detail(res.content)
            if isinstance(detail, dict) and "divergences" in detail:
                divergences = detail.get("divergences") or []
                raise ReconcileDivergence(
                    f"reconcile of {community} left {len(divergences)} member(s) "
                    f"outside their organization",
                    community=detail.get("community", community),
                    divergences=divergences,
                    status_code=res.status_code,
                    body=res.content,
                )

        return to_schema(self._check(res, "reconcile"), ReconcileResponseSchema)
