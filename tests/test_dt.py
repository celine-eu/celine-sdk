"""Tests for `celine.sdk.dt` — docs/specifications/digital-twin-client.md.

REQ-0160: every `celine.sdk.dt` method logs a refusal by status and error
types only, and no method keeps a mutable default or modifies the caller's
payload. The seam is `mock_http`: the
generated client builds its own `httpx.AsyncClient`, so the class is what gets
replaced, and the wrapper and the generated parse run against real responses.

Coordinates are synthetic and off land (the Gulf of Guinea, lat 0-0.1,
lon 0-0.4), so nothing here names a real place.
"""

from __future__ import annotations

import inspect
import json
import logging

import httpx
import pytest

from celine.sdk.auth import StaticTokenProvider
from celine.sdk.dt import DTClient
from celine.sdk.dt.community import CommunityClient
from celine.sdk.dt.grid import GridClient
from celine.sdk.dt.participant import ParticipantClient
from celine.sdk.dt.util import DTApiError

pytestmark = pytest.mark.asyncio

LAT, LON = "0.0421337", "0.3171717"

FETCH_PATH = "/communities/it/example-rec/values/boundary_at_point"

EMPTY_RESULT = {"count": 0, "items": [], "limit": 1, "offset": 0}


def _dt() -> DTClient:
    return DTClient(
        base_url="http://dt.test", token_provider=StaticTokenProvider("tok-dt")
    )


def _answer(status: int, payload: dict):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=payload)

    return handle


def _validation_error_echoing_the_point() -> dict:
    """FastAPI's shape: `msg` and `input` repeat what was sent."""
    return {
        "detail": [
            {
                "loc": ["body", "payload", "lat"],
                "msg": f"Input should be a valid number, got {LAT}",
                "type": "float_parsing",
                "input": {"lat": LAT, "lon": LON},
            },
            {
                "loc": ["body", "payload", LON],
                "msg": f"Field required near {LON}",
                "type": "missing",
                "input": LON,
            },
        ]
    }


class TestTheCommunityValueFetch:
    # @verifies REQ-0160
    async def test_a_validation_refusal_logs_no_payload_value(self, mock_http, caplog):
        mock_http(_answer(422, _validation_error_echoing_the_point()))
        caplog.set_level(logging.DEBUG, logger="celine.sdk.dt")

        with pytest.raises(DTApiError):
            await _dt().communities.fetch_values(
                "example-rec",
                "boundary_at_point",
                {"source": "gse_cabine_primarie", "lat": LAT, "lon": LON},
            )

        logged = "\n".join(
            record.getMessage()
            for record in caplog.records
            if record.name.startswith("celine.sdk.dt")
        )
        assert logged, "the refusal is still logged"
        assert LAT not in logged
        assert LON not in logged
        assert "0.04" not in logged and "0.31" not in logged
        assert "Input should be" not in logged

    # @verifies REQ-0160
    async def test_the_log_names_the_fetcher_status_and_error_types(
        self, mock_http, caplog
    ):
        mock_http(_answer(422, _validation_error_echoing_the_point()))
        caplog.set_level(logging.WARNING, logger="celine.sdk.dt")

        with pytest.raises(DTApiError):
            await _dt().communities.fetch_values(
                "example-rec", "boundary_at_point", {"lat": LAT, "lon": LON}
            )

        (record,) = [r for r in caplog.records if r.name == "celine.sdk.dt.community"]
        assert record.levelno == logging.WARNING
        message = record.getMessage()
        assert "boundary_at_point" in message
        assert "422" in message
        assert "float_parsing" in message and "missing" in message

    # @verifies REQ-0160
    async def test_the_raised_error_carries_no_payload_value(self, mock_http):
        mock_http(_answer(422, _validation_error_echoing_the_point()))

        with pytest.raises(DTApiError) as excinfo:
            await _dt().communities.fetch_values(
                "example-rec", "boundary_at_point", {"lat": LAT, "lon": LON}
            )

        assert LAT not in str(excinfo.value)
        assert excinfo.value.body is None

    # @verifies REQ-0160
    async def test_the_callers_payload_is_not_modified(self, mock_http):
        seen = mock_http(_answer(200, EMPTY_RESULT))
        payload = {"source": "gse_cabine_primarie", "lat": LAT, "lon": LON}
        before = dict(payload)

        await _dt().communities.fetch_values(
            "example-rec", "boundary_at_point", payload, limit=1, offset=0
        )

        assert payload == before
        sent = json.loads(seen[0].content)["payload"]
        assert seen[0].url.path == FETCH_PATH
        assert sent == {**before, "limit": 1, "offset": 0}

    # @verifies REQ-0160
    async def test_nothing_one_call_adds_reaches_the_next(self, mock_http):
        seen = mock_http(_answer(200, EMPTY_RESULT))
        dt = _dt()

        await dt.communities.fetch_values(
            "example-rec", "boundary_at_point", limit=5, offset=10
        )
        await dt.communities.fetch_values("example-rec", "boundary_at_point")

        assert json.loads(seen[0].content)["payload"] == {"limit": 5, "offset": 10}
        assert json.loads(seen[1].content)["payload"] == {}

    # @verifies REQ-0160
    async def test_the_default_payload_is_not_a_shared_dict(self):
        default = (
            inspect.signature(CommunityClient.fetch_values)
            .parameters["payload"]
            .default
        )

        assert default is None


# ── Every DT client method (REQ-0160, widened by the plan's D53) ──────────

#: What a refusal might echo: an id the caller sent, and a coordinate.
SECRET_ID = "ex-00001-secret"


def _refusal_echoing_the_request() -> dict:
    return {
        "detail": [
            {
                "loc": ["path", SECRET_ID],
                "msg": f"Input should be valid, got {SECRET_ID} at {LAT}",
                "type": "string_pattern_mismatch",
                "input": {"id": SECRET_ID, "lat": LAT, "lon": LON},
            }
        ]
    }


#: (accessor, method, positional args, keyword args) for every public method.
EVERY_METHOD = [
    ("communities", "info", (SECRET_ID,), {}),
    ("communities", "energy_balance", (SECRET_ID,), {"start": "2026-01-01"}),
    ("communities", "list_values", (SECRET_ID,), {}),
    ("communities", "fetch_values", (SECRET_ID, "boundary_at_point", {"lat": LAT}), {}),
    ("communities", "describe_value", (SECRET_ID, "boundary_shape"), {}),
    ("communities", "list_simulations", (SECRET_ID,), {}),
    ("communities", "list_ontology_specs", (SECRET_ID,), {}),
    ("communities", "fetch_ontology", (SECRET_ID, "rec_energy", {"lat": LAT}), {}),
    ("communities", "fetch_ontology", (SECRET_ID, "rec_energy"), {}),
    ("participants", "profile", (SECRET_ID,), {}),
    ("participants", "assets", (SECRET_ID,), {}),
    ("participants", "list_values", (SECRET_ID,), {}),
    ("participants", "fetch_values", (SECRET_ID, "meters", {"lat": LAT}), {}),
    ("participants", "describe_value", (SECRET_ID, "meters"), {}),
    ("participants", "list_simulations", (SECRET_ID,), {}),
    ("participants", "list_ontology_specs", (SECRET_ID,), {}),
    ("participants", "fetch_ontology", (SECRET_ID, "meters", {"lat": LAT}), {}),
    ("participants", "fetch_ontology", (SECRET_ID, "meters"), {}),
    ("grid", "fetch_values", (SECRET_ID, "shapes", {"lat": LAT}), {}),
    ("grid", "filters", (SECRET_ID,), {}),
    ("grid", "tile_index", (SECRET_ID,), {}),
    ("grid", "shapes", (SECRET_ID,), {}),
    ("grid", "risks", (SECRET_ID,), {"dates": ["2026-01-01"]}),
    ("grid", "risks_now", (SECRET_ID,), {}),
    ("grid", "trendline", (SECRET_ID,), {"date_from": "a", "date_to": "b"}),
    ("grid", "wind_map", (SECRET_ID,), {}),
    ("grid", "wind_bosco", (SECRET_ID,), {}),
    ("grid", "wind_alert_distribution", (SECRET_ID,), {}),
    ("grid", "wind_trend", (SECRET_ID,), {}),
    ("grid", "heat_map", (SECRET_ID,), {}),
    ("grid", "heat_alert_distribution", (SECRET_ID,), {}),
    ("grid", "heat_trend", (SECRET_ID,), {}),
    ("grid", "substations_map", (SECRET_ID,), {}),
    ("grid", "summary", (SECRET_ID,), {}),
]

CLIENT_CLASSES = (CommunityClient, ParticipantClient, GridClient)


def _public_methods(cls):
    return [
        (name, fn)
        for name, fn in inspect.getmembers(cls, inspect.iscoroutinefunction)
        if not name.startswith("_")
    ]


class TestEveryMethodLogsNoResponseDetail:
    # @verifies REQ-0160
    async def test_the_table_below_names_every_public_method(self):
        """So a method added later cannot skip the log test unnoticed."""
        accessor_of = {
            CommunityClient: "communities",
            ParticipantClient: "participants",
            GridClient: "grid",
        }
        listed = {(accessor, method) for accessor, method, _, _ in EVERY_METHOD}
        public = {
            (accessor_of[cls], name)
            for cls in CLIENT_CLASSES
            for name, _ in _public_methods(cls)
        }
        assert public == listed

    # @verifies REQ-0160
    @pytest.mark.parametrize(
        ("accessor", "method", "args", "kwargs"),
        EVERY_METHOD,
        ids=[f"{a}.{m}-{i}" for i, (a, m, _, _) in enumerate(EVERY_METHOD)],
    )
    async def test_a_refusal_logs_status_and_types_only(
        self, mock_http, caplog, accessor, method, args, kwargs
    ):
        mock_http(_answer(422, _refusal_echoing_the_request()))
        caplog.set_level(logging.DEBUG, logger="celine.sdk.dt")

        with pytest.raises(DTApiError) as excinfo:
            await getattr(getattr(_dt(), accessor), method)(*args, **kwargs)

        records = [r for r in caplog.records if r.name.startswith("celine.sdk.dt")]
        logged = "\n".join(r.getMessage() for r in records)
        assert SECRET_ID not in logged
        assert LAT not in logged and LON not in logged
        assert "Input should" not in logged
        assert SECRET_ID not in str(excinfo.value)
        for record in records:
            message = record.getMessage()
            assert "status=422" in message
            assert "string_pattern_mismatch" in message

    # @verifies REQ-0160
    async def test_no_method_hands_a_refusal_detail_to_a_logger(self):
        """A source guard beside the behaviour tests: the old
        `logger.warning(data.detail)` must not come back."""
        for cls in CLIENT_CLASSES:
            source = inspect.getsource(inspect.getmodule(cls))
            assert "(data.detail" not in source, cls.__name__


class TestNoMutableDefaults:
    # @verifies REQ-0160
    async def test_no_public_method_has_a_mutable_default(self):
        for cls in CLIENT_CLASSES:
            for name, fn in _public_methods(cls):
                for param in inspect.signature(fn).parameters.values():
                    assert not isinstance(
                        param.default, (dict, list, set, bytearray)
                    ), f"{cls.__name__}.{name}({param.name}=...)"

    # @verifies REQ-0160
    async def test_the_participant_fetch_leaves_the_callers_payload_alone(
        self, mock_http
    ):
        seen = mock_http(_answer(200, EMPTY_RESULT))
        dt = _dt()
        payload = {"lat": LAT}

        await dt.participants.fetch_values(SECRET_ID, "meters", payload, limit=3)
        await dt.participants.fetch_values(SECRET_ID, "meters")

        assert payload == {"lat": LAT}
        assert json.loads(seen[0].content)["payload"] == {
            "lat": LAT,
            "limit": 3,
            "offset": 0,
        }
        # The next call starts empty: nothing the first added is carried over.
        assert json.loads(seen[1].content)["payload"] == {"offset": 0}

    # @verifies REQ-0160
    @pytest.mark.parametrize("accessor", ["communities", "participants"])
    async def test_an_ontology_fetch_leaves_the_callers_payload_alone(
        self, mock_http, accessor
    ):
        seen = mock_http(_answer(200, {"@context": {}, "@graph": []}))
        payload = {"lat": LAT}

        await getattr(_dt(), accessor).fetch_ontology(
            SECRET_ID, "rec_energy", payload, limit=2, offset=4
        )

        assert payload == {"lat": LAT}
        assert json.loads(seen[0].content)["payload"] == {
            "lat": LAT,
            "limit": 2,
            "offset": 4,
        }

    # @verifies REQ-0160
    async def test_the_grid_fetch_leaves_the_callers_payload_alone(self, mock_http):
        seen = mock_http(_answer(200, EMPTY_RESULT))
        payload = {"dates": ["2026-01-01"]}

        await _dt().grid.fetch_values(SECRET_ID, "risks", payload, limit=9)

        assert payload == {"dates": ["2026-01-01"]}
        assert json.loads(seen[0].content)["payload"] == {
            "dates": ["2026-01-01"],
            "limit": 9,
        }
