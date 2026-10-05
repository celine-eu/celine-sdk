# Access audit

`celine.sdk.audit`. Each service records who read what, and who was refused, in the same
shape, so one log query answers the question for the whole platform. The record names the
caller by identifier only; the audit trail itself must not become a store of personal data.

---

### REQ-0190 — one record shape, on one logger, as one JSON line

Every record is emitted on the logger `celine.audit` as a single JSON object, and is also
attached to the log record as `record.audit`. It always carries the same fields, in this
order, with `null` for an unknown value:

| Field | Holds |
|---|---|
| `event` | `access` or `denied` |
| `service` | `configure_audit(service)`, a call's `service=`, else `OTEL_SERVICE_NAME`, else `unknown` |
| `sub`, `client_id`, `service_account` | the verified caller (REQ-0191) |
| `action` | what the service did, in its own words: `dataset.read`, `twin.values.read` |
| `method`, `route` | the HTTP method and the matched route template (`/datasets/{dataset_id}`) |
| `resource` | the identifier acted on (REQ-0191) |
| `outcome` | `allowed`, `denied` or `error` |
| `reason` | a short code for a refusal or an error: `http 403`, `not_member` |
| `request_id`, `trace_id` | `X-Request-ID` / `X-Correlation-ID`, and the `traceparent` trace id, when well-formed |
| `ts` | UTC, ISO 8601, milliseconds |

`audit_access` logs at `INFO`, `audit_denied` at `WARNING`. The `celine.audit` logger is
held at `INFO` whatever `LOG_LEVEL` says: quieting a service does not switch its audit off.

### REQ-0191 — no personal data in a record

- The caller is `sub`, `client_id` (`azp`, else `client_id`) and whether the token is a
  service account. Email, name and username are never read.
- `resource` holds an identifier the platform issued: a dataset id, an asset id, a twin or
  entity id, a community id, a commitment id. When the only identifier is personal (an
  email, a fiscal code, a delivery point code), the caller passes `pseudonymise(value)`:
  `h:` and 16 hex characters of SHA-256, keyed with `CELINE_AUDIT_PSEUDONYM_KEY` when set.
- As a backstop every string field is checked: an email-shaped value is replaced by its
  pseudonym, control characters are dropped, length is capped at 256.
- `route` is the template, never the raw path, and never the query string.

### REQ-0192 — a route opts in with one dependency

`audit_route(action, user=…, resource=…)` is a FastAPI dependency for a route or a router.
`user` is the service's own dependency returning the verified caller (FastAPI resolves it
once per request). Without it, or when it returns `None`, the caller is
`request.state.user` as it stands when the request ends: a middleware, an auth dependency
declared after this one, or the handler may set it, and the route needs no extra
dependency. `resource` names the path parameter holding the identifier, or is a callable
`(request) -> id`.

| The handler | Record |
|---|---|
| returns | `access`, `allowed` |
| raises `HTTPException` 401 or 403 | `denied`, `reason = "http <status>"` |
| raises another `HTTPException` | `access`, `error`, `reason = "http <status>"` |
| raises anything else | `access`, `error`, `reason = <exception class>` |

The exception is re-raised unchanged. A request the `user` dependency itself refuses is
not recorded (there is no verified caller to name), nor is a refusal *returned* as a
response rather than raised: the service calls `audit_denied` there.

A refusal raised by an auth dependency declared *after* `audit_route` is recorded as
`denied`, with no caller when none was verified.

### REQ-0193 — a record names the route outside a matched Starlette route

`audit_access` and `audit_denied` take the request as `request=`: a Starlette / FastAPI
request, or a Flask request inside its request context, whose matched URL rule under the
script root (`/dashboard/<int:pk>`) is the route. With no matched route or rule, `route`
is `null`.

Both also take `method=` and `route=`. Each, when given, wins over the request's value:
a middleware refusing before routing passes the route template it guards. `method` is
upper-cased, and `route` is cleaned like every string field (REQ-0191) — it is a
template, never the raw path.

### REQ-0194 — a gate names its own reason

A gate that refuses for a reason of its own calls `note_reason(request, reason)` before it
raises, or before it returns its refusal as a response. It sets
`request.state.audit_note` (`AUDIT_NOTE_ATTR`) to the pair `(outcome, reason)`; `outcome`
is `denied` (the default) or `error`, anything else is a `ValueError`. `reason` is a short
code, never what the caller sent. The last note of a request wins.

When the request ends, `audit_route` (REQ-0192) records the noted outcome and reason in
place of the ones the status gives:

| The request ends with | No note | A note `(denied, r)` |
|---|---|---|
| a returned response | `access`, `allowed` | `denied`, `reason = r` |
| `HTTPException` 401 or 403 | `denied`, `http <status>` | `denied`, `reason = r` |
| another `HTTPException` (a 404 that hides an entity) | `access`, `error`, `http <status>` | `denied`, `reason = r` |
| any other exception | `access`, `error`, `<exception class>` | unchanged |

A note `(error, r)` records `access`, `error`, `reason = r` in the same places. The caller,
resource and route are read as REQ-0192 says; the record shape (REQ-0190) is unchanged.
