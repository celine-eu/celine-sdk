"""Tests for `celine.sdk.policies` — docs/specifications/policy-evaluation.md.

The engine is exercised against a **real Rego bundle** evaluated by the real
regorus, written into a temporary directory. That is affordable here because
regorus is in-process: there is no OPA server to stand up, and asserting the
decision logic against a mock would assert nothing about the thing services
actually run.
"""

from __future__ import annotations

import threading

import pytest

from celine.sdk.policies import (
    Action,
    CachedPolicyEngine,
    Decision,
    DecisionCache,
    PolicyEngine,
    PolicyEngineError,
    PolicyInput,
    Resource,
    ResourceType,
    Subject,
    SubjectType,
)

ACCESS_REGO = """
package celine.test.access

import rego.v1

default allow := false

allow if {
	input.subject.type == "user"
	input.action.name == "read"
	"viewers" in input.subject.groups
}

allow if {
	input.subject.type == "service"
	"dataset.read" in input.subject.scopes
}

reason := "group grants read" if allow

reason := "no matching grant" if not allow

filters := [{"field": "community", "operator": "eq", "value": input.subject.id}] if allow
"""

# A package whose `allow` is never defined, and one whose `allow` is not a bool.
PARTIAL_REGO = """
package celine.test.partial

import rego.v1

greeting := "hello"
"""

STRINGY_REGO = """
package celine.test.stringy

import rego.v1

allow := "yes"
"""

TEST_REGO = """
package celine.test.access_test

import rego.v1

test_something if {
	true
}
"""


@pytest.fixture
def bundle(tmp_path):
    (tmp_path / "policies").mkdir()
    (tmp_path / "policies" / "access.rego").write_text(ACCESS_REGO)
    (tmp_path / "policies" / "nested").mkdir()
    (tmp_path / "policies" / "nested" / "partial.rego").write_text(PARTIAL_REGO)
    (tmp_path / "policies" / "nested" / "stringy.rego").write_text(STRINGY_REGO)
    (tmp_path / "policies" / "access_test.rego").write_text(TEST_REGO)
    return tmp_path / "policies"


@pytest.fixture
def engine(bundle) -> PolicyEngine:
    e = PolicyEngine(bundle)
    e.load()
    return e


def _input(**kw) -> PolicyInput:
    subject = kw.pop(
        "subject", Subject(id="u1", type=SubjectType.USER, groups=["viewers"])
    )
    return PolicyInput(
        subject=subject,
        resource=kw.pop("resource", Resource(type=ResourceType.DATASET, id="d1")),
        action=kw.pop("action", Action(name="read")),
        environment=kw.pop("environment", {}),
    )


def _decision(allowed: bool = True) -> Decision:
    return Decision(allowed=allowed, reason="because", policy="p")


# ---------------------------------------------------------------------------
# The bundle
# ---------------------------------------------------------------------------


class TestBundle:
    # @verifies REQ-0050
    def test_evaluating_before_loading_is_an_error(self, bundle):
        """Not a denial: a service whose policies never loaded is broken, and
        answering "denied" would make that indistinguishable from a policy that
        denies.
        """
        with pytest.raises(PolicyEngineError):
            PolicyEngine(bundle).evaluate_decision("celine.test.access", _input())

    # @verifies REQ-0050
    def test_a_loaded_engine_says_so(self, bundle):
        e = PolicyEngine(bundle)
        assert not e.is_loaded
        e.load()
        assert e.is_loaded

    # @verifies REQ-0051
    def test_every_rego_file_is_loaded_recursively(self, engine):
        assert engine.policy_count == 3
        assert "celine.test.partial" in engine.get_packages()

    # @verifies REQ-0051
    def test_rego_unit_tests_are_excluded(self, engine):
        """`*_test.rego` holds Rego's own tests. Loading them would put test rules
        into the production decision path.
        """
        assert "celine.test.access_test" not in engine.get_packages()

    # @verifies REQ-0052
    def test_a_missing_policy_directory_is_a_startup_failure(self, tmp_path):
        with pytest.raises(PolicyEngineError, match="policies_dir"):
            PolicyEngine(tmp_path / "absent").load()

    # @verifies REQ-0053
    def test_the_loaded_packages_are_inspectable(self, engine):
        assert engine.has_package("celine.test.access")
        assert not engine.has_package("celine.test.never_shipped")
        assert engine.get_packages() == sorted(engine.get_packages())

    # @verifies REQ-0053
    # @verifies REQ-0057
    def test_querying_a_package_that_was_never_shipped_is_not_a_reliable_deny(
        self, engine
    ):
        """Two shapes of "not shipped", and they behave differently: a name under a
        path some loaded package shares resolves to undefined and denies, while an
        unrelated path is an error out of the engine. Neither is something to rely
        on — that is what `has_package` is for, at startup.
        """
        denied = engine.evaluate_decision("celine.test.never_shipped", _input())
        assert denied.allowed is False

        with pytest.raises(Exception):
            engine.evaluate_decision("totally.unrelated.package", _input())

    # @verifies REQ-0054
    def test_policy_data_is_optional(self, bundle, tmp_path):
        PolicyEngine(bundle, data_dir=None).load()
        PolicyEngine(bundle, data_dir=tmp_path / "absent-data").load()

    # @verifies REQ-0054
    def test_policy_data_is_loaded_when_present(self, bundle, tmp_path):
        data = tmp_path / "data"
        (data / "nested").mkdir(parents=True)
        (data / "nested" / "tiers.json").write_text('{"tiers": {"gold": 1}}')
        e = PolicyEngine(bundle, data_dir=data)
        e.load()
        result = e.evaluate("data.tiers.gold", {})
        assert result["result"][0]["expressions"][0]["value"] == 1


# ---------------------------------------------------------------------------
# Deciding
# ---------------------------------------------------------------------------


class TestDecisions:
    # @verifies REQ-0056
    def test_the_input_document_has_a_fixed_shape(self, engine):
        built = engine.build_input_dict(
            _input(
                subject=Subject(
                    id="u1",
                    type=SubjectType.SERVICE,
                    groups=["g"],
                    scopes=["s"],
                    claims={"c": 1},
                ),
                environment={"request_id": "r1"},
            )
        )
        assert set(built) == {"subject", "resource", "action", "environment"}
        assert built["subject"]["type"] == "service"  # the value, not the enum repr
        assert built["resource"]["type"] == "dataset"
        assert built["action"] == {"name": "read", "context": {}}
        assert built["environment"] == {"request_id": "r1"}

    # @verifies REQ-0056
    def test_an_anonymous_request_is_an_explicit_null_subject(self, engine):
        built = engine.build_input_dict(
            PolicyInput(
                subject=None,
                resource=Resource(type=ResourceType.DATASET, id="d1"),
                action=Action(name="read"),
            )
        )
        assert "subject" in built and built["subject"] is None

    # @verifies REQ-0056
    def test_the_anonymous_subject_is_a_subject(self):
        anon = Subject.anonymous()
        assert (anon.id, anon.type) == ("anonymous", SubjectType.ANONYMOUS)
        assert anon.groups == [] and anon.scopes == []

    # @verifies REQ-0057
    def test_a_user_is_allowed_by_group(self, engine):
        decision = engine.evaluate_decision("celine.test.access", _input())
        assert decision.allowed
        assert decision.reason == "group grants read"
        assert decision.policy == "celine.test.access"
        assert decision.cached is False

    # @verifies REQ-0057
    def test_a_service_is_allowed_by_scope(self, engine):
        decision = engine.evaluate_decision(
            "celine.test.access",
            _input(
                subject=Subject(
                    id="svc", type=SubjectType.SERVICE, scopes=["dataset.read"]
                )
            ),
        )
        assert decision.allowed

    # @verifies REQ-0057
    def test_the_absence_of_a_grant_denies_with_a_reason(self, engine):
        decision = engine.evaluate_decision(
            "celine.test.access",
            _input(subject=Subject(id="u1", type=SubjectType.USER, groups=[])),
        )
        assert not decision.allowed
        assert decision.reason == "no matching grant"

    # @verifies REQ-0057
    def test_an_undefined_allow_rule_denies(self, engine):
        decision = engine.evaluate_decision("celine.test.partial", _input())
        assert decision.allowed is False
        assert decision.reason == ""

    # @verifies REQ-0057
    def test_a_non_boolean_allow_denies(self, engine):
        """A policy that answers `"yes"` is a policy with a bug. It must not be
        read as consent.
        """
        assert not engine.evaluate_decision("celine.test.stringy", _input()).allowed

    # @verifies REQ-0058
    def test_filters_come_back_as_predicates(self, engine):
        decision = engine.evaluate_decision("celine.test.access", _input())
        assert len(decision.filters) == 1
        assert decision.filters[0].field == "community"
        assert decision.filters[0].operator == "eq"
        assert decision.filters[0].value == "u1"

    # @verifies REQ-0058
    def test_a_bundle_without_filters_still_decides(self, engine):
        decision = engine.evaluate_decision("celine.test.stringy", _input())
        assert decision.filters == []

    # @verifies REQ-0055
    def test_each_thread_evaluates_on_its_own_engine(self, engine):
        """The bundle is shared and immutable; the regorus engine is not shared at
        all. This is what makes the engine usable from a threaded server with no
        lock on the request path.
        """
        results: list[bool] = []
        errors: list[BaseException] = []

        def run() -> None:
            try:
                results.append(
                    engine.evaluate_decision("celine.test.access", _input()).allowed
                )
            except BaseException as exc:  # pragma: no cover - failure path
                errors.append(exc)

        threads = [threading.Thread(target=run) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert not errors
        assert results == [True] * 4


# ---------------------------------------------------------------------------
# The decision cache
# ---------------------------------------------------------------------------


class TestDecisionCache:
    # @verifies REQ-0059
    def test_identical_requests_hit_and_different_ones_miss(self):
        cache = DecisionCache()
        request = {
            "subject": {"id": "u1"},
            "resource": {"id": "d1"},
            "action": {"name": "read"},
        }
        assert cache.get("p", request) is None
        cache.set("p", request, _decision())
        assert cache.get("p", request) is not None
        other = {**request, "action": {"name": "write"}}
        assert cache.get("p", other) is None

    # @verifies REQ-0059
    def test_the_key_is_scoped_by_policy(self):
        cache = DecisionCache()
        request = {"subject": {"id": "u1"}}
        cache.set("policy.a", request, _decision())
        assert cache.get("policy.b", request) is None

    # @verifies REQ-0060
    def test_volatile_environment_fields_do_not_change_the_key(self):
        """A timestamp or a request id changes on every request and changes no
        decision. Keying on them yields a cache with a hit rate of zero, which
        costs memory and buys nothing.
        """
        cache = DecisionCache()
        base = {
            "subject": {"id": "u1"},
            "environment": {"timestamp": 1, "request_id": "a"},
        }
        cache.set("p", base, _decision())
        later = {
            "subject": {"id": "u1"},
            "environment": {"timestamp": 2, "trace_id": "b"},
        }
        assert cache.get("p", later) is not None

    # @verifies REQ-0060
    def test_a_meaningful_environment_field_does_change_the_key(self):
        cache = DecisionCache()
        cache.set("p", {"environment": {"tenant": "a"}}, _decision())
        assert cache.get("p", {"environment": {"tenant": "b"}}) is None

    # @verifies REQ-0059
    def test_key_order_does_not_matter(self):
        cache = DecisionCache()
        cache.set(
            "p", {"subject": {"id": "u1"}, "action": {"name": "read"}}, _decision()
        )
        assert cache.get("p", {"action": {"name": "read"}, "subject": {"id": "u1"}})

    # @verifies REQ-0063
    def test_entries_are_invalidated_by_policy_or_wholesale(self):
        cache = DecisionCache()
        cache.set("policy.a", {"subject": {"id": "1"}}, _decision())
        cache.set("policy.a", {"subject": {"id": "2"}}, _decision())
        cache.set("policy.b", {"subject": {"id": "1"}}, _decision())
        assert cache.invalidate("policy.a") == 2
        assert cache.get("policy.b", {"subject": {"id": "1"}}) is not None
        assert cache.invalidate() == 1
        assert cache.stats["size"] == 0

    # @verifies REQ-0064
    def test_it_reports_hits_misses_and_size(self):
        cache = DecisionCache(maxsize=5, ttl_seconds=60)
        request = {"subject": {"id": "u1"}}
        cache.get("p", request)
        cache.set("p", request, _decision())
        cache.get("p", request)
        stats = cache.stats
        assert stats["hits"] == 1 and stats["misses"] == 1
        assert stats["size"] == 1 and stats["maxsize"] == 5
        assert stats["hit_rate"] == 0.5

    # @verifies REQ-0064
    def test_it_is_bounded(self):
        cache = DecisionCache(maxsize=2, ttl_seconds=60)
        for i in range(5):
            cache.set("p", {"subject": {"id": str(i)}}, _decision())
        assert cache.stats["size"] == 2


class _RecordingEngine:
    """Enough of the engine protocol to see what the cache does with it."""

    def __init__(self) -> None:
        self.calls = 0
        self.loaded = 0

    @property
    def is_loaded(self) -> bool:
        return True

    @property
    def policy_count(self) -> int:
        return 7

    def load(self) -> None:
        self.loaded += 1

    def has_package(self, package: str) -> bool:
        return package == "known"

    def get_packages(self) -> list[str]:
        return ["known"]

    def evaluate(self, query: str, input_data: dict) -> dict:
        self.calls += 1
        return {"query": query}

    def evaluate_decision(
        self, policy_package: str, policy_input: PolicyInput
    ) -> Decision:
        self.calls += 1
        return _decision()

    def build_input_dict(self, policy_input: PolicyInput) -> dict:
        return {
            "subject": {"id": policy_input.subject.id if policy_input.subject else None}
        }


class TestCachedEngine:
    # @verifies REQ-0059
    def test_a_repeated_decision_is_served_from_the_cache(self):
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner)
        cached.evaluate_decision("p", _input())
        cached.evaluate_decision("p", _input())
        assert inner.calls == 1

    # @verifies REQ-0061
    def test_a_cached_decision_says_that_it_is_cached(self):
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner)
        assert cached.evaluate_decision("p", _input()).cached is False
        assert cached.evaluate_decision("p", _input()).cached is True

    # @verifies REQ-0061
    def test_marking_a_decision_cached_does_not_mutate_the_stored_one(self):
        """Otherwise the second reader is told the decision came from a cache of a
        cache, and `cached` stops meaning anything.
        """
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner)
        cached.evaluate_decision("p", _input())
        first = cached.evaluate_decision("p", _input())
        second = cached.evaluate_decision("p", _input())
        assert first.cached and second.cached
        assert first is not second

    # @verifies REQ-0062
    def test_a_single_call_can_skip_the_cache(self):
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner)
        cached.evaluate_decision("p", _input())
        fresh = cached.evaluate_decision("p", _input(), skip_cache=True)
        assert inner.calls == 2
        assert fresh.cached is False

    # @verifies REQ-0062
    def test_the_cache_can_be_disabled_entirely(self):
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner, enabled=False)
        cached.evaluate_decision("p", _input())
        cached.evaluate_decision("p", _input())
        assert inner.calls == 2
        cached.set_enabled(True)
        cached.evaluate_decision("p", _input())
        cached.evaluate_decision("p", _input())
        assert inner.calls == 3

    # @verifies REQ-0063
    def test_invalidation_reaches_the_wrapped_cache(self):
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner)
        cached.evaluate_decision("p", _input())
        assert cached.invalidate_cache("p") == 1
        cached.evaluate_decision("p", _input())
        assert inner.calls == 2

    # @verifies REQ-0065
    def test_it_is_a_drop_in_for_the_engine(self):
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner)
        assert cached.is_loaded and cached.policy_count == 7
        cached.load()
        assert inner.loaded == 1
        assert cached.has_package("known") and not cached.has_package("other")
        assert cached.get_packages() == ["known"]
        assert "hits" in cached.cache_stats

    # @verifies REQ-0065
    def test_the_raw_query_path_is_never_cached(self):
        """Its query is an arbitrary string, so there is no input document to key
        on and no way to know what would invalidate the entry.
        """
        inner = _RecordingEngine()
        cached = CachedPolicyEngine(inner)
        cached.evaluate("data.x", {})
        cached.evaluate("data.x", {})
        assert inner.calls == 2
