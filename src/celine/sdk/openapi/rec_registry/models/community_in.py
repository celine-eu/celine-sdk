from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.areas import Areas
    from ..models.contact_in import ContactIn
    from ..models.legal_info_in import LegalInfoIn
    from ..models.links_in import LinksIn
    from ..models.operators import Operators
    from ..models.settings_in import SettingsIn
    from ..models.topology_node_in import TopologyNodeIn


T = TypeVar("T", bound="CommunityIn")


@_attrs_define
class CommunityIn:
    """Community definition.

    Attributes:
        id (str):
        name (str):
        description (None | str | Unset):
        legal (LegalInfoIn | None | Unset):
        links (LinksIn | None | Unset):
        contact (ContactIn | None | Unset):
        settings (None | SettingsIn | Unset):
        operators (Operators | Unset):
        areas (Areas | Unset):
        topology (list[TopologyNodeIn] | Unset):
    """

    id: str
    name: str
    description: None | str | Unset = UNSET
    legal: LegalInfoIn | None | Unset = UNSET
    links: LinksIn | None | Unset = UNSET
    contact: ContactIn | None | Unset = UNSET
    settings: None | SettingsIn | Unset = UNSET
    operators: Operators | Unset = UNSET
    areas: Areas | Unset = UNSET
    topology: list[TopologyNodeIn] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.contact_in import ContactIn
        from ..models.legal_info_in import LegalInfoIn
        from ..models.links_in import LinksIn
        from ..models.settings_in import SettingsIn

        id = self.id

        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        legal: dict[str, Any] | None | Unset
        if isinstance(self.legal, Unset):
            legal = UNSET
        elif isinstance(self.legal, LegalInfoIn):
            legal = self.legal.to_dict()
        else:
            legal = self.legal

        links: dict[str, Any] | None | Unset
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, LinksIn):
            links = self.links.to_dict()
        else:
            links = self.links

        contact: dict[str, Any] | None | Unset
        if isinstance(self.contact, Unset):
            contact = UNSET
        elif isinstance(self.contact, ContactIn):
            contact = self.contact.to_dict()
        else:
            contact = self.contact

        settings: dict[str, Any] | None | Unset
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, SettingsIn):
            settings = self.settings.to_dict()
        else:
            settings = self.settings

        operators: dict[str, Any] | Unset = UNSET
        if not isinstance(self.operators, Unset):
            operators = self.operators.to_dict()

        areas: dict[str, Any] | Unset = UNSET
        if not isinstance(self.areas, Unset):
            areas = self.areas.to_dict()

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
                "id": id,
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
        if operators is not UNSET:
            field_dict["operators"] = operators
        if areas is not UNSET:
            field_dict["areas"] = areas
        if topology is not UNSET:
            field_dict["topology"] = topology

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.areas import Areas
        from ..models.contact_in import ContactIn
        from ..models.legal_info_in import LegalInfoIn
        from ..models.links_in import LinksIn
        from ..models.operators import Operators
        from ..models.settings_in import SettingsIn
        from ..models.topology_node_in import TopologyNodeIn

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_legal(data: object) -> LegalInfoIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                legal_type_0 = LegalInfoIn.from_dict(data)

                return legal_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LegalInfoIn | None | Unset, data)

        legal = _parse_legal(d.pop("legal", UNSET))

        def _parse_links(data: object) -> LinksIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = LinksIn.from_dict(data)

                return links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LinksIn | None | Unset, data)

        links = _parse_links(d.pop("links", UNSET))

        def _parse_contact(data: object) -> ContactIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                contact_type_0 = ContactIn.from_dict(data)

                return contact_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContactIn | None | Unset, data)

        contact = _parse_contact(d.pop("contact", UNSET))

        def _parse_settings(data: object) -> None | SettingsIn | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = SettingsIn.from_dict(data)

                return settings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SettingsIn | Unset, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        _operators = d.pop("operators", UNSET)
        operators: Operators | Unset
        if isinstance(_operators, Unset):
            operators = UNSET
        else:
            operators = Operators.from_dict(_operators)

        _areas = d.pop("areas", UNSET)
        areas: Areas | Unset
        if isinstance(_areas, Unset):
            areas = UNSET
        else:
            areas = Areas.from_dict(_areas)

        _topology = d.pop("topology", UNSET)
        topology: list[TopologyNodeIn] | Unset = UNSET
        if _topology is not UNSET:
            topology = []
            for topology_item_data in _topology:
                topology_item = TopologyNodeIn.from_dict(topology_item_data)

                topology.append(topology_item)

        community_in = cls(
            id=id,
            name=name,
            description=description,
            legal=legal,
            links=links,
            contact=contact,
            settings=settings,
            operators=operators,
            areas=areas,
            topology=topology,
        )

        community_in.additional_properties = d
        return community_in

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
