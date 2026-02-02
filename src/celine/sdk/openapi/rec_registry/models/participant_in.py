from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParticipantIn")


@_attrs_define
class ParticipantIn:
    """
    Attributes:
        key (str):
        auth_iri (None | str | Unset):
        iri (None | str | Unset):
        kind (None | str | Unset):
        name (None | str | Unset):
    """

    key: str
    auth_iri: None | str | Unset = UNSET
    iri: None | str | Unset = UNSET
    kind: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        auth_iri: None | str | Unset
        if isinstance(self.auth_iri, Unset):
            auth_iri = UNSET
        else:
            auth_iri = self.auth_iri

        iri: None | str | Unset
        if isinstance(self.iri, Unset):
            iri = UNSET
        else:
            iri = self.iri

        kind: None | str | Unset
        if isinstance(self.kind, Unset):
            kind = UNSET
        else:
            kind = self.kind

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
            }
        )
        if auth_iri is not UNSET:
            field_dict["auth_iri"] = auth_iri
        if iri is not UNSET:
            field_dict["iri"] = iri
        if kind is not UNSET:
            field_dict["kind"] = kind
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        def _parse_auth_iri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        auth_iri = _parse_auth_iri(d.pop("auth_iri", UNSET))

        def _parse_iri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        iri = _parse_iri(d.pop("iri", UNSET))

        def _parse_kind(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        kind = _parse_kind(d.pop("kind", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        participant_in = cls(
            key=key,
            auth_iri=auth_iri,
            iri=iri,
            kind=kind,
            name=name,
        )

        participant_in.additional_properties = d
        return participant_in

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
