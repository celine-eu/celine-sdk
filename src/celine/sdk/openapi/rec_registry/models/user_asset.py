from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_asset_device import UserAssetDevice
    from ..models.user_asset_properties import UserAssetProperties
    from ..models.user_asset_relationships import UserAssetRelationships


T = TypeVar("T", bound="UserAsset")


@_attrs_define
class UserAsset:
    """
    Attributes:
        asset_type (str):
        key (str):
        name (str):
        device (UserAssetDevice | Unset):
        properties (UserAssetProperties | Unset):
        relationships (UserAssetRelationships | Unset):
        sensor_id (None | str | Unset):
    """

    asset_type: str
    key: str
    name: str
    device: UserAssetDevice | Unset = UNSET
    properties: UserAssetProperties | Unset = UNSET
    relationships: UserAssetRelationships | Unset = UNSET
    sensor_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset_type = self.asset_type

        key = self.key

        name = self.name

        device: dict[str, Any] | Unset = UNSET
        if not isinstance(self.device, Unset):
            device = self.device.to_dict()

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        relationships: dict[str, Any] | Unset = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

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
                "key": key,
                "name": name,
            }
        )
        if device is not UNSET:
            field_dict["device"] = device
        if properties is not UNSET:
            field_dict["properties"] = properties
        if relationships is not UNSET:
            field_dict["relationships"] = relationships
        if sensor_id is not UNSET:
            field_dict["sensor_id"] = sensor_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_asset_device import UserAssetDevice
        from ..models.user_asset_properties import UserAssetProperties
        from ..models.user_asset_relationships import UserAssetRelationships

        d = dict(src_dict)
        asset_type = d.pop("asset_type")

        key = d.pop("key")

        name = d.pop("name")

        _device = d.pop("device", UNSET)
        device: UserAssetDevice | Unset
        if isinstance(_device, Unset):
            device = UNSET
        else:
            device = UserAssetDevice.from_dict(_device)

        _properties = d.pop("properties", UNSET)
        properties: UserAssetProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = UserAssetProperties.from_dict(_properties)

        _relationships = d.pop("relationships", UNSET)
        relationships: UserAssetRelationships | Unset
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = UserAssetRelationships.from_dict(_relationships)

        def _parse_sensor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sensor_id = _parse_sensor_id(d.pop("sensor_id", UNSET))

        user_asset = cls(
            asset_type=asset_type,
            key=key,
            name=name,
            device=device,
            properties=properties,
            relationships=relationships,
            sensor_id=sensor_id,
        )

        user_asset.additional_properties = d
        return user_asset

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
