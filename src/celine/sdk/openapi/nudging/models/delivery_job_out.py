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
        body (str):
        channel (str):
        created_at (datetime.datetime):
        dedup_key (str):
        destination (str):
        job_id (str):
        nudge_id (str):
        rule_id (str):
        title (str):
        user_id (str):
    """

    body: str
    channel: str
    created_at: datetime.datetime
    dedup_key: str
    destination: str
    job_id: str
    nudge_id: str
    rule_id: str
    title: str
    user_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        channel = self.channel

        created_at = self.created_at.isoformat()

        dedup_key = self.dedup_key

        destination = self.destination

        job_id = self.job_id

        nudge_id = self.nudge_id

        rule_id = self.rule_id

        title = self.title

        user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
                "channel": channel,
                "created_at": created_at,
                "dedup_key": dedup_key,
                "destination": destination,
                "job_id": job_id,
                "nudge_id": nudge_id,
                "rule_id": rule_id,
                "title": title,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body = d.pop("body")

        channel = d.pop("channel")

        created_at = isoparse(d.pop("created_at"))

        dedup_key = d.pop("dedup_key")

        destination = d.pop("destination")

        job_id = d.pop("job_id")

        nudge_id = d.pop("nudge_id")

        rule_id = d.pop("rule_id")

        title = d.pop("title")

        user_id = d.pop("user_id")

        delivery_job_out = cls(
            body=body,
            channel=channel,
            created_at=created_at,
            dedup_key=dedup_key,
            destination=destination,
            job_id=job_id,
            nudge_id=nudge_id,
            rule_id=rule_id,
            title=title,
            user_id=user_id,
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
