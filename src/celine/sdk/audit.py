"""Access audit: who read what, and who was refused.

One record shape for every service, emitted on the logger ``celine.audit`` as a
single JSON object per line, so a log pipeline can select the audit trail by
logger name and parse it without knowing which service wrote it.

Fields (every record carries all of them; an unknown value is ``null``):

========== ==================================================================
event      ``access`` or ``denied``
service    the emitting service (``configure_audit`` or ``service=``)
sub        the caller's ``sub`` claim
client_id  the OAuth client the token was issued to (``azp``, else ``client_id``)
service_account  true for a client-credentials token
action     what the service did, in its own words (``dataset.read``)
method     the HTTP method, when a request is known
route      the route *template* (``/datasets/{dataset_id}``), never the raw
           path and never the query string
resource   the identifier of the thing acted on — see below
outcome    ``allowed``, ``denied`` or ``error``
reason     a short code for a refusal or an error (``http 403``, ``not_member``)
request_id ``X-Request-ID`` / ``X-Correlation-ID``, when the caller sent one
trace_id   the W3C ``traceparent`` trace id, when present
ts         UTC timestamp, ISO 8601
========== ==================================================================

**No personal data.** The caller is named by ``sub`` and client id only — never
email, name or username. ``resource`` holds an identifier the platform issued: a
dataset id, an asset id, a twin or entity id, a community id, a commitment id.
When the only identifier of the thing is itself personal (an email, a fiscal
code, a delivery point code), pass ``pseudonymise(value)`` instead. As a backstop
every string field is checked: a value that looks like an email is replaced by
its pseudonym, control characters are dropped and length is capped.

Explicit calls::

    from celine.sdk.audit import audit_access, audit_denied

    audit_access("dataset.read", caller=user, resource=dataset_id, request=request)
    audit_denied("dataset.read", caller=user, resource=dataset_id, reason="not_member")

    # A middleware refusing before routing names the route template it guards:
    audit_denied("commitments.export", caller=user, reason="not_service",
                 request=request, route="/commitments/export")

    # Flask: the request (inside its context) gives the method and the URL rule.
    from flask import request
    audit_access("dashboard.read", caller=claims, resource=pk, request=request)

Per route, recording the outcome of the handler::

    from celine.sdk.audit import audit_route

    @router.get(
        "/datasets/{dataset_id}",
        dependencies=[Depends(audit_route("dataset.read", user=get_current_user,
                                          resource="dataset_id"))],
    )

Without ``user=`` the caller is ``request.state.user`` as it stands when the
request ends, so the route's own auth dependency may set it after this one ran.

The audit logger is held at ``INFO`` whatever ``LOG_LEVEL`` says: lowering the
application's verbosity must not switch the audit trail off.
"""

import hashlib
import hmac
import json
import logging
import os
import re
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from typing import Any

from celine.sdk.auth.jwt import is_service_account

AUDIT_LOGGER = "celine.audit"

#: Keys the HMAC behind ``pseudonymise``. Unset, a plain SHA-256 is used.
PSEUDONYM_KEY_VAR = "CELINE_AUDIT_PSEUDONYM_KEY"

ACCESS = "access"
DENIED = "denied"

ALLOWED = "allowed"
ERROR = "error"

FIELDS: tuple[str, ...] = (
    "event",
    "service",
    "sub",
    "client_id",
    "service_account",
    "action",
    "method",
    "route",
    "resource",
    "outcome",
    "reason",
    "request_id",
    "trace_id",
    "ts",
)

_MAX_LEN = 256
_EMAIL = re.compile(r"[^\s@<>()\"',;:]+@[^\s@<>()\"',;:]+\.[^\s@<>()\"',;:]+")
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
_REQUEST_ID = re.compile(r"^[A-Za-z0-9._:\-]{1,128}$")
_TRACEPARENT = re.compile(r"^[0-9a-f]{2}-([0-9a-f]{32})-[0-9a-f]{16}-[0-9a-f]{2}$")

log = logging.getLogger(AUDIT_LOGGER)
log.setLevel(logging.INFO)

_service: str | None = None


def configure_audit(service: str) -> None:
    """Name the service every record of this process carries. Call once at startup."""
    global _service
    _service = service


def _service_name(override: str | None) -> str:
    return override or _service or os.environ.get("OTEL_SERVICE_NAME") or "unknown"


def pseudonymise(value: str) -> str:
    """A stable, non-reversible stand-in for a personal identifier: ``h:`` + 16 hex.

    Keyed with ``CELINE_AUDIT_PSEUDONYM_KEY`` when set, so a short identifier
    space (codes, numbers) cannot be enumerated back from the log.
    """
    data = value.encode("utf-8")
    key = os.environ.get(PSEUDONYM_KEY_VAR, "")
    if key:
        digest = hmac.new(key.encode("utf-8"), data, hashlib.sha256).hexdigest()
    else:
        digest = hashlib.sha256(data).hexdigest()
    return "h:" + digest[:16]


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = _CONTROL.sub("", str(value)).strip()
    if not text:
        return None
    text = _EMAIL.sub(lambda m: pseudonymise(m.group(0)), text)
    return text[:_MAX_LEN]


def _claims_of(caller: Any) -> dict:
    if caller is None:
        return {}
    if isinstance(caller, Mapping):
        return dict(caller)
    claims = getattr(caller, "claims", None)
    out = dict(claims) if isinstance(claims, Mapping) else {}
    sub = getattr(caller, "sub", None)
    if sub and "sub" not in out:
        out["sub"] = sub
    return out


def caller_fields(caller: Any) -> dict[str, Any]:
    """``sub``, ``client_id`` and ``service_account`` of a verified caller.

    ``caller`` is a ``JwtUser``, any object with ``sub`` / ``claims``, a claims
    mapping, or ``None`` for an anonymous request. Nothing else is read.
    """
    claims = _claims_of(caller)
    if not claims:
        return {"sub": None, "client_id": None, "service_account": None}
    return {
        "sub": _clean(claims.get("sub")),
        "client_id": _clean(claims.get("azp") or claims.get("client_id")),
        "service_account": is_service_account(claims),
    }


def _route_template(request: Any) -> str | None:
    scope = getattr(request, "scope", None)
    if isinstance(scope, Mapping):
        # Starlette / FastAPI: the matched route, under the mount's root path.
        route = scope.get("route")
        template = getattr(route, "path_format", None) or getattr(route, "path", None)
        return (scope.get("root_path") or "") + template if template else None
    # Flask / Werkzeug: the matched URL rule, under the application's script root.
    rule = getattr(getattr(request, "url_rule", None), "rule", None)
    if isinstance(rule, str) and rule:
        return (getattr(request, "script_root", None) or "") + rule
    return None


def request_fields(request: Any) -> dict[str, Any]:
    """``method``, ``route``, ``request_id`` and ``trace_id`` of a request.

    ``request`` is a Starlette / FastAPI request or a Flask request (inside its
    request context). The route is the matched template (``/datasets/{dataset_id}``)
    or Flask rule (``/dashboard/<int:pk>``); before routing (or with no route) it is
    ``None`` rather than the raw path, which may carry identifiers of people.
    """
    if request is None:
        return {"method": None, "route": None, "request_id": None, "trace_id": None}
    scope = getattr(request, "scope", None)
    scope = scope if isinstance(scope, Mapping) else {}
    template = _route_template(request)
    headers = getattr(request, "headers", {}) or {}

    request_id = headers.get("x-request-id") or headers.get("x-correlation-id")
    if request_id and not _REQUEST_ID.match(request_id):
        request_id = None

    trace_id = None
    match = _TRACEPARENT.match((headers.get("traceparent") or "").strip().lower())
    if match:
        trace_id = match.group(1)

    return {
        "method": _clean(scope.get("method") or getattr(request, "method", None)),
        "route": _clean(template),
        "request_id": request_id,
        "trace_id": trace_id,
    }


def _emit(
    event: str,
    action: str,
    *,
    caller: Any,
    resource: Any,
    outcome: str,
    reason: str | None,
    service: str | None,
    request: Any,
    method: str | None,
    route: str | None,
    request_id: str | None,
    trace_id: str | None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "event": event,
        "service": _clean(_service_name(service)),
        **caller_fields(caller),
        "action": _clean(action),
        **request_fields(request),
        "resource": _clean(resource),
        "outcome": outcome,
        "reason": _clean(reason),
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
    }
    if method is not None:
        record["method"] = _clean(method.upper())
    if route is not None:
        record["route"] = _clean(route)
    if request_id is not None:
        record["request_id"] = request_id if _REQUEST_ID.match(request_id) else None
    if trace_id is not None:
        record["trace_id"] = _clean(trace_id)
    record = {name: record.get(name) for name in FIELDS}

    level = logging.WARNING if event == DENIED else logging.INFO
    log.log(level, json.dumps(record, separators=(",", ":")), extra={"audit": record})
    return record


def audit_access(
    action: str,
    *,
    caller: Any = None,
    resource: Any = None,
    outcome: str = ALLOWED,
    reason: str | None = None,
    service: str | None = None,
    request: Any = None,
    method: str | None = None,
    route: str | None = None,
    request_id: str | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    """Record that ``caller`` performed ``action`` on ``resource``. Returns the record.

    ``request`` fills ``method``, ``route``, ``request_id`` and ``trace_id``
    (``request_fields``). ``method=`` and ``route=`` set those two where the
    request cannot: a middleware refusing before routing knows the method but
    has no matched route, and passes the route *template* it protects. Each
    explicit value wins over the request's.
    """
    return _emit(
        ACCESS,
        action,
        caller=caller,
        resource=resource,
        outcome=outcome,
        reason=reason,
        service=service,
        request=request,
        method=method,
        route=route,
        request_id=request_id,
        trace_id=trace_id,
    )


def audit_denied(
    action: str,
    *,
    caller: Any = None,
    resource: Any = None,
    reason: str | None = None,
    service: str | None = None,
    request: Any = None,
    method: str | None = None,
    route: str | None = None,
    request_id: str | None = None,
    trace_id: str | None = None,
) -> dict[str, Any]:
    """Record that ``caller`` was refused ``action``, at ``WARNING``. Returns the record.

    ``reason`` is a short code, not a message: it must not repeat what the
    caller sent. ``request``, ``method=`` and ``route=`` as for ``audit_access``.
    """
    return _emit(
        DENIED,
        action,
        caller=caller,
        resource=resource,
        outcome=DENIED,
        reason=reason,
        service=service,
        request=request,
        method=method,
        route=route,
        request_id=request_id,
        trace_id=trace_id,
    )


ResourceSpec = str | Callable[[Any], Any] | None


def _caller_at_exit(request: Any, caller: Any) -> Any:
    """The ``user`` dependency's caller, else whatever ``request.state.user`` holds now."""
    if caller is not None:
        return caller
    return getattr(getattr(request, "state", None), "user", None)


def _resource_of(request: Any, resource: ResourceSpec) -> Any:
    if resource is None:
        return None
    if callable(resource):
        return resource(request)
    return (getattr(request, "path_params", None) or {}).get(resource)


def audit_route(
    action: str,
    *,
    user: Callable[..., Any] | None = None,
    resource: ResourceSpec = None,
    service: str | None = None,
) -> Callable[..., Any]:
    """A FastAPI dependency recording one audit record per request of a route.

    - ``user``: the service's own dependency returning the verified caller
      (``JwtUser`` or similar). FastAPI caches it per request, so the token is
      verified once. Optional: without it (or when it returns ``None``) the
      caller is ``request.state.user``, read when the request *ends* — so a
      middleware, a route's own auth dependency or the handler may set it
      after this dependency has run.
    - ``resource``: the name of the path parameter holding the identifier, or a
      callable ``(request) -> id``.

    The handler returning records ``access``/``allowed``. An ``HTTPException``
    401 or 403 records ``denied`` with ``reason="http <status>"``; any other
    ``HTTPException`` or error records ``access``/``error``. The exception is
    re-raised unchanged. A refusal *returned* as a response rather than raised
    is not seen: call ``audit_denied`` there.

    Use it as ``dependencies=[Depends(audit_route(...))]`` on a route or a
    router. A refusal raised by a *sibling* dependency resolved before this one
    is not seen either; depend on the gate through ``user`` instead.
    """
    from fastapi import Depends, Request
    from starlette.exceptions import HTTPException

    async def _no_user() -> None:
        return None

    async def dependency(request: Request, caller: Any = Depends(user or _no_user)):  # noqa: B008
        target = _resource_of(request, resource)
        try:
            yield
        except HTTPException as exc:
            who = _caller_at_exit(request, caller)
            if exc.status_code in (401, 403):
                audit_denied(
                    action,
                    caller=who,
                    resource=target,
                    reason=f"http {exc.status_code}",
                    service=service,
                    request=request,
                )
            else:
                audit_access(
                    action,
                    caller=who,
                    resource=target,
                    outcome=ERROR,
                    reason=f"http {exc.status_code}",
                    service=service,
                    request=request,
                )
            raise
        except Exception as exc:
            audit_access(
                action,
                caller=_caller_at_exit(request, caller),
                resource=target,
                outcome=ERROR,
                reason=type(exc).__name__,
                service=service,
                request=request,
            )
            raise
        else:
            audit_access(
                action,
                caller=_caller_at_exit(request, caller),
                resource=target,
                service=service,
                request=request,
            )

    return dependency


__all__ = [
    "ACCESS",
    "ALLOWED",
    "AUDIT_LOGGER",
    "DENIED",
    "ERROR",
    "FIELDS",
    "PSEUDONYM_KEY_VAR",
    "audit_access",
    "audit_denied",
    "audit_route",
    "caller_fields",
    "configure_audit",
    "pseudonymise",
    "request_fields",
]
