"""Enhanced JWT token handling with PyJWT."""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
import logging
from typing import Any, Optional
import time

import jwt
from jwt import PyJWKClient

from celine.sdk.settings.models import OidcSettings


logger = logging.getLogger(__name__)


@lru_cache(maxsize=8)
def _get_jwks_client(jwks_uri: str) -> PyJWKClient:
    logger.info(f"Loading JWKS from {jwks_uri}")
    return PyJWKClient(jwks_uri, cache_jwk_set=True, lifespan=3600)


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


@dataclass
class Organization:
    """Organization membership parsed from the JWT 'organization' claim.

    KC 26 ``oidc-organization-membership-mapper`` with ``org.add.attributes=true``
    and ``org.include.member.roles=true`` produces::

        "organization": {
            "set": {
                "attributes": {"type": ["dso"]},
                "roles": ["member"]
            }
        }

    ``alias`` is the KC organization alias (used directly as the DT network ID).
    ``attributes`` contains org-level attributes, e.g. ``{"type": ["dso"]}``.
    ``roles`` contains member roles (built-in ``"member"`` in KC 26).
    """

    alias: str
    type: Optional[str] = None
    attributes: dict[str, list[str]] = field(default_factory=dict)

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

        org_type: str | None = None
        if isinstance(data, dict):

            org_type = data.get("type", None)
            org_type = (
                org_type[0]
                if isinstance(org_type, list) and len(org_type) > 0
                else None
            )

            raw_attrs = data.get("attributes", {})
            if isinstance(raw_attrs, dict):
                attributes = {
                    k: v if isinstance(v, list) else [v] for k, v in raw_attrs.items()
                }
        return cls(alias=alias, type=org_type, attributes=attributes)


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


@dataclass
class AccessToken:
    """Access token with expiration tracking."""

    access_token: str
    expires_at: float
    refresh_token: str | None = None
    token_type: str = "Bearer"

    def is_valid(self, leeway: int = 30) -> bool:
        """Check if token is still valid."""
        return time.time() < (self.expires_at - leeway)

    def to_header(self) -> str:
        """Get Authorization header value."""
        return f"{self.token_type} {self.access_token}"
