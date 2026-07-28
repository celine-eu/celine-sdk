from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.global_asset_lookup_device import GlobalAssetLookupDevice
    from ..models.global_asset_lookup_properties import GlobalAssetLookupProperties
    from ..models.global_asset_lookup_relationships import GlobalAssetLookupRelationships


T = TypeVar("T", bound="GlobalAssetLookup")


@_attrs_define
class GlobalAssetLookup:
    """
    Attributes:
        id (str):
        key (str):
        asset_type (str):
        name (str):
        owner_key (str):
        owner_user_id (str):
        community_key (str):
        community_name (str):
        sensor_id (None | str | Unset):
        properties (GlobalAssetLookupProperties | Unset):
        device (GlobalAssetLookupDevice | Unset):
        relationships (GlobalAssetLookupRelationships | Unset):
    """

    id: str
    key: str
    asset_type: str
    name: str
    owner_key: str
    owner_user_id: str
    community_key: str
    community_name: str
    sensor_id: None | str | Unset = UNSET
    properties: GlobalAssetLookupProperties | Unset = UNSET
    device: GlobalAssetLookupDevice | Unset = UNSET
    relationships: GlobalAssetLookupRelationships | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        asset_type = self.asset_type

        name = self.name

        owner_key = self.owner_key

        owner_user_id = self.owner_user_id

        community_key = self.community_key

        community_name = self.community_name

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
                "community_key": community_key,
                "community_name": community_name,
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.global_asset_lookup_device import GlobalAssetLookupDevice
        from ..models.global_asset_lookup_properties import GlobalAssetLookupProperties
        from ..models.global_asset_lookup_relationships import GlobalAssetLookupRelationships

        d = dict(src_dict)
        id = d.pop("id")

        key = d.pop("key")

        asset_type = d.pop("asset_type")

        name = d.pop("name")

        owner_key = d.pop("owner_key")

        owner_user_id = d.pop("owner_user_id")

        community_key = d.pop("community_key")

        community_name = d.pop("community_name")

        def _parse_sensor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sensor_id = _parse_sensor_id(d.pop("sensor_id", UNSET))

        _properties = d.pop("properties", UNSET)
        properties: GlobalAssetLookupProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = GlobalAssetLookupProperties.from_dict(_properties)

        _device = d.pop("device", UNSET)
        device: GlobalAssetLookupDevice | Unset
        if isinstance(_device, Unset):
            device = UNSET
        else:
            device = GlobalAssetLookupDevice.from_dict(_device)

        _relationships = d.pop("relationships", UNSET)
        relationships: GlobalAssetLookupRelationships | Unset
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = GlobalAssetLookupRelationships.from_dict(_relationships)

        global_asset_lookup = cls(
            id=id,
            key=key,
            asset_type=asset_type,
            name=name,
            owner_key=owner_key,
            owner_user_id=owner_user_id,
            community_key=community_key,
            community_name=community_name,
            sensor_id=sensor_id,
            properties=properties,
            device=device,
            relationships=relationships,
        )

        global_asset_lookup.additional_properties = d
        return global_asset_lookup

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
