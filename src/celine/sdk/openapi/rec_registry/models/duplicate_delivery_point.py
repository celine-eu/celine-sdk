from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.duplicate_holder import DuplicateHolder


T = TypeVar("T", bound="DuplicateDeliveryPoint")


@_attrs_define
class DuplicateDeliveryPoint:
    """One delivery point of the community that more than one active member holds.

    Attributes:
        active_holders (int): Every active member holding it, here and elsewhere.
        delivery_point (str): The point in its compared form: trimmed and lower-cased, as the registry compares delivery
            points (REQ-0085).
        held_elsewhere (int): How many active members of other communities hold it. They are never named, nor their
            communities.
        holders (list[DuplicateHolder]): This community's active holders, by member key, with their stored spelling.
    """

    active_holders: int
    delivery_point: str
    held_elsewhere: int
    holders: list[DuplicateHolder]
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
        from ..models.duplicate_holder import DuplicateHolder

        d = dict(src_dict)
        active_holders = d.pop("active_holders")

        delivery_point = d.pop("delivery_point")

        held_elsewhere = d.pop("held_elsewhere")

        holders = []
        _holders = d.pop("holders")
        for holders_item_data in _holders:
            holders_item = DuplicateHolder.from_dict(holders_item_data)

            holders.append(holders_item)

        duplicate_delivery_point = cls(
            active_holders=active_holders,
            delivery_point=delivery_point,
            held_elsewhere=held_elsewhere,
            holders=holders,
        )

        duplicate_delivery_point.additional_properties = d
        return duplicate_delivery_point

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
