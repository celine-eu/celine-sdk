from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AssetRelationshipsIn")


@_attrs_define
class AssetRelationshipsIn:
    """Relationships between assets.

    Attributes:
        measures (list[str] | Unset):
        paired_with (None | str | Unset):
    """

    measures: list[str] | Unset = UNSET
    paired_with: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        measures: list[str] | Unset = UNSET
        if not isinstance(self.measures, Unset):
            measures = self.measures

        paired_with: None | str | Unset
        if isinstance(self.paired_with, Unset):
            paired_with = UNSET
        else:
            paired_with = self.paired_with

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if measures is not UNSET:
            field_dict["measures"] = measures
        if paired_with is not UNSET:
            field_dict["paired_with"] = paired_with

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        measures = cast(list[str], d.pop("measures", UNSET))

        def _parse_paired_with(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        paired_with = _parse_paired_with(d.pop("paired_with", UNSET))

        asset_relationships_in = cls(
            measures=measures,
            paired_with=paired_with,
        )

        asset_relationships_in.additional_properties = d
        return asset_relationships_in

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
