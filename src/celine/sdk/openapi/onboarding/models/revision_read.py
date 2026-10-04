from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.revision_step_read import RevisionStepRead


T = TypeVar("T", bound="RevisionRead")


@_attrs_define
class RevisionRead:
    """
    Attributes:
        actor_email (None | str):
        actor_sub (None | str):
        actor_type (str):
        created_at (datetime.datetime):
        document_id (None | UUID):
        field (str):
        id (UUID):
        method (str):
        new_value (str):
        note (None | str):
        previous_value (None | str):
        steps (list[RevisionStepRead] | Unset):
    """

    actor_email: None | str
    actor_sub: None | str
    actor_type: str
    created_at: datetime.datetime
    document_id: None | UUID
    field: str
    id: UUID
    method: str
    new_value: str
    note: None | str
    previous_value: None | str
    steps: list[RevisionStepRead] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actor_email: None | str
        actor_email = self.actor_email

        actor_sub: None | str
        actor_sub = self.actor_sub

        actor_type = self.actor_type

        created_at = self.created_at.isoformat()

        document_id: None | str
        if isinstance(self.document_id, UUID):
            document_id = str(self.document_id)
        else:
            document_id = self.document_id

        field = self.field

        id = str(self.id)

        method = self.method

        new_value = self.new_value

        note: None | str
        note = self.note

        previous_value: None | str
        previous_value = self.previous_value

        steps: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.steps, Unset):
            steps = []
            for steps_item_data in self.steps:
                steps_item = steps_item_data.to_dict()
                steps.append(steps_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actor_email": actor_email,
                "actor_sub": actor_sub,
                "actor_type": actor_type,
                "created_at": created_at,
                "document_id": document_id,
                "field": field,
                "id": id,
                "method": method,
                "new_value": new_value,
                "note": note,
                "previous_value": previous_value,
            }
        )
        if steps is not UNSET:
            field_dict["steps"] = steps

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.revision_step_read import RevisionStepRead

        d = dict(src_dict)

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

        def _parse_document_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                document_id_type_0 = UUID(data)

                return document_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        document_id = _parse_document_id(d.pop("document_id"))

        field = d.pop("field")

        id = UUID(d.pop("id"))

        method = d.pop("method")

        new_value = d.pop("new_value")

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        def _parse_previous_value(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        previous_value = _parse_previous_value(d.pop("previous_value"))

        _steps = d.pop("steps", UNSET)
        steps: list[RevisionStepRead] | Unset = UNSET
        if _steps is not UNSET:
            steps = []
            for steps_item_data in _steps:
                steps_item = RevisionStepRead.from_dict(steps_item_data)

                steps.append(steps_item)

        revision_read = cls(
            actor_email=actor_email,
            actor_sub=actor_sub,
            actor_type=actor_type,
            created_at=created_at,
            document_id=document_id,
            field=field,
            id=id,
            method=method,
            new_value=new_value,
            note=note,
            previous_value=previous_value,
            steps=steps,
        )

        revision_read.additional_properties = d
        return revision_read

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
