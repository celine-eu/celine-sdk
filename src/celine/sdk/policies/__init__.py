"""Policy evaluation module for CELINE SDK.

This module provides in-process policy evaluation using regorus (embedded OPA).

Example usage:
    ```python
    from celine.sdk.policies import (
        PolicyEngine,
        CachedPolicyEngine,
        DecisionCache,
        PolicyInput,
        Subject,
        Resource,
        Action,
        ResourceType,
        SubjectType,
    )

    # Initialize engine
    engine = PolicyEngine(
        policies_dir="./policies",
        data_dir="./policies/data"  # optional
    )
    engine.load()

    # Optionally wrap with cache
    cached_engine = CachedPolicyEngine(
        engine=engine,
        cache=DecisionCache(maxsize=10000, ttl_seconds=300)
    )

    # Evaluate a policy
    policy_input = PolicyInput(
        subject=Subject(
            id="user-123",
            type=SubjectType.USER,
            groups=["engineering"],
            scopes=["dataset.read"]
        ),
        resource=Resource(
            type=ResourceType.DATASET,
            id="dataset-456",
            attributes={"access_level": "internal"}
        ),
        action=Action(name="read"),
        environment={"timestamp": 1234567890}
    )

    decision = cached_engine.evaluate_decision(
        policy_package="celine.dataset.access",
        policy_input=policy_input
    )

    if decision.allowed:
        print(f"Access granted: {decision.reason}")
    else:
        print(f"Access denied: {decision.reason}")
    ```
"""

from celine.sdk.policies.cache import CachedPolicyEngine, DecisionCache
from celine.sdk.policies.engine import PolicyEngine, PolicyEngineError
from celine.sdk.policies.models import (
    Action,
    Decision,
    FilterPredicate,
    PolicyInput,
    Resource,
    ResourceType,
    Subject,
    SubjectType,
)

__all__ = [
    # Engine
    "PolicyEngine",
    "PolicyEngineError",
    "CachedPolicyEngine",
    "DecisionCache",
    # Models
    "Subject",
    "SubjectType",
    "Resource",
    "ResourceType",
    "Action",
    "PolicyInput",
    "Decision",
    "FilterPredicate",
]
