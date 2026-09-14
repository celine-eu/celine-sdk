"""Provisioning API wrapper.

Reusable client design for multi-tenant/per-request scenarios: initialize once,
pass tokens per call — the shape `rec_registry` and `onboarding` already use.

## What this wrapper decides

**Only a `200` is parsed by the generated code; every other answer becomes
:class:`ProvisioningApiError`**, carrying the status, the service's `code` and
its sentence. Since 1.2.0 the service declares its error statuses with an
`ErrorResponse` body, so the generated `_parse_response` parses them — and
raises on a body of another shape: an older service's `{"detail": "..."}`, a
proxy's HTML `502`. A crash there would hide the refusal it was reporting, so
the wrapper sends through the generated request builder (`_get_kwargs`) and
reads a non-`200` itself (:meth:`ProvisioningClient._request`).
`raise_on_unexpected_status` stays off for the same reason as in `onboarding`.

**Branch on `ProvisioningApiError.code`, never on the message.** It is the
service's machine-readable reason (`has_password`, `cooldown`, ...), a plain
string, and `None` for an older service that answered a string `detail`.

**`invitation` in an answer is an enum, not a string.** The generated schemas
use plain `Enum`s, so compare `account.invitation.value == "sent"` — or read
`account.invited` — rather than `account.invitation == "sent"`, which is always
false. The same holds for `InvitationResponseSchema.invitation`. `intent` going
out is a plain string (:data:`SendIntent`), so nothing needs comparing there.

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
from http import HTTPStatus
from typing import Any, Literal, Optional, get_args

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
    send_invitation_participants_community_key_invitation_post as _send_invitation,
)
from celine.sdk.openapi.provisioning.api.provisioning import (
    upsert_participant_participants_community_key_put as _upsert_participant,
)
from celine.sdk.openapi.provisioning.models import (
    InvitationIntent,
    InvitationRequest,
    Locale,
    ParticipantUpsert,
)
from celine.sdk.openapi.provisioning.schemas import (
    DisableResponseSchema,
    InvitationResponseSchema,
    ParticipantResponseSchema,
    ReconcileResponseSchema,
)
from celine.sdk.openapi.provisioning.types import UNSET, Response
from celine.sdk.provisioning.errors import ProvisioningApiError, ReconcileDivergence
from celine.sdk.utils.convert import to_schema

__all__ = ["ProvisioningClient", "SendIntent"]

#: Which email `send_invitation` asks for. `invitation` sets a first password
#: (7 days) and is refused `409 has_password` on an account that has one;
#: `password_reset` replaces it (1 hour) and is refused `409 no_password` on an
#: account that has none. The service never turns one into the other.
SendIntent = Literal["invitation", "password_reset"]


class ProvisioningClient:
    """Participant accounts in the celine realm, written through one service.

    Covers:
    - PUT  /participants/{community}/{key}             - ensure the account, optionally invite
    - POST /participants/{community}/{key}/invitation  - an invitation, or a reset, as named
    - POST /participants/{community}/{key}/disable     - revoke access
    - POST /reconcile/{community}                      - sweep a community

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
    async def _request(
        operation: Any, client: AuthenticatedClient, **kwargs: Any
    ) -> Response[Any]:
        """Send one generated operation; parse only a `200`.

        The generated `asyncio_detailed` parses every status the service
        declares, and raises inside that parse on an error body of another shape
        (a string `detail` from an older service, a proxy's HTML page). Building
        the request with the operation's own `_get_kwargs` keeps the path, the
        body and the headers generated, and leaves reading a refusal to
        :meth:`_check`, which accepts any shape.
        """
        response = await client.get_async_httpx_client().request(
            **operation._get_kwargs(**kwargs)
        )
        parsed = None
        if response.status_code == 200:
            parsed = operation._parse_response(client=client, response=response)
        try:
            status: Any = HTTPStatus(response.status_code)
        except ValueError:
            status = response.status_code
        return Response(
            status_code=status,
            content=response.content,
            headers=response.headers,
            parsed=parsed,
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
        """Return the parsed answer, or raise with what provisioning said.

        `detail` is `{"code", "message"}` from a 1.2.0+ service and a string from
        an older one; both keep the sentence in the exception text, and only the
        first has a `code`.
        """
        if res.status_code != 200:
            detail = self._detail(res.content)
            code = ProvisioningApiError.code_of(detail)
            if isinstance(detail, dict):
                hint = detail.get("message")
                hint = hint if isinstance(hint, str) else None
            else:
                hint = detail if isinstance(detail, str) else None
            raise ProvisioningApiError(
                f"{what} failed: provisioning answered {int(res.status_code)}"
                + (f" {code}" if code else "")
                + (f" ({hint})" if hint else ""),
                status_code=int(res.status_code),
                detail=detail,
                body=res.content,
                code=code,
                retry_after=_retry_after(res.headers),
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
        locale: Optional[str] = None,
        invite: bool = False,
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

        `locale` is one of `it`, `en`, `es`, and anything else raises
        `ValueError` before a request is made (the service would answer `422`).
        It is written on a new account, and on an existing one only if it has
        none.

        `invite=True` asks Keycloak to email an invitation to set a password —
        only for an account created in this call, or one with no password, and
        never a reset. **It never fails the call.** What happened is in
        `invitation`, a reason code to show the operator: `not_requested`,
        `sent`, `has_password`, `no_email` (the account has no email address),
        `not_on_dev_list`, `account_disabled`, `cooldown` (emailed a few minutes
        ago, nothing sent), `send_failed` (Keycloak did not send it; asking
        again may). `invited` is true only for `sent`. It is an enum: compare
        `.value`.
        """
        wire_locale = Locale(locale) if locale is not None else UNSET
        client = await self._get_client(token)
        res = await self._request(
            _upsert_participant,
            community=community,
            key=key,
            client=client,
            body=ParticipantUpsert(
                email=email,
                first_name=first_name,
                last_name=last_name,
                locale=wire_locale,
                invite=invite,
            ),
        )
        return to_schema(
            self._check(res, "ensure_participant"), ParticipantResponseSchema
        )

    async def send_invitation(
        self,
        community: str,
        key: str,
        *,
        intent: SendIntent,
        token: Optional[str] = None,
    ) -> InvitationResponseSchema:
        """Email a member the registry already holds the email `intent` names.

        **The caller names the email**, and the service checks it against the
        account in the same call that sends:

        - `"invitation"`: `actions` `UPDATE_PASSWORD` and `VERIFY_EMAIL`, the
          long invitation lifespan (7 days). Refused with `409` code
          `has_password` when the account already has a password.
        - `"password_reset"`: `UPDATE_PASSWORD` only, one hour by default.
          Refused with `409` code `no_password` when the account has none.

        A mismatch is refused before anything is sent and starts no cooldown, so
        the other intent works at once; the service never sends the other email
        instead. `intent` is required, and anything but these two raises
        `ValueError` before a request is made. `lifespan` in the answer is in
        seconds. No credential is generated or returned: Keycloak sends the link.

        `invitation` in the answer is `sent`, or `not_on_dev_list` when the
        service runs in dev email mode and the address is not allowed — nothing
        was sent then. It is an enum: compare `.value`.

        Refusals arrive as :class:`ProvisioningApiError`; branch on its `code`:

        - `404`: `community_not_found`, `member_not_found` (no *active* member
          under `key`), `account_not_found` (the realm has no account for it);
        - `409`: `account_disabled`, `has_password`, `no_password`, `no_email`
          (the account has no email address);
        - `429`: `cooldown`, the same account was emailed within a few minutes;
          `retry_after` has the seconds;
        - `502`: `send_failed` (Keycloak did not send it; a retry may),
          `registry_unavailable`, `provisioning_failed`.
        """
        wire_intent = _intent(intent)
        client = await self._get_client(token)
        res = await self._request(
            _send_invitation,
            community=community,
            key=key,
            client=client,
            body=InvitationRequest(intent=wire_intent),
        )
        return to_schema(
            self._check(res, "send_invitation"), InvitationResponseSchema
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

        A `404` is not always "nothing to disable": its `code` is
        `community_not_found`, `member_not_found` or `account_not_found`, and
        only the last means the realm has no account.
        """
        client = await self._get_client(token)
        res = await self._request(
            _disable, community=community, key=key, client=client
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
        res = await self._request(_reconcile, community=community, client=client)

        if res.status_code == 500:
            detail = self._detail(res.content)
            if isinstance(detail, dict) and "divergences" in detail:
                divergences = detail.get("divergences") or []
                raise ReconcileDivergence(
                    f"reconcile of {community} left {len(divergences)} member(s) "
                    f"outside their organization",
                    community=detail.get("community", community),
                    divergences=divergences,
                    status_code=int(res.status_code),
                    body=res.content,
                    code=ProvisioningApiError.code_of(detail),
                )

        return to_schema(self._check(res, "reconcile"), ReconcileResponseSchema)


def _intent(intent: Any) -> InvitationIntent:
    """The wire value of `intent`, or `ValueError` before any request.

    Accepts the string, or either generated enum (`InvitationIntent`, or the
    schema's `InvitationIntentSchema`, whose members are not strings).
    """
    value = getattr(intent, "value", intent)
    if value not in get_args(SendIntent):
        raise ValueError(
            f"intent must be one of {', '.join(get_args(SendIntent))}; got {intent!r}"
        )
    return InvitationIntent(value)


def _retry_after(headers: Any) -> Optional[int]:
    """`Retry-After` in whole seconds, when the service sent one (a `429`)."""
    value = headers.get("retry-after") if headers is not None else None
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None
