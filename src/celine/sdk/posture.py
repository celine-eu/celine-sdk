"""Deployment posture: development is permissive, everything else is hardened.

Every service in the platform ships zero-config development defaults — a guessable
database password, a client secret equal to the client id, the local Keycloak as
issuer, a policy engine that may be missing. Those defaults are deliberate, and
they are safe for exactly one reason: **something refuses them when the
environment does not say it is development.**

This module is that something, shared, so the rule is the same in every service:

- The signal is ``CELINE_ENV``, then ``ENVIRONMENT``, then any legacy name a
  service still accepts. The first non-empty one wins.
- **Only the value ``dev`` relaxes.** Unset, empty, ``prod``, ``staging``,
  ``test`` or a typo is hardened. Enumerating the one relaxed value rather than
  the hardened ones is the point: the failure mode of being strict in dev is a
  one-line export, the failure mode of the reverse is a guessable secret in a
  live deployment.
- In a hardened environment a missing security dependency (policy engine,
  issuer, key) fails closed. Only ``dev`` may degrade instead.

Development opts in explicitly: each component's ``task run`` exports
``CELINE_ENV=dev``, so both dev runners inherit it, and
``CELINE_ENV=staging task run`` is the prod-like mode of the same entry point.

Usage at startup::

    guard = PostureGuard("grid-api")
    guard.forbid_dev_database_url("DATABASE_URL", settings.database_url)
    guard.forbid_secret_equal_to_client_id(
        "CELINE_OIDC_CLIENT_SECRET", settings.oidc.client_id, settings.oidc.client_secret
    )
    guard.require_explicit_oidc(settings.oidc)
    guard.enforce()

In dev every violation is logged as one warning and startup proceeds. Anywhere
else the guard raises once with the complete list, so a deployment learns every
missing value in one cycle rather than one at a time.

The same shape is ``ds_auth.production.ProductionGuard`` in the dataspace stack.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import unquote, urlsplit

log = logging.getLogger(__name__)

#: Read in this order; the first non-empty value wins. A prefixed name comes
#: first because a bare one is easily inherited from an unrelated shell.
ENV_VARS: tuple[str, ...] = ("CELINE_ENV", "ENVIRONMENT")

#: The only value that relaxes the posture.
DEV = "dev"

#: Database passwords the local stack uses. Never acceptable outside dev.
DEV_DATABASE_PASSWORDS = frozenset({"securepassword123", "postgres"})

#: Values that are never acceptable as a secret, whatever the setting is named.
UNIVERSAL_WEAK_VALUES = frozenset(
    {"", "admin", "changeme", "change-me", "password", "postgres", "secret", "test"}
)


class InsecureConfiguration(RuntimeError):
    """Raised at startup when a hardened environment still carries dev settings."""


def current_env(*legacy: str) -> str:
    """The environment signal, stripped and lowercased; ``""`` when unset.

    ``legacy`` names are consulted after ``CELINE_ENV`` and ``ENVIRONMENT``, for
    services that already read a name of their own (``APP_ENV``, ``ENV``).
    """
    for name in (*ENV_VARS, *legacy):
        value = os.environ.get(name)
        if value is not None and value.strip():
            return value.strip().lower()
    return ""


def is_dev(*legacy: str) -> bool:
    """True only when the signal says exactly ``dev``."""
    return current_env(*legacy) == DEV


def is_hardened(*legacy: str) -> bool:
    """True unless the signal says exactly ``dev``. Unset is hardened."""
    return not is_dev(*legacy)


def describe(env: str) -> str:
    """How an environment value reads in a log line."""
    return env if env else "<unset>"


def database_password(url: str | None) -> str | None:
    """The password in a database URL, or ``None`` when it carries none."""
    if not url:
        return None
    try:
        password = urlsplit(url).password
    except ValueError:
        return None
    return unquote(password) if password is not None else None


@dataclass(frozen=True)
class Violation:
    setting: str
    reason: str
    remediation: str

    def render(self) -> str:
        return f"  - {self.setting}: {self.reason}\n    → {self.remediation}"


class PostureGuard:
    """Collects dev-only settings and enforces them per environment.

    Each service registers its own dangerous values next to the settings that
    produce them, so a new dev default cannot be added without being declared.
    Run it **before** the side effect it protects — opening a pool, syncing a
    realm, serving a request — so a misconfigured deployment fails on its own
    machine rather than halfway through.
    """

    def __init__(
        self,
        service: str,
        env: str | None = None,
        legacy: Iterable[str] = (),
    ) -> None:
        self.service = service
        self.env = (env if env is not None else current_env(*legacy)).strip().lower()
        self._violations: list[Violation] = []

    @property
    def hardened(self) -> bool:
        return self.env != DEV

    @property
    def violations(self) -> list[Violation]:
        return list(self._violations)

    def add(self, setting: str, reason: str, remediation: str) -> None:
        self._violations.append(Violation(setting, reason, remediation))

    def forbid_default(
        self,
        setting: str,
        value: object,
        dev_defaults: Iterable[str],
        remediation: str,
    ) -> None:
        """Flag a value still equal to a known dev default, or trivially weak."""
        if value is None:
            return
        text = str(value)
        if text in set(dev_defaults):
            self.add(setting, "is still the development default", remediation)
        elif text.strip().lower() in UNIVERSAL_WEAK_VALUES:
            self.add(setting, "is set to a trivially weak value", remediation)

    def forbid_secret_equal_to_client_id(
        self,
        setting: str,
        client_id: object,
        client_secret: object,
        remediation: str = "Set the client's real secret from the realm.",
    ) -> None:
        """Flag an OIDC client secret that is empty or still the client id.

        Locally every service client's secret equals its own id, on both sides
        — the realm sync writes it and the service defaults to it — so nothing
        distinguishes *configured* from *never configured* except this check.
        An unset client id means the service holds no client identity, which is
        not a violation.
        """
        if client_id is None or not str(client_id).strip():
            return
        identifier = str(client_id).strip()
        secret = "" if client_secret is None else str(client_secret).strip()
        if not secret:
            self.add(setting, f"is empty for client {identifier!r}", remediation)
        elif secret == identifier:
            self.add(
                setting,
                f"is still equal to the client id ({identifier!r}) — the dev default",
                remediation,
            )

    def forbid_dev_database_url(
        self,
        setting: str,
        url: str | None,
        remediation: str = "Use a per-service role with a generated password.",
    ) -> None:
        """Flag a database URL whose password is a local-stack password."""
        password = database_password(url)
        if password is None:
            return
        if password in DEV_DATABASE_PASSWORDS or password.strip().lower() in UNIVERSAL_WEAK_VALUES:
            self.add(setting, "uses a development database password", remediation)

    def require_set(self, setting: str, value: object, remediation: str) -> None:
        """Flag a value that must be present outside dev."""
        if value is None or (isinstance(value, str) and not value.strip()):
            self.add(setting, "is not set", remediation)

    def forbid_true(self, setting: str, value: object, remediation: str) -> None:
        """Flag a development-only switch that must be off outside dev."""
        if bool(value):
            self.add(setting, "is enabled — development only", remediation)

    def forbid_false(self, setting: str, value: object, remediation: str) -> None:
        """Flag a protection that must be on outside dev."""
        if not bool(value):
            self.add(setting, "is disabled — development only", remediation)

    def require_explicit_oidc(
        self,
        oidc: object,
        *,
        prefix: str = "CELINE_OIDC_",
        require_audience: bool = False,
    ) -> None:
        """Flag an OIDC configuration that silently took the SDK's local defaults.

        ``OidcSettings`` defaults its issuer and JWKS to the local Keycloak so
        dev needs no configuration. Outside dev they must be stated: a value
        that came from the environment or from code is accepted, a value nobody
        set is not. TLS on the issuer is a deployment property and is not
        checked here.
        """
        fields_set = getattr(oidc, "model_fields_set", None)
        for field, name in (("base_url", "BASE_URL"), ("jwks_uri", "JWKS_URI")):
            if fields_set is not None and field not in fields_set:
                self.add(
                    f"{prefix}{name}",
                    "is not set — the SDK's local Keycloak default is in use",
                    "Point it at the deployment's realm.",
                )
        if require_audience and not getattr(oidc, "audience", None):
            self.add(
                f"{prefix}AUDIENCE",
                "is not set — tokens for any client would be accepted",
                "Set the audience this service validates.",
            )

    def enforce(self) -> None:
        """Warn in dev; raise anywhere else. Safe to call with no violations."""
        env = describe(self.env)
        if not self._violations:
            if self.hardened:
                log.info("%s: hardened posture check passed (CELINE_ENV=%s)", self.service, env)
            return

        detail = "\n".join(v.render() for v in self._violations)
        if self.hardened:
            raise InsecureConfiguration(
                f"{self.service}: refusing to start — {len(self._violations)} "
                f"development setting(s) with CELINE_ENV={env} "
                f"(only CELINE_ENV=dev relaxes this):\n{detail}"
            )
        log.warning(
            "%s: %d development setting(s) in use (CELINE_ENV=dev):\n%s",
            self.service,
            len(self._violations),
            detail,
        )


__all__ = [
    "DEV",
    "DEV_DATABASE_PASSWORDS",
    "ENV_VARS",
    "InsecureConfiguration",
    "PostureGuard",
    "UNIVERSAL_WEAK_VALUES",
    "Violation",
    "current_env",
    "database_password",
    "describe",
    "is_dev",
    "is_hardened",
]
