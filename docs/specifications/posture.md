# Deployment posture

`celine.sdk.posture`. The SDK's defaults describe the local platform (REQ-0003), and so do
every service's: a guessable database password, a client secret equal to the client id, a
policy engine that may be missing. They are safe only because something refuses them when
the environment does not say it is development. This module is that something, shared, so
every service applies the same rule.

---

### REQ-0180 — only `dev` relaxes; unset is hardened

`current_env()` reads `CELINE_ENV`, then `ENVIRONMENT`, then any legacy names the caller
passes, and returns the first non-empty value stripped and lowercased, or `""`. `is_dev()` is
true **only** for `dev`. Unset, empty, `prod`, `staging`, `test` and any misspelling are
hardened (`is_hardened()`).

The one relaxed value is enumerated, never the hardened ones: forgetting the variable, or
mistyping it, must leave a deployment strict. Development opts in, in each component's own
`task run`.

### REQ-0181 — the guard collects every violation and raises once outside dev

`PostureGuard(service)` collects violations; `enforce()` raises `InsecureConfiguration`
listing all of them when hardened and logs one warning when `dev`. A guard with no violations
never raises. A deployment learns every missing value in one cycle.

### REQ-0182 — the local stack's credentials are recognised

- `forbid_dev_database_url` flags a URL whose password is a local-stack password
  (`securepassword123`, `postgres`) or trivially weak. A URL without a password is not
  flagged.
- `forbid_secret_equal_to_client_id` flags a client secret that is empty or equal to the
  client id. A service with no client id holds no client identity and is not flagged.
- `forbid_default`, `forbid_true`, `forbid_false` and `require_set` register a service's own
  dev defaults and switches.

### REQ-0183 — an issuer nobody configured is refused outside dev

`require_explicit_oidc(oidc)` flags `CELINE_OIDC_BASE_URL` and `CELINE_OIDC_JWKS_URI` when
the value is the SDK's default rather than one set by the environment or by code, and,
with `require_audience=True`, an unset audience. TLS on the issuer is a deployment property
and is not checked: a prod-like local run names the local realm explicitly and passes.

### REQ-0184 — the API documentation is off outside dev unless opted in

`docs_urls(docs_url=…, redoc_url=…, openapi_url=…)` returns the three `FastAPI(...)` keyword
arguments. In `dev` they are the service's own paths, unchanged — a service mounting its
documentation under `/api/docs` passes those paths. Anywhere else all three are `None`, so
FastAPI serves no Swagger UI, no ReDoc and no `openapi.json`, unless `CELINE_PUBLIC_DOCS`
is `true` (`1`, `yes`, `on`). Unset, empty or any other value keeps them off: a deployment
that wants its API description public says so.
