from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SendTestResponse")


@_attrs_define
class SendTestResponse:
    """
    Attributes:
        status (str):
        failed (int | None | Unset):
        sent (int | None | Unset):
    """

    status: str
    failed: int | None | Unset = UNSET
    sent: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        failed: int | None | Unset
        if isinstance(self.failed, Unset):
            failed = UNSET
        else:
            failed = self.failed

        sent: int | None | Unset
        if isinstance(self.sent, Unset):
            sent = UNSET
        else:
            sent = self.sent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if failed is not UNSET:
            field_dict["failed"] = failed
        if sent is not UNSET:
            field_dict["sent"] = sent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        def _parse_failed(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        failed = _parse_failed(d.pop("failed", UNSET))

        def _parse_sent(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        sent = _parse_sent(d.pop("sent", UNSET))

        send_test_response = cls(
            status=status,
            failed=failed,
            sent=sent,
        )

        send_test_response.additional_properties = d
        return send_test_response

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
