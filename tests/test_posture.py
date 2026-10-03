"""Tests for `celine.sdk.posture` — see docs/specifications/posture.md."""

from __future__ import annotations

import logging

import pytest

from celine.sdk.posture import (
    InsecureConfiguration,
    PostureGuard,
    current_env,
    database_password,
    is_dev,
    is_hardened,
)
from celine.sdk.settings.models import OidcSettings


@pytest.fixture(autouse=True)
def no_env_signal(monkeypatch):
    for name in ("CELINE_ENV", "ENVIRONMENT", "APP_ENV", "ENV"):
        monkeypatch.delenv(name, raising=False)


class TestTheSignal:
    # @verifies REQ-0180
    def test_unset_is_hardened(self):
        assert current_env() == ""
        assert is_hardened()
        assert not is_dev()

    # @verifies REQ-0180
    @pytest.mark.parametrize("value", ["prod", "production", "staging", "test", "ci", "local", "development", "deev", " "])
    def test_anything_but_dev_is_hardened(self, monkeypatch, value):
        monkeypatch.setenv("CELINE_ENV", value)
        assert is_hardened()

    # @verifies REQ-0180
    @pytest.mark.parametrize("value", ["dev", "DEV", " dev "])
    def test_dev_relaxes(self, monkeypatch, value):
        monkeypatch.setenv("CELINE_ENV", value)
        assert is_dev()

    # @verifies REQ-0180
    def test_celine_env_wins_over_environment(self, monkeypatch):
        monkeypatch.setenv("CELINE_ENV", "staging")
        monkeypatch.setenv("ENVIRONMENT", "dev")
        assert is_hardened()

    # @verifies REQ-0180
    def test_environment_is_read(self, monkeypatch):
        monkeypatch.setenv("ENVIRONMENT", "dev")
        assert is_dev()

    # @verifies REQ-0180
    def test_a_legacy_name_is_read_only_when_passed_and_last(self, monkeypatch):
        monkeypatch.setenv("APP_ENV", "dev")
        assert is_hardened()
        assert is_dev("APP_ENV")
        monkeypatch.setenv("CELINE_ENV", "prod")
        assert is_hardened("APP_ENV")

    # @verifies REQ-0180
    def test_an_empty_value_falls_through(self, monkeypatch):
        monkeypatch.setenv("CELINE_ENV", "")
        monkeypatch.setenv("ENVIRONMENT", "dev")
        assert is_dev()


class TestTheGuard:
    # @verifies REQ-0181
    def test_hardened_raises_once_with_every_violation(self):
        guard = PostureGuard("svc", env="")
        guard.forbid_true("A", True, "turn A off")
        guard.require_set("B", None, "set B")
        with pytest.raises(InsecureConfiguration) as err:
            guard.enforce()
        text = str(err.value)
        assert "svc" in text and "A" in text and "B" in text and "<unset>" in text

    # @verifies REQ-0181
    def test_dev_warns_and_proceeds(self, caplog):
        guard = PostureGuard("svc", env="dev")
        guard.forbid_true("A", True, "turn A off")
        with caplog.at_level(logging.WARNING):
            guard.enforce()
        assert "A" in caplog.text

    # @verifies REQ-0181
    def test_no_violation_never_raises(self):
        PostureGuard("svc", env="prod").enforce()

    # @verifies REQ-0181
    def test_the_guard_reads_the_environment_when_not_told(self, monkeypatch):
        assert PostureGuard("svc").hardened
        monkeypatch.setenv("CELINE_ENV", "dev")
        assert not PostureGuard("svc").hardened


class TestDevCredentials:
    @pytest.mark.parametrize(
        "url",
        [
            "postgresql+asyncpg://postgres:securepassword123@host.docker.internal:15432/grid",
            "postgresql://postgres:postgres@172.17.0.1:35432/x",
            "postgresql://u:password@h/x",
        ],
    )
    # @verifies REQ-0182
    def test_a_local_database_password_is_flagged(self, url):
        guard = PostureGuard("svc", env="prod")
        guard.forbid_dev_database_url("DATABASE_URL", url)
        assert [v.setting for v in guard.violations] == ["DATABASE_URL"]

    @pytest.mark.parametrize(
        "url",
        ["postgresql://svc:Zq8%40r2kP@db/x", "postgresql:///x?host=/run/postgresql", None, ""],
    )
    # @verifies REQ-0182
    def test_a_real_or_absent_password_is_not_flagged(self, url):
        guard = PostureGuard("svc", env="prod")
        guard.forbid_dev_database_url("DATABASE_URL", url)
        assert guard.violations == []

    def test_the_password_is_url_decoded(self):
        assert database_password("postgresql://u:a%40b@h/x") == "a@b"

    # @verifies REQ-0182
    @pytest.mark.parametrize("secret", ["svc-grid", "", None, "  "])
    def test_a_secret_equal_to_the_id_or_empty_is_flagged(self, secret):
        guard = PostureGuard("svc", env="prod")
        guard.forbid_secret_equal_to_client_id("CELINE_OIDC_CLIENT_SECRET", "svc-grid", secret)
        assert len(guard.violations) == 1

    # @verifies REQ-0182
    def test_no_client_id_is_no_violation(self):
        guard = PostureGuard("svc", env="prod")
        guard.forbid_secret_equal_to_client_id("CELINE_OIDC_CLIENT_SECRET", None, None)
        assert guard.violations == []

    # @verifies REQ-0182
    def test_a_real_secret_passes(self):
        guard = PostureGuard("svc", env="prod")
        guard.forbid_secret_equal_to_client_id("S", "svc-grid", "k3J9-generated")
        assert guard.violations == []

    # @verifies REQ-0182
    def test_forbid_default_and_switches(self):
        guard = PostureGuard("svc", env="prod")
        guard.forbid_default("K", "dev-key", {"dev-key"}, "rotate")
        guard.forbid_default("W", "changeme", set(), "rotate")
        guard.forbid_default("N", None, {"dev-key"}, "rotate")
        guard.forbid_false("P", False, "turn on")
        guard.forbid_false("Q", True, "turn on")
        assert [v.setting for v in guard.violations] == ["K", "W", "P"]


class TestExplicitOidc:
    # @verifies REQ-0183
    def test_sdk_defaults_are_refused(self):
        guard = PostureGuard("svc", env="prod")
        guard.require_explicit_oidc(OidcSettings())
        assert {v.setting for v in guard.violations} == {
            "CELINE_OIDC_BASE_URL",
            "CELINE_OIDC_JWKS_URI",
        }

    # @verifies REQ-0183
    def test_values_from_the_environment_pass_even_over_http(self, monkeypatch):
        monkeypatch.setenv("CELINE_OIDC_BASE_URL", "http://keycloak.celine.localhost/realms/celine")
        monkeypatch.setenv("CELINE_OIDC_JWKS_URI", "http://keycloak.celine.localhost/realms/celine/certs")
        guard = PostureGuard("svc", env="prod")
        guard.require_explicit_oidc(OidcSettings())
        assert guard.violations == []

    # @verifies REQ-0183
    def test_an_audience_can_be_required(self, monkeypatch):
        monkeypatch.setenv("CELINE_OIDC_BASE_URL", "https://kc/realms/r")
        monkeypatch.setenv("CELINE_OIDC_JWKS_URI", "https://kc/realms/r/certs")
        guard = PostureGuard("svc", env="prod")
        guard.require_explicit_oidc(OidcSettings(), require_audience=True)
        assert [v.setting for v in guard.violations] == ["CELINE_OIDC_AUDIENCE"]
        guard = PostureGuard("svc", env="prod")
        guard.require_explicit_oidc(OidcSettings(audience="svc-x"), require_audience=True)
        assert guard.violations == []
