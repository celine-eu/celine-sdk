from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LinksIn")


@_attrs_define
class LinksIn:
    """Public URLs for the community.

    Attributes:
        website (None | str | Unset):
        logo (None | str | Unset):
        privacy_policy (None | str | Unset):
        terms (None | str | Unset):
        statute (None | str | Unset):
        regulations (None | str | Unset):
    """

    website: None | str | Unset = UNSET
    logo: None | str | Unset = UNSET
    privacy_policy: None | str | Unset = UNSET
    terms: None | str | Unset = UNSET
    statute: None | str | Unset = UNSET
    regulations: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        website: None | str | Unset
        if isinstance(self.website, Unset):
            website = UNSET
        else:
            website = self.website

        logo: None | str | Unset
        if isinstance(self.logo, Unset):
            logo = UNSET
        else:
            logo = self.logo

        privacy_policy: None | str | Unset
        if isinstance(self.privacy_policy, Unset):
            privacy_policy = UNSET
        else:
            privacy_policy = self.privacy_policy

        terms: None | str | Unset
        if isinstance(self.terms, Unset):
            terms = UNSET
        else:
            terms = self.terms

        statute: None | str | Unset
        if isinstance(self.statute, Unset):
            statute = UNSET
        else:
            statute = self.statute

        regulations: None | str | Unset
        if isinstance(self.regulations, Unset):
            regulations = UNSET
        else:
            regulations = self.regulations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if website is not UNSET:
            field_dict["website"] = website
        if logo is not UNSET:
            field_dict["logo"] = logo
        if privacy_policy is not UNSET:
            field_dict["privacy_policy"] = privacy_policy
        if terms is not UNSET:
            field_dict["terms"] = terms
        if statute is not UNSET:
            field_dict["statute"] = statute
        if regulations is not UNSET:
            field_dict["regulations"] = regulations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_website(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        website = _parse_website(d.pop("website", UNSET))

        def _parse_logo(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        logo = _parse_logo(d.pop("logo", UNSET))

        def _parse_privacy_policy(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        privacy_policy = _parse_privacy_policy(d.pop("privacy_policy", UNSET))

        def _parse_terms(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        terms = _parse_terms(d.pop("terms", UNSET))

        def _parse_statute(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        statute = _parse_statute(d.pop("statute", UNSET))

        def _parse_regulations(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        regulations = _parse_regulations(d.pop("regulations", UNSET))

        links_in = cls(
            website=website,
            logo=logo,
            privacy_policy=privacy_policy,
            terms=terms,
            statute=statute,
            regulations=regulations,
        )

        links_in.additional_properties = d
        return links_in

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
