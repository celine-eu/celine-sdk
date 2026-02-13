from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.fetch_result_schema_items_item import FetchResultSchemaItemsItem


T = TypeVar("T", bound="FetchResultSchema")


@_attrs_define
class FetchResultSchema:
    """Result of a value fetch operation.

    Attributes:
        count (int):
        items (list[FetchResultSchemaItemsItem]):
        limit (int):
        offset (int):
    """

    count: int
    items: list[FetchResultSchemaItemsItem]
    limit: int
    offset: int

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        limit = self.limit

        offset = self.offset

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "count": count,
                "items": items,
                "limit": limit,
                "offset": offset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fetch_result_schema_items_item import FetchResultSchemaItemsItem

        d = dict(src_dict)
        count = d.pop("count")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = FetchResultSchemaItemsItem.from_dict(items_item_data)

            items.append(items_item)

        limit = d.pop("limit")

        offset = d.pop("offset")

        fetch_result_schema = cls(
            count=count,
            items=items,
            limit=limit,
            offset=offset,
        )

        return fetch_result_schema
