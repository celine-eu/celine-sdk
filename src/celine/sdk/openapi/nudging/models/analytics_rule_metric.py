from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.analytics_funnel_step import AnalyticsFunnelStep


T = TypeVar("T", bound="AnalyticsRuleMetric")


@_attrs_define
class AnalyticsRuleMetric:
    """
    Attributes:
        id (str):
        name (str):
        family (str):
        channel (str): webpush | email
        severity (str):
        active (bool):
        volume (int):
        steps (list[AnalyticsFunnelStep]):
        last_fired_at (datetime.datetime | None | Unset):
    """

    id: str
    name: str
    family: str
    channel: str
    severity: str
    active: bool
    volume: int
    steps: list[AnalyticsFunnelStep]
    last_fired_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        family = self.family

        channel = self.channel

        severity = self.severity

        active = self.active

        volume = self.volume

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        last_fired_at: None | str | Unset
        if isinstance(self.last_fired_at, Unset):
            last_fired_at = UNSET
        elif isinstance(self.last_fired_at, datetime.datetime):
            last_fired_at = self.last_fired_at.isoformat()
        else:
            last_fired_at = self.last_fired_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "family": family,
                "channel": channel,
                "severity": severity,
                "active": active,
                "volume": volume,
                "steps": steps,
            }
        )
        if last_fired_at is not UNSET:
            field_dict["last_fired_at"] = last_fired_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analytics_funnel_step import AnalyticsFunnelStep

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        family = d.pop("family")

        channel = d.pop("channel")

        severity = d.pop("severity")

        active = d.pop("active")

        volume = d.pop("volume")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = AnalyticsFunnelStep.from_dict(steps_item_data)

            steps.append(steps_item)

        def _parse_last_fired_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_fired_at_type_0 = isoparse(data)

                return last_fired_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_fired_at = _parse_last_fired_at(d.pop("last_fired_at", UNSET))

        analytics_rule_metric = cls(
            id=id,
            name=name,
            family=family,
            channel=channel,
            severity=severity,
            active=active,
            volume=volume,
            steps=steps,
            last_fired_at=last_fired_at,
        )

        analytics_rule_metric.additional_properties = d
        return analytics_rule_metric

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
