from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dataset_access_request_access_level import DatasetAccessRequestAccessLevel
from ..models.dataset_access_request_action import DatasetAccessRequestAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetAccessRequest")


@_attrs_define
class DatasetAccessRequest:
    """Request to check dataset access.

    Attributes:
        access_level (DatasetAccessRequestAccessLevel): Dataset access level
        dataset_id (str): Dataset identifier
        action (DatasetAccessRequestAction | Unset): Action type Default: DatasetAccessRequestAction.READ.
    """

    access_level: DatasetAccessRequestAccessLevel
    dataset_id: str
    action: DatasetAccessRequestAction | Unset = DatasetAccessRequestAction.READ
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_level = self.access_level.value

        dataset_id = self.dataset_id

        action: str | Unset = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_level": access_level,
                "dataset_id": dataset_id,
            }
        )
        if action is not UNSET:
            field_dict["action"] = action

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        access_level = DatasetAccessRequestAccessLevel(d.pop("access_level"))

        dataset_id = d.pop("dataset_id")

        _action = d.pop("action", UNSET)
        action: DatasetAccessRequestAction | Unset
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = DatasetAccessRequestAction(_action)

        dataset_access_request = cls(
            access_level=access_level,
            dataset_id=dataset_id,
            action=action,
        )

        dataset_access_request.additional_properties = d
        return dataset_access_request

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
