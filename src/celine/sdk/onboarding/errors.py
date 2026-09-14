"""Errors raised by the onboarding wrapper.

Separate from `client.py` so a caller can catch the error without importing the
client — the same shape as `celine.sdk.rec_registry.errors.RecRegistryApiError`,
which this mirrors.
"""

from __future__ import annotations


class OnboardingApiError(RuntimeError):
    """Onboarding refused or failed a request.

    Unlike its siblings this carries the **status code and the service's own
    detail**, because on the member surface they are part of the answer rather
    than diagnostics. A `409` there means "there is no decision to make, and
    `state` says why" — an offer the community does not publish, one disclosed
    under a contract, or a member with no dataspace identity yet. The caller is a
    backend-for-frontend that shows that sentence to the member, so flattening
    the refusal into a generic failure would lose it.

    On the admin member routes the refusal is a **code** instead
    (`{"detail": {"code", "message"}}`): `code` carries it, `detail` the English
    message, and `retry_after_seconds` the wait a `cooldown` names. Compare `code`
    as a string; it is never an enum.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        detail: str | None = None,
        body: object | None = None,
        code: str | None = None,
        retry_after_seconds: int | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail
        self.body = body
        self.code = code
        self.retry_after_seconds = retry_after_seconds
