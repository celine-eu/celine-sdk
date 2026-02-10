import json
import logging
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from regorus import Engine

from celine.sdk.policies.models import Decision, FilterPredicate, PolicyInput

logger = logging.getLogger(__name__)


class PolicyEngineError(Exception):
    pass


@dataclass(frozen=True)
class _Bundle:
    policies: tuple[tuple[str, str], ...]  # (path, rego source)
    data_json: tuple[str, ...]  # raw JSON strings (each add_data_json)


class PolicyEngine:
    """
    Production policy engine:
      - immutable policy/data bundle loaded once
      - per-thread regorus Engine instance (no cross-thread mutation)
    """

    def __init__(self, policies_dir: Path | str, data_dir: Path | str | None = None):
        self._policies_dir = Path(policies_dir)
        self._data_dir = Path(data_dir) if data_dir else None

        self._bundle: _Bundle | None = None
        self._known_packages: set[str] = set()
        self._policy_count = 0

        self._tls = threading.local()

    @property
    def is_loaded(self) -> bool:
        return self._bundle is not None

    def build_input_dict(self, policy_input: PolicyInput) -> dict[str, Any]:
        return self._build_input(policy_input)

    def load(self) -> None:
        """
        Load and freeze policies/data into an immutable bundle.
        Call once at process startup.
        """
        if not self._policies_dir.exists():
            raise PolicyEngineError(
                f"policies_dir does not exist: {self._policies_dir}"
            )

        policies = list(self._read_policies(self._policies_dir))
        data_json = list(self._read_data_json(self._data_dir) if self._data_dir else [])

        known_packages: set[str] = set()
        for _, content in policies:
            pkg = self._extract_package_name(content)
            if pkg:
                known_packages.add(pkg)

        self._bundle = _Bundle(policies=tuple(policies), data_json=tuple(data_json))
        self._known_packages = known_packages
        self._policy_count = len(policies)

        logger.info(
            "Policy engine bundle loaded: %d policies, %d data files, packages=%s",
            self._policy_count,
            len(data_json),
            sorted(self._known_packages),
        )

    @property
    def policy_count(self) -> int:
        return self._policy_count

    def has_package(self, package: str) -> bool:
        return package in self._known_packages

    def get_packages(self) -> list[str]:
        return sorted(self._known_packages)

    def _engine_for_thread(self) -> Engine:
        """
        Get or create the per-thread Engine. No locking required because
        each thread initializes its own instance once.
        """
        eng = getattr(self._tls, "engine", None)
        if eng is not None:
            return eng

        if self._bundle is None:
            raise PolicyEngineError("Policy engine not loaded (call load() at startup)")

        eng = Engine()

        # Add policies
        for path, content in self._bundle.policies:
            eng.add_policy(path, content)

        # Add data (raw JSON blobs)
        for blob in self._bundle.data_json:
            eng.add_data_json(blob)

        self._tls.engine = eng
        return eng

    def evaluate(self, query: str, input_data: dict[str, Any]) -> Any:
        eng = self._engine_for_thread()
        eng.set_input_json(json.dumps(input_data))
        return eng.eval_query(query)

    def evaluate_decision(
        self, policy_package: str, policy_input: PolicyInput
    ) -> Decision:
        eng = self._engine_for_thread()
        input_dict = self._build_input(policy_input)
        eng.set_input_json(json.dumps(input_dict))

        allow_query = f"data.{policy_package}.allow"
        allow_result = eng.eval_query(allow_query)
        allowed = self._extract_bool(allow_result, False)

        reason_query = f"data.{policy_package}.reason"
        reason_result = eng.eval_query(reason_query)
        reason = self._extract_string(reason_result, "")

        filters: list[FilterPredicate] = []
        try:
            filters_query = f"data.{policy_package}.filters"
            filters_result = eng.eval_query(filters_query)
            filters = self._extract_filters(filters_result)
        except Exception:
            pass

        return Decision(
            allowed=allowed,
            reason=reason,
            policy=policy_package,
            filters=filters,
            cached=False,
        )

    # ---------- bundle reading ----------

    def _read_policies(self, directory: Path) -> Iterable[tuple[str, str]]:
        for rego_file in directory.rglob("*.rego"):
            if rego_file.name.endswith("_test.rego"):
                continue
            yield (str(rego_file), rego_file.read_text())

    def _read_data_json(self, directory: Path | None) -> Iterable[str]:
        if directory is None or not directory.exists():
            return
        for json_file in directory.rglob("*.json"):
            yield json_file.read_text()

    def _extract_package_name(self, content: str) -> str | None:
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("package "):
                return line.split()[1].strip()
        return None

    # ---------- same extraction helpers as you already have ----------

    def _build_input(self, policy_input: PolicyInput) -> dict[str, Any]:
        result: dict[str, Any] = {
            "resource": {
                "type": policy_input.resource.type.value,
                "id": policy_input.resource.id,
                "attributes": policy_input.resource.attributes,
            },
            "action": {
                "name": policy_input.action.name,
                "context": policy_input.action.context,
            },
            "environment": policy_input.environment,
        }
        if policy_input.subject:
            result["subject"] = {
                "id": policy_input.subject.id,
                "type": policy_input.subject.type.value,
                "groups": policy_input.subject.groups,
                "scopes": policy_input.subject.scopes,
                "claims": policy_input.subject.claims,
            }
        else:
            result["subject"] = None
        return result

    def _extract_bool(self, result: Any, default: bool) -> bool:
        if isinstance(result, list) and result:
            item = result[0]
            if isinstance(item, dict) and "expressions" in item:
                exprs = item["expressions"]
                if exprs:
                    return bool(exprs[0].get("value", default))
        return default

    def _extract_string(self, result: Any, default: str) -> str:
        if isinstance(result, list) and result:
            item = result[0]
            if isinstance(item, dict) and "expressions" in item:
                exprs = item["expressions"]
                if exprs:
                    value = exprs[0].get("value")
                    if isinstance(value, str):
                        return value
        return default

    def _extract_filters(self, result: Any) -> list[FilterPredicate]:
        filters: list[FilterPredicate] = []
        if isinstance(result, list) and result:
            item = result[0]
            if isinstance(item, dict) and "expressions" in item:
                exprs = item["expressions"]
                if exprs:
                    value = exprs[0].get("value")
                    if isinstance(value, list):
                        for f in value:
                            if isinstance(f, dict):
                                try:
                                    filters.append(FilterPredicate(**f))
                                except Exception as e:
                                    logger.warning("Failed to parse filter: %s", e)
        return filters
