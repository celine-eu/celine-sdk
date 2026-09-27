"""Tests for `celine.sdk.rec_registry` — docs/specifications/rec-registry-client.md.

The batch asset lookups and the meter writes (`put_asset`, `delete_asset`), which
is what that document specifies. The seam is
`mock_http`: the generated client builds its own `httpx.AsyncClient`, so the
class is what gets replaced, and everything this repository owns — chunking, the
refusal check, the schema conversion, reading the registry's refusal `code` —
runs against real responses.
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


def _member(key: str, *, did: str, pods: tuple[str, ...] = ()) -> dict:
    return {
        "area": "north",
        "community_key": "cer-1",
        "community_name": "CER One",
        "delivery_points": [{"id": p, "type": "pod"} for p in pods],
        "did": did,
        "id": f"id-{key}",
        "key": key,
        "name": f"Member {key}",
        "role": "consumer",
        "status": "active",
        "user_id": f"u-{key}",
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


class TestTheDidBatch:
    """The third batch route, and the first that answers members.

    It shares the helper with the two asset lookups, so what is tested here is
    what sharing must not have broken — the bound, the refusal rule and the
    empty batch — plus the one thing that is genuinely different: the shape of
    the answer.
    """

    # @verifies REQ-0124
    async def test_it_resolves_dids_to_members(self, mock_http):
        seen = mock_http(_rows([_member("m-1", did="did:web:x:alice")]))

        members = await _client().lookup_members_by_dids(["did:web:x:alice"])

        assert seen[0].url.path == "/admin/lookup/members-by-dids"
        assert json.loads(seen[0].content)["dids"] == ["did:web:x:alice"]
        assert [m.key for m in members] == ["m-1"]

    # @verifies REQ-0124
    async def test_every_row_carries_the_did_it_answers(self, mock_http):
        """Without it the caller cannot attribute a row back to the DID it asked
        about, which is the entire purpose of a batch form."""
        mock_http(_rows([_member("m-1", did="did:web:x:alice")]))

        members = await _client().lookup_members_by_dids(["did:web:x:alice"])

        assert [m.did for m in members] == ["did:web:x:alice"]

    # @verifies REQ-0124
    async def test_the_supply_point_arrives_without_any_asset(self, mock_http):
        """The reason this route is member-shaped. A participant registered but
        not yet metered has a declared POD and no asset at all, so an
        asset-shaped answer would be empty for exactly the population a
        consent-gated export is authorised over."""
        mock_http(_rows([_member("m-1", did="did:web:x:alice", pods=("IT-DP-1",))]))

        members = await _client().lookup_members_by_dids(["did:web:x:alice"])

        assert [dp.id for dp in members[0].delivery_points] == ["IT-DP-1"]

    # @verifies REQ-0124
    # @verifies REQ-0120
    async def test_a_refusal_raises_rather_than_answering_an_empty_list(
        self, mock_http
    ):
        """The hazard the helper is shared for: on this route too, an empty list
        is a real answer the service gives on purpose."""
        mock_http(_status(422, VALIDATION_ERROR))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().lookup_members_by_dids(["did:web:x:alice"])

        assert excinfo.value.status_code == 422
        assert "members-by-dids" in str(excinfo.value)

    # @verifies REQ-0124
    # @verifies REQ-0121
    async def test_a_batch_over_the_bound_is_split_and_concatenated_in_order(
        self, mock_http
    ):
        seen = mock_http(
            _rows([_member("a", did="did:a")], [_member("b", did="did:b")])
        )
        dids = [f"did:web:x:{n}" for n in range(MAX_BATCH_LOOKUP_IDS + 1)]

        members = await _client().lookup_members_by_dids(dids)

        sent = [json.loads(r.content)["dids"] for r in seen]
        assert [len(chunk) for chunk in sent] == [MAX_BATCH_LOOKUP_IDS, 1]
        assert [d for chunk in sent for d in chunk] == dids
        assert [m.key for m in members] == ["a", "b"]

    # @verifies REQ-0124
    # @verifies REQ-0122
    async def test_an_empty_batch_asks_nothing(self, mock_http):
        seen = mock_http(_rows())

        assert await _client().lookup_members_by_dids([]) == []
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


# ── Meter writes (REQ-0125 – REQ-0127) ──────────────────────────────────────

METER_PATH = "/admin/communities/example-rec/members/ex-00001/assets/meter-SEN-1"


def _meter_body(sensor_id: str = "SEN-1") -> dict:
    return {
        "key": f"meter-{sensor_id}",
        "asset_type": "meter",
        "properties": {
            "name": "Main meter",
            "sensor_id": sensor_id,
            "meter_type": "consumption",
        },
    }


def _stored(sensor_id: str = "SEN-1") -> dict:
    return {
        "id": "7f2c",
        "key": f"meter-{sensor_id}",
        "asset_type": "meter",
        "name": "Main meter",
        "sensor_id": sensor_id,
        "properties": {"meter_type": "consumption"},
        "device": {},
        "relationships": {},
        "owner_key": "ex-00001",
        "owner_user_id": "user-1",
        "extra": {},
        "created_at": "2026-09-27T10:00:00Z",
        "updated_at": "2026-09-27T10:00:00Z",
    }


def _refusal(status: int, detail, code: str | None = None):
    body = {"detail": detail}
    if code is not None:
        body["code"] = code
    return _status(status, body)


def _bare_generated_client():
    from celine.sdk.openapi.rec_registry import Client

    return Client(base_url="http://registry.test", raise_on_unexpected_status=False)


def _raw(status: int, content: bytes, content_type: str = "text/html"):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status, content=content, headers={"content-type": content_type}
        )

    return handle


class TestAttachingAMeter:
    # @verifies REQ-0125
    async def test_it_puts_one_asset_at_the_key_the_caller_gives(self, mock_http):
        seen = mock_http(_rows(_stored()))

        await _client().put_asset(
            "example-rec", "ex-00001", "meter-SEN-1", _meter_body(), token="tok-meter"
        )

        assert len(seen) == 1
        assert seen[0].method == "PUT"
        assert seen[0].url.path == METER_PATH
        assert seen[0].headers["authorization"] == "Bearer tok-meter"

    # @verifies REQ-0125
    async def test_the_body_is_sent_as_given_with_nothing_added(self, mock_http):
        seen = mock_http(_rows(_stored()))

        await _client().put_asset(
            "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
        )

        assert json.loads(seen[0].content) == _meter_body()

    # @verifies REQ-0125
    async def test_a_generated_asset_upsert_is_sent_the_same_way(self, mock_http):
        from celine.sdk.openapi.rec_registry.models import AssetUpsert

        seen = mock_http(_rows(_stored()))

        await _client().put_asset(
            "example-rec",
            "ex-00001",
            "meter-SEN-1",
            AssetUpsert.from_dict(_meter_body()),
        )

        assert json.loads(seen[0].content) == _meter_body()

    # @verifies REQ-0125
    async def test_the_key_and_the_sensor_id_are_neither_composed_nor_trimmed(
        self, mock_http
    ):
        """The convention and the trimmed comparison are the registry's; a
        second copy here would be the one that drifts."""
        seen = mock_http(_rows(_stored()))
        body = _meter_body()
        body["properties"]["sensor_id"] = "  SEN-1 "

        await _client().put_asset("example-rec", "ex-00001", "any-key", body)

        assert seen[0].url.path.endswith("/assets/any-key")
        sent = json.loads(seen[0].content)
        assert sent["key"] == "meter-SEN-1"
        assert sent["properties"]["sensor_id"] == "  SEN-1 "

    # @verifies REQ-0125
    async def test_it_answers_the_stored_asset_as_a_schema(self, mock_http):
        mock_http(_rows(_stored()))

        asset = await _client().put_asset(
            "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
        )

        assert asset.key == "meter-SEN-1"
        assert asset.asset_type == "meter"
        assert asset.sensor_id == "SEN-1"
        assert asset.properties == {"meter_type": "consumption"}

    # @verifies REQ-0125
    async def test_an_attach_that_changes_nothing_still_answers_the_asset(
        self, mock_http
    ):
        """Attaching the same sensor to the same member again is the
        registry's no-op `200`; the wrapper does not turn it into an error."""
        seen = mock_http(_rows(_stored(), _stored()))
        client = _client()

        first = await client.put_asset(
            "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
        )
        second = await client.put_asset(
            "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
        )

        assert first == second
        assert len(seen) == 2

    # @verifies REQ-0125
    async def test_it_answers_the_generated_asset_detail_the_get_answers(
        self, mock_http
    ):
        """Registry 1.6.0 declares `AssetDetail` on the `PUT`, as on the asset
        `GET`; the wrapper answers the generated schema, not one of its own."""
        from celine.sdk.openapi.rec_registry.schemas import AssetDetailSchema
        from celine.sdk.rec_registry import AssetDetailSchema as exported

        mock_http(_rows(_stored()))

        asset = await _client().put_asset(
            "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
        )

        assert exported is AssetDetailSchema
        assert type(asset) is AssetDetailSchema
        assert asset.owner_key == "ex-00001"
        assert asset.owner_user_id == "user-1"
        assert asset.created_at == "2026-09-27T10:00:00Z"

    # @verifies REQ-0125
    async def test_a_key_the_registry_adds_later_does_not_fail_the_caller(
        self, mock_http
    ):
        stored = _stored()
        stored["some_future_field"] = "x"
        mock_http(_rows(stored))

        asset = await _client().put_asset(
            "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
        )

        assert asset.key == "meter-SEN-1"

    # @verifies REQ-0125
    def test_the_generated_put_parses_its_200_as_asset_detail(self):
        """Guards the regeneration: the generated operation reads the `200`
        into `AssetDetail`, no longer `Any`."""
        from celine.sdk.openapi.rec_registry.api.admin import (
            upsert_asset_admin_communities_community_key_members_member_key_assets_asset_key_put as op,
        )
        from celine.sdk.openapi.rec_registry.models import AssetDetail

        parsed = op._parse_response(
            client=_bare_generated_client(),
            response=httpx.Response(200, json=_stored()),
        )

        assert isinstance(parsed, AssetDetail)


class TestDetachingAMeter:
    # @verifies REQ-0126
    async def test_it_deletes_that_one_asset_and_answers_nothing(self, mock_http):
        seen = mock_http(lambda request: httpx.Response(204))

        result = await _client().delete_asset(
            "example-rec", "ex-00001", "meter-SEN-1", token="tok-meter"
        )

        assert result is None
        assert len(seen) == 1
        assert seen[0].method == "DELETE"
        assert seen[0].url.path == METER_PATH
        assert seen[0].headers["authorization"] == "Bearer tok-meter"
        assert seen[0].content == b""

    # @verifies REQ-0126
    # @verifies REQ-0127
    async def test_an_asset_the_member_does_not_hold_is_raised_not_swallowed(
        self, mock_http
    ):
        """Whether "already detached" is success is the caller's decision."""
        mock_http(_refusal(404, "Asset 'meter-SEN-1' not found", "asset_not_found"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().delete_asset("example-rec", "ex-00001", "meter-SEN-1")

        assert excinfo.value.status_code == 404
        assert excinfo.value.code == "asset_not_found"

    # @verifies REQ-0126
    # @verifies REQ-0127
    async def test_a_member_that_is_gone_is_told_apart_from_a_detached_meter(
        self, mock_http
    ):
        mock_http(_refusal(404, "Member 'ex-00001' not found", "member_not_found"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().delete_asset("example-rec", "ex-00001", "meter-SEN-1")

        assert excinfo.value.code == "member_not_found"

    # @verifies REQ-0126
    async def test_a_200_is_not_the_answer_a_delete_expects(self, mock_http):
        """Only `204` is success: anything else raises, so a proxy or an older
        service answering something unexpected is never read as detached."""
        mock_http(_rows({}))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().delete_asset("example-rec", "ex-00001", "meter-SEN-1")

        assert excinfo.value.status_code == 200


class TestARefusedWriteCarriesTheCode:
    # @verifies REQ-0127
    async def test_sensor_held_arrives_as_the_top_level_code(self, mock_http):
        sentence = "The sensor is held by another active member"
        mock_http(_refusal(409, sentence, "sensor_held"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        error = excinfo.value
        assert error.status_code == 409
        assert error.code == "sensor_held"
        assert error.detail == sentence
        assert b"sensor_held" in error.body

    # @verifies REQ-0127
    async def test_the_code_is_a_plain_string_not_an_enum(self, mock_http):
        mock_http(_refusal(409, "held", "sensor_held"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert type(excinfo.value.code) is str

    # @verifies REQ-0127
    async def test_a_code_the_registry_adds_later_does_not_fail_the_caller(
        self, mock_http
    ):
        mock_http(_refusal(409, "A rule from a newer registry", "some_future_rule"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.code == "some_future_rule"

    # @verifies REQ-0127
    async def test_asset_key_taken_is_its_own_code(self, mock_http):
        mock_http(_refusal(409, "Asset key taken", "asset_key_taken"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.code == "asset_key_taken"

    # @verifies REQ-0127
    async def test_asset_key_too_long_is_its_own_code(self, mock_http):
        """Registry 1.6.0 refuses a key over its 128 characters with a coded
        `422`, beside the list-shaped validation `422` on the same route."""
        mock_http(_refusal(422, "Asset key is 129 characters", "asset_key_too_long"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.status_code == 422
        assert excinfo.value.code == "asset_key_too_long"

    # @verifies REQ-0127
    def test_the_generated_422_reads_a_validation_body_as_an_error_response(self):
        """Why the wrapper reads the raw body: the generated `oneOf` parse
        tries `ErrorResponse` first, and it accepts a list `detail` with no
        `code`. Which model came back does not tell the two 422s apart."""
        from celine.sdk.openapi.rec_registry.api.admin import (
            admin_import_admin_import_post as op,
        )
        from celine.sdk.openapi.rec_registry.models import ErrorResponse
        from celine.sdk.openapi.rec_registry.types import Unset

        parsed = op._parse_response(
            client=_bare_generated_client(),
            response=httpx.Response(422, json=VALIDATION_ERROR),
        )

        assert isinstance(parsed, ErrorResponse)
        assert isinstance(parsed.code, Unset)
        assert RecRegistryApiError.refusal_of(
            json.dumps(VALIDATION_ERROR).encode()
        ) == (None, VALIDATION_ERROR["detail"])

    # @verifies REQ-0127
    async def test_a_validation_422_raises_with_no_code(self, mock_http):
        mock_http(_status(422, VALIDATION_ERROR))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.status_code == 422
        assert excinfo.value.code is None
        assert excinfo.value.detail == VALIDATION_ERROR["detail"]

    # @verifies REQ-0127
    async def test_a_refusal_with_a_sentence_and_no_code_has_code_none(
        self, mock_http
    ):
        mock_http(_refusal(422, "Invalid meter asset: sensor_id is blank"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.code is None
        assert excinfo.value.detail == "Invalid meter asset: sensor_id is blank"

    # @verifies REQ-0127
    async def test_a_code_nested_inside_detail_is_not_the_registrys_shape(
        self, mock_http
    ):
        """Onboarding nests its code inside `detail`; the registry does not,
        and this wrapper reads only the registry's shape."""
        mock_http(
            _status(409, {"detail": {"code": "sensor_held", "message": "held"}})
        )

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.code is None

    # @verifies REQ-0127
    async def test_the_sentence_is_never_parsed_for_a_code(self, mock_http):
        mock_http(_refusal(409, "sensor_held"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.code is None

    # @verifies REQ-0127
    async def test_an_undeclared_status_raises_the_wrappers_error(self, mock_http):
        """`403` is not in the route's spec; the generated layer's
        `UnexpectedStatus` must not reach the caller."""
        mock_http(_status(403, {"detail": "forbidden"}))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert not isinstance(excinfo.value, UnexpectedStatus)
        assert excinfo.value.status_code == 403
        assert excinfo.value.code is None

    # @verifies REQ-0127
    async def test_a_body_that_is_not_json_still_raises_the_wrappers_error(
        self, mock_http
    ):
        mock_http(_raw(502, b"<html>Bad gateway</html>"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().delete_asset("example-rec", "ex-00001", "meter-SEN-1")

        assert excinfo.value.status_code == 502
        assert excinfo.value.code is None
        assert excinfo.value.detail is None

    # @verifies REQ-0127
    async def test_an_unreadable_200_raises_rather_than_answering_nothing(
        self, mock_http
    ):
        mock_http(_raw(200, b"not json"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_asset(
                "example-rec", "ex-00001", "meter-SEN-1", _meter_body()
            )

        assert excinfo.value.status_code == 200

    # @verifies REQ-0127
    async def test_the_error_keeps_status_and_body_positionally(self):
        """A caller of the batch lookups that builds or catches the error is
        unchanged: `code` and `detail` are keyword-only additions."""
        error = RecRegistryApiError("refused", 422, b"{}")

        assert (error.status_code, error.body) == (422, b"{}")
        assert error.code is None
        assert error.detail is None
