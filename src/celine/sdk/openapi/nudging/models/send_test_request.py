from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

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
        community_id (None | str | Unset): Optional community scope for the test send
        title (str | Unset):  Default: 'Test'.
        url (str | Unset):  Default: '/'.
    """

    user_id: str
    body: str | Unset = "Hello!"
    community_id: None | str | Unset = UNSET
    title: str | Unset = "Test"
    url: str | Unset = "/"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        body = self.body

        community_id: None | str | Unset
        if isinstance(self.community_id, Unset):
            community_id = UNSET
        else:
            community_id = self.community_id

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
        if community_id is not UNSET:
            field_dict["community_id"] = community_id
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

        def _parse_community_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        community_id = _parse_community_id(d.pop("community_id", UNSET))

        title = d.pop("title", UNSET)

        url = d.pop("url", UNSET)

        send_test_request = cls(
            user_id=user_id,
            body=body,
            community_id=community_id,
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
