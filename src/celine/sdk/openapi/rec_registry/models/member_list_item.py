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
        area (str):
        id (str):
        key (str):
        name (str):
        role (str):
        status (str):
        user_id (str):
        delivery_points_count (int | Unset):  Default: 0.
    """

    area: str
    id: str
    key: str
    name: str
    role: str
    status: str
    user_id: str
    delivery_points_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area

        id = self.id

        key = self.key

        name = self.name

        role = self.role

        status = self.status

        user_id = self.user_id

        delivery_points_count = self.delivery_points_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "id": id,
                "key": key,
                "name": name,
                "role": role,
                "status": status,
                "user_id": user_id,
            }
        )
        if delivery_points_count is not UNSET:
            field_dict["delivery_points_count"] = delivery_points_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        area = d.pop("area")

        id = d.pop("id")

        key = d.pop("key")

        name = d.pop("name")

        role = d.pop("role")

        status = d.pop("status")

        user_id = d.pop("user_id")

        delivery_points_count = d.pop("delivery_points_count", UNSET)

        member_list_item = cls(
            area=area,
            id=id,
            key=key,
            name=name,
            role=role,
            status=status,
            user_id=user_id,
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
