from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.duplicate_delivery_point import DuplicateDeliveryPoint


T = TypeVar("T", bound="DeliveryPointDuplicates")


@_attrs_define
class DeliveryPointDuplicates:
    """`GET …/communities/{key}/delivery-points/duplicates` (REQ-0087).

    Attributes:
        community_key (str):
        items (list[DuplicateDeliveryPoint] | Unset):
    """

    community_key: str
    items: list[DuplicateDeliveryPoint] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community_key = self.community_key

        items: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()
                items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community_key": community_key,
            }
        )
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.duplicate_delivery_point import DuplicateDeliveryPoint

        d = dict(src_dict)
        community_key = d.pop("community_key")

        _items = d.pop("items", UNSET)
        items: list[DuplicateDeliveryPoint] | Unset = UNSET
        if _items is not UNSET:
            items = []
            for items_item_data in _items:
                items_item = DuplicateDeliveryPoint.from_dict(items_item_data)

                items.append(items_item)

        delivery_point_duplicates = cls(
            community_key=community_key,
            items=items,
        )

        delivery_point_duplicates.additional_properties = d
        return delivery_point_duplicates

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
