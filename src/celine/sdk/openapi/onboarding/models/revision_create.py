from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.revision_create_field import RevisionCreateField
from ..models.verification_method import VerificationMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="RevisionCreate")


@_attrs_define
class RevisionCreate:
    """An operator's correction of one declared field, from `submitted` on.

    `value` is checked per field by `services.revision.normalise`. The supply
    address is its text, as the eligibility step saves it, and is revisable only
    before approval (REQ-0026).

        Attributes:
            field (RevisionCreateField):
            method (VerificationMethod):
            note (str):
            value (str):
            document_id (None | Unset | UUID):
    """

    field: RevisionCreateField
    method: VerificationMethod
    note: str
    value: str
    document_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field.value

        method = self.method.value

        note = self.note

        value = self.value

        document_id: None | str | Unset
        if isinstance(self.document_id, Unset):
            document_id = UNSET
        elif isinstance(self.document_id, UUID):
            document_id = str(self.document_id)
        else:
            document_id = self.document_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "field": field,
                "method": method,
                "note": note,
                "value": value,
            }
        )
        if document_id is not UNSET:
            field_dict["document_id"] = document_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = RevisionCreateField(d.pop("field"))

        method = VerificationMethod(d.pop("method"))

        note = d.pop("note")

        value = d.pop("value")

        def _parse_document_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                document_id_type_0 = UUID(data)

                return document_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        document_id = _parse_document_id(d.pop("document_id", UNSET))

        revision_create = cls(
            field=field,
            method=method,
            note=note,
            value=value,
            document_id=document_id,
        )

        revision_create.additional_properties = d
        return revision_create

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
