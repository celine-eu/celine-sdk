from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SuggestionItem")


@_attrs_define
class SuggestionItem:
    """
    Attributes:
        clock_range (str):
        from_period (str):
        id (str):
        period_end (str):
        period_start (str):
        suggestion_type (str):
        to_is_tomorrow (bool):
        to_period (str):
        to_time (str):
        community_kwh (float | Unset):  Default: 0.0.
        confidence (float | Unset):  Default: 0.75.
        impact_kwh_estimated (float | None | Unset):
        reward_points (int | None | Unset):
    """

    clock_range: str
    from_period: str
    id: str
    period_end: str
    period_start: str
    suggestion_type: str
    to_is_tomorrow: bool
    to_period: str
    to_time: str
    community_kwh: float | Unset = 0.0
    confidence: float | Unset = 0.75
    impact_kwh_estimated: float | None | Unset = UNSET
    reward_points: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        clock_range = self.clock_range

        from_period = self.from_period

        id = self.id

        period_end = self.period_end

        period_start = self.period_start

        suggestion_type = self.suggestion_type

        to_is_tomorrow = self.to_is_tomorrow

        to_period = self.to_period

        to_time = self.to_time

        community_kwh = self.community_kwh

        confidence = self.confidence

        impact_kwh_estimated: float | None | Unset
        if isinstance(self.impact_kwh_estimated, Unset):
            impact_kwh_estimated = UNSET
        else:
            impact_kwh_estimated = self.impact_kwh_estimated

        reward_points: int | None | Unset
        if isinstance(self.reward_points, Unset):
            reward_points = UNSET
        else:
            reward_points = self.reward_points

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "clock_range": clock_range,
                "from_period": from_period,
                "id": id,
                "period_end": period_end,
                "period_start": period_start,
                "suggestion_type": suggestion_type,
                "to_is_tomorrow": to_is_tomorrow,
                "to_period": to_period,
                "to_time": to_time,
            }
        )
        if community_kwh is not UNSET:
            field_dict["community_kwh"] = community_kwh
        if confidence is not UNSET:
            field_dict["confidence"] = confidence
        if impact_kwh_estimated is not UNSET:
            field_dict["impact_kwh_estimated"] = impact_kwh_estimated
        if reward_points is not UNSET:
            field_dict["reward_points"] = reward_points

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        clock_range = d.pop("clock_range")

        from_period = d.pop("from_period")

        id = d.pop("id")

        period_end = d.pop("period_end")

        period_start = d.pop("period_start")

        suggestion_type = d.pop("suggestion_type")

        to_is_tomorrow = d.pop("to_is_tomorrow")

        to_period = d.pop("to_period")

        to_time = d.pop("to_time")

        community_kwh = d.pop("community_kwh", UNSET)

        confidence = d.pop("confidence", UNSET)

        def _parse_impact_kwh_estimated(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        impact_kwh_estimated = _parse_impact_kwh_estimated(d.pop("impact_kwh_estimated", UNSET))

        def _parse_reward_points(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        reward_points = _parse_reward_points(d.pop("reward_points", UNSET))

        suggestion_item = cls(
            clock_range=clock_range,
            from_period=from_period,
            id=id,
            period_end=period_end,
            period_start=period_start,
            suggestion_type=suggestion_type,
            to_is_tomorrow=to_is_tomorrow,
            to_period=to_period,
            to_time=to_time,
            community_kwh=community_kwh,
            confidence=confidence,
            impact_kwh_estimated=impact_kwh_estimated,
            reward_points=reward_points,
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
