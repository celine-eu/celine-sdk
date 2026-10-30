"""Tests for `celine.sdk.flexibility`.

The seam is `mock_http`: the generated client builds its own `httpx.AsyncClient`,
so the class is what gets replaced, and the wrapper runs against real responses.

What is pinned here is the commitments export, the one call a mirror flow makes.
On that route an empty list is a *meaningful* answer — "no commitment since that
date" — so a refused or unreadable answer must not look like one: a mirror that
receives `[]` for a `403` completes, writes nothing, and reports success.
"""

from __future__ import annotations

from datetime import datetime, timezone

import httpx
import pytest

from celine.sdk.flexibility import FlexibilityAdminClient, FlexibilityApiError
from celine.sdk.flexibility.errors import FlexibilityApiError as _FromErrors

pytestmark = pytest.mark.asyncio

TOKEN = "tok-example-service-secret"
BODY_MARKER = "example-body-secret"

COMMITMENT = {
    "id": "00000000-0000-4000-8000-000000000001",
    "user_id": "example-user",
    "suggestion_id": "example-suggestion",
    "suggestion_type": "shift-consumption",
    "community_id": "example-community",
    "device_id": None,
    "period_start": "2026-07-01T10:00:00+00:00",
    "period_end": "2026-07-01T12:00:00+00:00",
    "committed_at": "2026-06-30T09:00:00+00:00",
    "reminded_at": None,
    "settled_at": None,
    "reward_points_estimated": 10,
    "reward_points_actual": None,
    "status": "committed",
}


def _admin() -> FlexibilityAdminClient:
    return FlexibilityAdminClient("http://flexibility.test", default_token=TOKEN)


def _answer(code: int, **kwargs):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(code, **kwargs)

    return handle


class TestExportCommitmentsAnswers:
    # @verifies REQ-0210
    async def test_a_list_comes_back_as_schemas(self, mock_http):
        seen = mock_http(_answer(200, json=[COMMITMENT]))

        rows = await _admin().export_commitments(
            created_after=datetime(2026, 6, 1, tzinfo=timezone.utc)
        )

        assert [str(r.id) for r in rows] == [COMMITMENT["id"]]
        assert rows[0].user_id == "example-user"
        assert seen[0].url.path == "/api/commitments/export"
        assert seen[0].url.params["created_after"].startswith("2026-06-01T00:00:00")
        assert seen[0].headers["authorization"] == f"Bearer {TOKEN}"

    # @verifies REQ-0210
    async def test_an_empty_list_is_an_empty_result(self, mock_http):
        mock_http(_answer(200, json=[]))

        assert await _admin().export_commitments() == []


class TestExportCommitmentsRefusals:
    # @verifies REQ-0210
    @pytest.mark.parametrize("status", [401, 403, 404, 422, 500, 503])
    async def test_a_non_2xx_raises_with_its_status(self, mock_http, status):
        mock_http(_answer(status, json={"detail": BODY_MARKER}))

        with pytest.raises(FlexibilityApiError) as caught:
            await _admin().export_commitments()

        assert caught.value.status_code == status
        assert str(status) in str(caught.value)

    # @verifies REQ-0210
    async def test_a_proxy_page_raises_rather_than_failing_to_decode(self, mock_http):
        mock_http(_answer(502, text=f"<html>{BODY_MARKER}</html>"))

        with pytest.raises(FlexibilityApiError) as caught:
            await _admin().export_commitments()

        assert caught.value.status_code == 502

    # @verifies REQ-0210
    @pytest.mark.parametrize("status", [403, 500])
    async def test_the_message_carries_no_token_and_no_body(self, mock_http, status):
        mock_http(_answer(status, json={"detail": BODY_MARKER, "token": TOKEN}))

        with pytest.raises(FlexibilityApiError) as caught:
            await _admin().export_commitments()

        rendered = str(caught.value) + repr(caught.value)
        assert TOKEN not in rendered
        assert BODY_MARKER not in rendered
        # Nothing chained underneath carries the body into a traceback either.
        assert caught.value.__cause__ is None
        assert caught.value.__suppress_context__ or caught.value.__context__ is None


class TestExportCommitmentsUnreadable:
    # @verifies REQ-0210
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"json": None},
            {"json": {"items": [COMMITMENT]}},
            {"text": "not json"},
            {"json": [{"id": "not-a-commitment"}]},
        ],
        ids=["null", "object", "not-json", "malformed-item"],
    )
    async def test_a_200_that_is_not_a_list_of_commitments_raises(
        self, mock_http, kwargs
    ):
        mock_http(_answer(200, **kwargs))

        with pytest.raises(FlexibilityApiError) as caught:
            await _admin().export_commitments()

        assert caught.value.status_code == 200
        assert TOKEN not in str(caught.value)


async def test_the_error_is_importable_without_the_client():
    assert FlexibilityApiError is _FromErrors
