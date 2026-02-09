from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeliveryPointIn")


@_attrs_define
class DeliveryPointIn:
    """Physical delivery point (POD, CUPS, PRM, etc.).

    Attributes:
        id (str):
        type_ (str):
        active (bool | Unset):  Default: True.
        address (None | str | Unset):
        description (None | str | Unset):
        tariff (None | str | Unset):
    """

    id: str
    type_: str
    active: bool | Unset = True
    address: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    tariff: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        active = self.active

        address: None | str | Unset
        if isinstance(self.address, Unset):
            address = UNSET
        else:
            address = self.address

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        tariff: None | str | Unset
        if isinstance(self.tariff, Unset):
            tariff = UNSET
        else:
            tariff = self.tariff

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )
        if active is not UNSET:
            field_dict["active"] = active
        if address is not UNSET:
            field_dict["address"] = address
        if description is not UNSET:
            field_dict["description"] = description
        if tariff is not UNSET:
            field_dict["tariff"] = tariff

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        active = d.pop("active", UNSET)

        def _parse_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        address = _parse_address(d.pop("address", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_tariff(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tariff = _parse_tariff(d.pop("tariff", UNSET))

        delivery_point_in = cls(
            id=id,
            type_=type_,
            active=active,
            address=address,
            description=description,
            tariff=tariff,
        )

        delivery_point_in.additional_properties = d
        return delivery_point_in

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
