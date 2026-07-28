from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.community_detail_areas import CommunityDetailAreas
    from ..models.community_detail_contact import CommunityDetailContact
    from ..models.community_detail_extra import CommunityDetailExtra
    from ..models.community_detail_legal import CommunityDetailLegal
    from ..models.community_detail_links import CommunityDetailLinks
    from ..models.community_detail_settings import CommunityDetailSettings
    from ..models.topology_node import TopologyNode


T = TypeVar("T", bound="CommunityDetail")


@_attrs_define
class CommunityDetail:
    """
    Attributes:
        id (str):
        key (str):
        name (str):
        description (None | str | Unset):
        legal (CommunityDetailLegal | Unset):
        links (CommunityDetailLinks | Unset):
        contact (CommunityDetailContact | Unset):
        settings (CommunityDetailSettings | Unset):
        areas (CommunityDetailAreas | Unset):
        topology (list[TopologyNode] | Unset):
        extra (CommunityDetailExtra | Unset):
        created_at (None | str | Unset):
        updated_at (None | str | Unset):
    """

    id: str
    key: str
    name: str
    description: None | str | Unset = UNSET
    legal: CommunityDetailLegal | Unset = UNSET
    links: CommunityDetailLinks | Unset = UNSET
    contact: CommunityDetailContact | Unset = UNSET
    settings: CommunityDetailSettings | Unset = UNSET
    areas: CommunityDetailAreas | Unset = UNSET
    topology: list[TopologyNode] | Unset = UNSET
    extra: CommunityDetailExtra | Unset = UNSET
    created_at: None | str | Unset = UNSET
    updated_at: None | str | Unset = UNSET
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

        legal: dict[str, Any] | Unset = UNSET
        if not isinstance(self.legal, Unset):
            legal = self.legal.to_dict()

        links: dict[str, Any] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = self.links.to_dict()

        contact: dict[str, Any] | Unset = UNSET
        if not isinstance(self.contact, Unset):
            contact = self.contact.to_dict()

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        areas: dict[str, Any] | Unset = UNSET
        if not isinstance(self.areas, Unset):
            areas = self.areas.to_dict()

        topology: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.topology, Unset):
            topology = []
            for topology_item_data in self.topology:
                topology_item = topology_item_data.to_dict()
                topology.append(topology_item)

        extra: dict[str, Any] | Unset = UNSET
        if not isinstance(self.extra, Unset):
            extra = self.extra.to_dict()

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

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
        if legal is not UNSET:
            field_dict["legal"] = legal
        if links is not UNSET:
            field_dict["links"] = links
        if contact is not UNSET:
            field_dict["contact"] = contact
        if settings is not UNSET:
            field_dict["settings"] = settings
        if areas is not UNSET:
            field_dict["areas"] = areas
        if topology is not UNSET:
            field_dict["topology"] = topology
        if extra is not UNSET:
            field_dict["extra"] = extra
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.community_detail_areas import CommunityDetailAreas
        from ..models.community_detail_contact import CommunityDetailContact
        from ..models.community_detail_extra import CommunityDetailExtra
        from ..models.community_detail_legal import CommunityDetailLegal
        from ..models.community_detail_links import CommunityDetailLinks
        from ..models.community_detail_settings import CommunityDetailSettings
        from ..models.topology_node import TopologyNode

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

        _legal = d.pop("legal", UNSET)
        legal: CommunityDetailLegal | Unset
        if isinstance(_legal, Unset):
            legal = UNSET
        else:
            legal = CommunityDetailLegal.from_dict(_legal)

        _links = d.pop("links", UNSET)
        links: CommunityDetailLinks | Unset
        if isinstance(_links, Unset):
            links = UNSET
        else:
            links = CommunityDetailLinks.from_dict(_links)

        _contact = d.pop("contact", UNSET)
        contact: CommunityDetailContact | Unset
        if isinstance(_contact, Unset):
            contact = UNSET
        else:
            contact = CommunityDetailContact.from_dict(_contact)

        _settings = d.pop("settings", UNSET)
        settings: CommunityDetailSettings | Unset
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = CommunityDetailSettings.from_dict(_settings)

        _areas = d.pop("areas", UNSET)
        areas: CommunityDetailAreas | Unset
        if isinstance(_areas, Unset):
            areas = UNSET
        else:
            areas = CommunityDetailAreas.from_dict(_areas)

        _topology = d.pop("topology", UNSET)
        topology: list[TopologyNode] | Unset = UNSET
        if _topology is not UNSET:
            topology = []
            for topology_item_data in _topology:
                topology_item = TopologyNode.from_dict(topology_item_data)

                topology.append(topology_item)

        _extra = d.pop("extra", UNSET)
        extra: CommunityDetailExtra | Unset
        if isinstance(_extra, Unset):
            extra = UNSET
        else:
            extra = CommunityDetailExtra.from_dict(_extra)

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        community_detail = cls(
            id=id,
            key=key,
            name=name,
            description=description,
            legal=legal,
            links=links,
            contact=contact,
            settings=settings,
            areas=areas,
            topology=topology,
            extra=extra,
            created_at=created_at,
            updated_at=updated_at,
        )

        community_detail.additional_properties = d
        return community_detail

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
