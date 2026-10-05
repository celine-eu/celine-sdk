# Identity

`celine.sdk.auth`. Twelve repositories import it, and it is where every CELINE service
decides whether a token is genuine. A permissive change here is permissive everywhere.

---

## Verifying a token

### REQ-0020 — a token is verified, never merely decoded

`JwtUser.from_token` checks the signature against the issuer's published keys and enforces
`exp`, `nbf` and `iss`. There is no unverified decode path in the public surface: a caller
holding a token and settings either gets a verified `JwtUser` or an exception.

Which signature algorithms are accepted is REQ-0043.

### REQ-0021 — signing keys come from the configured JWKS URI, over a client cached per URI

`OidcSettings.jwks_uri` is the source. The `PyJWKClient` is memoised per URI so a service
verifying thousands of requests fetches the key set once, and the key set is itself cached
for an hour.

**This memoisation is the single seam for testing.** A test replaces the JWKS *fetch* and
leaves every check above live; substituting a mocked validator instead proves only that the
mock was called.

### REQ-0022 — an expired token is rejected, with thirty seconds of leeway

The leeway exists for clock skew between a service and the identity provider. A token
expired by less than it is still accepted; one expired by more is not.

### REQ-0023 — a token signed by a key the issuer does not publish is rejected

Signature verification is the point of the exercise: a well-formed token carrying correct
claims and a foreign signature must not parse.

### REQ-0024 — a token from another issuer is rejected

`iss` must equal `OidcSettings.base_url`. A token that is genuine elsewhere is not genuine
here.

### REQ-0025 — an `Authorization` header value is accepted as well as a bare token

`Bearer <token>` is stripped, in any case. Services pass the header through unchanged often
enough that requiring them to split it produced the bug this absorbs.

### REQ-0026 — the audience is validated only when one is configured

With `OidcSettings.audience` set, `aud` must contain it. With it unset, **audience
validation is skipped entirely** — a permissive default, and the reason a service that never
declares an audience is not checking one.

`get_expected_audiences()` composes `audience` with `client_id` (when
`include_client_id_as_audience` is on) and returns `None` when there is nothing to check.
It is a helper **for callers that build their own validation**; `from_token` does not use
it, so `allowed_audiences` and `include_client_id_as_audience` have no effect on
`from_token`. Anything relying on them must apply them itself.

### REQ-0027 — a token without a subject is refused

`sub` identifies the principal; a verified token that names nobody is useless and is a
`ValueError` rather than a `JwtUser` with an empty id.

### REQ-0028 — a missing or empty token is refused before any network call

`None`, `""` or whitespace raises `ValueError` without touching the JWKS endpoint. An
unauthenticated request must not be able to cause an outbound fetch.

### REQ-0043 — the signature algorithm comes from an asymmetric allow-list and the published key, and `exp` is required

`ALLOWED_JWT_ALGORITHMS` is `RS256` and `ES256` — what a Keycloak key set publishes for its
RSA and EC P-256 signing keys. A caller's `algorithms` may narrow that set, never widen it:
names outside it are ignored, and a set that leaves nothing raises `ValueError`. `HS*` and
`none` are never accepted, since a key set has no shared secret to verify them against.

The algorithm is the signing key's, as the key set assigns it (`alg`, or derived from
`kty`/`crv`), never the one the token's header names. A key whose algorithm is outside the
allowed set verifies nothing.

A token without `exp` is refused: a token that never expires is not one this platform issues.

---

## Reading a verified token

### REQ-0029 — organization memberships are parsed from the `organization` claim

Each key becomes an `Organization` with that key as its `alias` — which is used directly as
the Digital Twin network id. `type` is a single-element list in Keycloak and is flattened to
a string; `attributes` are normalised so every value is a list, whatever the claim shape.

`organization_aliases`, `get_organization(alias)` and `is_member_of(alias)` read them. An
unparseable or absent claim yields no memberships rather than an error.

### REQ-0031 — a service account is distinguished from a user

`is_service_account` treats a `preferred_username` beginning `service-account-` as
authoritative (Keycloak's client-credentials convention) and `gty=client-credentials` as an
equivalent signal from other providers. An email, any group, or any other
`preferred_username` marks a human. Failing all of those, a token carrying a client id and
no email is a service, and so is a token whose Keycloak grant marker (the `jti` prefix Keycloak
26 writes, e.g. `trrtcc:`) names client credentials. A realm that does not assign Keycloak's
built-in `service_account` scope issues such tokens with neither `preferred_username` nor
`client_id`.

"Any group" means a group at either level, realm or organization. It is a signal that a
person is behind the token, **not a grant**: a realm group present in a token classifies it
as a user's and authorises nothing (REQ-0042). Classifying by group errs towards "user",
which is the safe direction — a user is never authorised by scope.

The platform authorises services by scope and users by their platform role and organization
groups (REQ-0042); this is the function that decides which of the two a caller is.

### REQ-0032 — claims are reachable by name, role and scope

`get_claim`, `has_role` (a realm role, read from `realm_access.roles` as REQ-0042 states;
until 2.0.0 it read a top-level `roles` claim, which no Keycloak mapper on the platform
emits), `has_scope` (a space-separated string or a list), `display_name` (name, then username, then email, then `user-<sub>`), `get_username`
(username, else `user-<sub>`) and `to_dict`. Each tolerates the claim being absent or of the
wrong shape, because the claim set is the identity provider's to change.

### REQ-0033 — a parsed token can report its own expiry

`is_expired(leeway)` and `is_valid(leeway)` read `exp`. A token with no `exp` is treated as
not expired — the verification step has already refused an expired one, so these serve
callers holding a token they intend to reuse.

---

### REQ-0040 — an organization membership carries its Keycloak id and the groups held inside it

`Organization` exposes `id` (the KC organization UUID) and `groups` (the groups the caller
holds **inside that organization**, leading slashes stripped) alongside `alias`, `type` and
`attributes`. Both are absent from the claim on a realm whose mapper does not emit them, and
are then an empty value rather than an error.

`type` is read from the flattened `type` key first and from `attributes.type` second.
Keycloak's own organization mapper emits the flattened shape; the nested one is what a
differently configured mapper produces, and both must parse.

### REQ-0042 — a platform grant comes only from the realm role `platform-admin`; an organization's groups count only inside that organization

There are exactly two levels of authority in a token, and nothing in this package merges
them:

- **Platform.** `realm_roles(claims)` reads `realm_access.roles` and nothing else: not a
  top-level `roles` claim, not `resource_access.<client>.roles`, not `groups`. The one
  platform-wide grant is the realm role `PLATFORM_ADMIN_ROLE` (`"platform-admin"`), and
  `is_platform_admin(claims)` is true exactly when that role is among them. A missing or
  malformed `realm_access` yields no roles and is not an error.
- **Organization.** `organization_groups(claims, alias)` reads
  `organization.<alias>.groups` for that one alias, leading slashes stripped. A group held in
  one organization is never visible through another alias, and is never a platform grant,
  whatever it is called — an organization's `admins` is not a platform administrator.

A **realm group grants nothing.** The top-level `groups` claim (`/admins`, `admins`, …) is not
read by any authorization helper; a token that still carries one is treated exactly as if it
did not.

`Grants.from_claims(claims)` (also `JwtUser.grants`) is the structured reader for callers that
need both levels: `.platform` holds the realm roles, `.in_org(alias)` one organization's
groups, `.is_platform_admin` the platform check. It offers no flat list of both levels.
`JwtUser.realm_roles`, `JwtUser.is_platform_admin` and `JwtUser.has_role(role)` read the same
realm roles.

**In a policy decision** the two levels stay in two fields of `celine.sdk.policies.Subject`:
`roles` (the realm roles, filled from `realm_roles`) reaches Rego as `input.subject.roles`,
and `groups` (one organization's groups) as `input.subject.groups`. A policy checks the
platform grant as `"platform-admin" in input.subject.roles`. The engine never copies a role
into `groups` or a group into `roles`, and a subject built without roles has an empty list,
never a missing key (REQ-0056).

`organization_aliases(claims)` returns every alias the caller is a member of, sorted. Every
reader tolerates a claim of the wrong shape and answers empty.

**Removed in the same change (breaking):** `extract_groups`, which merged the realm `groups`
claim with every organization's groups (formerly REQ-0030, deprecated 2026-10-03 after it made
a community's own `admins` dataset-api's platform administrator, NIS2 R1), and
`realm_groups`, which read the realm `groups` claim as a platform grant (formerly REQ-0041).
Realm groups are no longer a platform mechanism at all; the platform level is the realm role.

## Obtaining a token

### REQ-0034 — an access token carries its expiry and answers whether it is still usable

`AccessToken(access_token, expires_at, refresh_token=None, token_type="Bearer")`.

**There is one such class, whatever path it is imported by.** `celine.sdk.auth.AccessToken`,
`celine.sdk.auth.models.AccessToken` and `celine.sdk.auth.jwt.AccessToken` are the same
object; `celine.sdk.auth.jwt` carried a second, byte-identical definition until 2026-08-15,
which made an `isinstance` check across the two paths fail for reasons that read as
impossible.

`expires_at` is an epoch float. `is_valid(leeway=30)` is false once the token is within the
leeway of expiring — early, deliberately, so a token is replaced before it is refused.
`to_header()` renders `"<token_type> <access_token>"`.

### REQ-0035 — a forwarded token is used as-is

`StaticTokenProvider` wraps a token a caller already holds — the case for every service that
forwards its user's JWT downstream. A `Bearer ` prefix is stripped; nothing is refreshed and
nothing is verified, because whoever accepted the request already verified it.

It is exported by `celine.sdk.auth`, beside the provider it is an alternative to. (It was
reachable only as `celine.sdk.auth.static.StaticTokenProvider` until 2026-08-15; that path
still works.)

### REQ-0036 — a provider notifies its listeners when a new token is issued

`add_token_renewed_listener` registers an async callback, fired after each issuance. This is
what lets a long-lived MQTT connection rebuild itself on fresh credentials (REQ-0080).

**A failing listener does not fail the issuance**, and does not stop the remaining
listeners: the exception is logged and the loop continues. A token was still obtained, and
dropping it because a subscriber misbehaved would be worse.

### REQ-0037 — the client-credentials provider reuses a token until it is close to expiring

`OidcClientCredentialsProvider.get_token()` returns the cached token while `is_valid()`
holds, so the common path makes no network call.

### REQ-0038 — a refresh is attempted before re-authenticating, and its failure is not fatal

Holding a refresh token, the provider tries the refresh grant; if that fails for any reason
it falls back to a full client-credentials authentication. Either way the renewal listeners
are fired with the new token.

### REQ-0039 — endpoints are discovered from the issuer, once

`OidcDiscoveryClient` reads `<issuer>/.well-known/openid-configuration` and caches the
`issuer`, `token_endpoint` and `jwks_uri` it finds for the life of the client. A trailing
slash on the configured issuer is not a second URL.

`expires_in` from the token response fixes `expires_at`; a response omitting it is treated
as five minutes.
