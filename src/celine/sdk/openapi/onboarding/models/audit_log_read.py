from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="AuditLogRead")


@_attrs_define
class AuditLogRead:
    """
    Attributes:
        action (str):
        actor_client_id (None | str):
        actor_email (None | str):
        actor_sub (None | str):
        actor_type (str):
        created_at (datetime.datetime):
        detail (None | str):
        entity_id (None | str):
        entity_type (str):
        id (UUID):
        ip_address (None | str):
        rec_slug (None | str):
    """

    action: str
    actor_client_id: None | str
    actor_email: None | str
    actor_sub: None | str
    actor_type: str
    created_at: datetime.datetime
    detail: None | str
    entity_id: None | str
    entity_type: str
    id: UUID
    ip_address: None | str
    rec_slug: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        actor_client_id: None | str
        actor_client_id = self.actor_client_id

        actor_email: None | str
        actor_email = self.actor_email

        actor_sub: None | str
        actor_sub = self.actor_sub

        actor_type = self.actor_type

        created_at = self.created_at.isoformat()

        detail: None | str
        detail = self.detail

        entity_id: None | str
        entity_id = self.entity_id

        entity_type = self.entity_type

        id = str(self.id)

        ip_address: None | str
        ip_address = self.ip_address

        rec_slug: None | str
        rec_slug = self.rec_slug

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "actor_client_id": actor_client_id,
                "actor_email": actor_email,
                "actor_sub": actor_sub,
                "actor_type": actor_type,
                "created_at": created_at,
                "detail": detail,
                "entity_id": entity_id,
                "entity_type": entity_type,
                "id": id,
                "ip_address": ip_address,
                "rec_slug": rec_slug,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = d.pop("action")

        def _parse_actor_client_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_client_id = _parse_actor_client_id(d.pop("actor_client_id"))

        def _parse_actor_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_email = _parse_actor_email(d.pop("actor_email"))

        def _parse_actor_sub(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_sub = _parse_actor_sub(d.pop("actor_sub"))

        actor_type = d.pop("actor_type")

        created_at = isoparse(d.pop("created_at"))

        def _parse_detail(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        detail = _parse_detail(d.pop("detail"))

        def _parse_entity_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        entity_id = _parse_entity_id(d.pop("entity_id"))

        entity_type = d.pop("entity_type")

        id = UUID(d.pop("id"))

        def _parse_ip_address(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        ip_address = _parse_ip_address(d.pop("ip_address"))

        def _parse_rec_slug(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        rec_slug = _parse_rec_slug(d.pop("rec_slug"))

        audit_log_read = cls(
            action=action,
            actor_client_id=actor_client_id,
            actor_email=actor_email,
            actor_sub=actor_sub,
            actor_type=actor_type,
            created_at=created_at,
            detail=detail,
            entity_id=entity_id,
            entity_type=entity_type,
            id=id,
            ip_address=ip_address,
            rec_slug=rec_slug,
        )

        audit_log_read.additional_properties = d
        return audit_log_read

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
