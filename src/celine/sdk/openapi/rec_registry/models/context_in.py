from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prefixes import Prefixes


T = TypeVar("T", bound="ContextIn")


@_attrs_define
class ContextIn:
    """
    Attributes:
        base (None | str | Unset):
        prefixes (Prefixes | Unset):
    """

    base: None | str | Unset = UNSET
    prefixes: Prefixes | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base: None | str | Unset
        if isinstance(self.base, Unset):
            base = UNSET
        else:
            base = self.base

        prefixes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.prefixes, Unset):
            prefixes = self.prefixes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base is not UNSET:
            field_dict["base"] = base
        if prefixes is not UNSET:
            field_dict["prefixes"] = prefixes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prefixes import Prefixes

        d = dict(src_dict)

        def _parse_base(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base = _parse_base(d.pop("base", UNSET))

        _prefixes = d.pop("prefixes", UNSET)
        prefixes: Prefixes | Unset
        if isinstance(_prefixes, Unset):
            prefixes = UNSET
        else:
            prefixes = Prefixes.from_dict(_prefixes)

        context_in = cls(
            base=base,
            prefixes=prefixes,
        )

        context_in.additional_properties = d
        return context_in

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
