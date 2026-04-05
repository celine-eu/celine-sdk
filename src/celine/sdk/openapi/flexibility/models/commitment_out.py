from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.commitment_out_status import CommitmentOutStatus

T = TypeVar("T", bound="CommitmentOut")


@_attrs_define
class CommitmentOut:
    """
    Attributes:
        committed_at (datetime.datetime):
        community_id (None | str):
        device_id (None | str):
        id (UUID):
        period_end (datetime.datetime):
        period_start (datetime.datetime):
        reminded_at (datetime.datetime | None):
        reward_points_actual (int | None):
        reward_points_estimated (int):
        settled_at (datetime.datetime | None):
        status (CommitmentOutStatus):
        suggestion_id (str):
        suggestion_type (str):
        user_id (str):
    """

    committed_at: datetime.datetime
    community_id: None | str
    device_id: None | str
    id: UUID
    period_end: datetime.datetime
    period_start: datetime.datetime
    reminded_at: datetime.datetime | None
    reward_points_actual: int | None
    reward_points_estimated: int
    settled_at: datetime.datetime | None
    status: CommitmentOutStatus
    suggestion_id: str
    suggestion_type: str
    user_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        committed_at = self.committed_at.isoformat()

        community_id: None | str
        community_id = self.community_id

        device_id: None | str
        device_id = self.device_id

        id = str(self.id)

        period_end = self.period_end.isoformat()

        period_start = self.period_start.isoformat()

        reminded_at: None | str
        if isinstance(self.reminded_at, datetime.datetime):
            reminded_at = self.reminded_at.isoformat()
        else:
            reminded_at = self.reminded_at

        reward_points_actual: int | None
        reward_points_actual = self.reward_points_actual

        reward_points_estimated = self.reward_points_estimated

        settled_at: None | str
        if isinstance(self.settled_at, datetime.datetime):
            settled_at = self.settled_at.isoformat()
        else:
            settled_at = self.settled_at

        status = self.status.value

        suggestion_id = self.suggestion_id

        suggestion_type = self.suggestion_type

        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "committed_at": committed_at,
                "community_id": community_id,
                "device_id": device_id,
                "id": id,
                "period_end": period_end,
                "period_start": period_start,
                "reminded_at": reminded_at,
                "reward_points_actual": reward_points_actual,
                "reward_points_estimated": reward_points_estimated,
                "settled_at": settled_at,
                "status": status,
                "suggestion_id": suggestion_id,
                "suggestion_type": suggestion_type,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        committed_at = isoparse(d.pop("committed_at"))

        def _parse_community_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        community_id = _parse_community_id(d.pop("community_id"))

        def _parse_device_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        device_id = _parse_device_id(d.pop("device_id"))

        id = UUID(d.pop("id"))

        period_end = isoparse(d.pop("period_end"))

        period_start = isoparse(d.pop("period_start"))

        def _parse_reminded_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reminded_at_type_0 = isoparse(data)

                return reminded_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        reminded_at = _parse_reminded_at(d.pop("reminded_at"))

        def _parse_reward_points_actual(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        reward_points_actual = _parse_reward_points_actual(d.pop("reward_points_actual"))

        reward_points_estimated = d.pop("reward_points_estimated")

        def _parse_settled_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                settled_at_type_0 = isoparse(data)

                return settled_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        settled_at = _parse_settled_at(d.pop("settled_at"))

        status = CommitmentOutStatus(d.pop("status"))

        suggestion_id = d.pop("suggestion_id")

        suggestion_type = d.pop("suggestion_type")

        user_id = d.pop("user_id")

        commitment_out = cls(
            committed_at=committed_at,
            community_id=community_id,
            device_id=device_id,
            id=id,
            period_end=period_end,
            period_start=period_start,
            reminded_at=reminded_at,
            reward_points_actual=reward_points_actual,
            reward_points_estimated=reward_points_estimated,
            settled_at=settled_at,
            status=status,
            suggestion_id=suggestion_id,
            suggestion_type=suggestion_type,
            user_id=user_id,
        )

        commitment_out.additional_properties = d
        return commitment_out

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
