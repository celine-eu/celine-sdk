from __future__ import annotations

import logging
from typing import TypeVar, Generic
from celine.sdk.openapi.dt.models.http_validation_error import HTTPValidationError
from celine.sdk.openapi.dt.types import Response, Unset

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


def validation_types(error: HTTPValidationError) -> list[str]:
    """The error `type` codes of a validation refusal, and nothing else.

    `msg`, `loc` and the `input` FastAPI adds can repeat a submitted value, so
    they are left out; `type` (`missing`, `float_parsing`, ...) never carries
    one.
    """
    if isinstance(error.detail, Unset):
        return []
    return sorted({item.type_ for item in error.detail if isinstance(item.type_, str)})


def log_refusal(
    logger: logging.Logger,
    what: str,
    response: Response[object],
    error: HTTPValidationError,
) -> None:
    """Log a Digital Twin validation refusal by status and error types only.

    Every `celine.sdk.dt` method logs a refusal through here (REQ-0160). The
    refusal's `detail` echoes what was sent — a participant id, a date, for the
    boundary fetchers a coordinate — so no part of it but the `type` codes is
    written to a log.
    """
    logger.warning(
        "digital-twin refused %s: status=%s types=%s",
        what,
        int(response.status_code),
        validation_types(error),
    )
