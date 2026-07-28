from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DeletionReport")


@_attrs_define
class DeletionReport:
    """What a delete did.

    `purged` distinguishes deactivation from erasure — the same endpoint does
    both, and the caller should be able to tell which happened.

        Attributes:
            community_key (str):
            member_key (str):
            purged (bool):
            status (None | str | Unset):
            assets_removed (int | Unset):  Default: 0.
    """

    community_key: str
    member_key: str
    purged: bool
    status: None | str | Unset = UNSET
    assets_removed: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community_key = self.community_key

        member_key = self.member_key

        purged = self.purged

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        assets_removed = self.assets_removed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community_key": community_key,
                "member_key": member_key,
                "purged": purged,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if assets_removed is not UNSET:
            field_dict["assets_removed"] = assets_removed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        community_key = d.pop("community_key")

        member_key = d.pop("member_key")

        purged = d.pop("purged")

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        assets_removed = d.pop("assets_removed", UNSET)

        deletion_report = cls(
            community_key=community_key,
            member_key=member_key,
            purged=purged,
            status=status,
            assets_removed=assets_removed,
        )

        deletion_report.additional_properties = d
        return deletion_report

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
