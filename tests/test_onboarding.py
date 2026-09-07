"""Tests for `celine.sdk.onboarding`.

The seam is `mock_http`: the generated client builds its own `httpx.AsyncClient`,
so the class is what gets replaced, and everything this repository owns — the
status mapping, the detail extraction, the schema conversion — runs against real
responses.

What is pinned here is the one way this wrapper differs from its siblings.
Onboarding's member surface answers **409 as an answer**, not as a fault: "there
is no decision here to make, and `state` says why". Its caller is a
backend-for-frontend that shows that sentence to a member, so the status code and
the service's own detail have to survive the wrapper.
"""

from __future__ import annotations

import json

import httpx
import pytest

from celine.sdk.onboarding import OnboardingApiError, OnboardingClient

pytestmark = pytest.mark.asyncio


def _client() -> OnboardingClient:
    return OnboardingClient("http://onboarding.test", default_token="tok-member")


STATUS_OK = {
    "has_identity": True,
    "state": "ok",
    "offers": [
        {
            "id": "household-energy-flexibility",
            "requires_consent": True,
            "granted": True,
            "evidence": {"consent_text_version": "1.0"},
            "decided_at": "2026-07-01T10:00:00Z",
        }
    ],
}

HISTORY_OK = {
    "has_identity": True,
    "state": "ok",
    "events": [{"event_type": "ConsentGranted"}],
}


def _answer(code: int, payload):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(code, json=payload)

    return handle


class TestReading:
    async def test_the_status_comes_back_as_a_schema(self, mock_http):
        mock_http(_answer(200, STATUS_OK))

        status = await _client().get_data_sharing()

        assert status.has_identity is True
        assert status.state.value == "ok"
        assert status.offers[0]["granted"] is True
        # The offer body is passed through as-is: the vocabulary is onboarding's
        # and a wrapper that named its fields would go stale against it.
        assert status.offers[0]["evidence"] == {"consent_text_version": "1.0"}

    async def test_the_member_token_goes_out(self, mock_http):
        seen = mock_http(_answer(200, STATUS_OK))

        await _client().get_data_sharing(token="tok-request")

        assert seen[0].headers["authorization"] == "Bearer tok-request"
        assert seen[0].url.path == "/api/me/data-sharing"

    async def test_no_identity_is_an_answer_not_an_error(self, mock_http):
        """Normal for a preregistered member who holds no credential yet."""
        mock_http(_answer(200, {"has_identity": False, "state": "no_identity"}))

        status = await _client().get_data_sharing()

        assert status.has_identity is False
        assert status.state.value == "no_identity"

    async def test_history(self, mock_http):
        seen = mock_http(_answer(200, HISTORY_OK))

        history = await _client().get_data_sharing_history()

        assert history.events[0]["event_type"] == "ConsentGranted"
        assert seen[0].url.path == "/api/me/data-sharing/history"


class TestDeciding:
    async def test_withdrawing_sends_the_decision(self, mock_http):
        seen = mock_http(_answer(200, STATUS_OK))

        await _client().set_data_sharing("household-energy-flexibility", enabled=False)

        assert seen[0].method == "POST"
        assert seen[0].url.path == "/api/me/data-sharing/household-energy-flexibility"
        assert json.loads(seen[0].read()) == {"enabled": False}

    async def test_granting_sends_the_decision(self, mock_http):
        seen = mock_http(_answer(200, STATUS_OK))

        await _client().set_data_sharing("household-energy-flexibility", enabled=True)

        assert json.loads(seen[0].read()) == {"enabled": True}


class TestRefusals:
    """The status and the sentence both survive, because both are the answer."""

    async def test_a_409_carries_the_code_and_the_detail(self, mock_http):
        mock_http(
            _answer(409, {"detail": "grid-operations is disclosed under a contract"})
        )

        with pytest.raises(OnboardingApiError) as raised:
            await _client().set_data_sharing("grid-operations", enabled=True)

        assert raised.value.status_code == 409
        assert raised.value.detail == "grid-operations is disclosed under a contract"

    async def test_an_unreachable_dataspace_is_a_503(self, mock_http):
        mock_http(_answer(503, {"detail": "Connector unreachable"}))

        with pytest.raises(OnboardingApiError) as raised:
            await _client().get_data_sharing()

        assert raised.value.status_code == 503
        assert raised.value.detail == "Connector unreachable"

    async def test_a_body_that_is_not_json_still_raises_with_the_code(self, mock_http):
        def handle(request: httpx.Request) -> httpx.Response:
            return httpx.Response(502, content=b"<html>gateway</html>")

        mock_http(handle)

        with pytest.raises(OnboardingApiError) as raised:
            await _client().get_data_sharing()

        assert raised.value.status_code == 502
        assert raised.value.detail is None

    async def test_a_validation_error_is_not_returned_as_a_result(self, mock_http):
        """422 is declared in the spec, so the generated client parses it into a
        model rather than leaving `parsed` empty. It is still a refusal."""
        mock_http(
            _answer(
                422,
                {"detail": [{"loc": ["body"], "msg": "nope", "type": "value_error"}]},
            )
        )

        with pytest.raises(OnboardingApiError) as raised:
            await _client().set_data_sharing("x", enabled=True)

        assert raised.value.status_code == 422


class TestTokens:
    async def test_no_token_at_all_is_refused_before_any_request(self, mock_http):
        seen = mock_http(_answer(200, STATUS_OK))

        with pytest.raises(ValueError):
            await OnboardingClient("http://onboarding.test").get_data_sharing()

        assert seen == []
