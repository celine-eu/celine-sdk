"""Tests for `celine.sdk.nudging.NudgingAdminClient.ingest_event`.

The seam is `mock_http`, as in the sibling suites: the generated client builds its
own `httpx.AsyncClient`, so the class is what gets replaced.

What is pinned here is how the wrapper survives an answer that does not match the
contract nudging declares. In staging (September 2026) every 409 came wrapped in
FastAPI's `{"detail": …}` and every 500 was a bare text body; the generated parser
raised `KeyError: 'error'` and `JSONDecodeError` respectively, straight into the
digital-twin's pipeline handler (489 errors in a week) and flexibility-api's
reminders. A sender that is *told* "duplicate" must not be handed a stack trace.
"""

from __future__ import annotations

import httpx
import pytest

from celine.sdk.nudging.client import NudgingAdminClient
from celine.sdk.openapi.nudging.models import DigitalTwinEvent
from celine.sdk.openapi.nudging.schemas import (
    IngestErrorDetailSchema,
    IngestOkResponseSchema,
)

pytestmark = pytest.mark.asyncio


def _client() -> NudgingAdminClient:
    return NudgingAdminClient("http://nudging.test", default_token="tok-service")


def _event() -> DigitalTwinEvent:
    return DigitalTwinEvent.from_dict(
        {
            "event_type": "flexibility_reminder",
            "user_id": "user-alice",
            "facts": {
                "facts_version": "1",
                "scenario": "flexibility_reminder",
                "time": "2026-09-07",
            },
        }
    )


def _answer(status_code: int, **kwargs):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, **kwargs)

    return handler


# @verifies REQ-0027
async def test_a_contract_conformant_error_is_the_error_detail(mock_http):
    mock_http(_answer(409, json={"error": "suppressed", "reason": "all_rules_dedup"}))

    result = await _client().ingest_event(_event())

    assert isinstance(result, IngestErrorDetailSchema)
    assert (result.error, result.reason) == ("suppressed", "all_rules_dedup")


# @verifies REQ-0027
async def test_an_error_wrapped_in_fastapis_detail_is_unwrapped(mock_http):
    """What nudging ≤ v1.6.3 actually sends for 400 / 409 / 422 / 500."""
    mock_http(
        _answer(
            409,
            json={
                "detail": {
                    "error": "suppressed",
                    "reason": "all_rules_dedup",
                    "results": [
                        {
                            "status": "suppressed_dedup",
                            "reason": "duplicate_in_dedup_window",
                            "details": {"dedup_key": "k"},
                        }
                    ],
                }
            },
        )
    )

    result = await _client().ingest_event(_event())

    assert isinstance(result, IngestErrorDetailSchema)
    assert result.error == "suppressed"
    assert result.results is not None
    assert result.results[0].reason == "duplicate_in_dedup_window"


# @verifies REQ-0027
async def test_an_unreadable_error_body_is_reported_with_its_status(mock_http):
    """A 500 from an unhandled exception is plain text — still an answer, not a crash."""
    mock_http(_answer(500, text="Internal Server Error"))

    result = await _client().ingest_event(_event())

    assert isinstance(result, IngestErrorDetailSchema)
    assert result.error == "http_500"
    assert "Internal Server Error" in (result.reason or "")


# @verifies REQ-0027
async def test_a_string_detail_is_kept_as_the_reason(mock_http):
    mock_http(_answer(422, json={"detail": "Missing facts in DT event"}))

    result = await _client().ingest_event(_event())

    assert isinstance(result, IngestErrorDetailSchema)
    assert result.error == "http_422"
    assert result.reason == "Missing facts in DT event"


# @verifies REQ-0027
async def test_a_200_is_the_ok_response(mock_http):
    mock_http(_answer(200, json={"status": "ok", "created": [], "suppressed": []}))

    result = await _client().ingest_event(_event())

    assert isinstance(result, IngestOkResponseSchema)
    assert result.status == "ok"


# @verifies REQ-0027
async def test_a_204_is_none(mock_http):
    mock_http(_answer(204))

    assert await _client().ingest_event(_event()) is None
