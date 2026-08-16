from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.facts import Facts
    from ..models.payload import Payload


T = TypeVar("T", bound="DigitalTwinEvent")


@_attrs_define
class DigitalTwinEvent:
    """
    Attributes:
        event_type (str):
        community_id (None | str | Unset):
        facts (Facts | Unset): Enriched facts computed by Digital Twin
        payload (Payload | Unset):
        timestamp (datetime.datetime | Unset):
        user_id (None | str | Unset):
    """

    event_type: str
    community_id: None | str | Unset = UNSET
    facts: Facts | Unset = UNSET
    payload: Payload | Unset = UNSET
    timestamp: datetime.datetime | Unset = UNSET
    user_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        event_type = self.event_type

        community_id: None | str | Unset
        if isinstance(self.community_id, Unset):
            community_id = UNSET
        else:
            community_id = self.community_id

        facts: dict[str, Any] | Unset = UNSET
        if not isinstance(self.facts, Unset):
            facts = self.facts.to_dict()

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        timestamp: str | Unset = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        user_id: None | str | Unset
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_type": event_type,
            }
        )
        if community_id is not UNSET:
            field_dict["community_id"] = community_id
        if facts is not UNSET:
            field_dict["facts"] = facts
        if payload is not UNSET:
            field_dict["payload"] = payload
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facts import Facts
        from ..models.payload import Payload

        d = dict(src_dict)
        event_type = d.pop("event_type")

        def _parse_community_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        community_id = _parse_community_id(d.pop("community_id", UNSET))

        _facts = d.pop("facts", UNSET)
        facts: Facts | Unset
        if isinstance(_facts, Unset):
            facts = UNSET
        else:
            facts = Facts.from_dict(_facts)

        _payload = d.pop("payload", UNSET)
        payload: Payload | Unset
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = Payload.from_dict(_payload)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: datetime.datetime | Unset
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        def _parse_user_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_id = _parse_user_id(d.pop("user_id", UNSET))

        digital_twin_event = cls(
            event_type=event_type,
            community_id=community_id,
            facts=facts,
            payload=payload,
            timestamp=timestamp,
            user_id=user_id,
        )

        digital_twin_event.additional_properties = d
        return digital_twin_event

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
