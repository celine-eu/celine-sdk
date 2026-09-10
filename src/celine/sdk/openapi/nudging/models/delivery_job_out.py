from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="DeliveryJobOut")


@_attrs_define
class DeliveryJobOut:
    """
    Attributes:
        job_id (str):
        user_id (str):
        rule_id (str):
        nudge_id (str):
        channel (str):
        destination (str):
        title (str):
        body (str):
        dedup_key (str):
        created_at (datetime.datetime):
    """

    job_id: str
    user_id: str
    rule_id: str
    nudge_id: str
    channel: str
    destination: str
    title: str
    body: str
    dedup_key: str
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job_id = self.job_id

        user_id = self.user_id

        rule_id = self.rule_id

        nudge_id = self.nudge_id

        channel = self.channel

        destination = self.destination

        title = self.title

        body = self.body

        dedup_key = self.dedup_key

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_id": job_id,
                "user_id": user_id,
                "rule_id": rule_id,
                "nudge_id": nudge_id,
                "channel": channel,
                "destination": destination,
                "title": title,
                "body": body,
                "dedup_key": dedup_key,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        job_id = d.pop("job_id")

        user_id = d.pop("user_id")

        rule_id = d.pop("rule_id")

        nudge_id = d.pop("nudge_id")

        channel = d.pop("channel")

        destination = d.pop("destination")

        title = d.pop("title")

        body = d.pop("body")

        dedup_key = d.pop("dedup_key")

        created_at = isoparse(d.pop("created_at"))

        delivery_job_out = cls(
            job_id=job_id,
            user_id=user_id,
            rule_id=rule_id,
            nudge_id=nudge_id,
            channel=channel,
            destination=destination,
            title=title,
            body=body,
            dedup_key=dedup_key,
            created_at=created_at,
        )

        delivery_job_out.additional_properties = d
        return delivery_job_out

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
