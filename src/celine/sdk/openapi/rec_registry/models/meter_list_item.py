from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.meter_list_item_device import MeterListItemDevice


T = TypeVar("T", bound="MeterListItem")


@_attrs_define
class MeterListItem:
    """
    Attributes:
        id (str):
        key (str):
        name (str):
        owner_key (str):
        owner_user_id (str):
        sensor_id (None | str | Unset):
        meter_type (None | str | Unset):
        pod (None | str | Unset):
        device (MeterListItemDevice | Unset):
    """

    id: str
    key: str
    name: str
    owner_key: str
    owner_user_id: str
    sensor_id: None | str | Unset = UNSET
    meter_type: None | str | Unset = UNSET
    pod: None | str | Unset = UNSET
    device: MeterListItemDevice | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        name = self.name

        owner_key = self.owner_key

        owner_user_id = self.owner_user_id

        sensor_id: None | str | Unset
        if isinstance(self.sensor_id, Unset):
            sensor_id = UNSET
        else:
            sensor_id = self.sensor_id

        meter_type: None | str | Unset
        if isinstance(self.meter_type, Unset):
            meter_type = UNSET
        else:
            meter_type = self.meter_type

        pod: None | str | Unset
        if isinstance(self.pod, Unset):
            pod = UNSET
        else:
            pod = self.pod

        device: dict[str, Any] | Unset = UNSET
        if not isinstance(self.device, Unset):
            device = self.device.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key": key,
                "name": name,
                "owner_key": owner_key,
                "owner_user_id": owner_user_id,
            }
        )
        if sensor_id is not UNSET:
            field_dict["sensor_id"] = sensor_id
        if meter_type is not UNSET:
            field_dict["meter_type"] = meter_type
        if pod is not UNSET:
            field_dict["pod"] = pod
        if device is not UNSET:
            field_dict["device"] = device

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.meter_list_item_device import MeterListItemDevice

        d = dict(src_dict)
        id = d.pop("id")

        key = d.pop("key")

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

        def _parse_meter_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        meter_type = _parse_meter_type(d.pop("meter_type", UNSET))

        def _parse_pod(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pod = _parse_pod(d.pop("pod", UNSET))

        _device = d.pop("device", UNSET)
        device: MeterListItemDevice | Unset
        if isinstance(_device, Unset):
            device = UNSET
        else:
            device = MeterListItemDevice.from_dict(_device)

        meter_list_item = cls(
            id=id,
            key=key,
            name=name,
            owner_key=owner_key,
            owner_user_id=owner_user_id,
            sensor_id=sensor_id,
            meter_type=meter_type,
            pod=pod,
            device=device,
        )

        meter_list_item.additional_properties = d
        return meter_list_item

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
