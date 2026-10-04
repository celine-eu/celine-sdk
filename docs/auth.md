# Authentication

The `celine.sdk.auth` module provides OIDC token acquisition and verified JWT parsing for
CELINE services. What it must do is stated in
[specifications/identity.md](specifications/identity.md); this page is how to use it.

## Verifying a token

`JwtUser.from_token()` verifies and parses in one step. There is no unverified decode path:
the signature is checked against the issuer's JWKS, and `exp`, `nbf` and `iss` are enforced.

```python
from celine.sdk.auth import JwtUser
from celine.sdk.settings import OidcSettings

oidc = OidcSettings()                    # CELINE_OIDC_* from the environment
user = JwtUser.from_token(authorization_header, oidc)   # "Bearer eyJ…" or "eyJ…"

user.sub                 # subject id
user.email               # may be None
user.claims              # every verified claim
user.is_service_account  # bool
```

A failure raises — `jwt.ExpiredSignatureError`, `jwt.InvalidIssuerError`,
`jwt.InvalidSignatureError`, or `ValueError` for a missing token or a token with no `sub`.

**Audience is only checked when you configure one.** With `CELINE_OIDC_AUDIENCE` unset, a
token minted for another service verifies here. Set it in any service that is a resource
server.

`CELINE_OIDC_ALLOWED_AUDIENCES` and `CELINE_OIDC_INCLUDE_CLIENT_ID_AS_AUDIENCE` do **not**
affect `from_token`; they feed `get_expected_audiences()`, for callers doing their own
validation.

## Platform roles and organization groups

A token carries authority at exactly two levels, and the SDK never merges them:

| Level | JWT claim | Example | Valid |
|---|---|---|---|
| **Platform** | `realm_access.roles` | `{"roles": ["platform-admin", …]}` | everywhere |
| **Organization** | `organization.<alias>.groups` | `{"example_rec": {"groups": ["/admins"]}}` | inside `example_rec` only |

The only platform-wide grant is the realm **role** `platform-admin` (`PLATFORM_ADMIN_ROLE`).
An organization's `admins` group is that organization's administrator and nothing more.
**Realm groups** (the top-level `groups` claim, `/admins` and friends) are not a platform
mechanism: no helper reads them, and a token that still carries one gains nothing from it.
Neither does a top-level `roles` claim or a client role in `resource_access`.

```python
from celine.sdk.auth import Grants, is_platform_admin, organization_groups

if is_platform_admin(user.claims):            # or user.is_platform_admin
    ...
groups = organization_groups(user.claims, "example_rec")   # ["admins"]

grants = user.grants                          # Grants.from_claims(user.claims)
grants.platform                               # frozenset({"platform-admin", ...})
grants.in_org("example_rec")                  # frozenset({"admins"})
grants.in_org("example_dso")                  # frozenset() — not a member
```

`user.has_role(name)` reads a realm role too. There is deliberately no function returning
both levels as one list: `extract_groups` did, and a community's own `admins` became a
platform administrator through it. It and `realm_groups` were removed in 2.0.0.

### In a policy decision

`celine.sdk.policies.Subject` keeps the two levels in two fields, and the engine passes both
to Rego unchanged: `roles` becomes `input.subject.roles`, `groups` becomes
`input.subject.groups`. Fill `roles` from `realm_roles` and `groups` from the one
organization the request is about; never put a role into `groups` or a group into `roles`.

```python
from celine.sdk.auth import organization_groups, realm_roles
from celine.sdk.policies import Subject, SubjectType

subject = Subject(
    id=user.sub,
    type=SubjectType.SERVICE if user.is_service_account else SubjectType.USER,
    roles=realm_roles(user.claims),                         # or user.realm_roles
    groups=organization_groups(user.claims, "example_rec"),
)
```

```rego
allow if "platform-admin" in input.subject.roles     # the platform administrator
allow if "admins" in input.subject.groups            # this organization's admins
```

**Service vs. user** is `is_service_account()`: `preferred_username` starting
`service-account-` (Keycloak's convention), `gty=client-credentials`, or Keycloak's
client-credentials `jti` marker; an email, any group at either level, or any other username
marks a human. A group here only classifies the token, it grants nothing.

```python
from celine.sdk.auth.jwt import is_service_account

if is_service_account(user.claims):
    ...  # authorize by scope
else:
    ...  # authorize by platform role and organization groups
```

## Organizations

Keycloak organization memberships are parsed from the `organization` claim. The alias is the
Digital Twin network id.

```python
user.organization_aliases          # ["example_rec"]
org = user.get_organization("example_rec")
org.type                           # "rec"
org.get_attribute("tier")          # always a list
user.is_member_of("example_rec")   # bool
```

## Obtaining a token

### OidcClientCredentialsProvider

Service-to-service calls. Endpoints are discovered from the issuer, the token is cached
until it is close to expiring, and a refresh is attempted before re-authenticating.

```python
from celine.sdk.auth import OidcClientCredentialsProvider
from celine.sdk.settings import OidcSettings

oidc = OidcSettings()
provider = OidcClientCredentialsProvider(
    base_url=oidc.base_url,
    client_id=oidc.client_id,
    client_secret=oidc.client_secret,
    scope=oidc.scope,           # optional
    timeout=oidc.timeout,
    verify_ssl=oidc.verify_ssl,
)

token = await provider.get_token()
token.access_token   # raw JWT
token.expires_at     # epoch seconds (float)
token.to_header()    # "Bearer eyJ…"
```

### StaticTokenProvider

For a service forwarding the caller's own JWT downstream. No refresh, no verification — the
request that carried it was already verified.

```python
from celine.sdk.auth import StaticTokenProvider   # or celine.sdk.auth.static

provider = StaticTokenProvider(request.headers["authorization"])   # "Bearer …" is stripped
```

### Reacting to a renewal

```python
async def on_renewed() -> None:
    ...  # e.g. rebuild a long-lived connection

provider.add_token_renewed_listener(on_renewed)
```

Listeners are fired after each issuance. An exception in one is logged and does not affect
the others or the token.

## AccessToken

```python
@dataclass
class AccessToken:
    access_token: str
    expires_at: float          # epoch seconds
    refresh_token: str | None = None
    token_type: str = "Bearer"

    def is_valid(self, leeway: int = 30) -> bool: ...
    def to_header(self) -> str: ...
```

Importable as `celine.sdk.auth.AccessToken`, `celine.sdk.auth.models.AccessToken` or
`celine.sdk.auth.jwt.AccessToken` — all three are the same class. (Until 2026-08-15 the
`jwt` one was a separate, identical definition, so `isinstance` across the two failed.)

## Configuration

See [settings.md](settings.md). The variables this module reads are `CELINE_OIDC_*`:
`BASE_URL`, `JWKS_URI`, `CLIENT_ID`, `CLIENT_SECRET`, `AUDIENCE`, `SCOPE`, `TIMEOUT`,
`VERIFY_SSL`.
