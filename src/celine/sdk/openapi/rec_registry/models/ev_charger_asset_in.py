from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_relationships_in import AssetRelationshipsIn
    from ..models.device_in import DeviceIn


T = TypeVar("T", bound="EVChargerAssetIn")


@_attrs_define
class EVChargerAssetIn:
    """EV charger asset.

    Attributes:
        name (str):
        max_power (float):
        charger_type (str):
        connector_types (list[str] | Unset):
        smart_charging (bool | None | Unset):
        bidirectional (bool | None | Unset):
        num_ports (int | None | Unset):
        installation_date (None | str | Unset):
        device (DeviceIn | None | Unset):
        relationships (AssetRelationshipsIn | Unset): Relationships between assets.
    """

    name: str
    max_power: float
    charger_type: str
    connector_types: list[str] | Unset = UNSET
    smart_charging: bool | None | Unset = UNSET
    bidirectional: bool | None | Unset = UNSET
    num_ports: int | None | Unset = UNSET
    installation_date: None | str | Unset = UNSET
    device: DeviceIn | None | Unset = UNSET
    relationships: AssetRelationshipsIn | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.device_in import DeviceIn

        name = self.name

        max_power = self.max_power

        charger_type = self.charger_type

        connector_types: list[str] | Unset = UNSET
        if not isinstance(self.connector_types, Unset):
            connector_types = self.connector_types

        smart_charging: bool | None | Unset
        if isinstance(self.smart_charging, Unset):
            smart_charging = UNSET
        else:
            smart_charging = self.smart_charging

        bidirectional: bool | None | Unset
        if isinstance(self.bidirectional, Unset):
            bidirectional = UNSET
        else:
            bidirectional = self.bidirectional

        num_ports: int | None | Unset
        if isinstance(self.num_ports, Unset):
            num_ports = UNSET
        else:
            num_ports = self.num_ports

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
                "max_power": max_power,
                "charger_type": charger_type,
            }
        )
        if connector_types is not UNSET:
            field_dict["connector_types"] = connector_types
        if smart_charging is not UNSET:
            field_dict["smart_charging"] = smart_charging
        if bidirectional is not UNSET:
            field_dict["bidirectional"] = bidirectional
        if num_ports is not UNSET:
            field_dict["num_ports"] = num_ports
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

        max_power = d.pop("max_power")

        charger_type = d.pop("charger_type")

        connector_types = cast(list[str], d.pop("connector_types", UNSET))

        def _parse_smart_charging(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        smart_charging = _parse_smart_charging(d.pop("smart_charging", UNSET))

        def _parse_bidirectional(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        bidirectional = _parse_bidirectional(d.pop("bidirectional", UNSET))

        def _parse_num_ports(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_ports = _parse_num_ports(d.pop("num_ports", UNSET))

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

        ev_charger_asset_in = cls(
            name=name,
            max_power=max_power,
            charger_type=charger_type,
            connector_types=connector_types,
            smart_charging=smart_charging,
            bidirectional=bidirectional,
            num_ports=num_ports,
            installation_date=installation_date,
            device=device,
            relationships=relationships,
        )

        ev_charger_asset_in.additional_properties = d
        return ev_charger_asset_in

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
