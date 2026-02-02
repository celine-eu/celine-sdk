from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.values_request_payload import ValuesRequestPayload


T = TypeVar("T", bound="ValuesRequest")


@_attrs_define
class ValuesRequest:
    """
    Attributes:
        payload (ValuesRequestPayload | Unset):
    """

    payload: ValuesRequestPayload | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.values_request_payload import ValuesRequestPayload

        d = dict(src_dict)
        _payload = d.pop("payload", UNSET)
        payload: ValuesRequestPayload | Unset
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = ValuesRequestPayload.from_dict(_payload)

        values_request = cls(
            payload=payload,
        )

        values_request.additional_properties = d
        return values_request

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
