from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrainingMaterialsSyncRequest")


@_attrs_define
class TrainingMaterialsSyncRequest:
    """
    Attributes:
        target_ref (None | str | Unset): Git commit SHA, tag, or ref to sync
    """

    target_ref: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target_ref: None | str | Unset
        if isinstance(self.target_ref, Unset):
            target_ref = UNSET
        else:
            target_ref = self.target_ref

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if target_ref is not UNSET:
            field_dict["target_ref"] = target_ref

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_target_ref(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        target_ref = _parse_target_ref(d.pop("target_ref", UNSET))

        training_materials_sync_request = cls(
            target_ref=target_ref,
        )

        training_materials_sync_request.additional_properties = d
        return training_materials_sync_request

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
