from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScheduledEventOut")


@_attrs_define
class ScheduledEventOut:
    """
    Attributes:
        created_at (datetime.datetime):
        event_type (str):
        id (str):
        status (str):
        trigger_at (datetime.datetime):
        user_id (str):
        community_id (None | str | Unset):
        dispatched_at (datetime.datetime | None | Unset):
        external_key (None | str | Unset):
    """

    created_at: datetime.datetime
    event_type: str
    id: str
    status: str
    trigger_at: datetime.datetime
    user_id: str
    community_id: None | str | Unset = UNSET
    dispatched_at: datetime.datetime | None | Unset = UNSET
    external_key: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        event_type = self.event_type

        id = self.id

        status = self.status

        trigger_at = self.trigger_at.isoformat()

        user_id = self.user_id

        community_id: None | str | Unset
        if isinstance(self.community_id, Unset):
            community_id = UNSET
        else:
            community_id = self.community_id

        dispatched_at: None | str | Unset
        if isinstance(self.dispatched_at, Unset):
            dispatched_at = UNSET
        elif isinstance(self.dispatched_at, datetime.datetime):
            dispatched_at = self.dispatched_at.isoformat()
        else:
            dispatched_at = self.dispatched_at

        external_key: None | str | Unset
        if isinstance(self.external_key, Unset):
            external_key = UNSET
        else:
            external_key = self.external_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "event_type": event_type,
                "id": id,
                "status": status,
                "trigger_at": trigger_at,
                "user_id": user_id,
            }
        )
        if community_id is not UNSET:
            field_dict["community_id"] = community_id
        if dispatched_at is not UNSET:
            field_dict["dispatched_at"] = dispatched_at
        if external_key is not UNSET:
            field_dict["external_key"] = external_key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        event_type = d.pop("event_type")

        id = d.pop("id")

        status = d.pop("status")

        trigger_at = isoparse(d.pop("trigger_at"))

        user_id = d.pop("user_id")

        def _parse_community_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        community_id = _parse_community_id(d.pop("community_id", UNSET))

        def _parse_dispatched_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                dispatched_at_type_0 = isoparse(data)

                return dispatched_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        dispatched_at = _parse_dispatched_at(d.pop("dispatched_at", UNSET))

        def _parse_external_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_key = _parse_external_key(d.pop("external_key", UNSET))

        scheduled_event_out = cls(
            created_at=created_at,
            event_type=event_type,
            id=id,
            status=status,
            trigger_at=trigger_at,
            user_id=user_id,
            community_id=community_id,
            dispatched_at=dispatched_at,
            external_key=external_key,
        )

        scheduled_event_out.additional_properties = d
        return scheduled_event_out

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
