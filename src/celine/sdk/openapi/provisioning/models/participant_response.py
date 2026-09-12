from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ParticipantResponse")


@_attrs_define
class ParticipantResponse:
    """What the caller cannot compute and has to be told.

    Attributes:
        created (bool): Whether this call created the account. A retry returns false.
        user_id (str): The Keycloak uuid of the account (not the registry's user_id)
        username (str): What this account authenticates as, read back from Keycloak. This is the value that becomes the
            registry's Member.user_id.
    """

    created: bool
    user_id: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = self.created

        user_id = self.user_id

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "user_id": user_id,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created = d.pop("created")

        user_id = d.pop("user_id")

        username = d.pop("username")

        participant_response = cls(
            created=created,
            user_id=user_id,
            username=username,
        )

        participant_response.additional_properties = d
        return participant_response

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
