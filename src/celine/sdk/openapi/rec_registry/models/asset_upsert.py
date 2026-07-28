from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_upsert_properties import AssetUpsertProperties


T = TypeVar("T", bound="AssetUpsert")


@_attrs_define
class AssetUpsert:
    """Create or replace one asset of a member.

    `properties` is validated against the model for `asset_type`, so an EV
    charger cannot be stored with a heat pump's fields.

        Attributes:
            key (str):
            asset_type (str):
            properties (AssetUpsertProperties | Unset):
    """

    key: str
    asset_type: str
    properties: AssetUpsertProperties | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        asset_type = self.asset_type

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "asset_type": asset_type,
            }
        )
        if properties is not UNSET:
            field_dict["properties"] = properties

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_upsert_properties import AssetUpsertProperties

        d = dict(src_dict)
        key = d.pop("key")

        asset_type = d.pop("asset_type")

        _properties = d.pop("properties", UNSET)
        properties: AssetUpsertProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = AssetUpsertProperties.from_dict(_properties)

        asset_upsert = cls(
            key=key,
            asset_type=asset_type,
            properties=properties,
        )

        asset_upsert.additional_properties = d
        return asset_upsert

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
