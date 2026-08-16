"""Tests for `celine.sdk.settings` — see docs/specifications/configuration.md.

Ten repositories construct these classes at import time. The environment is
stripped by the autouse `clean_env` fixture so what is asserted here is the
code's behaviour and not the developer's shell.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from celine.sdk.settings import (
    MqttSettings,
    OidcSettings,
    SdkSettings,
    load_settings,
)
from celine.sdk.settings.models import PoliciesSettings


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------


class TestEnvironmentPrefixes:
    # @verifies REQ-0001
    def test_oidc_reads_its_own_prefix(self, monkeypatch):
        monkeypatch.setenv("CELINE_OIDC_CLIENT_ID", "svc")
        monkeypatch.setenv("CELINE_OIDC_TIMEOUT", "2.5")
        s = OidcSettings()
        assert s.client_id == "svc"
        assert s.timeout == 2.5

    # @verifies REQ-0001
    def test_mqtt_reads_its_own_prefix(self, monkeypatch):
        monkeypatch.setenv("CELINE_MQTT_HOST", "broker.internal")
        monkeypatch.setenv("CELINE_MQTT_PORT", "8883")
        s = MqttSettings()
        assert (s.host, s.port) == ("broker.internal", 8883)

    # @verifies REQ-0001
    # @verifies REQ-0012
    def test_policies_reads_its_own_prefix(self, monkeypatch):
        monkeypatch.setenv("CELINE_POLICIES_POLICIES_DIR", "/srv/policies")
        monkeypatch.setenv("CELINE_POLICIES_POLICIES_CACHE_TTL", "60")
        s = PoliciesSettings()
        assert s.policies_dir == Path("/srv/policies")
        assert s.policies_cache_ttl == 60

    # @verifies REQ-0001
    def test_unprefixed_variable_is_not_read(self, monkeypatch):
        monkeypatch.setenv("CLIENT_ID", "leaked")
        assert OidcSettings().client_id is None

    # @verifies REQ-0001
    def test_composite_builds_each_section_from_the_environment(self, monkeypatch):
        monkeypatch.setenv("CELINE_OIDC_CLIENT_ID", "svc")
        monkeypatch.setenv("CELINE_MQTT_HOST", "broker.internal")
        s = SdkSettings()
        assert s.oidc.client_id == "svc"
        assert s.mqtt.host == "broker.internal"
        assert s.oidc.client_id == OidcSettings().client_id

    # @verifies REQ-0001
    def test_all_four_classes_are_exported(self):
        """`PoliciesSettings` was reachable only through `settings.models`, so
        every service configuring policies imported a private path.
        """
        import celine.sdk.settings as settings

        for name in ("SdkSettings", "OidcSettings", "MqttSettings", "PoliciesSettings"):
            assert hasattr(settings, name)
            assert name in settings.__all__
        assert settings.PoliciesSettings is PoliciesSettings

    # @verifies REQ-0002
    def test_unknown_variable_in_the_namespace_is_ignored(self, monkeypatch):
        monkeypatch.setenv("CELINE_OIDC_SOMETHING_ELSE", "x")
        monkeypatch.setenv("CELINE_MQTT_FUTURE_OPTION", "x")
        assert OidcSettings().client_id is None
        assert MqttSettings().host == "host.docker.internal"


class TestDefaults:
    # @verifies REQ-0003
    def test_everything_has_a_default(self):
        s = SdkSettings()
        assert s.oidc.base_url.startswith("http://keycloak.celine.localhost")
        assert s.oidc.jwks_uri.endswith("/protocol/openid-connect/certs")
        assert (s.mqtt.host, s.mqtt.port) == ("host.docker.internal", 1883)
        assert s.policies.policies_dir == Path("./policies")

    # @verifies REQ-0003
    # @verifies REQ-0026
    def test_the_defaults_are_permissive_not_safe(self):
        """Nothing is required out of the box: no audience, no client id, and TLS
        verification on but pointed at a development host. Asserted so that
        anyone tightening it sees a failing test rather than shipping a silent
        behaviour change to ten services.
        """
        s = OidcSettings()
        assert s.audience is None
        assert s.client_id is None
        assert s.verify_ssl is True

    # @verifies REQ-0004
    def test_oidc_carries_acquisition_and_verification(self):
        fields = set(OidcSettings.model_fields)
        assert {"base_url", "client_id", "client_secret", "scope", "timeout"} <= fields
        assert {
            "jwks_uri",
            "audience",
            "allowed_audiences",
            "include_client_id_as_audience",
        } <= fields

    # @verifies REQ-0012
    def test_policies_settings_locate_the_bundle_and_size_the_cache(self):
        s = PoliciesSettings()
        assert s.policies_data_dir is None
        assert s.policies_cache_enabled is True
        assert (s.policies_cache_ttl, s.policies_cache_maxsize) == (300, 10000)


# ---------------------------------------------------------------------------
# The YAML overlay
# ---------------------------------------------------------------------------


class TestLoadSettings:
    # @verifies REQ-0005
    def test_no_path_is_environment_only(self, monkeypatch):
        monkeypatch.setenv("CELINE_OIDC_CLIENT_ID", "svc")
        assert load_settings().oidc.client_id == "svc"

    # @verifies REQ-0006
    def test_a_missing_file_is_not_an_error(self, monkeypatch, tmp_path):
        monkeypatch.setenv("CELINE_OIDC_CLIENT_ID", "svc")
        loaded = load_settings(tmp_path / "absent.yaml")
        assert loaded.oidc.client_id == "svc"

    # @verifies REQ-0007
    def test_overlay_overrides_the_environment(self, monkeypatch, tmp_path):
        monkeypatch.setenv("CELINE_OIDC_AUDIENCE", "from-env")
        cfg = tmp_path / "c.yaml"
        cfg.write_text("oidc:\n  audience: from-yaml\n")
        assert load_settings(cfg).oidc.audience == "from-yaml"

    # @verifies REQ-0007
    def test_overlay_leaves_untouched_keys_at_their_environment_values(
        self, monkeypatch, tmp_path
    ):
        """The overlay is merged section by section at the top level, so this
        would be the natural place for `oidc:` in YAML to wipe every OIDC value
        that came from the environment. It does not.
        """
        monkeypatch.setenv("CELINE_OIDC_CLIENT_ID", "svc")
        monkeypatch.setenv("CELINE_MQTT_HOST", "broker.internal")
        cfg = tmp_path / "c.yaml"
        cfg.write_text("oidc:\n  audience: from-yaml\n")
        loaded = load_settings(cfg)
        assert loaded.oidc.audience == "from-yaml"
        assert loaded.oidc.client_id == "svc"
        assert loaded.mqtt.host == "broker.internal"

    # @verifies REQ-0008
    def test_a_non_mapping_document_is_refused(self, tmp_path):
        cfg = tmp_path / "c.yaml"
        cfg.write_text("- one\n- two\n")
        with pytest.raises(ValueError):
            load_settings(cfg)

    # @verifies REQ-0008
    def test_an_empty_document_is_accepted(self, tmp_path):
        cfg = tmp_path / "c.yaml"
        cfg.write_text("")
        assert load_settings(cfg).oidc.client_id is None


class TestInterpolation:
    # @verifies REQ-0009
    def test_a_set_variable_is_substituted(self, monkeypatch, tmp_path):
        monkeypatch.setenv("MY_AUD", "resolved")
        cfg = tmp_path / "c.yaml"
        cfg.write_text("oidc:\n  audience: ${MY_AUD}\n")
        assert load_settings(cfg).oidc.audience == "resolved"

    # @verifies REQ-0009
    def test_an_unset_variable_takes_the_default(self, monkeypatch, tmp_path):
        monkeypatch.delenv("MY_AUD", raising=False)
        cfg = tmp_path / "c.yaml"
        cfg.write_text("oidc:\n  audience: ${MY_AUD:-fallback}\n")
        assert load_settings(cfg).oidc.audience == "fallback"

    # @verifies REQ-0009
    def test_an_empty_variable_takes_the_default(self, monkeypatch, tmp_path):
        """Empty is treated as unset. An exported-but-blank variable is the usual
        shape of a value the deployment forgot to fill in.
        """
        monkeypatch.setenv("MY_AUD", "")
        cfg = tmp_path / "c.yaml"
        cfg.write_text("oidc:\n  audience: ${MY_AUD:-fallback}\n")
        assert load_settings(cfg).oidc.audience == "fallback"

    # @verifies REQ-0009
    def test_an_unresolvable_variable_becomes_empty_not_literal(
        self, monkeypatch, tmp_path
    ):
        """The literal `${VAR}` reaching a URL or a credential is the failure this
        prevents: it would be sent, logged, and read as configuration.
        """
        monkeypatch.delenv("MY_AUD", raising=False)
        cfg = tmp_path / "c.yaml"
        cfg.write_text("oidc:\n  audience: ${MY_AUD}\n")
        assert load_settings(cfg).oidc.audience == ""

    # @verifies REQ-0010
    def test_interpolation_reaches_nested_values(self, monkeypatch, tmp_path):
        monkeypatch.setenv("HOST", "broker.internal")
        cfg = tmp_path / "c.yaml"
        cfg.write_text("mqtt:\n  host: ${HOST}\n  topic_prefix: celine/${HOST}\n")
        loaded = load_settings(cfg)
        assert loaded.mqtt.host == "broker.internal"
        assert loaded.mqtt.topic_prefix == "celine/broker.internal"

    # @verifies REQ-0010
    def test_interpolation_reaches_inside_lists(self, monkeypatch):
        from celine.sdk.settings.loader import _resolve_env

        monkeypatch.setenv("A", "one")
        assert _resolve_env({"k": ["${A}", {"n": "${A}"}]}) == {
            "k": ["one", {"n": "one"}]
        }

    # @verifies REQ-0011
    def test_a_variable_holding_a_placeholder_resolves(self, monkeypatch):
        from celine.sdk.settings.loader import _resolve_env_str

        monkeypatch.setenv("OUTER", "${INNER}")
        monkeypatch.setenv("INNER", "final")
        assert _resolve_env_str("${OUTER}") == "final"

    # @verifies REQ-0011
    def test_a_self_referential_variable_terminates(self, monkeypatch):
        """Bounded passes, so this returns rather than looping. What it returns is
        not the point; that the call returns at all is.
        """
        from celine.sdk.settings.loader import _resolve_env_str

        monkeypatch.setenv("LOOP", "${LOOP}")
        assert _resolve_env_str("${LOOP}") == "${LOOP}"
