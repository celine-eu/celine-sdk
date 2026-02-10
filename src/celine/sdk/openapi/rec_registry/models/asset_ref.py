from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AssetRef")


@_attrs_define
class AssetRef:
    """
    Attributes:
        asset_type (str):
        id (str):
        key (str):
        name (str):
        sensor_id (None | str | Unset):
    """

    asset_type: str
    id: str
    key: str
    name: str
    sensor_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_type = self.asset_type

        id = self.id

        key = self.key

        name = self.name

        sensor_id: None | str | Unset
        if isinstance(self.sensor_id, Unset):
            sensor_id = UNSET
        else:
            sensor_id = self.sensor_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset_type": asset_type,
                "id": id,
                "key": key,
                "name": name,
            }
        )
        if sensor_id is not UNSET:
            field_dict["sensor_id"] = sensor_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        asset_type = d.pop("asset_type")

        id = d.pop("id")

        key = d.pop("key")

        name = d.pop("name")

        def _parse_sensor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sensor_id = _parse_sensor_id(d.pop("sensor_id", UNSET))

        asset_ref = cls(
            asset_type=asset_type,
            id=id,
            key=key,
            name=name,
            sensor_id=sensor_id,
        )

        asset_ref.additional_properties = d
        return asset_ref

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
