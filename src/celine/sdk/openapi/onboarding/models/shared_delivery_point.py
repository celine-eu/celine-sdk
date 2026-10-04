from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.shared_holder import SharedHolder


T = TypeVar("T", bound="SharedDeliveryPoint")


@_attrs_define
class SharedDeliveryPoint:
    """
    Attributes:
        active_holders (int):
        delivery_point (str):
        held_elsewhere (int):
        holders (list[SharedHolder]):
    """

    active_holders: int
    delivery_point: str
    held_elsewhere: int
    holders: list[SharedHolder]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active_holders = self.active_holders

        delivery_point = self.delivery_point

        held_elsewhere = self.held_elsewhere

        holders = []
        for holders_item_data in self.holders:
            holders_item = holders_item_data.to_dict()
            holders.append(holders_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active_holders": active_holders,
                "delivery_point": delivery_point,
                "held_elsewhere": held_elsewhere,
                "holders": holders,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shared_holder import SharedHolder

        d = dict(src_dict)
        active_holders = d.pop("active_holders")

        delivery_point = d.pop("delivery_point")

        held_elsewhere = d.pop("held_elsewhere")

        holders = []
        _holders = d.pop("holders")
        for holders_item_data in _holders:
            holders_item = SharedHolder.from_dict(holders_item_data)

            holders.append(holders_item)

        shared_delivery_point = cls(
            active_holders=active_holders,
            delivery_point=delivery_point,
            held_elsewhere=held_elsewhere,
            holders=holders,
        )

        shared_delivery_point.additional_properties = d
        return shared_delivery_point

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
