"""Errors raised by the REC Registry wrapper.

Separate from `client.py` so a caller can catch the error without importing the
client — the same shape as `celine.sdk.dt.util.DTApiError`, which this mirrors.
"""

from __future__ import annotations


class RecRegistryApiError(RuntimeError):
    """The registry refused or failed a request.

    Carries what the caller needs to tell one refusal from another: `422` for a
    request the service would not accept, `403` for a missing grant, anything
    else for a service that is unwell.
    """

    def __init__(
        self, message: str, status_code: int | None = None, body: object | None = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.body = body
