"""Tests for `celine.sdk.rec_registry` — docs/specifications/rec-registry-client.md.

The batch asset lookups, the meter writes (`put_asset`, `delete_asset`), the
profile write (`patch_member_profile`), the area and topology writes with the
community read (`put_area`, `delete_area`, `put_topology_node`,
`delete_topology_node`, `read_community`), the area rename (`rename_area`), the per-field member writes
(`put_member_name`, `put_member_role`, `put_member_area`), the delivery-point
writes (`put_delivery_point`, `delete_delivery_point`, `upsert_delivery_point`'s
`replaces`) and the self-service refusals, which
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


# ── Profile write (REQ-0128) ────────────────────────────────────────────────

PROFILE_PATH = "/admin/communities/example-rec/members/ex-00001/profile"


def _member_detail(role: str = "prosumer", area: str = "area-1") -> dict:
    return {
        "id": "4b1d",
        "key": "ex-00001",
        "name": "Member One",
        "user_id": "user-1",
        "did": None,
        "role": role,
        "status": "active",
        "area": area,
        "extra": {},
        "delivery_points": [],
        "created_at": "2026-09-27T10:00:00Z",
        "updated_at": "2026-09-27T11:00:00Z",
    }


class TestTheProfileWrite:
    # @verifies REQ-0128
    async def test_it_patches_the_profile_route_and_never_the_general_one(
        self, mock_http
    ):
        seen = mock_http(_rows(_member_detail()))

        await _client().patch_member_profile(
            "example-rec", "ex-00001", role="prosumer", token="tok-profile"
        )

        assert len(seen) == 1
        assert seen[0].method == "PATCH"
        assert seen[0].url.path == PROFILE_PATH
        assert seen[0].headers["authorization"] == "Bearer tok-profile"

    # @verifies REQ-0128
    @pytest.mark.parametrize(
        ("kwargs", "sent"),
        [
            ({"role": "prosumer"}, {"role": "prosumer"}),
            ({"area": "area-2"}, {"area": "area-2"}),
            (
                {"role": "consumer", "area": "area-2"},
                {"role": "consumer", "area": "area-2"},
            ),
        ],
    )
    async def test_the_body_is_only_the_keys_set_and_an_omitted_one_is_not_null(
        self, mock_http, kwargs, sent
    ):
        seen = mock_http(_rows(_member_detail()))

        await _client().patch_member_profile("example-rec", "ex-00001", **kwargs)

        assert json.loads(seen[0].content) == sent

    # @verifies REQ-0128
    async def test_it_has_no_parameter_for_any_other_member_field(self):
        import inspect

        params = set(
            inspect.signature(RecRegistryAdminClient.patch_member_profile).parameters
        )

        assert params == {"self", "community_key", "member_key", "role", "area", "token"}

    # @verifies REQ-0128
    async def test_another_member_field_cannot_be_smuggled_in(self, mock_http):
        seen = mock_http(_rows(_member_detail()))

        with pytest.raises(TypeError):
            await _client().patch_member_profile(  # type: ignore[call-arg]
                "example-rec", "ex-00001", role="prosumer", status="inactive"
            )

        assert seen == []

    # @verifies REQ-0128
    async def test_neither_role_nor_area_sends_nothing(self, mock_http):
        """An empty body would be the registry's uncoded `422`; there is
        nothing to show a manager, so it is refused before any request."""
        seen = mock_http(_rows(_member_detail()))

        with pytest.raises(ValueError):
            await _client().patch_member_profile("example-rec", "ex-00001")

        assert seen == []

    # @verifies REQ-0128
    async def test_it_answers_the_updated_member_as_a_schema(self, mock_http):
        from celine.sdk.openapi.rec_registry.schemas import MemberDetailSchema
        from celine.sdk.rec_registry import MemberDetailSchema as exported

        mock_http(_rows(_member_detail(role="prosumer", area="area-2")))

        member = await _client().patch_member_profile(
            "example-rec", "ex-00001", role="prosumer", area="area-2"
        )

        assert exported is MemberDetailSchema
        assert type(member) is MemberDetailSchema
        assert (member.key, member.role, member.area) == (
            "ex-00001",
            "prosumer",
            "area-2",
        )

    # @verifies REQ-0128
    # @verifies REQ-0127
    @pytest.mark.parametrize(
        ("status", "code"),
        [
            (422, "invalid_role"),
            (422, "unknown_area"),
            (404, "member_not_found"),
            (404, "community_not_found"),
            (409, "some_future_conflict"),
        ],
    )
    async def test_a_refusal_raises_with_the_registrys_code(
        self, mock_http, status, code
    ):
        mock_http(_refusal(status, "refused", code))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().patch_member_profile(
                "example-rec", "ex-00001", role="prosumer"
            )

        assert excinfo.value.status_code == status
        assert excinfo.value.code == code
        assert excinfo.value.detail == "refused"

    # @verifies REQ-0128
    # @verifies REQ-0127
    @pytest.mark.parametrize(
        "respond",
        [
            _status(422, VALIDATION_ERROR),
            _status(403, {"detail": "Forbidden"}),
            _raw(502, b"<html>Bad gateway</html>"),
        ],
    )
    async def test_a_refusal_that_names_no_code_raises_with_none(
        self, mock_http, respond
    ):
        """A validation `422`, a missing grant, a proxy's page: the wrapper's
        error, never the generated `UnexpectedStatus`, and no code."""
        mock_http(respond)

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().patch_member_profile(
                "example-rec", "ex-00001", area="area-2"
            )

        assert not isinstance(excinfo.value, UnexpectedStatus)
        assert excinfo.value.code is None

    # @verifies REQ-0128
    async def test_an_unreadable_200_raises_rather_than_answering_nothing(
        self, mock_http
    ):
        mock_http(_raw(200, b"not json"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().patch_member_profile(
                "example-rec", "ex-00001", role="consumer"
            )

        assert excinfo.value.status_code == 200

    # @verifies REQ-0128
    async def test_the_generated_profile_model_omits_what_is_unset(self):
        """Guards the regeneration: the generated body model drops an unset
        key rather than writing `null`, which the registry refuses."""
        from celine.sdk.openapi.rec_registry.models import MemberProfilePatch

        assert MemberProfilePatch(role="prosumer").to_dict() == {"role": "prosumer"}
        assert MemberProfilePatch(area="area-2").to_dict() == {"area": "area-2"}


# ── Regeneration guard: the area boundary (rec-registry REQ-0067/0068) ─────


class TestTheGeneratedAreaCarriesItsBoundary:
    """Guards the 1.6.0 regeneration, not a requirement of this SDK: the
    registry's area writes and reads carry `boundary` and `topology`, and a
    caller building an area through the generated models must be able to
    send and read both."""

    async def test_an_area_upsert_sends_its_boundary_and_one_node(self):
        from celine.sdk.openapi.rec_registry.models import AreaBoundaryIn, AreaUpsert

        area = AreaUpsert(
            name="Area One",
            boundary=AreaBoundaryIn(source="gse_cabine_primarie", id="AC000E00001"),
            topology=["AC000E00001"],
        )

        assert area.to_dict() == {
            "name": "Area One",
            "boundary": {"source": "gse_cabine_primarie", "id": "AC000E00001"},
            "topology": ["AC000E00001"],
        }

    async def test_a_read_area_parses_boundary_and_topology(self):
        from celine.sdk.openapi.rec_registry.schemas import AreaSchema

        area = AreaSchema.model_validate(
            {
                "name": "Area One",
                "boundary": {"source": "gse_cabine_primarie", "id": "AC000E00001"},
                "topology": ["AC000E00001"],
            }
        )
        legacy = AreaSchema.model_validate({"name": "Area Two"})

        assert (area.boundary.source, area.boundary.id) == (
            "gse_cabine_primarie",
            "AC000E00001",
        )
        assert area.topology == ["AC000E00001"]
        assert legacy.boundary is None

    async def test_the_error_vocabulary_names_invalid_area_boundary(self):
        from celine.sdk.openapi.rec_registry.models import ErrorCode

        assert ErrorCode("invalid_area_boundary").value == "invalid_area_boundary"


# ── Areas and topology: the onboarding template sync (REQ-0129–REQ-0131) ──


AREA_PATH = "/admin/communities/example-rec/areas/area-one"
NODE_PATH = "/admin/communities/example-rec/topology/AC000E00001"


def _area_body(node: str = "AC000E00001") -> dict:
    return {
        "name": "Area One",
        "boundary": {"source": "gse_cabine_primarie", "id": node},
        "topology": [node],
    }


def _node_body(node: str = "AC000E00001") -> dict:
    return {"id": node, "type": "primary_substation", "name": "Substation One"}


def _community(*, areas: dict | None = None, nodes: list | None = None) -> dict:
    return {
        "id": "c0ffee",
        "key": "example-rec",
        "name": "Example REC",
        "areas": {"area-one": _area_body()} if areas is None else areas,
        "topology": (
            [{**_node_body(), "operator_id": "op-1", "parent": None}]
            if nodes is None
            else nodes
        ),
    }


def _sync_client() -> RecRegistryAdminClient:
    """No default token: the sync passes its token per call (plan D37)."""
    return RecRegistryAdminClient("http://registry.test")


class TestReadingACommunity:
    # @verifies REQ-0129
    async def test_it_answers_areas_with_boundary_and_nodes_with_operator_id(
        self, mock_http
    ):
        seen = mock_http(_rows(_community()))

        community = await _sync_client().read_community(
            "example-rec", token="tok-read"
        )

        assert seen[0].method == "GET"
        assert seen[0].url.path == "/admin/communities/example-rec"
        assert seen[0].headers["authorization"] == "Bearer tok-read"
        area = community.areas["area-one"]
        assert (area.boundary.source, area.boundary.id) == (
            "gse_cabine_primarie",
            "AC000E00001",
        )
        assert area.topology == ["AC000E00001"]
        (node,) = community.topology
        assert (node.id, node.type, node.operator_id) == (
            "AC000E00001",
            "primary_substation",
            "op-1",
        )

    # @verifies REQ-0129
    async def test_a_missing_community_raises_and_is_not_an_empty_one(
        self, mock_http
    ):
        mock_http(_refusal(404, "Community not found"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().read_community("example-rec", token="tok-read")

        assert excinfo.value.status_code == 404
        assert excinfo.value.code is None

    # @verifies REQ-0129
    async def test_a_missing_grant_raises_the_wrappers_error(self, mock_http):
        """The policy middleware's `403` is undeclared: it must not arrive as
        the generated `UnexpectedStatus`."""
        mock_http(_refusal(403, "Forbidden"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().read_community("example-rec", token="tok-read")

        assert excinfo.value.status_code == 403
        assert not isinstance(excinfo.value, UnexpectedStatus)

    # @verifies REQ-0129
    async def test_an_unreadable_200_raises(self, mock_http):
        mock_http(_raw(200, b"<html>"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().read_community("example-rec", token="tok-read")

        assert excinfo.value.status_code == 200


class TestWritingAnArea:
    # @verifies REQ-0130
    async def test_it_puts_the_body_as_given_and_answers_the_community(
        self, mock_http
    ):
        seen = mock_http(_rows(_community()))

        community = await _sync_client().put_area(
            "example-rec", "area-one", _area_body(), token="tok-write"
        )

        assert len(seen) == 1
        assert seen[0].method == "PUT"
        assert seen[0].url.path == AREA_PATH
        assert seen[0].headers["authorization"] == "Bearer tok-write"
        assert json.loads(seen[0].content) == _area_body()
        assert community.key == "example-rec"
        assert list(community.areas) == ["area-one"]

    # @verifies REQ-0130
    async def test_a_generated_model_is_sent_unchanged(self, mock_http):
        from celine.sdk.openapi.rec_registry.models import AreaUpsert

        seen = mock_http(_rows(_community()))

        await _sync_client().put_area(
            "example-rec",
            "area-one",
            AreaUpsert.from_dict(_area_body()),
            token="tok-write",
        )

        assert json.loads(seen[0].content) == _area_body()

    # @verifies REQ-0130
    # @verifies REQ-0127
    async def test_invalid_area_boundary_arrives_as_the_code(self, mock_http):
        mock_http(
            _refusal(
                422,
                "An area references exactly one primary substation",
                "invalid_area_boundary",
            )
        )

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().put_area(
                "example-rec", "area-one", _area_body(), token="tok-write"
            )

        assert excinfo.value.status_code == 422
        assert excinfo.value.code == "invalid_area_boundary"

    # @verifies REQ-0130
    async def test_community_not_found_arrives_as_the_code(self, mock_http):
        mock_http(_refusal(404, "Community not found", "community_not_found"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().put_area(
                "example-rec", "area-one", _area_body(), token="tok-write"
            )

        assert excinfo.value.code == "community_not_found"

    # @verifies REQ-0130
    async def test_deleting_an_area_answers_the_community(self, mock_http):
        seen = mock_http(_rows(_community(areas={})))

        community = await _sync_client().delete_area(
            "example-rec", "area-one", token="tok-write"
        )

        assert seen[0].method == "DELETE"
        assert seen[0].url.path == AREA_PATH
        assert seen[0].content == b""
        assert community.areas == {}

    # @verifies REQ-0130
    # @verifies REQ-0127
    async def test_an_area_in_use_arrives_as_the_code_with_the_sentence(
        self, mock_http
    ):
        sentence = "Area 'area-one' is still referenced by 3 member(s); move them first"
        mock_http(_refusal(409, sentence, "area_in_use"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().delete_area(
                "example-rec", "area-one", token="tok-write"
            )

        assert excinfo.value.status_code == 409
        assert excinfo.value.code == "area_in_use"
        assert excinfo.value.detail == sentence

    # @verifies REQ-0130
    async def test_an_absent_area_is_raised_not_read_as_deleted(self, mock_http):
        mock_http(_refusal(404, "Area 'area-one' not found"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().delete_area(
                "example-rec", "area-one", token="tok-write"
            )

        assert excinfo.value.status_code == 404
        assert excinfo.value.code is None


class TestWritingATopologyNode:
    # @verifies REQ-0131
    async def test_it_puts_one_node_as_given_and_answers_the_community(
        self, mock_http
    ):
        seen = mock_http(_rows(_community()))

        community = await _sync_client().put_topology_node(
            "example-rec", "AC000E00001", _node_body(), token="tok-write"
        )

        assert len(seen) == 1
        assert seen[0].method == "PUT"
        assert seen[0].url.path == NODE_PATH
        assert seen[0].headers["authorization"] == "Bearer tok-write"
        assert json.loads(seen[0].content) == _node_body()
        assert [n.id for n in community.topology] == ["AC000E00001"]

    # @verifies REQ-0131
    async def test_a_body_id_differing_from_the_path_is_not_corrected(
        self, mock_http
    ):
        """The registry refuses the mismatch; the wrapper does not hide it by
        filling one from the other."""
        seen = mock_http(_status(422, VALIDATION_ERROR))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().put_topology_node(
                "example-rec",
                "AC000E00001",
                _node_body("AC000E00002"),
                token="tok-write",
            )

        assert seen[0].url.path == NODE_PATH
        assert json.loads(seen[0].content)["id"] == "AC000E00002"
        assert excinfo.value.status_code == 422
        assert excinfo.value.code is None

    # @verifies REQ-0131
    # @verifies REQ-0127
    async def test_a_type_change_an_area_relies_on_arrives_as_the_code(
        self, mock_http
    ):
        mock_http(
            _refusal(
                422,
                "Area 'area-one' needs a primary substation",
                "invalid_area_boundary",
            )
        )

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().put_topology_node(
                "example-rec",
                "AC000E00001",
                {**_node_body(), "type": "secondary_substation"},
                token="tok-write",
            )

        assert excinfo.value.code == "invalid_area_boundary"

    # @verifies REQ-0131
    async def test_deleting_a_node_answers_the_community(self, mock_http):
        seen = mock_http(_rows(_community(areas={}, nodes=[])))

        community = await _sync_client().delete_topology_node(
            "example-rec", "AC000E00001", token="tok-write"
        )

        assert seen[0].method == "DELETE"
        assert seen[0].url.path == NODE_PATH
        assert community.topology == []

    # @verifies REQ-0131
    # @verifies REQ-0127
    async def test_a_node_an_area_lists_arrives_as_the_code(self, mock_http):
        mock_http(
            _refusal(
                409,
                "Topology node is listed by area(s): area-one",
                "topology_node_in_use",
            )
        )

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().delete_topology_node(
                "example-rec", "AC000E00001", token="tok-write"
            )

        assert excinfo.value.status_code == 409
        assert excinfo.value.code == "topology_node_in_use"

    # @verifies REQ-0131
    async def test_an_absent_node_is_raised_not_read_as_deleted(self, mock_http):
        mock_http(_refusal(404, "Topology node not found"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().delete_topology_node(
                "example-rec", "AC000E00001", token="tok-write"
            )

        assert excinfo.value.status_code == 404
        assert excinfo.value.code is None


# ── Renaming an area with its members (REQ-0133) ─────────────────────────


RENAME_PATH = "/admin/communities/example-rec/areas/area-one/rename"


def _renamed(members_moved: int = 2) -> dict:
    return {
        "old_key": "area-one",
        "new_key": "area-uno",
        "members_moved": members_moved,
        "community": _community(areas={"area-uno": _area_body()}),
    }


class TestRenamingAnArea:
    # @verifies REQ-0133
    async def test_it_posts_only_the_new_key_and_answers_what_moved(
        self, mock_http
    ):
        seen = mock_http(_rows(_renamed()))

        renamed = await _sync_client().rename_area(
            "example-rec", "area-one", "area-uno", token="tok-write"
        )

        assert len(seen) == 1
        assert seen[0].method == "POST"
        assert seen[0].url.path == RENAME_PATH
        assert seen[0].headers["authorization"] == "Bearer tok-write"
        assert json.loads(seen[0].content) == {"new_key": "area-uno"}
        assert (renamed.old_key, renamed.new_key, renamed.members_moved) == (
            "area-one",
            "area-uno",
            2,
        )
        assert list(renamed.community.areas) == ["area-uno"]
        area = renamed.community.areas["area-uno"]
        assert (area.boundary.source, area.boundary.id) == (
            "gse_cabine_primarie",
            "AC000E00001",
        )

    # @verifies REQ-0133
    async def test_a_renamed_area_is_one_write_then_the_sync_replaces_the_new_key(
        self, mock_http
    ):
        """The plan's renamed-area case as the sync drives it: the rename moves
        the area and its members in one request (no `PUT` under the new key,
        which the one-substation rule refuses, and no `DELETE` of the old key,
        which members block), and the sync's later `PUT` of the new key is an
        ordinary replace."""
        seen = mock_http(_rows(_renamed(), _community(areas={"area-uno": _area_body()})))
        client = _sync_client()

        renamed = await client.rename_area(
            "example-rec", "area-one", "area-uno", token="tok-write"
        )
        community = await client.put_area(
            "example-rec", "area-uno", _area_body(), token="tok-write"
        )

        assert [(r.method, r.url.path) for r in seen] == [
            ("POST", RENAME_PATH),
            ("PUT", "/admin/communities/example-rec/areas/area-uno"),
        ]
        assert renamed.members_moved == 2
        assert list(community.areas) == ["area-uno"]

    # @verifies REQ-0133
    async def test_path_segments_are_quoted(self, mock_http):
        seen = mock_http(_rows(_renamed()))

        await _sync_client().rename_area(
            "example-rec", "area one/x", "area-uno", token="tok-write"
        )

        assert seen[0].url.raw_path.decode() == (
            "/admin/communities/example-rec/areas/area%20one%2Fx/rename"
        )

    # @verifies REQ-0133
    # @verifies REQ-0127
    @pytest.mark.parametrize(
        ("status", "code"),
        [
            (422, "invalid_area_key"),
            (404, "area_not_found"),
            (409, "area_key_taken"),
            (404, "community_not_found"),
        ],
    )
    async def test_a_refusal_arrives_as_the_code(self, mock_http, status, code):
        mock_http(_refusal(status, "Refused", code))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().rename_area(
                "example-rec", "area-one", "area uno", token="tok-write"
            )

        assert excinfo.value.status_code == status
        assert excinfo.value.code == code
        assert excinfo.value.detail == "Refused"

    # @verifies REQ-0133
    async def test_the_key_is_not_checked_here(self, mock_http):
        """The key pattern is the registry's; the wrapper sends what it is given."""
        seen = mock_http(_refusal(422, "Not an area key", "invalid_area_key"))

        with pytest.raises(RecRegistryApiError):
            await _sync_client().rename_area(
                "example-rec", "area-one", "-bad key", token="tok-write"
            )

        assert json.loads(seen[0].content) == {"new_key": "-bad key"}

    # @verifies REQ-0133
    async def test_a_validation_422_has_no_code(self, mock_http):
        mock_http(_status(422, VALIDATION_ERROR))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().rename_area(
                "example-rec", "area-one", "area-uno", token="tok-write"
            )

        assert excinfo.value.status_code == 422
        assert excinfo.value.code is None

    # @verifies REQ-0133
    async def test_a_missing_grant_raises_the_wrappers_error(self, mock_http):
        mock_http(_refusal(403, "Forbidden"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().rename_area(
                "example-rec", "area-one", "area-uno", token="tok-write"
            )

        assert excinfo.value.status_code == 403
        assert not isinstance(excinfo.value, UnexpectedStatus)

    # @verifies REQ-0133
    async def test_a_non_json_refusal_raises_without_a_code(self, mock_http):
        mock_http(_raw(409, b"<html>conflict</html>"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().rename_area(
                "example-rec", "area-one", "area-uno", token="tok-write"
            )

        assert excinfo.value.status_code == 409
        assert (excinfo.value.code, excinfo.value.detail) == (None, None)

    # @verifies REQ-0133
    async def test_an_unreadable_200_raises(self, mock_http):
        mock_http(_raw(200, b"<html>"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _sync_client().rename_area(
                "example-rec", "area-one", "area-uno", token="tok-write"
            )

        assert excinfo.value.status_code == 200

    # @verifies REQ-0133
    async def test_the_generated_vocabulary_names_the_rename_codes(self):
        from celine.sdk.openapi.rec_registry.models import ErrorCode

        for code in ("invalid_area_key", "area_not_found", "area_key_taken"):
            assert ErrorCode(code).value == code


# ── The self-service reads raise the wrapper's error (REQ-0132) ────────────


NOT_A_MEMBER = {
    "detail": "You are not a member of any community",
    "code": "not_a_member",
}

USER_READS = [
    ("get_my_community", (), "/user/community"),
    ("get_my_member", (), "/user/member"),
    ("get_my_assets", (), "/user/assets"),
    ("get_my_asset", ("meter-SEN-1",), "/user/assets/meter-SEN-1"),
    ("get_my_delivery_points", (), "/user/delivery-points"),
]

USER_ANSWERS = {
    "get_my_community": {
        "key": "example-rec",
        "name": "Example REC",
        "your_area": "area-one",
        "your_role": "consumer",
    },
    "get_my_member": {
        "key": "ex-00001",
        "name": "Member One",
        "area": "area-one",
        "role": "consumer",
        "status": "active",
    },
    "get_my_assets": {"items": [], "total": 0},
    "get_my_asset": {
        "key": "meter-SEN-1",
        "name": "Meter",
        "asset_type": "meter",
        "sensor_id": "SEN-1",
    },
    "get_my_delivery_points": {"items": [], "total": 0},
}


def _user_client():
    from celine.sdk.rec_registry import RecRegistryUserClient

    return RecRegistryUserClient("http://registry.test", default_token="tok-user")


class TestASelfServiceRefusalRaisesTheWrappersError:
    # @verifies REQ-0132
    @pytest.mark.parametrize(("method", "args", "path"), USER_READS)
    async def test_not_a_member_arrives_as_the_code(
        self, mock_http, method, args, path
    ):
        seen = mock_http(_status(403, NOT_A_MEMBER))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await getattr(_user_client(), method)(*args)

        assert seen[0].method == "GET"
        assert seen[0].url.path == path
        assert seen[0].headers["authorization"] == "Bearer tok-user"
        assert excinfo.value.status_code == 403
        assert excinfo.value.code == "not_a_member"
        assert excinfo.value.detail == NOT_A_MEMBER["detail"]
        assert json.loads(excinfo.value.body) == NOT_A_MEMBER

    # @verifies REQ-0132
    @pytest.mark.parametrize(("method", "args", "path"), USER_READS)
    async def test_a_non_json_declared_status_raises_without_a_code(
        self, mock_http, method, args, path
    ):
        """A proxy's HTML page on the `403` the route declares: the generated
        parse would call `response.json()` on it and fail with a decode error."""
        mock_http(_raw(403, b"<html>forbidden</html>"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await getattr(_user_client(), method)(*args)

        assert excinfo.value.status_code == 403
        assert (excinfo.value.code, excinfo.value.detail) == (None, None)
        assert excinfo.value.body == b"<html>forbidden</html>"

    # @verifies REQ-0132
    @pytest.mark.parametrize(("method", "args", "path"), USER_READS)
    async def test_an_undeclared_status_raises_the_same_error(
        self, mock_http, method, args, path
    ):
        mock_http(_raw(502, b"bad gateway", "text/plain"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await getattr(_user_client(), method)(*args)

        assert excinfo.value.status_code == 502
        assert not isinstance(excinfo.value, UnexpectedStatus)

    # @verifies REQ-0132
    async def test_a_non_json_validation_status_raises_without_a_code(
        self, mock_http
    ):
        """`/user/assets/{asset_key}` also declares `422`."""
        mock_http(_raw(422, b"<html>"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _user_client().get_my_asset("meter-SEN-1")

        assert excinfo.value.status_code == 422
        assert excinfo.value.code is None

    # @verifies REQ-0132
    @pytest.mark.parametrize(("method", "args", "path"), USER_READS)
    async def test_a_200_answers_the_schema(self, mock_http, method, args, path):
        mock_http(_rows(USER_ANSWERS[method]))

        answer = await getattr(_user_client(), method)(*args)

        assert answer is not None
        assert answer.model_dump(exclude_none=True) == {
            k: v for k, v in USER_ANSWERS[method].items()
        }

    # @verifies REQ-0132
    @pytest.mark.parametrize(("method", "args", "path"), USER_READS)
    async def test_an_unreadable_200_raises(self, mock_http, method, args, path):
        mock_http(_raw(200, b"<html>"))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await getattr(_user_client(), method)(*args)

        assert excinfo.value.status_code == 200

    # @verifies REQ-0132
    async def test_a_member_owning_nothing_is_not_a_refusal(self, mock_http):
        mock_http(_rows({"items": [], "total": 0}))

        assets = await _user_client().get_my_assets()

        assert (assets.items, assets.total) == ([], 0)

    # @verifies REQ-0132
    async def test_the_generated_vocabulary_names_the_new_codes(self):
        from celine.sdk.openapi.rec_registry.models import ErrorCode

        assert ErrorCode("not_a_member").value == "not_a_member"
        assert ErrorCode("topology_node_in_use").value == "topology_node_in_use"


# ── Member fields and delivery points (REQ-0134, REQ-0135) ──────────────────

MEMBER_PATH = "/admin/communities/example-rec/members/ex-00001"
POD_OLD = "IT001E00000001"
POD_NEW = "IT001E00000002"
POD_PATH = f"{MEMBER_PATH}/delivery-points/{POD_NEW}"

FIELD_WRITES = [
    ("put_member_name", "name", "Member Two"),
    ("put_member_role", "role", "consumer"),
    ("put_member_area", "area", "area-2"),
]


def _pod_body(point_id: str = POD_NEW) -> dict:
    return {"id": point_id, "type": "pod"}


def _points(*ids: str) -> dict:
    return {
        "delivery_points": [
            {
                "id": i,
                "type": "pod",
                "description": None,
                "address": None,
                "tariff": None,
                "active": True,
            }
            for i in ids
        ]
    }


class TestTheMemberFieldWrites:
    # @verifies REQ-0134
    @pytest.mark.parametrize(("method", "field", "value"), FIELD_WRITES)
    async def test_one_key_goes_to_its_own_route(self, mock_http, method, field, value):
        seen = mock_http(_rows(_member_detail()))

        await getattr(_client(), method)(
            "example-rec", "ex-00001", value, token="tok-field"
        )

        assert len(seen) == 1
        assert seen[0].method == "PUT"
        assert seen[0].url.path == f"{MEMBER_PATH}/{field}"
        assert json.loads(seen[0].content) == {field: value}
        assert seen[0].headers["authorization"] == "Bearer tok-field"

    # @verifies REQ-0134
    @pytest.mark.parametrize(("method", "field", "value"), FIELD_WRITES)
    async def test_it_has_no_parameter_for_any_other_member_field(
        self, method, field, value
    ):
        import inspect

        params = set(inspect.signature(getattr(RecRegistryAdminClient, method)).parameters)

        assert params == {"self", "community_key", "member_key", field, "token"}

    # @verifies REQ-0134
    @pytest.mark.parametrize(("method", "field", "value"), FIELD_WRITES)
    async def test_it_answers_the_updated_member_as_a_schema(
        self, mock_http, method, field, value
    ):
        from celine.sdk.rec_registry import MemberDetailSchema

        mock_http(_rows({**_member_detail(), "name": "Member Two"}))

        member = await getattr(_client(), method)("example-rec", "ex-00001", value)

        assert type(member) is MemberDetailSchema
        assert member.key == "ex-00001"

    # @verifies REQ-0134
    # @verifies REQ-0127
    @pytest.mark.parametrize(
        ("method", "status", "code"),
        [
            ("put_member_role", 422, "invalid_role"),
            ("put_member_area", 422, "unknown_area"),
            ("put_member_name", 404, "member_not_found"),
            ("put_member_area", 404, "community_not_found"),
        ],
    )
    async def test_a_refusal_raises_with_the_registrys_code(
        self, mock_http, method, status, code
    ):
        mock_http(_refusal(status, "refused", code))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await getattr(_client(), method)("example-rec", "ex-00001", "x")

        assert excinfo.value.status_code == status
        assert excinfo.value.code == code
        assert excinfo.value.detail == "refused"

    # @verifies REQ-0134
    # @verifies REQ-0127
    @pytest.mark.parametrize(
        "respond",
        [
            _status(422, VALIDATION_ERROR),
            _status(403, {"detail": "Forbidden"}),
            _raw(502, b"<html>Bad gateway</html>"),
        ],
    )
    @pytest.mark.parametrize(("method", "field", "value"), FIELD_WRITES)
    async def test_a_refusal_that_names_no_code_raises_with_none(
        self, mock_http, respond, method, field, value
    ):
        mock_http(respond)

        with pytest.raises(RecRegistryApiError) as excinfo:
            await getattr(_client(), method)("example-rec", "ex-00001", value)

        assert not isinstance(excinfo.value, UnexpectedStatus)
        assert excinfo.value.code is None


class TestTheDeliveryPointWrites:
    # @verifies REQ-0135
    async def test_without_replaces_no_query_is_sent(self, mock_http):
        seen = mock_http(_rows(_points(POD_OLD, POD_NEW)))

        await _client().put_delivery_point(
            "example-rec", "ex-00001", POD_NEW, _pod_body(), token="tok-dp"
        )

        assert seen[0].method == "PUT"
        assert seen[0].url.path == POD_PATH
        assert seen[0].url.query == b""
        assert json.loads(seen[0].content) == _pod_body()
        assert seen[0].headers["authorization"] == "Bearer tok-dp"

    # @verifies REQ-0135
    async def test_replaces_travels_as_the_query(self, mock_http):
        from celine.sdk.rec_registry import DeliveryPointsResponseSchema

        seen = mock_http(_rows(_points(POD_NEW)))

        points = await _client().put_delivery_point(
            "example-rec", "ex-00001", POD_NEW, _pod_body(), replaces=POD_OLD
        )

        assert seen[0].url.path == POD_PATH
        assert seen[0].url.params["replaces"] == POD_OLD
        assert type(points) is DeliveryPointsResponseSchema
        assert [p.id for p in points.delivery_points] == [POD_NEW]

    # @verifies REQ-0135
    async def test_the_undecoded_upsert_is_unchanged_without_replaces(self, mock_http):
        seen = mock_http(_rows(_points(POD_NEW)))
        from celine.sdk.openapi.rec_registry.models import DeliveryPointIn

        response = await _client().upsert_delivery_point(
            "example-rec", "ex-00001", POD_NEW, DeliveryPointIn.from_dict(_pod_body())
        )

        assert int(response.status_code) == 200
        assert seen[0].url.query == b""

    # @verifies REQ-0135
    async def test_the_undecoded_upsert_carries_replaces_and_does_not_raise(
        self, mock_http
    ):
        seen = mock_http(
            _refusal(409, "held by another member", "delivery_point_held")
        )
        from celine.sdk.openapi.rec_registry.models import DeliveryPointIn

        response = await _client().upsert_delivery_point(
            "example-rec",
            "ex-00001",
            POD_NEW,
            DeliveryPointIn.from_dict(_pod_body()),
            replaces=POD_OLD,
        )

        assert seen[0].url.params["replaces"] == POD_OLD
        assert int(response.status_code) == 409
        assert RecRegistryApiError.refusal_of(response.content)[0] == "delivery_point_held"

    # @verifies REQ-0135
    async def test_delete_sends_delete_and_answers_what_is_left(self, mock_http):
        seen = mock_http(_rows(_points(POD_OLD)))

        points = await _client().delete_delivery_point(
            "example-rec", "ex-00001", POD_NEW, token="tok-dp"
        )

        assert seen[0].method == "DELETE"
        assert seen[0].url.path == POD_PATH
        assert seen[0].headers["authorization"] == "Bearer tok-dp"
        assert [p.id for p in points.delivery_points] == [POD_OLD]

    # @verifies REQ-0135
    # @verifies REQ-0127
    @pytest.mark.parametrize(
        ("method", "status", "code"),
        [
            ("put", 409, "delivery_point_held"),
            ("put", 404, "member_not_found"),
            ("put", 404, "community_not_found"),
            ("delete", 409, "delivery_point_linked"),
            ("delete", 404, "member_not_found"),
        ],
    )
    async def test_a_refusal_raises_with_the_registrys_code(
        self, mock_http, method, status, code
    ):
        mock_http(_refusal(status, "refused", code))

        with pytest.raises(RecRegistryApiError) as excinfo:
            if method == "put":
                await _client().put_delivery_point(
                    "example-rec", "ex-00001", POD_NEW, _pod_body(), replaces=POD_OLD
                )
            else:
                await _client().delete_delivery_point("example-rec", "ex-00001", POD_NEW)

        assert excinfo.value.status_code == status
        assert excinfo.value.code == code
        assert excinfo.value.detail == "refused"
        assert code in str(excinfo.value)

    # @verifies REQ-0135
    async def test_replacing_a_point_the_member_lacks_is_an_uncoded_404(
        self, mock_http
    ):
        mock_http(_status(404, {"detail": f"Delivery point '{POD_OLD}' not found"}))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().put_delivery_point(
                "example-rec", "ex-00001", POD_NEW, _pod_body(), replaces=POD_OLD
            )

        assert excinfo.value.status_code == 404
        assert excinfo.value.code is None
        assert "not found" in str(excinfo.value)

    # @verifies REQ-0135
    @pytest.mark.parametrize(
        "respond",
        [
            _status(422, VALIDATION_ERROR),
            _status(403, {"detail": "Forbidden"}),
            _raw(502, b"<html>Bad gateway</html>"),
            _raw(200, b"not json"),
        ],
    )
    @pytest.mark.parametrize("method", ["put", "delete"])
    async def test_anything_else_raises_the_wrappers_error(
        self, mock_http, respond, method
    ):
        mock_http(respond)

        with pytest.raises(RecRegistryApiError) as excinfo:
            if method == "put":
                await _client().put_delivery_point(
                    "example-rec", "ex-00001", POD_NEW, _pod_body()
                )
            else:
                await _client().delete_delivery_point("example-rec", "ex-00001", POD_NEW)

        assert not isinstance(excinfo.value, UnexpectedStatus)
        assert excinfo.value.code is None

    # @verifies REQ-0135
    async def test_a_body_given_as_a_mapping_is_sent_as_given(self, mock_http):
        seen = mock_http(_rows(_points(POD_NEW)))

        await _client().put_delivery_point(
            "example-rec",
            "ex-00001",
            POD_NEW,
            {"id": POD_NEW, "type": "pod", "tariff": "D2"},
        )

        assert json.loads(seen[0].content) == {
            "id": POD_NEW,
            "type": "pod",
            "tariff": "D2",
        }

    async def test_the_generated_vocabulary_names_the_new_codes(self):
        from celine.sdk.openapi.rec_registry.models import ErrorCode

        assert ErrorCode("delivery_point_held").value == "delivery_point_held"
        assert ErrorCode("delivery_point_linked").value == "delivery_point_linked"


# ── YAML import ───────────────────────────────────────────────────────────────

IMPORT_YAML = (
    "community:\n  key: example-rec\n  name: Example REC\n"
    "---\n"
    "community:\n  key: example-rec-2\n  name: Example REC Two\n"
)


def _import_report(*keys: str, dry_run: bool = False) -> dict:
    return {
        "reports": [
            {
                "community_key": k,
                "deleted": {},
                "inserted": {"members": 1},
                "warnings": [],
                "refusals": [],
            }
            for k in keys
        ],
        "dry_run": dry_run,
    }


class TestImportingYaml:
    async def test_the_yaml_is_the_raw_request_body(self, mock_http):
        """The generated operation takes no `body`; passing one raised
        `TypeError` before anything was sent. The route reads the raw body."""
        seen = mock_http(_rows(_import_report("example-rec", "example-rec-2")))

        report = await _client().import_yaml(IMPORT_YAML, token="tok-import")

        assert len(seen) == 1
        assert seen[0].method == "POST"
        assert seen[0].url.path == "/admin/import/yaml"
        assert seen[0].content == IMPORT_YAML.encode("utf-8")
        assert seen[0].headers["content-type"] == "application/yaml"
        assert seen[0].headers["authorization"] == "Bearer tok-import"
        assert [r.community_key for r in report.reports] == [
            "example-rec",
            "example-rec-2",
        ]

    async def test_non_ascii_yaml_is_sent_as_utf8(self, mock_http):
        seen = mock_http(_rows(_import_report("example-rec")))
        text = "community:\n  key: example-rec\n  name: Comunità Esempio\n"

        await _client().import_yaml(text)

        assert seen[0].content.decode("utf-8") == text

    async def test_by_default_it_is_neither_a_dry_run_nor_forced(self, mock_http):
        seen = mock_http(_rows(_import_report("example-rec")))

        await _client().import_yaml(IMPORT_YAML)

        assert seen[0].url.params["dry_run"] == "false"
        assert seen[0].url.params["force"] == "false"

    async def test_dry_run_and_force_travel_as_the_query(self, mock_http):
        seen = mock_http(_rows(_import_report("example-rec", dry_run=True)))

        report = await _client().import_yaml(IMPORT_YAML, dry_run=True, force=True)

        assert seen[0].url.params["dry_run"] == "true"
        assert seen[0].url.params["force"] == "true"
        assert report.dry_run is True

    @pytest.mark.parametrize("code", ["sensor_held", "delivery_point_held"])
    async def test_a_refused_bundle_raises_with_the_registrys_code(
        self, mock_http, code
    ):
        mock_http(_refusal(422, "refused", code))

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().import_yaml(IMPORT_YAML)

        assert excinfo.value.status_code == 422
        assert excinfo.value.code == code
        assert excinfo.value.detail == "refused"
        assert code in str(excinfo.value)
        assert "import-yaml" in str(excinfo.value)

    @pytest.mark.parametrize(
        ("respond", "status"),
        [
            (_status(422, {"detail": "Document 0 validation error: ..."}), 422),
            (_status(422, VALIDATION_ERROR), 422),
            (_status(400, {"detail": "No YAML documents found in body"}), 400),
            (_status(409, {"detail": "Community 'example-rec' exists"}), 409),
            (_status(403, {"detail": "Forbidden"}), 403),
            (_raw(502, b"<html>Bad gateway</html>"), 502),
            (_raw(200, b"not json"), 200),
        ],
    )
    async def test_anything_else_raises_the_wrappers_error_without_a_code(
        self, mock_http, respond, status
    ):
        mock_http(respond)

        with pytest.raises(RecRegistryApiError) as excinfo:
            await _client().import_yaml(IMPORT_YAML)

        assert not isinstance(excinfo.value, UnexpectedStatus)
        assert excinfo.value.status_code == status
        assert excinfo.value.code is None
