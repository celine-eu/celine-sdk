from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PasswordResetResponse")


@_attrs_define
class PasswordResetResponse:
    """The one-time credential, and who it belongs to.

    Temporary by construction: the participant is made to change it at next
    login, so what travels back here is a handover and never their password.

        Attributes:
            temporary_password (str):
            user_id (str):
            username (str):
    """

    temporary_password: str
    user_id: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        temporary_password = self.temporary_password

        user_id = self.user_id

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "temporary_password": temporary_password,
                "user_id": user_id,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        temporary_password = d.pop("temporary_password")

        user_id = d.pop("user_id")

        username = d.pop("username")

        password_reset_response = cls(
            temporary_password=temporary_password,
            user_id=user_id,
            username=username,
        )

        password_reset_response.additional_properties = d
        return password_reset_response

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
