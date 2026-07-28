from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.community_ref import CommunityRef
    from ..models.delivery_point import DeliveryPoint
    from ..models.member_ref import MemberRef


T = TypeVar("T", bound="LookupByDeliveryPointResponse")


@_attrs_define
class LookupByDeliveryPointResponse:
    """
    Attributes:
        community (CommunityRef):
        member (MemberRef):
        delivery_point (DeliveryPoint):
    """

    community: CommunityRef
    member: MemberRef
    delivery_point: DeliveryPoint
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community = self.community.to_dict()

        member = self.member.to_dict()

        delivery_point = self.delivery_point.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community": community,
                "member": member,
                "delivery_point": delivery_point,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.community_ref import CommunityRef
        from ..models.delivery_point import DeliveryPoint
        from ..models.member_ref import MemberRef

        d = dict(src_dict)
        community = CommunityRef.from_dict(d.pop("community"))

        member = MemberRef.from_dict(d.pop("member"))

        delivery_point = DeliveryPoint.from_dict(d.pop("delivery_point"))

        lookup_by_delivery_point_response = cls(
            community=community,
            member=member,
            delivery_point=delivery_point,
        )

        lookup_by_delivery_point_response.additional_properties = d
        return lookup_by_delivery_point_response

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
