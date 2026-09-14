"""Errors raised by the provisioning wrapper.

Separate from `client.py` so a caller can catch them without importing the
client — the shape `celine.sdk.onboarding.errors` established, which this
follows because provisioning's non-2xx answers are addressed to somebody in the
same way.
"""

from __future__ import annotations

from typing import Any


class ProvisioningApiError(RuntimeError):
    """The provisioning service refused or failed a request.

    It carries the **status code, the service's `code` and its own detail**,
    because on this surface they are the answer rather than diagnostics.

    **Branch on :attr:`code`, never on the text.** A 1.2.0+ service answers
    `{"detail": {"code": ..., "message": ...}}`: `code` is that stable string,
    `detail` is the dict, and the message is in ``str(exc)``. An older service
    answered a string `detail`: `code` is then `None`, `detail` is the string,
    and it is in ``str(exc)`` too. `code` is a plain string, not an enum, so
    ``exc.code == "cooldown"`` is a real comparison. New codes may appear:
    fall back to :attr:`status_code` for one you do not know.

    - `401` — `missing_token`, `invalid_token`. Renew the credential.
    - `403` — `insufficient_scope`: no `provisioning.participants.write` or
      `provisioning.reconcile`. Ask for the grant; retrying will not help.
    - `404` — `community_not_found`, `member_not_found`, `account_not_found`.
      Only the last means the realm has no account for a member it knows.
    - `409` — `account_disabled`; on `send_invitation` also `has_password`
      (asked for an invitation), `no_password` (asked for a reset) and
      `no_email`. Nothing was sent and no cooldown started.
    - `422` — the request failed validation: no address on the upsert, or no
      intent on the invitation. FastAPI's own body; `code` is `None`.
    - `429` — `cooldown`. :attr:`retry_after` is the seconds to wait.
    - `500` — `reconcile_diverged`, raised as :class:`ReconcileDivergence`.
    - `502` — `send_failed`, `registry_unavailable`, `provisioning_failed`.
      **A dependency, not a refusal**, and worth retrying: a failed send starts
      no cooldown.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        detail: Any = None,
        body: object | None = None,
        *,
        code: str | None = None,
        retry_after: int | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail
        self.body = body
        self.code = code
        self.retry_after = retry_after

    @staticmethod
    def code_of(detail: Any) -> str | None:
        """`detail["code"]` when `detail` is the 1.2.0+ object, else `None`."""
        if isinstance(detail, dict):
            code = detail.get("code")
            return code if isinstance(code, str) else None
        return None


class ReconcileDivergence(ProvisioningApiError):
    """A community sweep ran and left members outside their own organization.

    Its own class because it is the one failure here that is neither a refusal
    nor an outage: the sweep provisioned everybody and the realm still disagrees,
    so every entry in :attr:`divergences` is a provisioning call that reported
    success and had not succeeded.

    **Do not swallow it.** The service answers `500` rather than `200` with a
    list precisely because a list nobody reads is how 10 of 45 members on demo3
    ended up with no `organization` claim and nothing saying so. A scheduler
    catching this should make somebody hear about it.
    """

    def __init__(
        self,
        message: str,
        *,
        community: str,
        divergences: list[dict],
        status_code: int | None = None,
        body: object | None = None,
        code: str | None = None,
    ):
        super().__init__(
            message, status_code=status_code, detail=divergences, body=body, code=code
        )
        self.community = community
        self.divergences = divergences
