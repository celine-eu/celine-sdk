from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CsvExportRequest")


@_attrs_define
class CsvExportRequest:
    """
    Attributes:
        agreement_ref (None | str | Unset):
        purpose (list[str] | Unset):
        recipient_ref (None | str | Unset): Who the data is being disclosed to. Naming one records a DataDisclosed
            provenance event; omit it for an internal dump.
    """

    agreement_ref: None | str | Unset = UNSET
    purpose: list[str] | Unset = UNSET
    recipient_ref: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agreement_ref: None | str | Unset
        if isinstance(self.agreement_ref, Unset):
            agreement_ref = UNSET
        else:
            agreement_ref = self.agreement_ref

        purpose: list[str] | Unset = UNSET
        if not isinstance(self.purpose, Unset):
            purpose = self.purpose

        recipient_ref: None | str | Unset
        if isinstance(self.recipient_ref, Unset):
            recipient_ref = UNSET
        else:
            recipient_ref = self.recipient_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agreement_ref is not UNSET:
            field_dict["agreement_ref"] = agreement_ref
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if recipient_ref is not UNSET:
            field_dict["recipient_ref"] = recipient_ref

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_agreement_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agreement_ref = _parse_agreement_ref(d.pop("agreement_ref", UNSET))

        purpose = cast(list[str], d.pop("purpose", UNSET))

        def _parse_recipient_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recipient_ref = _parse_recipient_ref(d.pop("recipient_ref", UNSET))

        csv_export_request = cls(
            agreement_ref=agreement_ref,
            purpose=purpose,
            recipient_ref=recipient_ref,
        )

        csv_export_request.additional_properties = d
        return csv_export_request

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
