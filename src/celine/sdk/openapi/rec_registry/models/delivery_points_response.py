from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery_point import DeliveryPoint


T = TypeVar("T", bound="DeliveryPointsResponse")


@_attrs_define
class DeliveryPointsResponse:
    """
    Attributes:
        delivery_points (list[DeliveryPoint] | Unset):
    """

    delivery_points: list[DeliveryPoint] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delivery_points: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.delivery_points, Unset):
            delivery_points = []
            for delivery_points_item_data in self.delivery_points:
                delivery_points_item = delivery_points_item_data.to_dict()
                delivery_points.append(delivery_points_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if delivery_points is not UNSET:
            field_dict["delivery_points"] = delivery_points

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delivery_point import DeliveryPoint

        d = dict(src_dict)
        _delivery_points = d.pop("delivery_points", UNSET)
        delivery_points: list[DeliveryPoint] | Unset = UNSET
        if _delivery_points is not UNSET:
            delivery_points = []
            for delivery_points_item_data in _delivery_points:
                delivery_points_item = DeliveryPoint.from_dict(delivery_points_item_data)

                delivery_points.append(delivery_points_item)

        delivery_points_response = cls(
            delivery_points=delivery_points,
        )

        delivery_points_response.additional_properties = d
        return delivery_points_response

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
