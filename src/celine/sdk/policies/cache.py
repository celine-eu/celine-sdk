"""Decision cache for policy evaluation results."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import threading
from typing import Any, Protocol

from cachetools import TTLCache

from celine.sdk.policies.engine import PolicyEngine
from celine.sdk.policies.models import Decision, PolicyInput

logger = logging.getLogger(__name__)


class _PolicyEngineLike(Protocol):
    @property
    def is_loaded(self) -> bool: ...

    @property
    def policy_count(self) -> int: ...

    def load(self) -> None: ...
    def has_package(self, package: str) -> bool: ...
    def get_packages(self) -> list[str]: ...
    def evaluate(self, query: str, input_data: dict[str, Any]) -> Any: ...
    def evaluate_decision(
        self, policy_package: str, policy_input: PolicyInput
    ) -> Decision: ...
    def build_input_dict(self, policy_input: PolicyInput) -> dict[str, Any]: ...


class DecisionCache:
    """LRU + TTL cache for policy decisions (thread-safe)."""

    def __init__(self, maxsize: int = 10_000, ttl_seconds: int = 300):
        self._cache: TTLCache[str, Decision] = TTLCache(
            maxsize=maxsize, ttl=ttl_seconds
        )
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def get(self, policy: str, input_data: dict[str, Any]) -> Decision | None:
        key = self._make_key(policy, input_data)
        with self._lock:
            result = self._cache.get(key)
            if result is not None:
                self._hits += 1
                logger.debug("Decision cache hit policy=%s key=%s", policy, key[:16])
            else:
                self._misses += 1
            return result

    def set(self, policy: str, input_data: dict[str, Any], decision: Decision) -> None:
        key = self._make_key(policy, input_data)
        with self._lock:
            self._cache[key] = decision
            logger.debug("Decision cache set policy=%s key=%s", policy, key[:16])

    def invalidate(self, policy: str | None = None) -> int:
        with self._lock:
            if policy is None:
                count = len(self._cache)
                self._cache.clear()
                logger.info("Decision cache cleared entries=%s", count)
                return count

            keys_to_remove = [k for k in self._cache if k.startswith(f"{policy}:")]
            for k in keys_to_remove:
                del self._cache[k]
            logger.info(
                "Decision cache invalidated policy=%s entries=%s",
                policy,
                len(keys_to_remove),
            )
            return len(keys_to_remove)

    @property
    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total else 0.0
            return {
                "size": len(self._cache),
                "maxsize": self._cache.maxsize,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": round(hit_rate, 3),
            }

    def _make_key(self, policy: str, input_data: dict[str, Any]) -> str:
        stable_input = self._extract_stable_input(input_data)
        payload = json.dumps(stable_input, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]
        return f"{policy}:{digest}"

    def _extract_stable_input(self, input_data: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}

        if "subject" in input_data:
            result["subject"] = input_data["subject"]

        if "resource" in input_data:
            result["resource"] = input_data["resource"]

        if "action" in input_data:
            result["action"] = input_data["action"]

        if "environment" in input_data:
            env = input_data["environment"] or {}
            stable_env = {
                k: v
                for k, v in env.items()
                if k not in ("timestamp", "request_id", "trace_id")
            }
            if stable_env:
                result["environment"] = stable_env

        return result


def _mark_cached(decision: Decision) -> Decision:
    if hasattr(decision, "model_copy"):
        return decision.model_copy(update={"cached": True})
    if dataclasses.is_dataclass(decision):
        return dataclasses.replace(decision, cached=True)
    try:
        new_obj = decision.__class__(**{**decision.__dict__, "cached": True})
        return new_obj
    except Exception:
        return decision


class CachedPolicyEngine:
    """Policy engine wrapper with decision caching."""

    def __init__(
        self,
        engine: _PolicyEngineLike,
        cache: DecisionCache | None = None,
        enabled: bool = True,
    ):
        self._engine = engine
        self._cache = cache or DecisionCache()
        self._enabled = enabled

    @property
    def is_loaded(self) -> bool:
        return self._engine.is_loaded

    @property
    def policy_count(self) -> int:
        return self._engine.policy_count

    @property
    def cache_stats(self) -> dict[str, Any]:
        return self._cache.stats

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def load(self) -> None:
        self._engine.load()

    def has_package(self, package: str) -> bool:
        return self._engine.has_package(package)

    def get_packages(self) -> list[str]:
        return self._engine.get_packages()

    def evaluate(self, query: str, input_data: dict[str, Any]) -> Any:
        return self._engine.evaluate(query, input_data)

    def evaluate_decision(
        self,
        policy_package: str,
        policy_input: PolicyInput,
        *,
        skip_cache: bool = False,
    ) -> Decision:
        input_dict = self._build_input_dict(policy_input)

        if self._enabled and not skip_cache:
            cached = self._cache.get(policy_package, input_dict)
            if cached is not None:
                return _mark_cached(cached)

        decision = self._engine.evaluate_decision(policy_package, policy_input)

        if self._enabled and not skip_cache:
            self._cache.set(policy_package, input_dict, decision)

        return decision

    def invalidate_cache(self, policy: str | None = None) -> int:
        return self._cache.invalidate(policy)

    def _build_input_dict(self, policy_input: PolicyInput) -> dict[str, Any]:
        return self._engine.build_input_dict(policy_input)
