from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OidcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELINE_OIDC_", extra="ignore")

    base_url: str | None = Field(default=None, description="OIDC issuer base URL")
    client_id: str | None = None
    client_secret: str | None = None
    scope: str | None = Field(default=None, description="OAuth2 scope string")
    timeout: float = 10.0


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


class SdkSettings(BaseSettings):
    """Top-level SDK settings.

    Loaded from environment variables (CELINE_*).
    Use celine.sdk.settings.load_settings() for optional YAML overlay.
    """

    model_config = SettingsConfigDict(env_prefix="CELINE_", extra="ignore")

    oidc: OidcSettings = Field(default_factory=OidcSettings)
    mqtt: MqttSettings = Field(default_factory=MqttSettings)

    config_file: str | None = Field(
        default=None, description="Optional path to YAML config"
    )
