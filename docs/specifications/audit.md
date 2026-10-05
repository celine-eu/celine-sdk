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
once per request); without it `request.state.user` is read. `resource` names the path
parameter holding the identifier, or is a callable `(request) -> id`.

| The handler | Record |
|---|---|
| returns | `access`, `allowed` |
| raises `HTTPException` 401 or 403 | `denied`, `reason = "http <status>"` |
| raises another `HTTPException` | `access`, `error`, `reason = "http <status>"` |
| raises anything else | `access`, `error`, `reason = <exception class>` |

The exception is re-raised unchanged. A request the `user` dependency itself refuses is
not recorded (there is no verified caller to name), nor is a refusal *returned* as a
response rather than raised: the service calls `audit_denied` there.
