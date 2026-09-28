from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncItem")


@_attrs_define
class SyncItem:
    """One area or topology node, and what the sync did or would do to it.

    ``outcome`` is ``created``, ``changed``, ``unchanged``, ``refused``,
    ``deleted``, ``undeclared`` (a registry area the template no longer
    declares, left in place without ``prune``), ``renamed`` (a registry area
    moved to this key from ``renamed_from``, with its members) or ``not_run``.
    In a dry run it is what a real run would do.

        Attributes:
            key (str):
            outcome (str):
            boundary_id (None | str | Unset):
            code (None | str | Unset):
            members (int | None | Unset):
            reason (None | str | Unset):
            renamed_from (None | str | Unset):
    """

    key: str
    outcome: str
    boundary_id: None | str | Unset = UNSET
    code: None | str | Unset = UNSET
    members: int | None | Unset = UNSET
    reason: None | str | Unset = UNSET
    renamed_from: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        outcome = self.outcome

        boundary_id: None | str | Unset
        if isinstance(self.boundary_id, Unset):
            boundary_id = UNSET
        else:
            boundary_id = self.boundary_id

        code: None | str | Unset
        if isinstance(self.code, Unset):
            code = UNSET
        else:
            code = self.code

        members: int | None | Unset
        if isinstance(self.members, Unset):
            members = UNSET
        else:
            members = self.members

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        renamed_from: None | str | Unset
        if isinstance(self.renamed_from, Unset):
            renamed_from = UNSET
        else:
            renamed_from = self.renamed_from

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "outcome": outcome,
            }
        )
        if boundary_id is not UNSET:
            field_dict["boundary_id"] = boundary_id
        if code is not UNSET:
            field_dict["code"] = code
        if members is not UNSET:
            field_dict["members"] = members
        if reason is not UNSET:
            field_dict["reason"] = reason
        if renamed_from is not UNSET:
            field_dict["renamed_from"] = renamed_from

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        outcome = d.pop("outcome")

        def _parse_boundary_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        boundary_id = _parse_boundary_id(d.pop("boundary_id", UNSET))

        def _parse_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        code = _parse_code(d.pop("code", UNSET))

        def _parse_members(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        members = _parse_members(d.pop("members", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_renamed_from(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        renamed_from = _parse_renamed_from(d.pop("renamed_from", UNSET))

        sync_item = cls(
            key=key,
            outcome=outcome,
            boundary_id=boundary_id,
            code=code,
            members=members,
            reason=reason,
            renamed_from=renamed_from,
        )

        sync_item.additional_properties = d
        return sync_item

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
