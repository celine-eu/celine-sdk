from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.community_detail import CommunityDetail


T = TypeVar("T", bound="AreaRenamed")


@_attrs_define
class AreaRenamed:
    """What a rename did (REQ-0079): the two keys, how many members moved, and
    the whole community after it, so the caller can see the others are still
    there.

        Attributes:
            community (CommunityDetail):
            members_moved (int): Members of the community, of any status, moved to `new_key`.
            new_key (str):
            old_key (str):
    """

    community: CommunityDetail
    members_moved: int
    new_key: str
    old_key: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community = self.community.to_dict()

        members_moved = self.members_moved

        new_key = self.new_key

        old_key = self.old_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community": community,
                "members_moved": members_moved,
                "new_key": new_key,
                "old_key": old_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.community_detail import CommunityDetail

        d = dict(src_dict)
        community = CommunityDetail.from_dict(d.pop("community"))

        members_moved = d.pop("members_moved")

        new_key = d.pop("new_key")

        old_key = d.pop("old_key")

        area_renamed = cls(
            community=community,
            members_moved=members_moved,
            new_key=new_key,
            old_key=old_key,
        )

        area_renamed.additional_properties = d
        return area_renamed

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
