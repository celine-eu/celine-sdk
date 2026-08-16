from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChatRequest")


@_attrs_define
class ChatRequest:
    """
    Attributes:
        message (str):
        attachment_ids (list[str] | Unset):
        conversation_id (None | str | Unset):
        include_citations (bool | Unset):  Default: True.
        top_k (int | Unset):  Default: 5.
    """

    message: str
    attachment_ids: list[str] | Unset = UNSET
    conversation_id: None | str | Unset = UNSET
    include_citations: bool | Unset = True
    top_k: int | Unset = 5
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        attachment_ids: list[str] | Unset = UNSET
        if not isinstance(self.attachment_ids, Unset):
            attachment_ids = self.attachment_ids

        conversation_id: None | str | Unset
        if isinstance(self.conversation_id, Unset):
            conversation_id = UNSET
        else:
            conversation_id = self.conversation_id

        include_citations = self.include_citations

        top_k = self.top_k

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if attachment_ids is not UNSET:
            field_dict["attachment_ids"] = attachment_ids
        if conversation_id is not UNSET:
            field_dict["conversation_id"] = conversation_id
        if include_citations is not UNSET:
            field_dict["include_citations"] = include_citations
        if top_k is not UNSET:
            field_dict["top_k"] = top_k

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        attachment_ids = cast(list[str], d.pop("attachment_ids", UNSET))

        def _parse_conversation_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        conversation_id = _parse_conversation_id(d.pop("conversation_id", UNSET))

        include_citations = d.pop("include_citations", UNSET)

        top_k = d.pop("top_k", UNSET)

        chat_request = cls(
            message=message,
            attachment_ids=attachment_ids,
            conversation_id=conversation_id,
            include_citations=include_citations,
            top_k=top_k,
        )

        chat_request.additional_properties = d
        return chat_request

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
