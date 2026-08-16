"""Tests for `celine.sdk.ai_assistant` — docs/specifications/spec-management.md.

The point of these is the delegation itself: that each wrapper method reaches
the route the generated client builds, carrying the caller's token. `mock_http`
replaces `httpx.AsyncClient`, which catches both paths — the generated client
constructs one internally, and the two non-delegating methods construct their
own.
"""

from __future__ import annotations

import json

import httpx
import pytest

from celine.sdk.ai_assistant import AssistantClient

pytestmark = pytest.mark.asyncio


def _json_ok(payload):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    return handle


def _client() -> AssistantClient:
    return AssistantClient("http://assistant.test", default_token="tok-default")


class TestDelegation:
    # @verifies REQ-0114
    @pytest.mark.parametrize(
        "call,method,path,payload",
        [
            ("list_conversations", "GET", "/conversations", [{"id": "c1"}]),
            ("list_attachments", "GET", "/attachments", [{"id": "a1"}]),
            ("get_user", "GET", "/user", {"user_id": "u1"}),
            ("health", "GET", "/health", {"status": "ok"}),
        ],
    )
    async def test_a_no_argument_route_is_reached_through_the_generated_client(
        self, mock_http, call, method, path, payload
    ):
        seen = mock_http(_json_ok(payload))
        result = await getattr(_client(), call)()
        assert (seen[0].method, seen[0].url.path) == (method, path)
        assert seen[0].headers["authorization"] == "Bearer tok-default"
        assert result == payload

    # @verifies REQ-0114
    async def test_a_path_parameter_is_placed_in_the_url(self, mock_http):
        seen = mock_http(_json_ok([{"role": "user"}]))
        result = await _client().get_conversation_messages("conv-42")
        assert seen[0].url.path == "/conversations/conv-42/messages"
        assert result == [{"role": "user"}]

    # @verifies REQ-0114
    @pytest.mark.parametrize(
        "call,arg,path",
        [
            ("delete_conversation", "conv-42", "/conversations/conv-42"),
            ("delete_attachment", "att-7", "/attachments/att-7"),
        ],
    )
    async def test_a_delete_returns_nothing_and_hits_its_route(
        self, mock_http, call, arg, path
    ):
        seen = mock_http(lambda r: httpx.Response(204))
        assert await getattr(_client(), call)(arg) is None
        assert (seen[0].method, seen[0].url.path) == ("DELETE", path)

    # @verifies REQ-0114
    async def test_an_upload_is_sent_as_multipart_with_the_filename(
        self, mock_http, tmp_path
    ):
        seen = mock_http(_json_ok({"id": "att-1", "status": "stored"}))
        source = tmp_path / "reading.csv"
        source.write_bytes(b"kwh,ts\n1.5,2026-01-01\n")

        result = await _client().upload(source, content_type="text/csv")

        assert (seen[0].method, seen[0].url.path) == ("POST", "/upload")
        assert seen[0].headers["content-type"].startswith("multipart/form-data")
        body = seen[0].content
        assert b"reading.csv" in body
        assert b"kwh,ts" in body
        assert result == {"id": "att-1", "status": "stored"}

    # @verifies REQ-0114
    async def test_a_per_call_token_overrides_the_default(self, mock_http):
        seen = mock_http(_json_ok([]))
        await _client().list_conversations(token="tok-caller")
        assert seen[0].headers["authorization"] == "Bearer tok-caller"

    # @verifies REQ-0114
    async def test_no_token_at_all_is_refused_before_any_request(self, mock_http):
        """Per-request usage means the token is usually the caller's; asking for
        one that was never supplied must not go out as an anonymous request.
        """
        seen = mock_http(_json_ok([]))
        with pytest.raises(ValueError, match="No token"):
            await AssistantClient("http://assistant.test").list_conversations()
        assert seen == []

    # @verifies REQ-0114
    async def test_a_failed_request_raises_rather_than_returning_none(self, mock_http):
        """`raise_on_unexpected_status` is set, so a 500 is an exception and not a
        `parsed` of `None` that reads like an empty result.
        """
        from celine.sdk.openapi.ai_assistant.errors import UnexpectedStatus

        mock_http(lambda r: httpx.Response(500, text="boom"))
        with pytest.raises(UnexpectedStatus):
            await _client().list_conversations()


class TestNotDelegated:
    """The two methods the generated client cannot express."""

    # @verifies REQ-0114
    async def test_a_raw_attachment_is_returned_as_bytes(self, mock_http):
        """Delegating this one would call `response.json()` on a file."""
        blob = b"\x89PNG\r\n\x1a\n not json at all"
        seen = mock_http(lambda r: httpx.Response(200, content=blob))
        result = await _client().get_attachment_raw("att-7")
        assert result == blob
        assert seen[0].url.path == "/attachments/att-7/raw"
        assert seen[0].headers["authorization"] == "Bearer tok-default"

    # @verifies REQ-0114
    async def test_a_chat_stream_is_parsed_frame_by_frame(self, mock_http):
        stream = (
            'event: meta\ndata: {"conversation_id": "c1"}\n\n'
            'event: token\ndata: {"text": "hel"}\n\n'
            'event: token\ndata: {"text": "lo"}\n\n'
            "event: done\ndata: [DONE]\n\n"
        )
        mock_http(lambda r: httpx.Response(200, text=stream))

        events = [e async for e in _client().chat_stream({"message": "hi"})]

        assert [e["type"] for e in events] == ["meta", "token", "token", "done"]
        assert events[0]["data"] == {"conversation_id": "c1"}
        assert "".join(e["data"]["text"] for e in events[1:3]) == "hello"
        # A data line that is not JSON survives as the raw string.
        assert events[3]["data"] == "[DONE]"

    # @verifies REQ-0114
    async def test_a_stream_that_fails_raises_before_yielding(self, mock_http):
        mock_http(lambda r: httpx.Response(403, text="nope"))
        with pytest.raises(httpx.HTTPStatusError):
            async for _ in _client().chat_stream({"message": "hi"}):
                pass

    # @verifies REQ-0114
    async def test_the_stream_body_is_the_payload_it_was_given(self, mock_http):
        seen = mock_http(lambda r: httpx.Response(200, text="event: done\ndata: {}\n\n"))
        async for _ in _client().chat_stream({"message": "hi", "conversation_id": "c1"}):
            pass
        assert json.loads(seen[0].content) == {"message": "hi", "conversation_id": "c1"}
        assert seen[0].url.path == "/chat"
