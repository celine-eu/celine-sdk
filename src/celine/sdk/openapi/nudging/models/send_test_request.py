from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SendTestRequest")


@_attrs_define
class SendTestRequest:
    """Admin-only: user_id is explicit because an admin targets any user.

    Attributes:
        user_id (str): Target user ID
        body (str | Unset):  Default: 'Hello!'.
        title (str | Unset):  Default: 'Test'.
        url (str | Unset):  Default: '/'.
    """

    user_id: str
    body: str | Unset = "Hello!"
    title: str | Unset = "Test"
    url: str | Unset = "/"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        body = self.body

        title = self.title

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_id": user_id,
            }
        )
        if body is not UNSET:
            field_dict["body"] = body
        if title is not UNSET:
            field_dict["title"] = title
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("user_id")

        body = d.pop("body", UNSET)

        title = d.pop("title", UNSET)

        url = d.pop("url", UNSET)

        send_test_request = cls(
            user_id=user_id,
            body=body,
            title=title,
            url=url,
        )

        send_test_request.additional_properties = d
        return send_test_request

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
