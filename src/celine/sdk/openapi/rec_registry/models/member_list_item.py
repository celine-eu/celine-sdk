from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MemberListItem")


@_attrs_define
class MemberListItem:
    """
    Attributes:
        id (str):
        key (str):
        user_id (str):
        name (str):
        role (str):
        area (str):
        status (str):
        delivery_points_count (int | Unset):  Default: 0.
    """

    id: str
    key: str
    user_id: str
    name: str
    role: str
    area: str
    status: str
    delivery_points_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        user_id = self.user_id

        name = self.name

        role = self.role

        area = self.area

        status = self.status

        delivery_points_count = self.delivery_points_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key": key,
                "user_id": user_id,
                "name": name,
                "role": role,
                "area": area,
                "status": status,
            }
        )
        if delivery_points_count is not UNSET:
            field_dict["delivery_points_count"] = delivery_points_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        key = d.pop("key")

        user_id = d.pop("user_id")

        name = d.pop("name")

        role = d.pop("role")

        area = d.pop("area")

        status = d.pop("status")

        delivery_points_count = d.pop("delivery_points_count", UNSET)

        member_list_item = cls(
            id=id,
            key=key,
            user_id=user_id,
            name=name,
            role=role,
            area=area,
            status=status,
            delivery_points_count=delivery_points_count,
        )

        member_list_item.additional_properties = d
        return member_list_item

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
