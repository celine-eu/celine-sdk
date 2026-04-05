from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CommitmentCreate")


@_attrs_define
class CommitmentCreate:
    """
    Attributes:
        period_end (datetime.datetime):
        period_start (datetime.datetime):
        suggestion_id (str):
        user_id (str):
        community_id (None | str | Unset):
        device_id (None | str | Unset):
        reward_points_estimated (int | Unset):  Default: 0.
        suggestion_type (str | Unset):  Default: 'shift-consumption'.
    """

    period_end: datetime.datetime
    period_start: datetime.datetime
    suggestion_id: str
    user_id: str
    community_id: None | str | Unset = UNSET
    device_id: None | str | Unset = UNSET
    reward_points_estimated: int | Unset = 0
    suggestion_type: str | Unset = "shift-consumption"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_end = self.period_end.isoformat()

        period_start = self.period_start.isoformat()

        suggestion_id = self.suggestion_id

        user_id = self.user_id

        community_id: None | str | Unset
        if isinstance(self.community_id, Unset):
            community_id = UNSET
        else:
            community_id = self.community_id

        device_id: None | str | Unset
        if isinstance(self.device_id, Unset):
            device_id = UNSET
        else:
            device_id = self.device_id

        reward_points_estimated = self.reward_points_estimated

        suggestion_type = self.suggestion_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "period_end": period_end,
                "period_start": period_start,
                "suggestion_id": suggestion_id,
                "user_id": user_id,
            }
        )
        if community_id is not UNSET:
            field_dict["community_id"] = community_id
        if device_id is not UNSET:
            field_dict["device_id"] = device_id
        if reward_points_estimated is not UNSET:
            field_dict["reward_points_estimated"] = reward_points_estimated
        if suggestion_type is not UNSET:
            field_dict["suggestion_type"] = suggestion_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period_end = isoparse(d.pop("period_end"))

        period_start = isoparse(d.pop("period_start"))

        suggestion_id = d.pop("suggestion_id")

        user_id = d.pop("user_id")

        def _parse_community_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        community_id = _parse_community_id(d.pop("community_id", UNSET))

        def _parse_device_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        device_id = _parse_device_id(d.pop("device_id", UNSET))

        reward_points_estimated = d.pop("reward_points_estimated", UNSET)

        suggestion_type = d.pop("suggestion_type", UNSET)

        commitment_create = cls(
            period_end=period_end,
            period_start=period_start,
            suggestion_id=suggestion_id,
            user_id=user_id,
            community_id=community_id,
            device_id=device_id,
            reward_points_estimated=reward_points_estimated,
            suggestion_type=suggestion_type,
        )

        commitment_create.additional_properties = d
        return commitment_create

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
