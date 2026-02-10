from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.asset_ref import AssetRef
    from ..models.community_ref import CommunityRef
    from ..models.member_in_community import MemberInCommunity


T = TypeVar("T", bound="LookupBySensorIdResponse")


@_attrs_define
class LookupBySensorIdResponse:
    """
    Attributes:
        asset (AssetRef):
        community (CommunityRef):
        member (MemberInCommunity):
    """

    asset: AssetRef
    community: CommunityRef
    member: MemberInCommunity
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        asset = self.asset.to_dict()

        community = self.community.to_dict()

        member = self.member.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "asset": asset,
                "community": community,
                "member": member,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_ref import AssetRef
        from ..models.community_ref import CommunityRef
        from ..models.member_in_community import MemberInCommunity

        d = dict(src_dict)
        asset = AssetRef.from_dict(d.pop("asset"))

        community = CommunityRef.from_dict(d.pop("community"))

        member = MemberInCommunity.from_dict(d.pop("member"))

        lookup_by_sensor_id_response = cls(
            asset=asset,
            community=community,
            member=member,
        )

        lookup_by_sensor_id_response.additional_properties = d
        return lookup_by_sensor_id_response

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
