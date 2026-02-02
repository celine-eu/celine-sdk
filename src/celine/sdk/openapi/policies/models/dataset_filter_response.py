from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_predicate import FilterPredicate


T = TypeVar("T", bound="DatasetFilterResponse")


@_attrs_define
class DatasetFilterResponse:
    """Response with row-level filters.

    Attributes:
        allowed (bool):
        request_id (str):
        filters (list[FilterPredicate] | Unset): Filters to apply to queries
        reason (str | Unset):  Default: ''.
    """

    allowed: bool
    request_id: str
    filters: list[FilterPredicate] | Unset = UNSET
    reason: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed = self.allowed

        request_id = self.request_id

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allowed": allowed,
                "request_id": request_id,
            }
        )
        if filters is not UNSET:
            field_dict["filters"] = filters
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_predicate import FilterPredicate

        d = dict(src_dict)
        allowed = d.pop("allowed")

        request_id = d.pop("request_id")

        _filters = d.pop("filters", UNSET)
        filters: list[FilterPredicate] | Unset = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:
                filters_item = FilterPredicate.from_dict(filters_item_data)

                filters.append(filters_item)

        reason = d.pop("reason", UNSET)

        dataset_filter_response = cls(
            allowed=allowed,
            request_id=request_id,
            filters=filters,
            reason=reason,
        )

        dataset_filter_response.additional_properties = d
        return dataset_filter_response

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
