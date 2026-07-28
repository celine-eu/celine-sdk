from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.community_patch_contact_type_0 import CommunityPatchContactType0
    from ..models.community_patch_extra_type_0 import CommunityPatchExtraType0
    from ..models.community_patch_legal_type_0 import CommunityPatchLegalType0
    from ..models.community_patch_links_type_0 import CommunityPatchLinksType0
    from ..models.community_patch_settings_type_0 import CommunityPatchSettingsType0


T = TypeVar("T", bound="CommunityPatch")


@_attrs_define
class CommunityPatch:
    """Partial update of community metadata.

    Areas and topology are not here: they are collections with their own
    identity, and a patch omitting them must not read as "this community now
    has none".

        Attributes:
            name (None | str | Unset):
            description (None | str | Unset):
            legal (CommunityPatchLegalType0 | None | Unset):
            links (CommunityPatchLinksType0 | None | Unset):
            contact (CommunityPatchContactType0 | None | Unset):
            settings (CommunityPatchSettingsType0 | None | Unset):
            extra (CommunityPatchExtraType0 | None | Unset):
    """

    name: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    legal: CommunityPatchLegalType0 | None | Unset = UNSET
    links: CommunityPatchLinksType0 | None | Unset = UNSET
    contact: CommunityPatchContactType0 | None | Unset = UNSET
    settings: CommunityPatchSettingsType0 | None | Unset = UNSET
    extra: CommunityPatchExtraType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.community_patch_contact_type_0 import CommunityPatchContactType0
        from ..models.community_patch_extra_type_0 import CommunityPatchExtraType0
        from ..models.community_patch_legal_type_0 import CommunityPatchLegalType0
        from ..models.community_patch_links_type_0 import CommunityPatchLinksType0
        from ..models.community_patch_settings_type_0 import CommunityPatchSettingsType0

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        legal: dict[str, Any] | None | Unset
        if isinstance(self.legal, Unset):
            legal = UNSET
        elif isinstance(self.legal, CommunityPatchLegalType0):
            legal = self.legal.to_dict()
        else:
            legal = self.legal

        links: dict[str, Any] | None | Unset
        if isinstance(self.links, Unset):
            links = UNSET
        elif isinstance(self.links, CommunityPatchLinksType0):
            links = self.links.to_dict()
        else:
            links = self.links

        contact: dict[str, Any] | None | Unset
        if isinstance(self.contact, Unset):
            contact = UNSET
        elif isinstance(self.contact, CommunityPatchContactType0):
            contact = self.contact.to_dict()
        else:
            contact = self.contact

        settings: dict[str, Any] | None | Unset
        if isinstance(self.settings, Unset):
            settings = UNSET
        elif isinstance(self.settings, CommunityPatchSettingsType0):
            settings = self.settings.to_dict()
        else:
            settings = self.settings

        extra: dict[str, Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, CommunityPatchExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
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
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.community_patch_contact_type_0 import CommunityPatchContactType0
        from ..models.community_patch_extra_type_0 import CommunityPatchExtraType0
        from ..models.community_patch_legal_type_0 import CommunityPatchLegalType0
        from ..models.community_patch_links_type_0 import CommunityPatchLinksType0
        from ..models.community_patch_settings_type_0 import CommunityPatchSettingsType0

        d = dict(src_dict)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_legal(data: object) -> CommunityPatchLegalType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                legal_type_0 = CommunityPatchLegalType0.from_dict(data)

                return legal_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CommunityPatchLegalType0 | None | Unset, data)

        legal = _parse_legal(d.pop("legal", UNSET))

        def _parse_links(data: object) -> CommunityPatchLinksType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                links_type_0 = CommunityPatchLinksType0.from_dict(data)

                return links_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CommunityPatchLinksType0 | None | Unset, data)

        links = _parse_links(d.pop("links", UNSET))

        def _parse_contact(data: object) -> CommunityPatchContactType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                contact_type_0 = CommunityPatchContactType0.from_dict(data)

                return contact_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CommunityPatchContactType0 | None | Unset, data)

        contact = _parse_contact(d.pop("contact", UNSET))

        def _parse_settings(data: object) -> CommunityPatchSettingsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                settings_type_0 = CommunityPatchSettingsType0.from_dict(data)

                return settings_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CommunityPatchSettingsType0 | None | Unset, data)

        settings = _parse_settings(d.pop("settings", UNSET))

        def _parse_extra(data: object) -> CommunityPatchExtraType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = CommunityPatchExtraType0.from_dict(data)

                return extra_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CommunityPatchExtraType0 | None | Unset, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        community_patch = cls(
            name=name,
            description=description,
            legal=legal,
            links=links,
            contact=contact,
            settings=settings,
            extra=extra,
        )

        community_patch.additional_properties = d
        return community_patch

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
