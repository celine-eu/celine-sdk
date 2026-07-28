from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_relationships_in import AssetRelationshipsIn
    from ..models.device_in import DeviceIn


T = TypeVar("T", bound="MeterAssetIn")


@_attrs_define
class MeterAssetIn:
    """Meter asset.

    Attributes:
        name (str):
        sensor_id (str):
        meter_type (str):
        pod (None | str | Unset):
        protocol (None | str | Unset):
        installation_date (None | str | Unset):
        device (DeviceIn | None | Unset):
        relationships (AssetRelationshipsIn | Unset): Relationships between assets.
    """

    name: str
    sensor_id: str
    meter_type: str
    pod: None | str | Unset = UNSET
    protocol: None | str | Unset = UNSET
    installation_date: None | str | Unset = UNSET
    device: DeviceIn | None | Unset = UNSET
    relationships: AssetRelationshipsIn | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.device_in import DeviceIn

        name = self.name

        sensor_id = self.sensor_id

        meter_type = self.meter_type

        pod: None | str | Unset
        if isinstance(self.pod, Unset):
            pod = UNSET
        else:
            pod = self.pod

        protocol: None | str | Unset
        if isinstance(self.protocol, Unset):
            protocol = UNSET
        else:
            protocol = self.protocol

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
                "sensor_id": sensor_id,
                "meter_type": meter_type,
            }
        )
        if pod is not UNSET:
            field_dict["pod"] = pod
        if protocol is not UNSET:
            field_dict["protocol"] = protocol
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

        sensor_id = d.pop("sensor_id")

        meter_type = d.pop("meter_type")

        def _parse_pod(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pod = _parse_pod(d.pop("pod", UNSET))

        def _parse_protocol(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        protocol = _parse_protocol(d.pop("protocol", UNSET))

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

        meter_asset_in = cls(
            name=name,
            sensor_id=sensor_id,
            meter_type=meter_type,
            pod=pod,
            protocol=protocol,
            installation_date=installation_date,
            device=device,
            relationships=relationships,
        )

        meter_asset_in.additional_properties = d
        return meter_asset_in

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
