from __future__ import annotations

from typing import TypeVar, Generic
from celine.sdk.openapi.dt.models.http_validation_error import HTTPValidationError
from celine.sdk.openapi.dt.types import Response

T = TypeVar("T")


class DTApiError(RuntimeError):
    def __init__(
        self, message: str, status_code: int | None = None, body: object | None = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


def unwrap(response: Response[T]) -> T:
    """
    Extract the parsed payload from an openapi-python-client Response[T].

    Raises:
        DTApiError: if the response is unsuccessful or unparsable.
    """
    if response.parsed is not None:
        return response.parsed

    raise DTApiError(
        f"request failed (status={response.status_code})",
        status_code=response.status_code,
        body=response.content,
    )
