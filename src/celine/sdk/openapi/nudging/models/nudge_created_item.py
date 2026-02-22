from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delivery_job_out import DeliveryJobOut


T = TypeVar("T", bound="NudgeCreatedItem")


@_attrs_define
class NudgeCreatedItem:
    """
    Attributes:
        deliveries (list[DeliveryJobOut]):
        nudge_id (str):
        rule_id (str):
    """

    deliveries: list[DeliveryJobOut]
    nudge_id: str
    rule_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        deliveries = []
        for deliveries_item_data in self.deliveries:
            deliveries_item = deliveries_item_data.to_dict()
            deliveries.append(deliveries_item)

        nudge_id = self.nudge_id

        rule_id = self.rule_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deliveries": deliveries,
                "nudge_id": nudge_id,
                "rule_id": rule_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delivery_job_out import DeliveryJobOut

        d = dict(src_dict)
        deliveries = []
        _deliveries = d.pop("deliveries")
        for deliveries_item_data in _deliveries:
            deliveries_item = DeliveryJobOut.from_dict(deliveries_item_data)

            deliveries.append(deliveries_item)

        nudge_id = d.pop("nudge_id")

        rule_id = d.pop("rule_id")

        nudge_created_item = cls(
            deliveries=deliveries,
            nudge_id=nudge_id,
            rule_id=rule_id,
        )

        nudge_created_item.additional_properties = d
        return nudge_created_item

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
