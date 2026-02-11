from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_membership_schema import UserMembershipSchema
    from ..models.user_profile_schema import UserProfileSchema


T = TypeVar("T", bound="UserMeResponseSchema")


@_attrs_define
class UserMeResponseSchema:
    """
    Attributes:
        profile (UserProfileSchema):
        membership (None | Unset | UserMembershipSchema):
    """

    profile: UserProfileSchema
    membership: None | Unset | UserMembershipSchema = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_membership_schema import UserMembershipSchema

        profile = self.profile.to_dict()

        membership: dict[str, Any] | None | Unset
        if isinstance(self.membership, Unset):
            membership = UNSET
        elif isinstance(self.membership, UserMembershipSchema):
            membership = self.membership.to_dict()
        else:
            membership = self.membership

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile": profile,
            }
        )
        if membership is not UNSET:
            field_dict["membership"] = membership

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_membership_schema import UserMembershipSchema
        from ..models.user_profile_schema import UserProfileSchema

        d = dict(src_dict)
        profile = UserProfileSchema.from_dict(d.pop("profile"))

        def _parse_membership(data: object) -> None | Unset | UserMembershipSchema:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                membership_type_0 = UserMembershipSchema.from_dict(data)

                return membership_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserMembershipSchema, data)

        membership = _parse_membership(d.pop("membership", UNSET))

        user_me_response_schema = cls(
            profile=profile,
            membership=membership,
        )

        user_me_response_schema.additional_properties = d
        return user_me_response_schema

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
