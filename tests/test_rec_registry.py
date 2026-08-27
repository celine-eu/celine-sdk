"""Tests for `celine.sdk.rec_registry` — docs/specifications/rec-registry-client.md.

Only the batch asset lookups, which is all that document specifies. The seam is
`mock_http`: the generated client builds its own `httpx.AsyncClient`, so the
class is what gets replaced, and everything this repository owns — chunking, the
refusal check, the schema conversion — runs against real responses.
"""

from __future__ import annotations

import json

import httpx
import pytest

from celine.sdk.openapi.rec_registry.errors import UnexpectedStatus
from celine.sdk.rec_registry import (
    MAX_BATCH_LOOKUP_IDS,
    RecRegistryAdminClient,
    RecRegistryApiError,
)

pytestmark = pytest.mark.asyncio


def _client() -> RecRegistryAdminClient:
    return RecRegistryAdminClient("http://registry.test", default_token="tok-admin")


def _asset(key: str, *, sensor_id: str | None = None, owner: str = "u-1") -> dict:
    return {
        "asset_type": "meter",
        "community_key": "cer-1",
        "community_name": "CER One",
        "id": f"id-{key}",
        "key": key,
        "name": f"Asset {key}",
        "owner_key": "m-1",
        "owner_user_id": owner,
        "sensor_id": sensor_id,
    }


def _rows(*payloads):
    """Answer each request with the next payload, `200`."""
    remaining = list(payloads)

    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=remaining.pop(0))

    return handle


def _status(code: int, payload):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(code, json=payload)

    return handle


VALIDATION_ERROR = {
    "detail": [
        {
            "loc": ["body", "user_ids"],
            "msg": "List should have at most 500 items",
            "type": "too_long",
        }
    ]
}


class TestRefusalIsNotAnEmptyResult:
    # @verifies REQ-0120
    async def test_a_422_raises_rather_than_answering_an_empty_list(self, mock_http):
        mock_http(_status(422, VALIDATION_ERROR))
        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().lookup_assets_by_user_ids(["u-1", "u-2"])
        assert excinfo.value.status_code == 422
        assert "assets-by-user-ids" in str(excinfo.value)
        assert b"at most 500" in excinfo.value.body

    # @verifies REQ-0120
    async def test_the_sensor_id_batch_raises_the_same_way(self, mock_http):
        mock_http(_status(422, VALIDATION_ERROR))
        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().lookup_assets_by_sensor_ids(["s-1"])
        assert excinfo.value.status_code == 422
        assert "assets-by-sensor-ids" in str(excinfo.value)

    # @verifies REQ-0120
    async def test_an_empty_answer_from_the_service_is_still_an_empty_list(
        self, mock_http
    ):
        """The two the service conflates on purpose stay conflated, and stay a
        result: nothing here turns "no rows" into a failure."""
        mock_http(_rows([]))
        assert await _client().lookup_assets_by_user_ids(["nobody"]) == []

    # @verifies REQ-0120
    async def test_a_missing_grant_is_not_flattened_into_an_empty_list(self, mock_http):
        """`403` is not one of the two statuses the route documents, so
        `raise_on_unexpected_status` catches it in the generated layer before
        this wrapper sees it. Pinned because the alternative — parsing to
        `None` — is the other way #41 produced an empty list."""
        mock_http(_status(403, {"detail": "forbidden"}))
        with pytest.raises(UnexpectedStatus):
            await _client().lookup_assets_by_user_ids(["u-1"])


class TestTheBoundIsChunked:
    # @verifies REQ-0121
    async def test_the_bound_matches_the_service(self):
        assert MAX_BATCH_LOOKUP_IDS == 500

    # @verifies REQ-0121
    async def test_a_batch_at_the_bound_is_one_request(self, mock_http):
        seen = mock_http(_rows([_asset("a")]))
        ids = [f"u-{n}" for n in range(MAX_BATCH_LOOKUP_IDS)]
        assets = await _client().lookup_assets_by_user_ids(ids)
        assert len(seen) == 1
        assert len(json.loads(seen[0].content)["user_ids"]) == MAX_BATCH_LOOKUP_IDS
        assert [a.key for a in assets] == ["a"]

    # @verifies REQ-0121
    async def test_a_batch_over_the_bound_is_split_and_concatenated_in_order(
        self, mock_http
    ):
        seen = mock_http(_rows([_asset("a")], [_asset("b")], [_asset("c")]))
        ids = [f"s-{n}" for n in range(MAX_BATCH_LOOKUP_IDS * 2 + 1)]
        assets = await _client().lookup_assets_by_sensor_ids(ids)

        sent = [json.loads(r.content)["sensor_ids"] for r in seen]
        assert [len(chunk) for chunk in sent] == [MAX_BATCH_LOOKUP_IDS, MAX_BATCH_LOOKUP_IDS, 1]
        assert [i for chunk in sent for i in chunk] == ids
        assert [a.key for a in assets] == ["a", "b", "c"]

    # @verifies REQ-0121
    # @verifies REQ-0120
    async def test_a_refusal_of_a_later_chunk_is_not_hidden_by_earlier_rows(
        self, mock_http
    ):
        """The dangerous shape: 500 ids resolve, the next request is refused.
        Answering with the rows collected so far would be a partial result
        wearing a complete one's clothes."""
        answers = [
            httpx.Response(200, json=[_asset("a")]),
            httpx.Response(422, json=VALIDATION_ERROR),
        ]

        def handle(request: httpx.Request) -> httpx.Response:
            return answers.pop(0)

        mock_http(handle)
        with pytest.raises(RecRegistryApiError):
            await _client().lookup_assets_by_user_ids(
                [f"u-{n}" for n in range(MAX_BATCH_LOOKUP_IDS + 1)]
            )

    # @verifies REQ-0122
    async def test_an_empty_batch_asks_nothing(self, mock_http):
        seen = mock_http(_rows())
        assert await _client().lookup_assets_by_user_ids([]) == []
        assert await _client().lookup_assets_by_sensor_ids([]) == []
        assert seen == []


class TestTheMirrorPair:
    # @verifies REQ-0123
    async def test_the_singular_name_still_reaches_the_same_route(self, mock_http):
        seen = mock_http(_rows([_asset("a", sensor_id="s-1")]))
        assets = await _client().lookup_asset_by_sensor_ids(sensor_ids=["s-1"])
        assert seen[0].url.path == "/admin/lookup/assets-by-sensor-ids"
        assert [a.sensor_id for a in assets] == ["s-1"]

    # @verifies REQ-0123
    async def test_both_names_are_present_on_the_client(self):
        assert hasattr(RecRegistryAdminClient, "lookup_assets_by_sensor_ids")
        assert hasattr(RecRegistryAdminClient, "lookup_asset_by_sensor_ids")

    # @verifies REQ-0121
    async def test_the_caller_token_reaches_every_chunk(self, mock_http):
        seen = mock_http(_rows([], []))
        await _client().lookup_assets_by_user_ids(
            [f"u-{n}" for n in range(MAX_BATCH_LOOKUP_IDS + 1)], token="tok-caller"
        )
        assert [r.headers["authorization"] for r in seen] == [
            "Bearer tok-caller",
            "Bearer tok-caller",
        ]
