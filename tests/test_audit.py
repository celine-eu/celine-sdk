"""Tests for `celine.sdk.audit` — see docs/specifications/audit.md."""

from __future__ import annotations

import json
import logging

import pytest
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.testclient import TestClient

from celine.sdk import audit
from celine.sdk.audit import (
    AUDIT_LOGGER,
    FIELDS,
    audit_access,
    audit_denied,
    audit_route,
    caller_fields,
    configure_audit,
    pseudonymise,
)
from celine.sdk.auth import JwtUser

USER_SUB = "0b7c6a1e-1111-4222-8333-944455556666"
SVC_SUB = "5d0e2f3a-aaaa-4bbb-8ccc-9ddddeeeefff"

USER_CLAIMS = {
    "sub": USER_SUB,
    "azp": "svc-example-webapp",
    "email": "member@example.org",
    "name": "Example Member",
    "preferred_username": "member",
}
SERVICE_CLAIMS = {
    "sub": SVC_SUB,
    "azp": "svc-example-job",
    "preferred_username": "service-account-svc-example-job",
}


def jwt_user(claims: dict) -> JwtUser:
    return JwtUser(
        sub=claims["sub"],
        email=claims.get("email"),
        name=claims.get("name"),
        preferred_username=claims.get("preferred_username"),
        claims=dict(claims),
    )


@pytest.fixture(autouse=True)
def service_name(monkeypatch):
    monkeypatch.setattr(audit, "_service", None)
    monkeypatch.delenv("OTEL_SERVICE_NAME", raising=False)
    monkeypatch.delenv("CELINE_AUDIT_PSEUDONYM_KEY", raising=False)
    configure_audit("example-api")


@pytest.fixture
def records(caplog):
    caplog.set_level(logging.INFO, logger=AUDIT_LOGGER)

    def read() -> list[dict]:
        return [json.loads(r.getMessage()) for r in caplog.records if r.name == AUDIT_LOGGER]

    return read


class TestTheRecord:
    # @verifies REQ-0190
    def test_one_json_line_with_every_field(self, caplog, records):
        caplog.set_level(logging.INFO, logger=AUDIT_LOGGER)
        returned = audit_access("dataset.read", caller=jwt_user(USER_CLAIMS), resource="ds-1")
        [line] = records()
        assert line == returned
        assert tuple(line) == FIELDS
        assert line["event"] == "access"
        assert line["outcome"] == "allowed"
        assert line["service"] == "example-api"
        assert line["action"] == "dataset.read"
        assert line["resource"] == "ds-1"
        assert line["ts"].endswith("+00:00")
        [record] = [r for r in caplog.records if r.name == AUDIT_LOGGER]
        assert record.audit == line
        assert record.levelno == logging.INFO

    # @verifies REQ-0190
    def test_a_denial_is_logged_at_warning(self, caplog, records):
        audit_denied("dataset.read", caller=USER_CLAIMS, resource="ds-1", reason="not_member")
        [line] = records()
        assert (line["event"], line["outcome"], line["reason"]) == ("denied", "denied", "not_member")
        assert [r.levelno for r in caplog.records if r.name == AUDIT_LOGGER] == [logging.WARNING]

    # @verifies REQ-0190
    def test_the_audit_logger_survives_a_quieter_log_level(self):
        logging.getLogger("celine").setLevel(logging.WARNING)
        try:
            assert logging.getLogger(AUDIT_LOGGER).isEnabledFor(logging.INFO)
        finally:
            logging.getLogger("celine").setLevel(logging.INFO)

    # @verifies REQ-0190
    def test_service_falls_back_to_the_otel_name(self, monkeypatch, records):
        monkeypatch.setattr(audit, "_service", None)
        monkeypatch.setenv("OTEL_SERVICE_NAME", "example-otel")
        audit_access("x")
        audit_access("x", service="override")
        assert [r["service"] for r in records()] == ["example-otel", "override"]


class TestNoPersonalData:
    # @verifies REQ-0191
    @pytest.mark.parametrize("caller", [jwt_user(USER_CLAIMS), USER_CLAIMS])
    def test_the_caller_is_sub_and_client_only(self, caplog, records, caller):
        audit_access("dataset.read", caller=caller)
        [line] = records()
        assert line["sub"] == USER_SUB
        assert line["client_id"] == "svc-example-webapp"
        assert line["service_account"] is False
        text = caplog.text
        for value in ("member@example.org", "Example Member", '"member"'):
            assert value not in text

    # @verifies REQ-0191
    def test_a_service_account_is_marked(self):
        fields = caller_fields(jwt_user(SERVICE_CLAIMS))
        assert fields == {"sub": SVC_SUB, "client_id": "svc-example-job", "service_account": True}

    # @verifies REQ-0191
    def test_anonymous_is_null(self):
        assert caller_fields(None) == {"sub": None, "client_id": None, "service_account": None}

    # @verifies REQ-0191
    def test_an_email_anywhere_is_pseudonymised(self, caplog, records):
        audit_denied(
            "member.read",
            caller={"sub": "person@example.org"},
            resource="person@example.org",
            reason="no grant for person@example.org",
        )
        [line] = records()
        pseudonym = pseudonymise("person@example.org")
        assert line["sub"] == pseudonym
        assert line["resource"] == pseudonym
        assert line["reason"] == f"no grant for {pseudonym}"
        assert "person@example.org" not in caplog.text

    # @verifies REQ-0191
    def test_control_characters_are_dropped_and_length_capped(self, records):
        audit_access("x", resource="ds-1\n{\"event\":\"forged\"}\r" + "a" * 1000)
        [line] = records()
        assert "\n" not in line["resource"] and "\r" not in line["resource"]
        assert len(line["resource"]) == 256

    # @verifies REQ-0191
    def test_pseudonym_is_stable_and_keyed_when_a_key_is_set(self, monkeypatch):
        plain = pseudonymise("EX-CODE-00001")
        assert plain == pseudonymise("EX-CODE-00001")
        assert plain.startswith("h:") and len(plain) == 18
        assert "EX-CODE-00001" not in plain
        monkeypatch.setenv("CELINE_AUDIT_PSEUDONYM_KEY", "k1")
        keyed = pseudonymise("EX-CODE-00001")
        assert keyed != plain
        monkeypatch.setenv("CELINE_AUDIT_PSEUDONYM_KEY", "k2")
        assert pseudonymise("EX-CODE-00001") != keyed


def build_app() -> FastAPI:
    def get_user(request: Request) -> JwtUser:
        if request.headers.get("authorization") != "Bearer ok":
            raise HTTPException(401, "Missing authentication token")
        return jwt_user(USER_CLAIMS)

    app = FastAPI()
    router = APIRouter(prefix="/datasets")

    @router.get(
        "/{dataset_id}",
        dependencies=[Depends(audit_route("dataset.read", user=get_user, resource="dataset_id"))],
    )
    def read(dataset_id: str):
        if dataset_id == "closed":
            raise HTTPException(403, "member@example.org may not read this")
        if dataset_id == "missing":
            raise HTTPException(404, "not found")
        if dataset_id == "broken":
            raise RuntimeError("boom")
        return {"id": dataset_id}

    @router.get(
        "/state/{dataset_id}",
        dependencies=[Depends(audit_route("dataset.read", resource=lambda r: "fixed-id"))],
    )
    def read_with_state(request: Request, dataset_id: str):
        return {"id": dataset_id}

    @app.middleware("http")
    async def set_user(request: Request, call_next):
        request.state.user = jwt_user(SERVICE_CLAIMS)
        return await call_next(request)

    @app.get("/plain/{dataset_id}")
    def plain(dataset_id: str):
        return {"id": dataset_id}

    app.include_router(router)
    return app


@pytest.fixture
def client():
    return TestClient(build_app(), raise_server_exceptions=False)


AUTH = {"authorization": "Bearer ok"}


class TestTheRouteDependency:
    # @verifies REQ-0192
    def test_a_served_request_records_access(self, client, records):
        headers = {
            **AUTH,
            "x-request-id": "req-123",
            "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
        }
        assert client.get("/datasets/ds-1?owner=member@example.org", headers=headers).status_code == 200
        [line] = records()
        assert line["event"] == "access" and line["outcome"] == "allowed"
        assert line["sub"] == USER_SUB
        assert line["resource"] == "ds-1"
        assert line["method"] == "GET"
        assert line["route"] == "/datasets/{dataset_id}"
        assert line["request_id"] == "req-123"
        assert line["trace_id"] == "4bf92f3577b34da6a3ce929d0e0e4736"

    # @verifies REQ-0192
    def test_a_raised_403_records_denied_with_the_caller(self, client, caplog, records):
        assert client.get("/datasets/closed", headers=AUTH).status_code == 403
        [line] = records()
        assert (line["event"], line["outcome"], line["reason"]) == ("denied", "denied", "http 403")
        assert line["sub"] == USER_SUB and line["resource"] == "closed"
        assert "member@example.org" not in caplog.text

    # @verifies REQ-0192
    @pytest.mark.parametrize(("path", "status", "reason"), [
        ("/datasets/missing", 404, "http 404"),
        ("/datasets/broken", 500, "RuntimeError"),
    ])
    def test_other_failures_record_an_error(self, client, records, path, status, reason):
        assert client.get(path, headers=AUTH).status_code == status
        [line] = records()
        assert (line["event"], line["outcome"], line["reason"]) == ("access", "error", reason)

    # @verifies REQ-0192
    def test_a_request_the_user_dependency_refuses_records_nothing(self, client, records):
        assert client.get("/datasets/ds-1").status_code == 401
        assert records() == []

    # @verifies REQ-0192
    def test_without_a_user_dependency_the_request_state_user_is_read(self, client, records):
        assert client.get("/datasets/state/ds-9").status_code == 200
        [line] = records()
        assert line["sub"] == SVC_SUB and line["service_account"] is True
        assert line["resource"] == "fixed-id"
        assert line["route"] == "/datasets/state/{dataset_id}"

    # @verifies REQ-0192
    def test_a_route_without_the_dependency_records_nothing(self, client, records):
        assert client.get("/plain/ds-1").status_code == 200
        assert records() == []

    # @verifies REQ-0192
    def test_a_malformed_request_id_or_traceparent_is_dropped(self, client, records):
        headers = {**AUTH, "x-request-id": "a b\"c", "traceparent": "garbage"}
        client.get("/datasets/ds-1", headers=headers)
        [line] = records()
        assert line["request_id"] is None and line["trace_id"] is None


def build_state_app() -> FastAPI:
    """``audit_route`` without ``user=``, on a router whose auth dependency comes later."""

    def require_user(request: Request) -> JwtUser:
        if request.headers.get("authorization") != "Bearer ok":
            raise HTTPException(401, "Missing authentication token")
        user = jwt_user(USER_CLAIMS)
        request.state.user = user
        return user

    def no_user() -> None:
        return None

    app = FastAPI()
    router = APIRouter(
        prefix="/twins/{twin_id}",
        dependencies=[Depends(audit_route("twin.read", resource="twin_id")), Depends(require_user)],
    )

    @router.get("/values")
    def values(twin_id: str):
        if twin_id == "closed":
            raise HTTPException(403, "refused")
        if twin_id == "missing":
            raise HTTPException(404, "not found")
        return {"id": twin_id}

    @app.get(
        "/late/{item_id}",
        dependencies=[Depends(audit_route("item.read", user=no_user, resource="item_id"))],
    )
    def late(request: Request, item_id: str):
        request.state.user = jwt_user(SERVICE_CLAIMS)
        return {"id": item_id}

    app.include_router(router)
    return app


class TestTheCallerIsReadWhenTheRequestEnds:
    @pytest.fixture
    def state_client(self):
        return TestClient(build_state_app(), raise_server_exceptions=False)

    # @verifies REQ-0192
    @pytest.mark.parametrize(("twin", "status", "event", "outcome"), [
        ("tw-1", 200, "access", "allowed"),
        ("closed", 403, "denied", "denied"),
        ("missing", 404, "access", "error"),
    ])
    def test_a_later_auth_dependency_names_the_caller(
        self, state_client, records, twin, status, event, outcome
    ):
        assert state_client.get(f"/twins/{twin}/values", headers=AUTH).status_code == status
        [line] = records()
        assert (line["event"], line["outcome"]) == (event, outcome)
        assert line["sub"] == USER_SUB and line["client_id"] == "svc-example-webapp"
        assert line["resource"] == twin
        assert line["route"] == "/twins/{twin_id}/values"

    # @verifies REQ-0192
    def test_a_refusal_by_the_later_auth_dependency_is_denied_without_a_caller(
        self, state_client, records
    ):
        assert state_client.get("/twins/tw-1/values").status_code == 401
        [line] = records()
        assert (line["event"], line["reason"]) == ("denied", "http 401")
        assert line["sub"] is None

    # @verifies REQ-0192
    def test_a_user_dependency_returning_none_falls_back_to_the_request_state(
        self, state_client, records
    ):
        assert state_client.get("/late/it-1").status_code == 200
        [line] = records()
        assert line["sub"] == SVC_SUB and line["service_account"] is True


class _Rule:
    def __init__(self, rule: str):
        self.rule = rule


class FlaskLikeRequest:
    """The attributes ``request_fields`` reads from a Flask / Werkzeug request."""

    def __init__(self, rule: str | None, headers: dict | None = None):
        self.method = "GET"
        self.url_rule = _Rule(rule) if rule else None
        self.script_root = "/app"
        self.path = "/app/dashboard/ex-00001"
        self.headers = headers or {}


def starlette_request_before_routing(path: str = "/commitments/export") -> Request:
    return Request({
        "type": "http",
        "method": "POST",
        "path": path,
        "root_path": "",
        "query_string": b"",
        "headers": [(b"x-request-id", b"req-7")],
    })


class TestMethodAndRouteOutsideAMatchedRoute:
    # @verifies REQ-0193
    def test_a_middleware_denial_names_the_route_it_guards(self, records):
        request = starlette_request_before_routing()
        audit_denied(
            "commitments.export", reason="not_service", request=request,
            route="/commitments/export",
        )
        [line] = records()
        assert line["route"] == "/commitments/export"
        assert line["method"] == "POST"
        assert line["request_id"] == "req-7"

    # @verifies REQ-0193
    def test_explicit_method_and_route_win_without_a_request(self, records):
        audit_access("dashboard.read", method="get", route="/dashboard/<int:pk>")
        audit_denied("dashboard.read", method="GET", route="/dashboard/<int:pk>", reason="x")
        assert [(r["method"], r["route"]) for r in records()] == [
            ("GET", "/dashboard/<int:pk>"),
            ("GET", "/dashboard/<int:pk>"),
        ]

    # @verifies REQ-0193
    def test_a_route_override_is_cleaned_like_every_field(self, records):
        audit_access("x", route="/a\n/person@example.org")
        [line] = records()
        assert "\n" not in line["route"] and "person@example.org" not in line["route"]

    # @verifies REQ-0193
    def test_a_flask_request_gives_its_url_rule(self, records):
        request = FlaskLikeRequest(
            "/dashboard/<int:pk>",
            headers={"x-request-id": "req-9"},
        )
        audit_access("dashboard.read", caller=USER_CLAIMS, resource="12", request=request)
        [line] = records()
        assert (line["method"], line["route"]) == ("GET", "/app/dashboard/<int:pk>")
        assert line["request_id"] == "req-9"
        assert "ex-00001" not in json.dumps(line)

    # @verifies REQ-0193
    def test_a_flask_request_with_no_matched_rule_has_no_route(self, records):
        audit_denied("dashboard.read", reason="csrf", request=FlaskLikeRequest(None))
        [line] = records()
        assert line["route"] is None and line["method"] == "GET"
