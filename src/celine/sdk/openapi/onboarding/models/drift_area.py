from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DriftArea")


@_attrs_define
class DriftArea:
    """
    Attributes:
        key (str):
        state (str):
        boundary_id (None | str | Unset):
        held_by (list[str] | Unset):
    """

    key: str
    state: str
    boundary_id: None | str | Unset = UNSET
    held_by: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        state = self.state

        boundary_id: None | str | Unset
        if isinstance(self.boundary_id, Unset):
            boundary_id = UNSET
        else:
            boundary_id = self.boundary_id

        held_by: list[str] | Unset = UNSET
        if not isinstance(self.held_by, Unset):
            held_by = self.held_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "state": state,
            }
        )
        if boundary_id is not UNSET:
            field_dict["boundary_id"] = boundary_id
        if held_by is not UNSET:
            field_dict["held_by"] = held_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        state = d.pop("state")

        def _parse_boundary_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        boundary_id = _parse_boundary_id(d.pop("boundary_id", UNSET))

        held_by = cast(list[str], d.pop("held_by", UNSET))

        drift_area = cls(
            key=key,
            state=state,
            boundary_id=boundary_id,
            held_by=held_by,
        )

        drift_area.additional_properties = d
        return drift_area

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
