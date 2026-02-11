from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_asset_schema_device_type_0 import UserAssetSchemaDeviceType0
    from ..models.user_asset_schema_properties_type_0 import UserAssetSchemaPropertiesType0
    from ..models.user_asset_schema_relationships_type_0 import UserAssetSchemaRelationshipsType0


T = TypeVar("T", bound="UserAssetSchema")


@_attrs_define
class UserAssetSchema:
    """
    Attributes:
        asset_type (str):
        key (str):
        name (str):
        device (None | Unset | UserAssetSchemaDeviceType0):
        properties (None | Unset | UserAssetSchemaPropertiesType0):
        relationships (None | Unset | UserAssetSchemaRelationshipsType0):
        sensor_id (None | str | Unset):
    """

    asset_type: str
    key: str
    name: str
    device: None | Unset | UserAssetSchemaDeviceType0 = UNSET
    properties: None | Unset | UserAssetSchemaPropertiesType0 = UNSET
    relationships: None | Unset | UserAssetSchemaRelationshipsType0 = UNSET
    sensor_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_asset_schema_device_type_0 import UserAssetSchemaDeviceType0
        from ..models.user_asset_schema_properties_type_0 import UserAssetSchemaPropertiesType0
        from ..models.user_asset_schema_relationships_type_0 import UserAssetSchemaRelationshipsType0

        asset_type = self.asset_type

        key = self.key

        name = self.name

        device: dict[str, Any] | None | Unset
        if isinstance(self.device, Unset):
            device = UNSET
        elif isinstance(self.device, UserAssetSchemaDeviceType0):
            device = self.device.to_dict()
        else:
            device = self.device

        properties: dict[str, Any] | None | Unset
        if isinstance(self.properties, Unset):
            properties = UNSET
        elif isinstance(self.properties, UserAssetSchemaPropertiesType0):
            properties = self.properties.to_dict()
        else:
            properties = self.properties

        relationships: dict[str, Any] | None | Unset
        if isinstance(self.relationships, Unset):
            relationships = UNSET
        elif isinstance(self.relationships, UserAssetSchemaRelationshipsType0):
            relationships = self.relationships.to_dict()
        else:
            relationships = self.relationships

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
        from ..models.user_asset_schema_device_type_0 import UserAssetSchemaDeviceType0
        from ..models.user_asset_schema_properties_type_0 import UserAssetSchemaPropertiesType0
        from ..models.user_asset_schema_relationships_type_0 import UserAssetSchemaRelationshipsType0

        d = dict(src_dict)
        asset_type = d.pop("asset_type")

        key = d.pop("key")

        name = d.pop("name")

        def _parse_device(data: object) -> None | Unset | UserAssetSchemaDeviceType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                device_type_0 = UserAssetSchemaDeviceType0.from_dict(data)

                return device_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserAssetSchemaDeviceType0, data)

        device = _parse_device(d.pop("device", UNSET))

        def _parse_properties(data: object) -> None | Unset | UserAssetSchemaPropertiesType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                properties_type_0 = UserAssetSchemaPropertiesType0.from_dict(data)

                return properties_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserAssetSchemaPropertiesType0, data)

        properties = _parse_properties(d.pop("properties", UNSET))

        def _parse_relationships(data: object) -> None | Unset | UserAssetSchemaRelationshipsType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                relationships_type_0 = UserAssetSchemaRelationshipsType0.from_dict(data)

                return relationships_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserAssetSchemaRelationshipsType0, data)

        relationships = _parse_relationships(d.pop("relationships", UNSET))

        def _parse_sensor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sensor_id = _parse_sensor_id(d.pop("sensor_id", UNSET))

        user_asset_schema = cls(
            asset_type=asset_type,
            key=key,
            name=name,
            device=device,
            properties=properties,
            relationships=relationships,
            sensor_id=sensor_id,
        )

        user_asset_schema.additional_properties = d
        return user_asset_schema

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
