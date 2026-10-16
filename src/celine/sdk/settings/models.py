from __future__ import annotations

from pathlib import Path

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OidcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELINE_OIDC_", extra="ignore")

    timeout: float = 10.0
    verify_ssl: bool = Field(default=True, description="Verify TLS certificates")

    scope: str | None = Field(default=None, description="OAuth2 scope string")

    # OIDC issuer (base URL of your auth server)
    base_url: str = Field(
        default="http://keycloak.celine.localhost/realms/celine",
        description="OIDC issuer URL (e.g., https://auth.example.com/realms/celine)",
    )

    # JWKS URI for JWT signature verification
    # NEW: celine.sdk.auth.JwtUser uses this directly
    jwks_uri: str = Field(
        default="http://keycloak.celine.localhost/realms/celine/protocol/openid-connect/certs",
        description="JWKS URI for JWT verification (e.g., https://auth.example.com/realms/celine/protocol/openid-connect/certs)",
    )

    # Client ID (for client-specific roles and audience validation)
    client_id: str | None = Field(default=None, description="OIDC client ID")
    client_secret: str | None = Field(default=None, description="OIDC client secret")

    # Expected audience (optional - can validate multiple)
    audience: str | None = Field(
        default=None, description="Expected JWT audience (optional)"
    )

    allowed_audiences: str | None = Field(
        default=None,
        description="Optional extra accepted audiences (comma-separated). Use sparingly.",
    )
    include_client_id_as_audience: bool = Field(
        default=True,
        description="If true, also accept CELINE_OIDC_CLIENT_ID as an audience.",
    )

    @field_validator("audience", "allowed_audiences", mode="before")
    @classmethod
    def _empty_audience_is_unset(cls, value: object) -> object:
        """An empty audience is no audience (REQ-0026).

        Compose files pass `CELINE_OIDC_AUDIENCE: ${CELINE_OIDC_AUDIENCE:-}`, so
        "not configured" arrives as `""`. Kept as a string, it switched audience
        verification on against an audience no token carries, and every token was
        refused with "Audience doesn't match".
        """
        if isinstance(value, str) and not value.strip():
            return None
        return value


class MqttSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELINE_MQTT_", extra="ignore")

    host: str = "host.docker.internal"
    port: int = 1883
    client_id: str | None = None
    topic_prefix: str = ""
    username: str | None = None
    password: str | None = None
    use_tls: bool = False
    ca_certs: str | None = None
    certfile: str | None = None
    keyfile: str | None = None
    keepalive: int = 60
    clean_session: bool = True
    reconnect_interval: float = 0.0
    max_reconnect_attempts: int = 10
    token_refresh_margin: float = 30.0


def _policies_env(name: str) -> AliasChoices:
    """``CELINE_POLICIES_<NAME>``, then the doubled spelling it replaced.

    The prefix and the field name both say ``policies``, so pydantic's own
    rule made the variable ``CELINE_POLICIES_POLICIES_DIR``. The infra chart,
    ``mqtt_auth`` and every hand-written ``.env`` said ``CELINE_POLICIES_DIR``,
    which no service built on this class read. The short name is the one; the
    doubled one is still accepted so a deployment that learned it keeps working.
    """
    return AliasChoices(f"CELINE_POLICIES_{name}", f"CELINE_POLICIES_POLICIES_{name}")


class PoliciesSettings(BaseSettings):
    """Policy engine settings: ``CELINE_POLICIES_DIR``, ``_DATA_DIR``, ``_CACHE_*``."""

    model_config = SettingsConfigDict(
        env_prefix="CELINE_POLICIES_", extra="ignore", populate_by_name=True
    )

    policies_dir: Path = Field(
        default=Path("./policies"),
        validation_alias=_policies_env("DIR"),
        description="Directory containing .rego policy files",
    )
    policies_data_dir: Path | None = Field(
        default=None,
        validation_alias=_policies_env("DATA_DIR"),
        description="Optional directory containing policy data JSON files",
    )
    policies_cache_enabled: bool = Field(
        default=True,
        validation_alias=_policies_env("CACHE_ENABLED"),
        description="Enable in-memory decision caching",
    )
    policies_cache_ttl: int = Field(
        default=300,
        validation_alias=_policies_env("CACHE_TTL"),
        description="Cache TTL in seconds",
    )
    policies_cache_maxsize: int = Field(
        default=10000,
        validation_alias=_policies_env("CACHE_MAXSIZE"),
        description="Maximum cache entries",
    )


class SdkSettings(BaseSettings):
    """Top-level SDK settings.

    Loaded from environment variables (CELINE_*).
    Use celine.sdk.settings.load_settings() for optional YAML overlay.
    """

    model_config = SettingsConfigDict(env_prefix="CELINE_", extra="ignore")

    oidc: OidcSettings = Field(default_factory=OidcSettings)
    mqtt: MqttSettings = Field(default_factory=MqttSettings)
    policies: PoliciesSettings = Field(default_factory=PoliciesSettings)

    config_file: str | None = Field(
        default=None, description="Optional path to YAML config"
    )
