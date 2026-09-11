"""Enhanced JWT token handling with PyJWT."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import logging
from typing import Any, Optional
import time

import jwt
from jwt import PyJWKClient

# Re-exported, not redefined. This module used to carry a second, byte-identical
# `AccessToken` of its own, which meant `celine.sdk.auth.AccessToken` and
# `celine.sdk.auth.jwt.AccessToken` were unrelated types to `isinstance` — a
# failure that reads as impossible. The name still resolves here, and now
# resolves to the one class every provider actually returns.
from celine.sdk.auth.models import AccessToken
from celine.sdk.settings.models import OidcSettings

__all__ = [
    "AccessToken",
    "JwtUser",
    "Organization",
    "extract_groups",
    "get_expected_audiences",
    "is_service_account",
    "normalize_groups",
    "organization_aliases",
    "organization_groups",
    "realm_groups",
]


logger = logging.getLogger(__name__)


@lru_cache(maxsize=8)
def _get_jwks_client(jwks_uri: str) -> PyJWKClient:
    logger.info(f"Loading JWKS from {jwks_uri}")
    return PyJWKClient(jwks_uri, cache_jwk_set=True, lifespan=3600)


def normalize_groups(values: Any) -> list[str]:
    """Strip Keycloak's leading slash and deduplicate, preserving order.

    Anything that is not a list is discarded rather than iterated: a ``groups``
    claim that arrived as a bare string would otherwise be walked character by
    character and yield single-letter "groups".
    """
    if not isinstance(values, (list, tuple)):
        return []

    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        name = value.lstrip("/")
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out


def realm_groups(claims: dict) -> list[str]:
    """Groups from the top-level ``groups`` claim — realm level **only**.

    Deliberately not `extract_groups`, which merges realm groups with every
    organization's groups into one flat list. That is the right answer for a
    service asking "is this user a viewer?", and the wrong one for a service
    deciding *which tenant* an action applies to: a realm group is a
    platform-wide grant, so merging lets a ``managers`` badge held inside
    organization A satisfy a realm-level check and authorise an action on
    organization B. A caller that authorises per organization must read the two
    levels apart, with this and `organization_groups`.
    """
    return normalize_groups(claims.get("groups"))


def organization_groups(claims: dict, alias: str) -> list[str]:
    """Groups the caller holds inside one specific organization.

    Read from the raw claim rather than `JwtUser.organizations` because the
    per-organization ``groups`` key is what carries a tenant-scoped role.
    """
    orgs = claims.get("organization")
    if not isinstance(orgs, dict):
        return []
    org = orgs.get(alias)
    if not isinstance(org, dict):
        return []
    return normalize_groups(org.get("groups"))


def organization_aliases(claims: dict) -> list[str]:
    """Every organization alias the caller is a member of, sorted."""
    orgs = claims.get("organization")
    if not isinstance(orgs, dict):
        return []
    return sorted(str(alias) for alias in orgs)


def extract_groups(claims: dict) -> list[str]:
    """Extract user groups from both realm-level and org-level claims.

    Realm groups come from the top-level ``groups`` claim.
    Org groups come from ``organization.<alias>.groups``.
    Returns a deduplicated flat list with leading slashes stripped.
    """
    raw: list[str] = []

    realm = claims.get("groups")
    if isinstance(realm, list):
        raw.extend(realm)

    orgs = claims.get("organization")
    if isinstance(orgs, dict):
        for org_data in orgs.values():
            if isinstance(org_data, dict):
                org_groups = org_data.get("groups")
                if isinstance(org_groups, list):
                    raw.extend(org_groups)

    seen: set[str] = set()
    result: list[str] = []
    for g in raw:
        if not isinstance(g, str):
            continue
        normalized = g.lstrip("/")
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def is_service_account(claims: dict) -> bool:
    """
    Detect a Keycloak client_credentials service account token.

    Keycloak sets preferred_username to 'service-account-<client_id>'
    for all client credentials grants. This is the most reliable signal.

    User tokens are identified by: email, groups (realm or org-level),
    or preferred_username that doesn't start with 'service-account-'.
    """

    preferred_username = claims.get("preferred_username", "")

    # Most reliable signal for Keycloak service accounts
    if isinstance(preferred_username, str) and preferred_username.startswith(
        "service-account-"
    ):
        return True

    # Explicit grant type (Auth0, other IdPs)
    if claims.get("gty") == "client-credentials":
        return True

    # Human indicators → not a service account
    if claims.get("email"):
        return False
    if extract_groups(claims):
        return False
    if preferred_username and not preferred_username.startswith("service-account-"):
        return False

    # Generic heuristic: has client_id/azp but no email (no human behind the token)
    if claims.get("client_id") and not claims.get("email"):
        return True

    return False


def get_expected_audiences(oidc: OidcSettings) -> list[str] | str | None:
    """
    Get expected audience(s) for token validation.

    Returns:
        List of audience strings, single string, or None to skip aud validation
    """
    audiences = []

    if oidc.audience:
        audiences.append(oidc.audience)

    if (
        oidc.include_client_id_as_audience
        and oidc.client_id
        and oidc.client_id != oidc.audience
    ):
        audiences.append(oidc.client_id)

    # Return list if we have audiences, None to skip validation
    return audiences if audiences else None


def _first(value: Any) -> str | None:
    """The first string of a KC multi-valued attribute, or the value itself."""
    if isinstance(value, str):
        return value or None
    if isinstance(value, (list, tuple)):
        for item in value:
            if isinstance(item, str) and item:
                return item
    return None


@dataclass
class Organization:
    """Organization membership parsed from the JWT 'organization' claim.

    KC 26 ``oidc-organization-membership-mapper`` with ``org.add.attributes=true``
    and ``org.include.member.roles=true``, plus
    ``oidc-organization-group-membership-mapper``, produces::

        "organization": {
            "gr-renewable-community": {
                "id": "0f4ba6e3-0f1c-43a6-a117-4eb88863bb02",
                "type": ["rec"],
                "groups": ["/managers"]
            }
        }

    **Org attributes arrive flattened, not under an ``attributes`` key.** Measured
    against KC 26.4 with the realm's own mapper: ``type`` sits at the top level of
    the entry, so ``org.type`` is the reliable reader and
    ``org.has_attribute("type", ...)`` answers False on a real token. ``attributes``
    is still parsed, because a differently configured mapper does nest them, and
    ``type`` falls back to it.

    ``alias`` is the KC organization alias (used directly as the DT network ID, and
    as the REC registry's community key). ``id`` is the organization's KC UUID.
    ``groups`` are the groups the caller holds **inside this organization** — a
    tenant-scoped role, which is not the same thing as a realm group; see
    `realm_groups`.
    """

    alias: str
    type: Optional[str] = None
    attributes: dict[str, list[str]] = field(default_factory=dict)
    id: Optional[str] = None
    groups: list[str] = field(default_factory=list)

    def is_type(self, type: str) -> bool:
        return type == self.type

    def get_attribute(self, name: str) -> list[str]:
        """Return the values for an org attribute, or an empty list."""
        return self.attributes.get(name, [])

    def has_attribute(self, name: str, value: str) -> bool:
        """Return True if the org attribute ``name`` contains ``value``."""
        return value in self.get_attribute(name)

    @classmethod
    def _from_claim(cls, alias: str, data: Any) -> "Organization":
        # organization: {'example-dso': {'id': '179d8382-58fe-4092-8bfe-ecc607a4b804', 'type': ['dso']}}
        attributes: dict[str, list[str]] = {}
        org_id: str | None = None
        groups: list[str] = []

        org_type: str | None = None
        if isinstance(data, dict):

            raw_attrs = data.get("attributes", {})
            if isinstance(raw_attrs, dict):
                attributes = {
                    k: v if isinstance(v, list) else [v] for k, v in raw_attrs.items()
                }

            # Flattened first, nested second. The realm's mapper emits the
            # flattened shape; the nested one is what the docstring above used to
            # promise, and a mapper elsewhere may still produce it.
            org_type = _first(data.get("type")) or _first(attributes.get("type"))

            raw_id = data.get("id")
            org_id = raw_id if isinstance(raw_id, str) and raw_id else None

            groups = normalize_groups(data.get("groups"))

        return cls(
            alias=alias,
            type=org_type,
            attributes=attributes,
            id=org_id,
            groups=groups,
        )


@dataclass
class JwtUser:
    """Structured user from JWT token with common claims."""

    # Standard OIDC claims
    sub: str  # Subject (user ID)
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    preferred_username: Optional[str] = None

    # Token metadata
    iss: Optional[str] = None  # Issuer
    aud: Optional[str | list[str]] = None  # Audience
    exp: Optional[int] = None  # Expiration time
    iat: Optional[int] = None  # Issued at

    # Organization memberships (from KC 'organization' claim)
    organizations: list[Organization] = field(default_factory=list)

    # All claims as dict for custom/service-specific claims
    claims: dict[str, Any] = field(default_factory=dict)

    token: Optional[str] = None

    @property
    def is_service_account(self) -> bool:
        return is_service_account(self.claims or {})

    @classmethod
    def from_token(
        cls, token: str, oidc: OidcSettings, algorithms: Optional[list[str]] = None
    ) -> JwtUser:
        """
        Parse JWT token and extract user information.

        Args:
            token: JWT token string
            verify: Whether to verify signature (requires jwks_uri)
            jwks_uri: JWKS URI for signature verification
            audience: Expected audience claim
            issuer: Expected issuer claim
            algorithms: Allowed algorithms (default: ["RS256", "HS256"])

        Returns:
            JwtUser instance with structured claims

        Examples:
            # Without verification (development/oauth2_proxy already verified)
            user = JwtUser.from_token(token)

            # With verification (production service-to-service)
            user = JwtUser.from_token(
                token,
                verify=True,
                jwks_uri="https://auth.example.com/.well-known/jwks.json",
                audience="my-service",
                issuer="https://auth.example.com"
            )
        """

        if token is None or token.strip() == "":
            raise ValueError("JWT is missing or empty")

        if "bearer" in token.lower():
            token = token.split(" ")[1]

        if algorithms is None:
            algorithms = ["RS256", "HS256", "ES256"]

        # Verified decode with signature check (reuse cached client to avoid per-request JWKS fetch)
        jwks_client = _get_jwks_client(oidc.jwks_uri)

        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
        except Exception as e:
            logger.warning(f"Failed to fetch signing key from {oidc.jwks_uri}: {e}")
            raise

        try:
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=algorithms,
                audience=oidc.audience,
                issuer=oidc.base_url,
                leeway=30,
                options={
                    "verify_exp": True,
                    "verify_aud": True if oidc.audience is not None else False,
                    "verify_nbf": True,
                },
            )
        except Exception as e:
            logger.warning(f"Failed to parse token: {e}")
            raise

        # Extract standard claims
        sub = payload.get("sub")
        if not sub:
            raise ValueError("JWT missing required 'sub' claim")

        # Parse organization memberships
        org_claim = payload.get("organization", {})
        organizations: list[Organization] = []
        if isinstance(org_claim, dict):
            for alias, data in org_claim.items():
                organizations.append(Organization._from_claim(alias, data))

        return cls(
            sub=sub,
            email=payload.get("email"),
            email_verified=payload.get("email_verified"),
            name=payload.get("name"),
            given_name=payload.get("given_name"),
            family_name=payload.get("family_name"),
            preferred_username=payload.get("preferred_username"),
            iss=payload.get("iss"),
            aud=payload.get("aud"),
            exp=payload.get("exp"),
            iat=payload.get("iat"),
            organizations=organizations,
            claims=payload,
            token=token,
        )

    def is_expired(self, leeway: int = 0) -> bool:
        """Check if token is expired."""
        if self.exp is None:
            return False
        return time.time() > (self.exp + leeway)

    def is_valid(self, leeway: int = 30) -> bool:
        """Check if token is still valid (not expired with leeway)."""
        return not self.is_expired(-leeway)

    @property
    def organization_aliases(self) -> list[str]:
        """Return the list of organization aliases the user belongs to."""
        return [o.alias for o in self.organizations]

    def get_organization(self, alias: str) -> Organization | None:
        """Return the Organization for the given alias, or None."""
        for o in self.organizations:
            if o.alias == alias:
                return o
        return None

    def is_member_of(self, alias: str) -> bool:
        """Return True if the user belongs to the given organization alias."""
        return any(o.alias == alias for o in self.organizations)

    def get_claim(self, key: str, default: Any = None) -> Any:
        """Get a custom claim value."""
        return self.claims.get(key, default)

    def has_role(self, role: str, claim_key: str = "roles") -> bool:
        """Check if user has a specific role."""
        roles = self.get_claim(claim_key, [])
        if isinstance(roles, list):
            return role in roles
        if isinstance(roles, str):
            return role == roles
        return False

    def has_scope(self, scope: str, claim_key: str = "scope") -> bool:
        """Check if token has a specific scope."""
        scopes_str = self.get_claim(claim_key, "")
        if isinstance(scopes_str, str):
            scopes = scopes_str.split()
            return scope in scopes
        if isinstance(scopes_str, list):
            return scope in scopes_str
        return False

    @property
    def display_name(self) -> str:
        """Get best available display name."""
        return self.name or self.preferred_username or self.email or f"user-{self.sub}"

    def get_username(self) -> str:
        """Get best available display name."""
        if not self.preferred_username:
            logger.warning(
                f"preferred_username claims not available for {self.sub}, defaulting to sub"
            )
        return self.preferred_username or f"user-{self.sub}"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "sub": self.sub,
            "email": self.email,
            "name": self.name,
            "display_name": self.display_name,
            **self.claims,
        }
