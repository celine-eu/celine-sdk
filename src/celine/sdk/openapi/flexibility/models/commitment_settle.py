from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CommitmentSettle")


@_attrs_define
class CommitmentSettle:
    """
    Attributes:
        reward_points_actual (int):
        actual_kwh (float | None | Unset):
    """

    reward_points_actual: int
    actual_kwh: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reward_points_actual = self.reward_points_actual

        actual_kwh: float | None | Unset
        if isinstance(self.actual_kwh, Unset):
            actual_kwh = UNSET
        else:
            actual_kwh = self.actual_kwh

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reward_points_actual": reward_points_actual,
            }
        )
        if actual_kwh is not UNSET:
            field_dict["actual_kwh"] = actual_kwh

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reward_points_actual = d.pop("reward_points_actual")

        def _parse_actual_kwh(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        actual_kwh = _parse_actual_kwh(d.pop("actual_kwh", UNSET))

        commitment_settle = cls(
            reward_points_actual=reward_points_actual,
            actual_kwh=actual_kwh,
        )

        commitment_settle.additional_properties = d
        return commitment_settle

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
