from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserInfo")


@_attrs_define
class UserInfo:
    """
    Attributes:
        email (str | Unset):  Default: ''.
        first_name (str | Unset):  Default: ''.
        full_name (str | Unset):  Default: ''.
        groups (list[str] | Unset):
        is_admin (bool | Unset):  Default: False.
        last_name (str | Unset):  Default: ''.
        user_id (str | Unset):  Default: ''.
        username (str | Unset):  Default: ''.
    """

    email: str | Unset = ""
    first_name: str | Unset = ""
    full_name: str | Unset = ""
    groups: list[str] | Unset = UNSET
    is_admin: bool | Unset = False
    last_name: str | Unset = ""
    user_id: str | Unset = ""
    username: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        first_name = self.first_name

        full_name = self.full_name

        groups: list[str] | Unset = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        is_admin = self.is_admin

        last_name = self.last_name

        user_id = self.user_id

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if full_name is not UNSET:
            field_dict["full_name"] = full_name
        if groups is not UNSET:
            field_dict["groups"] = groups
        if is_admin is not UNSET:
            field_dict["is_admin"] = is_admin
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if username is not UNSET:
            field_dict["username"] = username

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email", UNSET)

        first_name = d.pop("first_name", UNSET)

        full_name = d.pop("full_name", UNSET)

        groups = cast(list[str], d.pop("groups", UNSET))

        is_admin = d.pop("is_admin", UNSET)

        last_name = d.pop("last_name", UNSET)

        user_id = d.pop("user_id", UNSET)

        username = d.pop("username", UNSET)

        user_info = cls(
            email=email,
            first_name=first_name,
            full_name=full_name,
            groups=groups,
            is_admin=is_admin,
            last_name=last_name,
            user_id=user_id,
            username=username,
        )

        user_info.additional_properties = d
        return user_info

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
