"""Outbound request logging — docs/specifications/configuration.md REQ-0013.

Query strings carry emails and ids, so neither the level the SDK sets nor a
service that raises it again may put one in a log line.
"""

from __future__ import annotations

import logging

import httpx

import celine.sdk  # noqa: F401  - importing the SDK is what configures logging
from celine.sdk import configure_celine_logging


def _get(url: str) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={}))
    with httpx.Client(transport=transport) as client:
        client.get(url)


class TestOutboundRequestLogging:
    # @verifies REQ-0013
    def test_httpx_is_held_at_warning_whatever_the_log_level(self, monkeypatch):
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        configure_celine_logging()
        assert logging.getLogger("httpx").level == logging.WARNING
        assert logging.getLogger("httpcore").level == logging.WARNING

    # @verifies REQ-0013
    def test_no_request_line_at_the_default_level(self, caplog):
        configure_celine_logging()
        with caplog.at_level(logging.INFO):
            _get("http://registry.test/users/resolve?email=someone@example.org")
        assert "email=" not in caplog.text
        assert "registry.test" not in caplog.text

    # @verifies REQ-0013
    def test_a_service_that_raises_httpx_again_still_gets_no_query(self, caplog):
        configure_celine_logging()
        with caplog.at_level(logging.INFO, logger="httpx"):
            _get(
                "http://registry.test/users/resolve?email=someone@example.org&id=ex-00001"
            )
        assert "http://registry.test/users/resolve" in caplog.text
        assert "email=" not in caplog.text
        assert "ex-00001" not in caplog.text

    # @verifies REQ-0013
    def test_configuring_twice_adds_one_filter(self):
        configure_celine_logging()
        configure_celine_logging()
        assert len(logging.getLogger("httpx").filters) == 1
