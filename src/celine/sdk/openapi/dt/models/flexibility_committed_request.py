from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="FlexibilityCommittedRequest")


@_attrs_define
class FlexibilityCommittedRequest:
    """
    Attributes:
        commitment_id (str):
        community_id (str):
        device_id (str):
        reward_points_estimated (int):
        window_end (datetime.datetime):
        window_start (datetime.datetime):
    """

    commitment_id: str
    community_id: str
    device_id: str
    reward_points_estimated: int
    window_end: datetime.datetime
    window_start: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        commitment_id = self.commitment_id

        community_id = self.community_id

        device_id = self.device_id

        reward_points_estimated = self.reward_points_estimated

        window_end = self.window_end.isoformat()

        window_start = self.window_start.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commitment_id": commitment_id,
                "community_id": community_id,
                "device_id": device_id,
                "reward_points_estimated": reward_points_estimated,
                "window_end": window_end,
                "window_start": window_start,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        commitment_id = d.pop("commitment_id")

        community_id = d.pop("community_id")

        device_id = d.pop("device_id")

        reward_points_estimated = d.pop("reward_points_estimated")

        window_end = isoparse(d.pop("window_end"))

        window_start = isoparse(d.pop("window_start"))

        flexibility_committed_request = cls(
            commitment_id=commitment_id,
            community_id=community_id,
            device_id=device_id,
            reward_points_estimated=reward_points_estimated,
            window_end=window_end,
            window_start=window_start,
        )

        flexibility_committed_request.additional_properties = d
        return flexibility_committed_request

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
