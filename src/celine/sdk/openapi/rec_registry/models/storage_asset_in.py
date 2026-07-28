from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_relationships_in import AssetRelationshipsIn
    from ..models.device_in import DeviceIn


T = TypeVar("T", bound="StorageAssetIn")


@_attrs_define
class StorageAssetIn:
    """Battery storage asset.

    Attributes:
        name (str):
        capacity (float | None | Unset):
        max_charge_power (float | None | Unset):
        max_discharge_power (float | None | Unset):
        battery_type (None | str | Unset):
        round_trip_efficiency (float | None | Unset):
        installation_date (None | str | Unset):
        device (DeviceIn | None | Unset):
        relationships (AssetRelationshipsIn | Unset): Relationships between assets.
    """

    name: str
    capacity: float | None | Unset = UNSET
    max_charge_power: float | None | Unset = UNSET
    max_discharge_power: float | None | Unset = UNSET
    battery_type: None | str | Unset = UNSET
    round_trip_efficiency: float | None | Unset = UNSET
    installation_date: None | str | Unset = UNSET
    device: DeviceIn | None | Unset = UNSET
    relationships: AssetRelationshipsIn | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.device_in import DeviceIn

        name = self.name

        capacity: float | None | Unset
        if isinstance(self.capacity, Unset):
            capacity = UNSET
        else:
            capacity = self.capacity

        max_charge_power: float | None | Unset
        if isinstance(self.max_charge_power, Unset):
            max_charge_power = UNSET
        else:
            max_charge_power = self.max_charge_power

        max_discharge_power: float | None | Unset
        if isinstance(self.max_discharge_power, Unset):
            max_discharge_power = UNSET
        else:
            max_discharge_power = self.max_discharge_power

        battery_type: None | str | Unset
        if isinstance(self.battery_type, Unset):
            battery_type = UNSET
        else:
            battery_type = self.battery_type

        round_trip_efficiency: float | None | Unset
        if isinstance(self.round_trip_efficiency, Unset):
            round_trip_efficiency = UNSET
        else:
            round_trip_efficiency = self.round_trip_efficiency

        installation_date: None | str | Unset
        if isinstance(self.installation_date, Unset):
            installation_date = UNSET
        else:
            installation_date = self.installation_date

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
        if capacity is not UNSET:
            field_dict["capacity"] = capacity
        if max_charge_power is not UNSET:
            field_dict["max_charge_power"] = max_charge_power
        if max_discharge_power is not UNSET:
            field_dict["max_discharge_power"] = max_discharge_power
        if battery_type is not UNSET:
            field_dict["battery_type"] = battery_type
        if round_trip_efficiency is not UNSET:
            field_dict["round_trip_efficiency"] = round_trip_efficiency
        if installation_date is not UNSET:
            field_dict["installation_date"] = installation_date
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

        def _parse_capacity(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        capacity = _parse_capacity(d.pop("capacity", UNSET))

        def _parse_max_charge_power(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_charge_power = _parse_max_charge_power(d.pop("max_charge_power", UNSET))

        def _parse_max_discharge_power(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_discharge_power = _parse_max_discharge_power(d.pop("max_discharge_power", UNSET))

        def _parse_battery_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        battery_type = _parse_battery_type(d.pop("battery_type", UNSET))

        def _parse_round_trip_efficiency(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        round_trip_efficiency = _parse_round_trip_efficiency(d.pop("round_trip_efficiency", UNSET))

        def _parse_installation_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        installation_date = _parse_installation_date(d.pop("installation_date", UNSET))

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

        storage_asset_in = cls(
            name=name,
            capacity=capacity,
            max_charge_power=max_charge_power,
            max_discharge_power=max_discharge_power,
            battery_type=battery_type,
            round_trip_efficiency=round_trip_efficiency,
            installation_date=installation_date,
            device=device,
            relationships=relationships,
        )

        storage_asset_in.additional_properties = d
        return storage_asset_in

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
