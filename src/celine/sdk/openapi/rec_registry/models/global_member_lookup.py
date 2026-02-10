from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery_point import DeliveryPoint


T = TypeVar("T", bound="GlobalMemberLookup")


@_attrs_define
class GlobalMemberLookup:
    """
    Attributes:
        area (str):
        community_key (str):
        community_name (str):
        id (str):
        key (str):
        name (str):
        role (str):
        status (str):
        user_id (str):
        delivery_points (list[DeliveryPoint] | Unset):
    """

    area: str
    community_key: str
    community_name: str
    id: str
    key: str
    name: str
    role: str
    status: str
    user_id: str
    delivery_points: list[DeliveryPoint] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area

        community_key = self.community_key

        community_name = self.community_name

        id = self.id

        key = self.key

        name = self.name

        role = self.role

        status = self.status

        user_id = self.user_id

        delivery_points: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.delivery_points, Unset):
            delivery_points = []
            for delivery_points_item_data in self.delivery_points:
                delivery_points_item = delivery_points_item_data.to_dict()
                delivery_points.append(delivery_points_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "community_key": community_key,
                "community_name": community_name,
                "id": id,
                "key": key,
                "name": name,
                "role": role,
                "status": status,
                "user_id": user_id,
            }
        )
        if delivery_points is not UNSET:
            field_dict["delivery_points"] = delivery_points

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delivery_point import DeliveryPoint

        d = dict(src_dict)
        area = d.pop("area")

        community_key = d.pop("community_key")

        community_name = d.pop("community_name")

        id = d.pop("id")

        key = d.pop("key")

        name = d.pop("name")

        role = d.pop("role")

        status = d.pop("status")

        user_id = d.pop("user_id")

        _delivery_points = d.pop("delivery_points", UNSET)
        delivery_points: list[DeliveryPoint] | Unset = UNSET
        if _delivery_points is not UNSET:
            delivery_points = []
            for delivery_points_item_data in _delivery_points:
                delivery_points_item = DeliveryPoint.from_dict(delivery_points_item_data)

                delivery_points.append(delivery_points_item)

        global_member_lookup = cls(
            area=area,
            community_key=community_key,
            community_name=community_name,
            id=id,
            key=key,
            name=name,
            role=role,
            status=status,
            user_id=user_id,
            delivery_points=delivery_points,
        )

        global_member_lookup.additional_properties = d
        return global_member_lookup

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
