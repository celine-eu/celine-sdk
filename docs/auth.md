# Authentication

The `celine.sdk.auth` module provides OIDC-based token management for CELINE services.

## Key Components

### OidcTokenProvider

Fetches and caches access tokens from a Keycloak-compatible OIDC provider using the client credentials flow. Automatically refreshes tokens before expiry.

```python
from celine.sdk.auth import OidcTokenProvider
from celine.sdk.settings import OidcSettings

settings = OidcSettings()
provider = OidcTokenProvider(settings)

token = await provider.get_token()
# token.access_token: str  — raw JWT
# token.expires_at: datetime
```

### StaticTokenProvider

For testing and local development, accepts a pre-configured static token:

```python
from celine.sdk.auth import StaticTokenProvider

provider = StaticTokenProvider(token="eyJ...")
```

### JWT Parsing

The `jwt` module provides `JwtUser.from_token()` for verified JWT decoding and helpers for working with token claims.

### Groups & Subject Type Detection

CELINE uses two group models depending on how the user was provisioned:

| Source | JWT claim | Example |
|---|---|---|
| **Realm-level** (platform admins) | `groups` | `["/admins"]` |
| **Org-level** (REC participants) | `organization.<alias>.groups` | `{"example_rec": {"groups": ["/viewers"]}}` |

Realm-level groups grant cross-org capabilities (e.g., `admins` can manage all RECs). Org-level groups are scoped to a specific organization and are the default for REC participants imported via `celine-policies keycloak sync-users`.

**Always use `extract_groups()`** to read groups from JWT claims. It merges both sources into a flat, deduplicated list with leading slashes stripped:

```python
from celine.sdk.auth.jwt import extract_groups

groups = extract_groups(user.claims)
# ["viewers"]  — works for both realm and org-level groups
```

Do NOT use `claims.get("groups")` directly — it only returns realm-level groups and will miss org-level memberships.

**Service vs. user detection** uses `is_service_account()`, which checks `preferred_username` (authoritative for Keycloak service accounts) and human indicators (email, groups, organization membership):

```python
from celine.sdk.auth.jwt import is_service_account

if is_service_account(claims):
    # client credentials token — check scopes
else:
    # user token — check groups via extract_groups()
```

OPA policies follow this pattern: services are authorized by **scopes**, users by **group membership**.

### OIDC Discovery

The `oidc_discovery` module fetches the OIDC well-known configuration from the provider's discovery endpoint, used internally to resolve the JWKS URI and token endpoint.

## AccessToken Model

```python
class AccessToken:
    access_token: str       # Raw JWT string
    token_type: str         # Always "Bearer"
    expires_in: int         # Seconds until expiry
    expires_at: datetime    # Absolute expiry timestamp
    scope: str              # Space-separated scopes
```

## Configuration

Auth settings come from `OidcSettings` (see [settings.md](https://celine-eu.github.io/projects/celine-sdk/docs/settings)):

| Variable | Description |
|---|---|
| `OIDC_ISSUER` | OIDC issuer URL (e.g., Keycloak realm URL) |
| `OIDC_CLIENT_ID` | Service client ID |
| `OIDC_CLIENT_SECRET` | Service client secret |
