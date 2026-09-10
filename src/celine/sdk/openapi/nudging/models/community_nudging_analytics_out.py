from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.analytics_delivery_failure import AnalyticsDeliveryFailure
    from ..models.analytics_funnel_step import AnalyticsFunnelStep
    from ..models.analytics_reachability import AnalyticsReachability
    from ..models.analytics_rule_metric import AnalyticsRuleMetric


T = TypeVar("T", bound="CommunityNudgingAnalyticsOut")


@_attrs_define
class CommunityNudgingAnalyticsOut:
    """Privacy-safe, REC-scoped input for the manager dashboard.

    Attributes:
        community_id (str):
        start (datetime.date):
        end (datetime.date):
        steps (list[AnalyticsFunnelStep]):
        rules (list[AnalyticsRuleMetric]):
        failures (list[AnalyticsDeliveryFailure]):
        reachability (list[AnalyticsReachability]):
    """

    community_id: str
    start: datetime.date
    end: datetime.date
    steps: list[AnalyticsFunnelStep]
    rules: list[AnalyticsRuleMetric]
    failures: list[AnalyticsDeliveryFailure]
    reachability: list[AnalyticsReachability]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community_id = self.community_id

        start = self.start.isoformat()

        end = self.end.isoformat()

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        rules = []
        for rules_item_data in self.rules:
            rules_item = rules_item_data.to_dict()
            rules.append(rules_item)

        failures = []
        for failures_item_data in self.failures:
            failures_item = failures_item_data.to_dict()
            failures.append(failures_item)

        reachability = []
        for reachability_item_data in self.reachability:
            reachability_item = reachability_item_data.to_dict()
            reachability.append(reachability_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community_id": community_id,
                "start": start,
                "end": end,
                "steps": steps,
                "rules": rules,
                "failures": failures,
                "reachability": reachability,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analytics_delivery_failure import AnalyticsDeliveryFailure
        from ..models.analytics_funnel_step import AnalyticsFunnelStep
        from ..models.analytics_reachability import AnalyticsReachability
        from ..models.analytics_rule_metric import AnalyticsRuleMetric

        d = dict(src_dict)
        community_id = d.pop("community_id")

        start = isoparse(d.pop("start")).date()

        end = isoparse(d.pop("end")).date()

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = AnalyticsFunnelStep.from_dict(steps_item_data)

            steps.append(steps_item)

        rules = []
        _rules = d.pop("rules")
        for rules_item_data in _rules:
            rules_item = AnalyticsRuleMetric.from_dict(rules_item_data)

            rules.append(rules_item)

        failures = []
        _failures = d.pop("failures")
        for failures_item_data in _failures:
            failures_item = AnalyticsDeliveryFailure.from_dict(failures_item_data)

            failures.append(failures_item)

        reachability = []
        _reachability = d.pop("reachability")
        for reachability_item_data in _reachability:
            reachability_item = AnalyticsReachability.from_dict(reachability_item_data)

            reachability.append(reachability_item)

        community_nudging_analytics_out = cls(
            community_id=community_id,
            start=start,
            end=end,
            steps=steps,
            rules=rules,
            failures=failures,
            reachability=reachability,
        )

        community_nudging_analytics_out.additional_properties = d
        return community_nudging_analytics_out

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
