from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_community_summary import UserCommunitySummary
    from ..models.user_member_summary import UserMemberSummary
    from ..models.user_membership_assets_count import UserMembershipAssetsCount


T = TypeVar("T", bound="UserMembership")


@_attrs_define
class UserMembership:
    """
    Attributes:
        member (UserMemberSummary):
        community (UserCommunitySummary):
        delivery_points_count (int | Unset):  Default: 0.
        assets_count (UserMembershipAssetsCount | Unset):
    """

    member: UserMemberSummary
    community: UserCommunitySummary
    delivery_points_count: int | Unset = 0
    assets_count: UserMembershipAssetsCount | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        member = self.member.to_dict()

        community = self.community.to_dict()

        delivery_points_count = self.delivery_points_count

        assets_count: dict[str, Any] | Unset = UNSET
        if not isinstance(self.assets_count, Unset):
            assets_count = self.assets_count.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "member": member,
                "community": community,
            }
        )
        if delivery_points_count is not UNSET:
            field_dict["delivery_points_count"] = delivery_points_count
        if assets_count is not UNSET:
            field_dict["assets_count"] = assets_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_community_summary import UserCommunitySummary
        from ..models.user_member_summary import UserMemberSummary
        from ..models.user_membership_assets_count import UserMembershipAssetsCount

        d = dict(src_dict)
        member = UserMemberSummary.from_dict(d.pop("member"))

        community = UserCommunitySummary.from_dict(d.pop("community"))

        delivery_points_count = d.pop("delivery_points_count", UNSET)

        _assets_count = d.pop("assets_count", UNSET)
        assets_count: UserMembershipAssetsCount | Unset
        if isinstance(_assets_count, Unset):
            assets_count = UNSET
        else:
            assets_count = UserMembershipAssetsCount.from_dict(_assets_count)

        user_membership = cls(
            member=member,
            community=community,
            delivery_points_count=delivery_points_count,
            assets_count=assets_count,
        )

        user_membership.additional_properties = d
        return user_membership

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
