from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.contact_point import ContactPoint
    from ..models.temporal_coverage import TemporalCoverage


T = TypeVar("T", bound="Tags")


@_attrs_define
class Tags:
    """
    Attributes:
        access_rights (None | str | Unset):
        accrual_periodicity (None | str | Unset):
        conforms_to (None | str | Unset):
        contact_point (ContactPoint | None | Unset):
        identifier (None | str | Unset):
        keywords (list[str] | None | Unset):
        temporal (None | TemporalCoverage | Unset):
        themes (list[str] | None | Unset):
    """

    access_rights: None | str | Unset = UNSET
    accrual_periodicity: None | str | Unset = UNSET
    conforms_to: None | str | Unset = UNSET
    contact_point: ContactPoint | None | Unset = UNSET
    identifier: None | str | Unset = UNSET
    keywords: list[str] | None | Unset = UNSET
    temporal: None | TemporalCoverage | Unset = UNSET
    themes: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.contact_point import ContactPoint
        from ..models.temporal_coverage import TemporalCoverage

        access_rights: None | str | Unset
        if isinstance(self.access_rights, Unset):
            access_rights = UNSET
        else:
            access_rights = self.access_rights

        accrual_periodicity: None | str | Unset
        if isinstance(self.accrual_periodicity, Unset):
            accrual_periodicity = UNSET
        else:
            accrual_periodicity = self.accrual_periodicity

        conforms_to: None | str | Unset
        if isinstance(self.conforms_to, Unset):
            conforms_to = UNSET
        else:
            conforms_to = self.conforms_to

        contact_point: dict[str, Any] | None | Unset
        if isinstance(self.contact_point, Unset):
            contact_point = UNSET
        elif isinstance(self.contact_point, ContactPoint):
            contact_point = self.contact_point.to_dict()
        else:
            contact_point = self.contact_point

        identifier: None | str | Unset
        if isinstance(self.identifier, Unset):
            identifier = UNSET
        else:
            identifier = self.identifier

        keywords: list[str] | None | Unset
        if isinstance(self.keywords, Unset):
            keywords = UNSET
        elif isinstance(self.keywords, list):
            keywords = self.keywords

        else:
            keywords = self.keywords

        temporal: dict[str, Any] | None | Unset
        if isinstance(self.temporal, Unset):
            temporal = UNSET
        elif isinstance(self.temporal, TemporalCoverage):
            temporal = self.temporal.to_dict()
        else:
            temporal = self.temporal

        themes: list[str] | None | Unset
        if isinstance(self.themes, Unset):
            themes = UNSET
        elif isinstance(self.themes, list):
            themes = self.themes

        else:
            themes = self.themes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if access_rights is not UNSET:
            field_dict["accessRights"] = access_rights
        if accrual_periodicity is not UNSET:
            field_dict["accrualPeriodicity"] = accrual_periodicity
        if conforms_to is not UNSET:
            field_dict["conformsTo"] = conforms_to
        if contact_point is not UNSET:
            field_dict["contactPoint"] = contact_point
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if keywords is not UNSET:
            field_dict["keywords"] = keywords
        if temporal is not UNSET:
            field_dict["temporal"] = temporal
        if themes is not UNSET:
            field_dict["themes"] = themes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.contact_point import ContactPoint
        from ..models.temporal_coverage import TemporalCoverage

        d = dict(src_dict)

        def _parse_access_rights(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        access_rights = _parse_access_rights(d.pop("accessRights", UNSET))

        def _parse_accrual_periodicity(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        accrual_periodicity = _parse_accrual_periodicity(d.pop("accrualPeriodicity", UNSET))

        def _parse_conforms_to(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        conforms_to = _parse_conforms_to(d.pop("conformsTo", UNSET))

        def _parse_contact_point(data: object) -> ContactPoint | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                contact_point_type_0 = ContactPoint.from_dict(data)

                return contact_point_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContactPoint | None | Unset, data)

        contact_point = _parse_contact_point(d.pop("contactPoint", UNSET))

        def _parse_identifier(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        identifier = _parse_identifier(d.pop("identifier", UNSET))

        def _parse_keywords(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                keywords_type_0 = cast(list[str], data)

                return keywords_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        keywords = _parse_keywords(d.pop("keywords", UNSET))

        def _parse_temporal(data: object) -> None | TemporalCoverage | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                temporal_type_0 = TemporalCoverage.from_dict(data)

                return temporal_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TemporalCoverage | Unset, data)

        temporal = _parse_temporal(d.pop("temporal", UNSET))

        def _parse_themes(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                themes_type_0 = cast(list[str], data)

                return themes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        themes = _parse_themes(d.pop("themes", UNSET))

        tags = cls(
            access_rights=access_rights,
            accrual_periodicity=accrual_periodicity,
            conforms_to=conforms_to,
            contact_point=contact_point,
            identifier=identifier,
            keywords=keywords,
            temporal=temporal,
            themes=themes,
        )

        tags.additional_properties = d
        return tags

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
