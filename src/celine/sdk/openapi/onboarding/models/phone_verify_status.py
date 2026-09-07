from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PhoneVerifyStatus")


@_attrs_define
class PhoneVerifyStatus:
    """
    Attributes:
        phone_verified (bool):
        phone_verified_at (datetime.datetime | None | Unset):
        sent (bool | Unset):  Default: False.
    """

    phone_verified: bool
    phone_verified_at: datetime.datetime | None | Unset = UNSET
    sent: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        phone_verified = self.phone_verified

        phone_verified_at: None | str | Unset
        if isinstance(self.phone_verified_at, Unset):
            phone_verified_at = UNSET
        elif isinstance(self.phone_verified_at, datetime.datetime):
            phone_verified_at = self.phone_verified_at.isoformat()
        else:
            phone_verified_at = self.phone_verified_at

        sent = self.sent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "phone_verified": phone_verified,
            }
        )
        if phone_verified_at is not UNSET:
            field_dict["phone_verified_at"] = phone_verified_at
        if sent is not UNSET:
            field_dict["sent"] = sent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        phone_verified = d.pop("phone_verified")

        def _parse_phone_verified_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                phone_verified_at_type_0 = isoparse(data)

                return phone_verified_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        phone_verified_at = _parse_phone_verified_at(d.pop("phone_verified_at", UNSET))

        sent = d.pop("sent", UNSET)

        phone_verify_status = cls(
            phone_verified=phone_verified,
            phone_verified_at=phone_verified_at,
            sent=sent,
        )

        phone_verify_status.additional_properties = d
        return phone_verify_status

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
