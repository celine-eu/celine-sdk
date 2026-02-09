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


configure_celine_logging()
start_debugger()
