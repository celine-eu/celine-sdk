from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.topology_node import TopologyNode
    from ..models.user_community_detail_areas import UserCommunityDetailAreas
    from ..models.user_community_detail_contact import UserCommunityDetailContact
    from ..models.user_community_detail_legal import UserCommunityDetailLegal
    from ..models.user_community_detail_links import UserCommunityDetailLinks
    from ..models.user_community_detail_settings import UserCommunityDetailSettings


T = TypeVar("T", bound="UserCommunityDetail")


@_attrs_define
class UserCommunityDetail:
    """
    Attributes:
        key (str):
        name (str):
        your_area (str):
        your_role (str):
        areas (UserCommunityDetailAreas | Unset):
        contact (UserCommunityDetailContact | Unset):
        description (None | str | Unset):
        legal (UserCommunityDetailLegal | Unset):
        links (UserCommunityDetailLinks | Unset):
        settings (UserCommunityDetailSettings | Unset):
        topology (list[TopologyNode] | Unset):
    """

    key: str
    name: str
    your_area: str
    your_role: str
    areas: UserCommunityDetailAreas | Unset = UNSET
    contact: UserCommunityDetailContact | Unset = UNSET
    description: None | str | Unset = UNSET
    legal: UserCommunityDetailLegal | Unset = UNSET
    links: UserCommunityDetailLinks | Unset = UNSET
    settings: UserCommunityDetailSettings | Unset = UNSET
    topology: list[TopologyNode] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        name = self.name

        your_area = self.your_area

        your_role = self.your_role

        areas: dict[str, Any] | Unset = UNSET
        if not isinstance(self.areas, Unset):
            areas = self.areas.to_dict()

        contact: dict[str, Any] | Unset = UNSET
        if not isinstance(self.contact, Unset):
            contact = self.contact.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        legal: dict[str, Any] | Unset = UNSET
        if not isinstance(self.legal, Unset):
            legal = self.legal.to_dict()

        links: dict[str, Any] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        topology: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.topology, Unset):
            topology = []
            for topology_item_data in self.topology:
                topology_item = topology_item_data.to_dict()
                topology.append(topology_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "name": name,
                "your_area": your_area,
                "your_role": your_role,
            }
        )
        if areas is not UNSET:
            field_dict["areas"] = areas
        if contact is not UNSET:
            field_dict["contact"] = contact
        if description is not UNSET:
            field_dict["description"] = description
        if legal is not UNSET:
            field_dict["legal"] = legal
        if links is not UNSET:
            field_dict["links"] = links
        if settings is not UNSET:
            field_dict["settings"] = settings
        if topology is not UNSET:
            field_dict["topology"] = topology

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.topology_node import TopologyNode
        from ..models.user_community_detail_areas import UserCommunityDetailAreas
        from ..models.user_community_detail_contact import UserCommunityDetailContact
        from ..models.user_community_detail_legal import UserCommunityDetailLegal
        from ..models.user_community_detail_links import UserCommunityDetailLinks
        from ..models.user_community_detail_settings import UserCommunityDetailSettings

        d = dict(src_dict)
        key = d.pop("key")

        name = d.pop("name")

        your_area = d.pop("your_area")

        your_role = d.pop("your_role")

        _areas = d.pop("areas", UNSET)
        areas: UserCommunityDetailAreas | Unset
        if isinstance(_areas, Unset):
            areas = UNSET
        else:
            areas = UserCommunityDetailAreas.from_dict(_areas)

        _contact = d.pop("contact", UNSET)
        contact: UserCommunityDetailContact | Unset
        if isinstance(_contact, Unset):
            contact = UNSET
        else:
            contact = UserCommunityDetailContact.from_dict(_contact)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        _legal = d.pop("legal", UNSET)
        legal: UserCommunityDetailLegal | Unset
        if isinstance(_legal, Unset):
            legal = UNSET
        else:
            legal = UserCommunityDetailLegal.from_dict(_legal)

        _links = d.pop("links", UNSET)
        links: UserCommunityDetailLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = UserCommunityDetailLinks.from_dict(_links)

        _settings = d.pop("settings", UNSET)
        settings: UserCommunityDetailSettings | Unset
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = UserCommunityDetailSettings.from_dict(_settings)

        _topology = d.pop("topology", UNSET)
        topology: list[TopologyNode] | Unset = UNSET
        if _topology is not UNSET:
            topology = []
            for topology_item_data in _topology:
                topology_item = TopologyNode.from_dict(topology_item_data)

                topology.append(topology_item)

        user_community_detail = cls(
            key=key,
            name=name,
            your_area=your_area,
            your_role=your_role,
            areas=areas,
            contact=contact,
            description=description,
            legal=legal,
            links=links,
            settings=settings,
            topology=topology,
        )

        user_community_detail.additional_properties = d
        return user_community_detail

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
