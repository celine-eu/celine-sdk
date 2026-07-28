from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_relationships_in import AssetRelationshipsIn
    from ..models.device_in import DeviceIn


T = TypeVar("T", bound="HeatPumpAssetIn")


@_attrs_define
class HeatPumpAssetIn:
    """Heat pump asset.

    Attributes:
        name (str):
        thermal_power (float):
        electrical_power (float | None | Unset):
        cop (float | None | Unset):
        eer (float | None | Unset):
        scop (float | None | Unset):
        seer (float | None | Unset):
        heat_pump_type (None | str | Unset):
        reversible (bool | None | Unset):
        refrigerant (None | str | Unset):
        installation_date (None | str | Unset):
        device (DeviceIn | None | Unset):
        relationships (AssetRelationshipsIn | Unset): Relationships between assets.
    """

    name: str
    thermal_power: float
    electrical_power: float | None | Unset = UNSET
    cop: float | None | Unset = UNSET
    eer: float | None | Unset = UNSET
    scop: float | None | Unset = UNSET
    seer: float | None | Unset = UNSET
    heat_pump_type: None | str | Unset = UNSET
    reversible: bool | None | Unset = UNSET
    refrigerant: None | str | Unset = UNSET
    installation_date: None | str | Unset = UNSET
    device: DeviceIn | None | Unset = UNSET
    relationships: AssetRelationshipsIn | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.device_in import DeviceIn

        name = self.name

        thermal_power = self.thermal_power

        electrical_power: float | None | Unset
        if isinstance(self.electrical_power, Unset):
            electrical_power = UNSET
        else:
            electrical_power = self.electrical_power

        cop: float | None | Unset
        if isinstance(self.cop, Unset):
            cop = UNSET
        else:
            cop = self.cop

        eer: float | None | Unset
        if isinstance(self.eer, Unset):
            eer = UNSET
        else:
            eer = self.eer

        scop: float | None | Unset
        if isinstance(self.scop, Unset):
            scop = UNSET
        else:
            scop = self.scop

        seer: float | None | Unset
        if isinstance(self.seer, Unset):
            seer = UNSET
        else:
            seer = self.seer

        heat_pump_type: None | str | Unset
        if isinstance(self.heat_pump_type, Unset):
            heat_pump_type = UNSET
        else:
            heat_pump_type = self.heat_pump_type

        reversible: bool | None | Unset
        if isinstance(self.reversible, Unset):
            reversible = UNSET
        else:
            reversible = self.reversible

        refrigerant: None | str | Unset
        if isinstance(self.refrigerant, Unset):
            refrigerant = UNSET
        else:
            refrigerant = self.refrigerant

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
                "thermal_power": thermal_power,
            }
        )
        if electrical_power is not UNSET:
            field_dict["electrical_power"] = electrical_power
        if cop is not UNSET:
            field_dict["cop"] = cop
        if eer is not UNSET:
            field_dict["eer"] = eer
        if scop is not UNSET:
            field_dict["scop"] = scop
        if seer is not UNSET:
            field_dict["seer"] = seer
        if heat_pump_type is not UNSET:
            field_dict["heat_pump_type"] = heat_pump_type
        if reversible is not UNSET:
            field_dict["reversible"] = reversible
        if refrigerant is not UNSET:
            field_dict["refrigerant"] = refrigerant
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

        thermal_power = d.pop("thermal_power")

        def _parse_electrical_power(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        electrical_power = _parse_electrical_power(d.pop("electrical_power", UNSET))

        def _parse_cop(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        cop = _parse_cop(d.pop("cop", UNSET))

        def _parse_eer(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        eer = _parse_eer(d.pop("eer", UNSET))

        def _parse_scop(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        scop = _parse_scop(d.pop("scop", UNSET))

        def _parse_seer(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        seer = _parse_seer(d.pop("seer", UNSET))

        def _parse_heat_pump_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        heat_pump_type = _parse_heat_pump_type(d.pop("heat_pump_type", UNSET))

        def _parse_reversible(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        reversible = _parse_reversible(d.pop("reversible", UNSET))

        def _parse_refrigerant(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        refrigerant = _parse_refrigerant(d.pop("refrigerant", UNSET))

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

        heat_pump_asset_in = cls(
            name=name,
            thermal_power=thermal_power,
            electrical_power=electrical_power,
            cop=cop,
            eer=eer,
            scop=scop,
            seer=seer,
            heat_pump_type=heat_pump_type,
            reversible=reversible,
            refrigerant=refrigerant,
            installation_date=installation_date,
            device=device,
            relationships=relationships,
        )

        heat_pump_asset_in.additional_properties = d
        return heat_pump_asset_in

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
