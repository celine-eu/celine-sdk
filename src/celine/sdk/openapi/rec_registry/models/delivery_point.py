from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeliveryPoint")


@_attrs_define
class DeliveryPoint:
    """
    Attributes:
        id (str):
        type_ (str):
        description (None | str | Unset):
        address (None | str | Unset):
        tariff (None | str | Unset):
        active (bool | Unset):  Default: True.
    """

    id: str
    type_: str
    description: None | str | Unset = UNSET
    address: None | str | Unset = UNSET
    tariff: None | str | Unset = UNSET
    active: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        address: None | str | Unset
        if isinstance(self.address, Unset):
            address = UNSET
        else:
            address = self.address

        tariff: None | str | Unset
        if isinstance(self.tariff, Unset):
            tariff = UNSET
        else:
            tariff = self.tariff

        active = self.active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if address is not UNSET:
            field_dict["address"] = address
        if tariff is not UNSET:
            field_dict["tariff"] = tariff
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        address = _parse_address(d.pop("address", UNSET))

        def _parse_tariff(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tariff = _parse_tariff(d.pop("tariff", UNSET))

        active = d.pop("active", UNSET)

        delivery_point = cls(
            id=id,
            type_=type_,
            description=description,
            address=address,
            tariff=tariff,
            active=active,
        )

        delivery_point.additional_properties = d
        return delivery_point

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
