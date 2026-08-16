from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationOut")


@_attrs_define
class NotificationOut:
    """User-facing notification. Fields are proper columns, not buried JSON.

    Attributes:
        body (str):
        created_at (datetime.datetime):
        family (str): energy | onboarding | seasonal | …
        id (str):
        rule_id (str):
        severity (str): info | warning | critical
        status (str): pending | sent | suppressed | failed
        title (str):
        type_ (str): informative | opportunity | alert
        user_id (str):
        click_action (None | str | Unset): Action identifier reported by the notification click event
        clicked_at (datetime.datetime | None | Unset): Null if the push was never clicked
        deleted_at (datetime.datetime | None | Unset): Null if not soft-deleted
        nudge_log_id (None | str | Unset): Originating engine audit row
        read_at (datetime.datetime | None | Unset): Null if unread
    """

    body: str
    created_at: datetime.datetime
    family: str
    id: str
    rule_id: str
    severity: str
    status: str
    title: str
    type_: str
    user_id: str
    click_action: None | str | Unset = UNSET
    clicked_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    nudge_log_id: None | str | Unset = UNSET
    read_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        created_at = self.created_at.isoformat()

        family = self.family

        id = self.id

        rule_id = self.rule_id

        severity = self.severity

        status = self.status

        title = self.title

        type_ = self.type_

        user_id = self.user_id

        click_action: None | str | Unset
        if isinstance(self.click_action, Unset):
            click_action = UNSET
        else:
            click_action = self.click_action

        clicked_at: None | str | Unset
        if isinstance(self.clicked_at, Unset):
            clicked_at = UNSET
        elif isinstance(self.clicked_at, datetime.datetime):
            clicked_at = self.clicked_at.isoformat()
        else:
            clicked_at = self.clicked_at

        deleted_at: None | str | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        nudge_log_id: None | str | Unset
        if isinstance(self.nudge_log_id, Unset):
            nudge_log_id = UNSET
        else:
            nudge_log_id = self.nudge_log_id

        read_at: None | str | Unset
        if isinstance(self.read_at, Unset):
            read_at = UNSET
        elif isinstance(self.read_at, datetime.datetime):
            read_at = self.read_at.isoformat()
        else:
            read_at = self.read_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
                "created_at": created_at,
                "family": family,
                "id": id,
                "rule_id": rule_id,
                "severity": severity,
                "status": status,
                "title": title,
                "type": type_,
                "user_id": user_id,
            }
        )
        if click_action is not UNSET:
            field_dict["click_action"] = click_action
        if clicked_at is not UNSET:
            field_dict["clicked_at"] = clicked_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if nudge_log_id is not UNSET:
            field_dict["nudge_log_id"] = nudge_log_id
        if read_at is not UNSET:
            field_dict["read_at"] = read_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body = d.pop("body")

        created_at = isoparse(d.pop("created_at"))

        family = d.pop("family")

        id = d.pop("id")

        rule_id = d.pop("rule_id")

        severity = d.pop("severity")

        status = d.pop("status")

        title = d.pop("title")

        type_ = d.pop("type")

        user_id = d.pop("user_id")

        def _parse_click_action(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        click_action = _parse_click_action(d.pop("click_action", UNSET))

        def _parse_clicked_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                clicked_at_type_0 = isoparse(data)

                return clicked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        clicked_at = _parse_clicked_at(d.pop("clicked_at", UNSET))

        def _parse_deleted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_nudge_log_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        nudge_log_id = _parse_nudge_log_id(d.pop("nudge_log_id", UNSET))

        def _parse_read_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                read_at_type_0 = isoparse(data)

                return read_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        read_at = _parse_read_at(d.pop("read_at", UNSET))

        notification_out = cls(
            body=body,
            created_at=created_at,
            family=family,
            id=id,
            rule_id=rule_id,
            severity=severity,
            status=status,
            title=title,
            type_=type_,
            user_id=user_id,
            click_action=click_action,
            clicked_at=clicked_at,
            deleted_at=deleted_at,
            nudge_log_id=nudge_log_id,
            read_at=read_at,
        )

        notification_out.additional_properties = d
        return notification_out

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
