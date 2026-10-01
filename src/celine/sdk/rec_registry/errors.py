"""Errors raised by the REC Registry wrapper.

Separate from `client.py` so a caller can catch the error without importing the
client — the same shape as `celine.sdk.dt.util.DTApiError`, which this mirrors.
"""

from __future__ import annotations

import json
from typing import Any


class RecRegistryApiError(RuntimeError):
    """The registry refused or failed a request.

    Carries what the caller needs to tell one refusal from another: `422` for a
    request the service would not accept, `403` for a missing grant, anything
    else for a service that is unwell.

    **Branch on :attr:`code`, never on the text.** The registry answers a
    refusal it has named as a flat ``{"detail": "<sentence>", "code": "<code>"}``
    (its error-code vocabulary: `sensor_held`, `asset_key_taken`,
    `member_not_found`, and since registry 1.7.0 `delivery_point_held` —
    `409` on a delivery-point write, a create or a reactivation, `422` on an
    import — and `delivery_point_linked`, `409` on a delivery-point delete). `code` is that string, read from the top level of
    the body, and `None` for a refusal that names none — a validation error, a
    body that is not JSON, a proxy's page. It is a plain string, not an enum, so
    ``exc.code == "sensor_held"`` is a real comparison and a code added to the
    registry later does not fail here. :attr:`detail` is the registry's
    `detail` as it came — the sentence, for people, whose wording is not part of
    the API — or `None` when the body had none.

    `code` and `detail` are keyword-only and default to `None`, so an error
    raised by the batch lookups (which set neither) is unchanged for a caller.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        body: object | None = None,
        *,
        code: str | None = None,
        detail: Any = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.body = body
        self.code = code
        self.detail = detail

    @staticmethod
    def refusal_of(content: bytes | None) -> tuple[str | None, Any]:
        """`(code, detail)` from a registry refusal body; `(None, None)` if unreadable.

        Only the registry's own flat shape yields a code: `code` beside
        `detail` at the top level, as a string. A code nested inside `detail`
        (onboarding's shape) is not this service's and is not looked for, and
        the sentence is never parsed for one.
        """
        try:
            body = json.loads(content) if content else None
        except (ValueError, TypeError):
            return None, None
        if not isinstance(body, dict):
            return None, None
        code = body.get("code")
        return (code if isinstance(code, str) else None), body.get("detail")
