"""Errors raised by the Flexibility wrapper.

Separate from `client.py` so a caller can catch the error without importing the
client — the same shape as `celine.sdk.rec_registry.errors.RecRegistryApiError`,
which this mirrors.
"""

from __future__ import annotations


class FlexibilityApiError(RuntimeError):
    """The Flexibility API refused or failed a request.

    The message names the call and the status code only. The response body is
    kept on :attr:`body` for a caller that wants to inspect it, and is never
    written into the message, so logging the exception cannot leak what the
    service echoed back.

    Attributes:
        status_code: The HTTP status the service answered, `200` for an answer
            that could not be read as the documented shape.
        body: The raw response body, as bytes.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        body: object | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.args[0]!r}, status_code={self.status_code!r})"
