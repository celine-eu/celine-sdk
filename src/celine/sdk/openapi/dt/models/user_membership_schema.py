from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_community_summary_schema import UserCommunitySummarySchema
    from ..models.user_member_summary_schema import UserMemberSummarySchema
    from ..models.user_membership_schema_assets_count_type_0 import UserMembershipSchemaAssetsCountType0


T = TypeVar("T", bound="UserMembershipSchema")


@_attrs_define
class UserMembershipSchema:
    """
    Attributes:
        community (UserCommunitySummarySchema):
        member (UserMemberSummarySchema):
        assets_count (None | Unset | UserMembershipSchemaAssetsCountType0):
        delivery_points_count (int | None | Unset):  Default: 0.
    """

    community: UserCommunitySummarySchema
    member: UserMemberSummarySchema
    assets_count: None | Unset | UserMembershipSchemaAssetsCountType0 = UNSET
    delivery_points_count: int | None | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_membership_schema_assets_count_type_0 import UserMembershipSchemaAssetsCountType0

        community = self.community.to_dict()

        member = self.member.to_dict()

        assets_count: dict[str, Any] | None | Unset
        if isinstance(self.assets_count, Unset):
            assets_count = UNSET
        elif isinstance(self.assets_count, UserMembershipSchemaAssetsCountType0):
            assets_count = self.assets_count.to_dict()
        else:
            assets_count = self.assets_count

        delivery_points_count: int | None | Unset
        if isinstance(self.delivery_points_count, Unset):
            delivery_points_count = UNSET
        else:
            delivery_points_count = self.delivery_points_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community": community,
                "member": member,
            }
        )
        if assets_count is not UNSET:
            field_dict["assets_count"] = assets_count
        if delivery_points_count is not UNSET:
            field_dict["delivery_points_count"] = delivery_points_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_community_summary_schema import UserCommunitySummarySchema
        from ..models.user_member_summary_schema import UserMemberSummarySchema
        from ..models.user_membership_schema_assets_count_type_0 import UserMembershipSchemaAssetsCountType0

        d = dict(src_dict)
        community = UserCommunitySummarySchema.from_dict(d.pop("community"))

        member = UserMemberSummarySchema.from_dict(d.pop("member"))

        def _parse_assets_count(data: object) -> None | Unset | UserMembershipSchemaAssetsCountType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                assets_count_type_0 = UserMembershipSchemaAssetsCountType0.from_dict(data)

                return assets_count_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserMembershipSchemaAssetsCountType0, data)

        assets_count = _parse_assets_count(d.pop("assets_count", UNSET))

        def _parse_delivery_points_count(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        delivery_points_count = _parse_delivery_points_count(d.pop("delivery_points_count", UNSET))

        user_membership_schema = cls(
            community=community,
            member=member,
            assets_count=assets_count,
            delivery_points_count=delivery_points_count,
        )

        user_membership_schema.additional_properties = d
        return user_membership_schema

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
