from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MemberInCommunity")


@_attrs_define
class MemberInCommunity:
    """
    Attributes:
        id (str):
        key (str):
        user_id (str):
        name (str):
        role (str):
        status (str):
    """

    id: str
    key: str
    user_id: str
    name: str
    role: str
    status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        user_id = self.user_id

        name = self.name

        role = self.role

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key": key,
                "user_id": user_id,
                "name": name,
                "role": role,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        key = d.pop("key")

        user_id = d.pop("user_id")

        name = d.pop("name")

        role = d.pop("role")

        status = d.pop("status")

        member_in_community = cls(
            id=id,
            key=key,
            user_id=user_id,
            name=name,
            role=role,
            status=status,
        )

        member_in_community.additional_properties = d
        return member_in_community

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
