from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.topology_node_schema import TopologyNodeSchema
    from ..models.user_community_detail_schema_areas_type_0 import UserCommunityDetailSchemaAreasType0
    from ..models.user_community_detail_schema_contact_type_0 import UserCommunityDetailSchemaContactType0
    from ..models.user_community_detail_schema_legal_type_0 import UserCommunityDetailSchemaLegalType0
    from ..models.user_community_detail_schema_links_type_0 import UserCommunityDetailSchemaLinksType0
    from ..models.user_community_detail_schema_settings_type_0 import UserCommunityDetailSchemaSettingsType0


T = TypeVar("T", bound="UserCommunityDetailSchema")


@_attrs_define
class UserCommunityDetailSchema:
    """
    Attributes:
        key (str):
        name (str):
        your_area (str):
        your_role (str):
        areas (None | Unset | UserCommunityDetailSchemaAreasType0):
        contact (None | Unset | UserCommunityDetailSchemaContactType0):
        description (None | str | Unset):
        legal (None | Unset | UserCommunityDetailSchemaLegalType0):
        links (None | Unset | UserCommunityDetailSchemaLinksType0):
        settings (None | Unset | UserCommunityDetailSchemaSettingsType0):
        topology (list[TopologyNodeSchema] | None | Unset):
    """

    key: str
    name: str
    your_area: str
    your_role: str
    areas: None | Unset | UserCommunityDetailSchemaAreasType0 = UNSET
    contact: None | Unset | UserCommunityDetailSchemaContactType0 = UNSET
    description: None | str | Unset = UNSET
    legal: None | Unset | UserCommunityDetailSchemaLegalType0 = UNSET
    links: None | Unset | UserCommunityDetailSchemaLinksType0 = UNSET
    settings: None | Unset | UserCommunityDetailSchemaSettingsType0 = UNSET
    topology: list[TopologyNodeSchema] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_community_detail_schema_areas_type_0 import UserCommunityDetailSchemaAreasType0
        from ..models.user_community_detail_schema_contact_type_0 import UserCommunityDetailSchemaContactType0
        from ..models.user_community_detail_schema_legal_type_0 import UserCommunityDetailSchemaLegalType0
        from ..models.user_community_detail_schema_links_type_0 import UserCommunityDetailSchemaLinksType0
        from ..models.user_community_detail_schema_settings_type_0 import UserCommunityDetailSchemaSettingsType0

        key = self.key

        name = self.name

        your_area = self.your_area

        your_role = self.your_role

        areas: dict[str, Any] | None | Unset
        if isinstance(self.areas, Unset):
            areas = UNSET
        elif isinstance(self.areas, UserCommunityDetailSchemaAreasType0):
            areas = self.areas.to_dict()
        else:
            areas = self.areas

        contact: dict[str, Any] | None | Unset
        if isinstance(self.contact, Unset):
            contact = UNSET
        elif isinstance(self.contact, UserCommunityDetailSchemaContactType0):
            contact = self.contact.to_dict()
        else:
            contact = self.contact

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        legal: dict[str, Any] | None | Unset
        if isinstance(self.legal, Unset):
            legal = UNSET
        elif isinstance(self.legal, UserCommunityDetailSchemaLegalType0):
            legal = self.legal.to_dict()
        else:
            legal = self.legal

        links: dict[str, Any] | None | Unset
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, UserCommunityDetailSchemaLinksType0):
            links = self.links.to_dict()
        else:
            links = self.links

        settings: dict[str, Any] | None | Unset
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, UserCommunityDetailSchemaSettingsType0):
            settings = self.settings.to_dict()
        else:
            settings = self.settings

        topology: list[dict[str, Any]] | None | Unset
        if isinstance(self.topology, Unset):
            topology = UNSET
        elif isinstance(self.topology, list):
            topology = []
            for topology_type_0_item_data in self.topology:
                topology_type_0_item = topology_type_0_item_data.to_dict()
                topology.append(topology_type_0_item)

        else:
            topology = self.topology

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
        from ..models.topology_node_schema import TopologyNodeSchema
        from ..models.user_community_detail_schema_areas_type_0 import UserCommunityDetailSchemaAreasType0
        from ..models.user_community_detail_schema_contact_type_0 import UserCommunityDetailSchemaContactType0
        from ..models.user_community_detail_schema_legal_type_0 import UserCommunityDetailSchemaLegalType0
        from ..models.user_community_detail_schema_links_type_0 import UserCommunityDetailSchemaLinksType0
        from ..models.user_community_detail_schema_settings_type_0 import UserCommunityDetailSchemaSettingsType0

        d = dict(src_dict)
        key = d.pop("key")

        name = d.pop("name")

        your_area = d.pop("your_area")

        your_role = d.pop("your_role")

        def _parse_areas(data: object) -> None | Unset | UserCommunityDetailSchemaAreasType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                areas_type_0 = UserCommunityDetailSchemaAreasType0.from_dict(data)

                return areas_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserCommunityDetailSchemaAreasType0, data)

        areas = _parse_areas(d.pop("areas", UNSET))

        def _parse_contact(data: object) -> None | Unset | UserCommunityDetailSchemaContactType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                contact_type_0 = UserCommunityDetailSchemaContactType0.from_dict(data)

                return contact_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserCommunityDetailSchemaContactType0, data)

        contact = _parse_contact(d.pop("contact", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_legal(data: object) -> None | Unset | UserCommunityDetailSchemaLegalType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                legal_type_0 = UserCommunityDetailSchemaLegalType0.from_dict(data)

                return legal_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserCommunityDetailSchemaLegalType0, data)

        legal = _parse_legal(d.pop("legal", UNSET))

        def _parse_links(data: object) -> None | Unset | UserCommunityDetailSchemaLinksType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = UserCommunityDetailSchemaLinksType0.from_dict(data)

                return links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserCommunityDetailSchemaLinksType0, data)

        links = _parse_links(d.pop("links", UNSET))

        def _parse_settings(data: object) -> None | Unset | UserCommunityDetailSchemaSettingsType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = UserCommunityDetailSchemaSettingsType0.from_dict(data)

                return settings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserCommunityDetailSchemaSettingsType0, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        def _parse_topology(data: object) -> list[TopologyNodeSchema] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                topology_type_0 = []
                _topology_type_0 = data
                for topology_type_0_item_data in _topology_type_0:
                    topology_type_0_item = TopologyNodeSchema.from_dict(topology_type_0_item_data)

                    topology_type_0.append(topology_type_0_item)

                return topology_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[TopologyNodeSchema] | None | Unset, data)

        topology = _parse_topology(d.pop("topology", UNSET))

        user_community_detail_schema = cls(
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

        user_community_detail_schema.additional_properties = d
        return user_community_detail_schema

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
