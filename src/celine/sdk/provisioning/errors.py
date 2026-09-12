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

    It carries the **status code and the service's own detail**, because on this
    surface they are the answer rather than diagnostics, and they mean different
    things a caller has to act on differently:

    - `401` — the credential did not verify. Renew it.
    - `403` — it verified and does not hold `provisioning.participants.write` or
      `provisioning.reconcile`. Ask for the grant; retrying will not help.
    - `404` — no such member, or no Keycloak account for one. For a password
      reset or a revocation this is often the true answer, not a fault.
    - `422` — the request carried no address.
    - `502` — Keycloak or the registry failed. **A dependency, not a refusal**,
      and the one status here that is worth retrying.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        detail: Any = None,
        body: object | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail
        self.body = body


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
    ):
        super().__init__(message, status_code=status_code, detail=divergences, body=body)
        self.community = community
        self.divergences = divergences
