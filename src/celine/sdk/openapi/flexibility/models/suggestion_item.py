from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SuggestionItem")


@_attrs_define
class SuggestionItem:
    """
    Attributes:
        clock_range (str):
        confidence (float):
        from_period (str):
        id (str):
        impact_kwh_estimated (float):
        period_end (str):
        period_start (str):
        reward_points (int):
        suggestion_type (str):
        to_is_tomorrow (bool):
        to_period (str):
        to_time (str):
    """

    clock_range: str
    confidence: float
    from_period: str
    id: str
    impact_kwh_estimated: float
    period_end: str
    period_start: str
    reward_points: int
    suggestion_type: str
    to_is_tomorrow: bool
    to_period: str
    to_time: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clock_range = self.clock_range

        confidence = self.confidence

        from_period = self.from_period

        id = self.id

        impact_kwh_estimated = self.impact_kwh_estimated

        period_end = self.period_end

        period_start = self.period_start

        reward_points = self.reward_points

        suggestion_type = self.suggestion_type

        to_is_tomorrow = self.to_is_tomorrow

        to_period = self.to_period

        to_time = self.to_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "clock_range": clock_range,
                "confidence": confidence,
                "from_period": from_period,
                "id": id,
                "impact_kwh_estimated": impact_kwh_estimated,
                "period_end": period_end,
                "period_start": period_start,
                "reward_points": reward_points,
                "suggestion_type": suggestion_type,
                "to_is_tomorrow": to_is_tomorrow,
                "to_period": to_period,
                "to_time": to_time,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        clock_range = d.pop("clock_range")

        confidence = d.pop("confidence")

        from_period = d.pop("from_period")

        id = d.pop("id")

        impact_kwh_estimated = d.pop("impact_kwh_estimated")

        period_end = d.pop("period_end")

        period_start = d.pop("period_start")

        reward_points = d.pop("reward_points")

        suggestion_type = d.pop("suggestion_type")

        to_is_tomorrow = d.pop("to_is_tomorrow")

        to_period = d.pop("to_period")

        to_time = d.pop("to_time")

        suggestion_item = cls(
            clock_range=clock_range,
            confidence=confidence,
            from_period=from_period,
            id=id,
            impact_kwh_estimated=impact_kwh_estimated,
            period_end=period_end,
            period_start=period_start,
            reward_points=reward_points,
            suggestion_type=suggestion_type,
            to_is_tomorrow=to_is_tomorrow,
            to_period=to_period,
            to_time=to_time,
        )

        suggestion_item.additional_properties = d
        return suggestion_item

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
