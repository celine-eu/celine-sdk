"""Enhanced JWT token handling with PyJWT."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional
import time

import jwt
from jwt import PyJWKClient


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

    # All claims as dict for custom/service-specific claims
    claims: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_token(
        cls,
        token: str,
        *,
        verify: bool = False,
        jwks_uri: Optional[str] = None,
        audience: Optional[str | list[str]] = None,
        issuer: Optional[str] = None,
        algorithms: Optional[list[str]] = None,
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

        # Decode token
        if verify and jwks_uri:
            # Verified decode with signature check
            jwks_client = PyJWKClient(jwks_uri)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=algorithms,
                audience=audience,
                issuer=issuer,
                options={"verify_exp": True},
            )
        else:
            # Unverified decode (assumes upstream verification)
            payload = jwt.decode(
                token,
                options={
                    "verify_signature": False,
                    "verify_exp": False,
                    "verify_aud": False,
                },
            )

        # Extract standard claims
        sub = payload.get("sub")
        if not sub:
            raise ValueError("JWT missing required 'sub' claim")

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
            claims=payload,
        )

    def is_expired(self, leeway: int = 0) -> bool:
        """Check if token is expired."""
        if self.exp is None:
            return False
        return time.time() > (self.exp + leeway)

    def is_valid(self, leeway: int = 30) -> bool:
        """Check if token is still valid (not expired with leeway)."""
        return not self.is_expired(-leeway)

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
