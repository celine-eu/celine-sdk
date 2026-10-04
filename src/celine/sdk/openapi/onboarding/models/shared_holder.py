from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SharedHolder")


@_attrs_define
class SharedHolder:
    """
    Attributes:
        id (str):
        member_key (str):
        submission_id (None | Unset | UUID):
        submission_ref (None | str | Unset):
    """

    id: str
    member_key: str
    submission_id: None | Unset | UUID = UNSET
    submission_ref: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        member_key = self.member_key

        submission_id: None | str | Unset
        if isinstance(self.submission_id, Unset):
            submission_id = UNSET
        elif isinstance(self.submission_id, UUID):
            submission_id = str(self.submission_id)
        else:
            submission_id = self.submission_id

        submission_ref: None | str | Unset
        if isinstance(self.submission_ref, Unset):
            submission_ref = UNSET
        else:
            submission_ref = self.submission_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "member_key": member_key,
            }
        )
        if submission_id is not UNSET:
            field_dict["submission_id"] = submission_id
        if submission_ref is not UNSET:
            field_dict["submission_ref"] = submission_ref

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        member_key = d.pop("member_key")

        def _parse_submission_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                submission_id_type_0 = UUID(data)

                return submission_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        submission_id = _parse_submission_id(d.pop("submission_id", UNSET))

        def _parse_submission_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        submission_ref = _parse_submission_ref(d.pop("submission_ref", UNSET))

        shared_holder = cls(
            id=id,
            member_key=member_key,
            submission_id=submission_id,
            submission_ref=submission_ref,
        )

        shared_holder.additional_properties = d
        return shared_holder

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
