from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_relationships_in import AssetRelationshipsIn
    from ..models.device_in import DeviceIn


T = TypeVar("T", bound="PVAssetIn")


@_attrs_define
class PVAssetIn:
    """PV system asset.

    Attributes:
        name (str):
        rated_power (float | None | Unset):
        panel_type (None | str | Unset):
        inverter_power (float | None | Unset):
        orientation (float | None | Unset):
        tilt_angle (float | None | Unset):
        installation_date (None | str | Unset):
        device (DeviceIn | None | Unset):
        relationships (AssetRelationshipsIn | Unset): Relationships between assets.
    """

    name: str
    rated_power: float | None | Unset = UNSET
    panel_type: None | str | Unset = UNSET
    inverter_power: float | None | Unset = UNSET
    orientation: float | None | Unset = UNSET
    tilt_angle: float | None | Unset = UNSET
    installation_date: None | str | Unset = UNSET
    device: DeviceIn | None | Unset = UNSET
    relationships: AssetRelationshipsIn | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.device_in import DeviceIn

        name = self.name

        rated_power: float | None | Unset
        if isinstance(self.rated_power, Unset):
            rated_power = UNSET
        else:
            rated_power = self.rated_power

        panel_type: None | str | Unset
        if isinstance(self.panel_type, Unset):
            panel_type = UNSET
        else:
            panel_type = self.panel_type

        inverter_power: float | None | Unset
        if isinstance(self.inverter_power, Unset):
            inverter_power = UNSET
        else:
            inverter_power = self.inverter_power

        orientation: float | None | Unset
        if isinstance(self.orientation, Unset):
            orientation = UNSET
        else:
            orientation = self.orientation

        tilt_angle: float | None | Unset
        if isinstance(self.tilt_angle, Unset):
            tilt_angle = UNSET
        else:
            tilt_angle = self.tilt_angle

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
        if rated_power is not UNSET:
            field_dict["rated_power"] = rated_power
        if panel_type is not UNSET:
            field_dict["panel_type"] = panel_type
        if inverter_power is not UNSET:
            field_dict["inverter_power"] = inverter_power
        if orientation is not UNSET:
            field_dict["orientation"] = orientation
        if tilt_angle is not UNSET:
            field_dict["tilt_angle"] = tilt_angle
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

        def _parse_rated_power(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        rated_power = _parse_rated_power(d.pop("rated_power", UNSET))

        def _parse_panel_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        panel_type = _parse_panel_type(d.pop("panel_type", UNSET))

        def _parse_inverter_power(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        inverter_power = _parse_inverter_power(d.pop("inverter_power", UNSET))

        def _parse_orientation(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        orientation = _parse_orientation(d.pop("orientation", UNSET))

        def _parse_tilt_angle(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        tilt_angle = _parse_tilt_angle(d.pop("tilt_angle", UNSET))

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

        pv_asset_in = cls(
            name=name,
            rated_power=rated_power,
            panel_type=panel_type,
            inverter_power=inverter_power,
            orientation=orientation,
            tilt_angle=tilt_angle,
            installation_date=installation_date,
            device=device,
            relationships=relationships,
        )

        pv_asset_in.additional_properties = d
        return pv_asset_in

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
