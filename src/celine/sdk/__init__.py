"""CELINE SDK.

Public modules:
- celine.sdk.settings
- celine.sdk.auth
- celine.sdk.broker
- celine.sdk.openapi (generated clients)
"""

import os
import logging

from celine.sdk.settings import SdkSettings

__all__ = ["SdkSettings"]


def start_debugger():
    _with_debugger = os.getenv("DEBUG_ATTACH", None)
    if _with_debugger:
        import debugpy

        port = os.getenv("DEBUG_PORT", 5678)
        debugpy.listen(("0.0.0.0", int(port)))
        print(f"Debugger listening on 0.0.0.0:{port}")

        if _with_debugger == "wait":
            print(f"Debugger waiting for client")
            debugpy.wait_for_client()


def configure_celine_logging() -> None:
    """
    Configure loggers under the 'celine.*' namespace based on LOG_LEVEL.

    LOG_LEVEL may be one of:
    DEBUG, INFO, WARNING, ERROR, CRITICAL

    Default: INFO
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    # Ensure root is configured once
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(name)s %(message)s",
    )

    # Apply level to all celine.* loggers (existing and future)
    base_logger = logging.getLogger("celine")
    base_logger.setLevel(level)
    base_logger.propagate = True

    # `httpx` logs every request URL, query string included, at INFO — and query
    # strings carry emails and ids (`/users/resolve?email=`). It inherits the root
    # level from `basicConfig` above, so it is held at WARNING whatever LOG_LEVEL
    # says, and its records lose the query string should a service raise it again.
    muted_loggers = ["httpcore", "httpx"]
    for logger_name in muted_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.WARNING)
        logger.propagate = True

    httpx_logger = logging.getLogger("httpx")
    if not any(isinstance(f, _StripQueryFilter) for f in httpx_logger.filters):
        httpx_logger.addFilter(_StripQueryFilter())


class _StripQueryFilter(logging.Filter):
    """Drop the query string from any URL carried in a log record's arguments."""

    def filter(self, record: logging.LogRecord) -> bool:
        args = record.args
        if isinstance(args, tuple) and args:
            record.args = tuple(_without_query(a) for a in args)
        return True


def _without_query(value: object) -> object:
    try:
        import httpx
    except ImportError:  # pragma: no cover - httpx is a dependency
        return value
    if isinstance(value, httpx.URL) and value.query:
        return value.copy_with(query=None, fragment=None)
    return value


configure_celine_logging()
start_debugger()
