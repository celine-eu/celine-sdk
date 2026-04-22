from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetQueryModel")


@_attrs_define
class DatasetQueryModel:
    """
    Attributes:
        limit (int | Unset):  Default: 100.
        offset (int | Unset):  Default: 0.
        skip_count (bool | Unset):  Default: False.
        sql (None | str | Unset):
    """

    limit: int | Unset = 100
    offset: int | Unset = 0
    skip_count: bool | Unset = False
    sql: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        offset = self.offset

        skip_count = self.skip_count

        sql: None | str | Unset
        if isinstance(self.sql, Unset):
            sql = UNSET
        else:
            sql = self.sql

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if skip_count is not UNSET:
            field_dict["skip_count"] = skip_count
        if sql is not UNSET:
            field_dict["sql"] = sql

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        skip_count = d.pop("skip_count", UNSET)

        def _parse_sql(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sql = _parse_sql(d.pop("sql", UNSET))

        dataset_query_model = cls(
            limit=limit,
            offset=offset,
            skip_count=skip_count,
            sql=sql,
        )

        dataset_query_model.additional_properties = d
        return dataset_query_model

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
