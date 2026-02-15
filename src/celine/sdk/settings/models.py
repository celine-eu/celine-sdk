from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OidcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELINE_OIDC_", extra="ignore")

    timeout: float = 10.0

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


class MqttSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELINE_MQTT_", extra="ignore")

    host: str = "localhost"
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
    reconnect_interval: float = 5.0
    max_reconnect_attempts: int = 0
    token_refresh_margin: float = 30.0


class PoliciesSettings(BaseSettings):
    """Policy engine settings."""

    model_config = SettingsConfigDict(env_prefix="CELINE_POLICIES_", extra="ignore")

    policies_dir: Path = Field(
        default=Path("./policies"),
        description="Directory containing .rego policy files",
    )
    policies_data_dir: Path | None = Field(
        default=None,
        description="Optional directory containing policy data JSON files",
    )
    policies_cache_enabled: bool = Field(
        default=True, description="Enable in-memory decision caching"
    )
    policies_cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    policies_cache_maxsize: int = Field(
        default=10000, description="Maximum cache entries"
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
