from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_detail_device import AssetDetailDevice
    from ..models.asset_detail_extra import AssetDetailExtra
    from ..models.asset_detail_properties import AssetDetailProperties
    from ..models.asset_detail_relationships import AssetDetailRelationships


T = TypeVar("T", bound="AssetDetail")


@_attrs_define
class AssetDetail:
    """
    Attributes:
        id (str):
        key (str):
        asset_type (str):
        name (str):
        owner_key (str):
        owner_user_id (str):
        sensor_id (None | str | Unset):
        properties (AssetDetailProperties | Unset):
        device (AssetDetailDevice | Unset):
        relationships (AssetDetailRelationships | Unset):
        extra (AssetDetailExtra | Unset):
        created_at (None | str | Unset):
        updated_at (None | str | Unset):
    """

    id: str
    key: str
    asset_type: str
    name: str
    owner_key: str
    owner_user_id: str
    sensor_id: None | str | Unset = UNSET
    properties: AssetDetailProperties | Unset = UNSET
    device: AssetDetailDevice | Unset = UNSET
    relationships: AssetDetailRelationships | Unset = UNSET
    extra: AssetDetailExtra | Unset = UNSET
    created_at: None | str | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        asset_type = self.asset_type

        name = self.name

        owner_key = self.owner_key

        owner_user_id = self.owner_user_id

        sensor_id: None | str | Unset
        if isinstance(self.sensor_id, Unset):
            sensor_id = UNSET
        else:
            sensor_id = self.sensor_id

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        device: dict[str, Any] | Unset = UNSET
        if not isinstance(self.device, Unset):
            device = self.device.to_dict()

        relationships: dict[str, Any] | Unset = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        extra: dict[str, Any] | Unset = UNSET
        if not isinstance(self.extra, Unset):
            extra = self.extra.to_dict()

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key": key,
                "asset_type": asset_type,
                "name": name,
                "owner_key": owner_key,
                "owner_user_id": owner_user_id,
            }
        )
        if sensor_id is not UNSET:
            field_dict["sensor_id"] = sensor_id
        if properties is not UNSET:
            field_dict["properties"] = properties
        if device is not UNSET:
            field_dict["device"] = device
        if relationships is not UNSET:
            field_dict["relationships"] = relationships
        if extra is not UNSET:
            field_dict["extra"] = extra
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_detail_device import AssetDetailDevice
        from ..models.asset_detail_extra import AssetDetailExtra
        from ..models.asset_detail_properties import AssetDetailProperties
        from ..models.asset_detail_relationships import AssetDetailRelationships

        d = dict(src_dict)
        id = d.pop("id")

        key = d.pop("key")

        asset_type = d.pop("asset_type")

        name = d.pop("name")

        owner_key = d.pop("owner_key")

        owner_user_id = d.pop("owner_user_id")

        def _parse_sensor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sensor_id = _parse_sensor_id(d.pop("sensor_id", UNSET))

        _properties = d.pop("properties", UNSET)
        properties: AssetDetailProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = AssetDetailProperties.from_dict(_properties)

        _device = d.pop("device", UNSET)
        device: AssetDetailDevice | Unset
        if isinstance(_device, Unset):
            device = UNSET
        else:
            device = AssetDetailDevice.from_dict(_device)

        _relationships = d.pop("relationships", UNSET)
        relationships: AssetDetailRelationships | Unset
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = AssetDetailRelationships.from_dict(_relationships)

        _extra = d.pop("extra", UNSET)
        extra: AssetDetailExtra | Unset
        if isinstance(_extra, Unset):
            extra = UNSET
        else:
            extra = AssetDetailExtra.from_dict(_extra)

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        asset_detail = cls(
            id=id,
            key=key,
            asset_type=asset_type,
            name=name,
            owner_key=owner_key,
            owner_user_id=owner_user_id,
            sensor_id=sensor_id,
            properties=properties,
            device=device,
            relationships=relationships,
            extra=extra,
            created_at=created_at,
            updated_at=updated_at,
        )

        asset_detail.additional_properties = d
        return asset_detail

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
