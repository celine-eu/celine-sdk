from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dataset_filter_request_access_level import DatasetFilterRequestAccessLevel

T = TypeVar("T", bound="DatasetFilterRequest")


@_attrs_define
class DatasetFilterRequest:
    """Request to get row-level filters for a dataset.

    Attributes:
        access_level (DatasetFilterRequestAccessLevel): Dataset access level
        dataset_id (str): Dataset identifier
    """

    access_level: DatasetFilterRequestAccessLevel
    dataset_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_level = self.access_level.value

        dataset_id = self.dataset_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_level": access_level,
                "dataset_id": dataset_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_level = DatasetFilterRequestAccessLevel(d.pop("access_level"))

        dataset_id = d.pop("dataset_id")

        dataset_filter_request = cls(
            access_level=access_level,
            dataset_id=dataset_id,
        )

        dataset_filter_request.additional_properties = d
        return dataset_filter_request

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
