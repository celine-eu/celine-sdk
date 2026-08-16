from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LegalInfoIn")


@_attrs_define
class LegalInfoIn:
    """Legal and administrative details.

    Attributes:
        fiscal_code (None | str | Unset):
        legal_form (None | str | Unset):
        name (None | str | Unset):
        registered_office (None | str | Unset):
        registration_number (None | str | Unset):
        vat (None | str | Unset):
    """

    fiscal_code: None | str | Unset = UNSET
    legal_form: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    registered_office: None | str | Unset = UNSET
    registration_number: None | str | Unset = UNSET
    vat: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fiscal_code: None | str | Unset
        if isinstance(self.fiscal_code, Unset):
            fiscal_code = UNSET
        else:
            fiscal_code = self.fiscal_code

        legal_form: None | str | Unset
        if isinstance(self.legal_form, Unset):
            legal_form = UNSET
        else:
            legal_form = self.legal_form

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        registered_office: None | str | Unset
        if isinstance(self.registered_office, Unset):
            registered_office = UNSET
        else:
            registered_office = self.registered_office

        registration_number: None | str | Unset
        if isinstance(self.registration_number, Unset):
            registration_number = UNSET
        else:
            registration_number = self.registration_number

        vat: None | str | Unset
        if isinstance(self.vat, Unset):
            vat = UNSET
        else:
            vat = self.vat

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fiscal_code is not UNSET:
            field_dict["fiscal_code"] = fiscal_code
        if legal_form is not UNSET:
            field_dict["legal_form"] = legal_form
        if name is not UNSET:
            field_dict["name"] = name
        if registered_office is not UNSET:
            field_dict["registered_office"] = registered_office
        if registration_number is not UNSET:
            field_dict["registration_number"] = registration_number
        if vat is not UNSET:
            field_dict["vat"] = vat

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_fiscal_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fiscal_code = _parse_fiscal_code(d.pop("fiscal_code", UNSET))

        def _parse_legal_form(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        legal_form = _parse_legal_form(d.pop("legal_form", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_registered_office(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        registered_office = _parse_registered_office(d.pop("registered_office", UNSET))

        def _parse_registration_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        registration_number = _parse_registration_number(d.pop("registration_number", UNSET))

        def _parse_vat(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        vat = _parse_vat(d.pop("vat", UNSET))

        legal_info_in = cls(
            fiscal_code=fiscal_code,
            legal_form=legal_form,
            name=name,
            registered_office=registered_office,
            registration_number=registration_number,
            vat=vat,
        )

        legal_info_in.additional_properties = d
        return legal_info_in

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
