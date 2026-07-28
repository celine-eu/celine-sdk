from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_relationships_in import AssetRelationshipsIn
    from ..models.device_in import DeviceIn


T = TypeVar("T", bound="LoadAssetIn")


@_attrs_define
class LoadAssetIn:
    """Load asset.

    Attributes:
        name (str):
        load_type (None | str | Unset):
        rated_power (float | None | Unset):
        min_power (float | None | Unset):
        controllable (bool | None | Unset):
        priority (None | str | Unset):
        flexibility_kw (float | None | Unset):
        device (DeviceIn | None | Unset):
        relationships (AssetRelationshipsIn | Unset): Relationships between assets.
    """

    name: str
    load_type: None | str | Unset = UNSET
    rated_power: float | None | Unset = UNSET
    min_power: float | None | Unset = UNSET
    controllable: bool | None | Unset = UNSET
    priority: None | str | Unset = UNSET
    flexibility_kw: float | None | Unset = UNSET
    device: DeviceIn | None | Unset = UNSET
    relationships: AssetRelationshipsIn | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.device_in import DeviceIn

        name = self.name

        load_type: None | str | Unset
        if isinstance(self.load_type, Unset):
            load_type = UNSET
        else:
            load_type = self.load_type

        rated_power: float | None | Unset
        if isinstance(self.rated_power, Unset):
            rated_power = UNSET
        else:
            rated_power = self.rated_power

        min_power: float | None | Unset
        if isinstance(self.min_power, Unset):
            min_power = UNSET
        else:
            min_power = self.min_power

        controllable: bool | None | Unset
        if isinstance(self.controllable, Unset):
            controllable = UNSET
        else:
            controllable = self.controllable

        priority: None | str | Unset
        if isinstance(self.priority, Unset):
            priority = UNSET
        else:
            priority = self.priority

        flexibility_kw: float | None | Unset
        if isinstance(self.flexibility_kw, Unset):
            flexibility_kw = UNSET
        else:
            flexibility_kw = self.flexibility_kw

        device: dict[str, Any] | None | Unset
        if isinstance(self.device, Unset):
            device = UNSET
        elif isinstance(self.device, DeviceIn):
            device = self.device.to_dict()
        else:
            device = self.device

        relationships: dict[str, Any] | Unset = UNSET
        if not isinstance(self.relationships, Unset):
            relationships = self.relationships.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if load_type is not UNSET:
            field_dict["load_type"] = load_type
        if rated_power is not UNSET:
            field_dict["rated_power"] = rated_power
        if min_power is not UNSET:
            field_dict["min_power"] = min_power
        if controllable is not UNSET:
            field_dict["controllable"] = controllable
        if priority is not UNSET:
            field_dict["priority"] = priority
        if flexibility_kw is not UNSET:
            field_dict["flexibility_kw"] = flexibility_kw
        if device is not UNSET:
            field_dict["device"] = device
        if relationships is not UNSET:
            field_dict["relationships"] = relationships

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_relationships_in import AssetRelationshipsIn
        from ..models.device_in import DeviceIn

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_load_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        load_type = _parse_load_type(d.pop("load_type", UNSET))

        def _parse_rated_power(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        rated_power = _parse_rated_power(d.pop("rated_power", UNSET))

        def _parse_min_power(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        min_power = _parse_min_power(d.pop("min_power", UNSET))

        def _parse_controllable(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        controllable = _parse_controllable(d.pop("controllable", UNSET))

        def _parse_priority(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        priority = _parse_priority(d.pop("priority", UNSET))

        def _parse_flexibility_kw(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        flexibility_kw = _parse_flexibility_kw(d.pop("flexibility_kw", UNSET))

        def _parse_device(data: object) -> DeviceIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                device_type_0 = DeviceIn.from_dict(data)

                return device_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DeviceIn | None | Unset, data)

        device = _parse_device(d.pop("device", UNSET))

        _relationships = d.pop("relationships", UNSET)
        relationships: AssetRelationshipsIn | Unset
        if isinstance(_relationships, Unset):
            relationships = UNSET
        else:
            relationships = AssetRelationshipsIn.from_dict(_relationships)

        load_asset_in = cls(
            name=name,
            load_type=load_type,
            rated_power=rated_power,
            min_power=min_power,
            controllable=controllable,
            priority=priority,
            flexibility_kw=flexibility_kw,
            device=device,
            relationships=relationships,
        )

        load_asset_in.additional_properties = d
        return load_asset_in

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
