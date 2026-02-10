from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delivery_point import DeliveryPoint
    from ..models.member_ref import MemberRef


T = TypeVar("T", bound="DeliveryPointLookup")


@_attrs_define
class DeliveryPointLookup:
    """
    Attributes:
        delivery_point (DeliveryPoint):
        member (MemberRef):
    """

    delivery_point: DeliveryPoint
    member: MemberRef
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        delivery_point = self.delivery_point.to_dict()

        member = self.member.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "delivery_point": delivery_point,
                "member": member,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delivery_point import DeliveryPoint
        from ..models.member_ref import MemberRef

        d = dict(src_dict)
        delivery_point = DeliveryPoint.from_dict(d.pop("delivery_point"))

        member = MemberRef.from_dict(d.pop("member"))

        delivery_point_lookup = cls(
            delivery_point=delivery_point,
            member=member,
        )

        delivery_point_lookup.additional_properties = d
        return delivery_point_lookup

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
