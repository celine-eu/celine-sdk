from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.shared_delivery_point import SharedDeliveryPoint


T = TypeVar("T", bound="SharedDeliveryPointsRead")


@_attrs_define
class SharedDeliveryPointsRead:
    """
    Attributes:
        community_key (str):
        items (list[SharedDeliveryPoint]):
        revealed (bool):
    """

    community_key: str
    items: list[SharedDeliveryPoint]
    revealed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community_key = self.community_key

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        revealed = self.revealed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community_key": community_key,
                "items": items,
                "revealed": revealed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shared_delivery_point import SharedDeliveryPoint

        d = dict(src_dict)
        community_key = d.pop("community_key")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = SharedDeliveryPoint.from_dict(items_item_data)

            items.append(items_item)

        revealed = d.pop("revealed")

        shared_delivery_points_read = cls(
            community_key=community_key,
            items=items,
            revealed=revealed,
        )

        shared_delivery_points_read.additional_properties = d
        return shared_delivery_points_read

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
