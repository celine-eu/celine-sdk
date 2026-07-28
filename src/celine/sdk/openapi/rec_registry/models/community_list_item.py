from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.community_list_item_areas import CommunityListItemAreas


T = TypeVar("T", bound="CommunityListItem")


@_attrs_define
class CommunityListItem:
    """
    Attributes:
        id (str):
        key (str):
        name (str):
        description (None | str | Unset):
        areas (CommunityListItemAreas | Unset):
    """

    id: str
    key: str
    name: str
    description: None | str | Unset = UNSET
    areas: CommunityListItemAreas | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        areas: dict[str, Any] | Unset = UNSET
        if not isinstance(self.areas, Unset):
            areas = self.areas.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key": key,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if areas is not UNSET:
            field_dict["areas"] = areas

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.community_list_item_areas import CommunityListItemAreas

        d = dict(src_dict)
        id = d.pop("id")

        key = d.pop("key")

        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _areas = d.pop("areas", UNSET)
        areas: CommunityListItemAreas | Unset
        if isinstance(_areas, Unset):
            areas = UNSET
        else:
            areas = CommunityListItemAreas.from_dict(_areas)

        community_list_item = cls(
            id=id,
            key=key,
            name=name,
            description=description,
            areas=areas,
        )

        community_list_item.additional_properties = d
        return community_list_item

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
