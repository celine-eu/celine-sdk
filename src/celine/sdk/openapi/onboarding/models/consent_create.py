from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConsentCreate")


@_attrs_define
class ConsentCreate:
    """
    Attributes:
        declared_existing_member (bool | Unset):  Default: False.
        gdpr_consent (bool | Unset):  Default: False.
        gdpr_consent_version (None | str | Unset):
        policy_consent (bool | Unset):  Default: False.
        policy_consent_version (None | str | Unset):
        statute_consent (bool | Unset):  Default: False.
        statute_consent_version (None | str | Unset):
    """

    declared_existing_member: bool | Unset = False
    gdpr_consent: bool | Unset = False
    gdpr_consent_version: None | str | Unset = UNSET
    policy_consent: bool | Unset = False
    policy_consent_version: None | str | Unset = UNSET
    statute_consent: bool | Unset = False
    statute_consent_version: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        declared_existing_member = self.declared_existing_member

        gdpr_consent = self.gdpr_consent

        gdpr_consent_version: None | str | Unset
        if isinstance(self.gdpr_consent_version, Unset):
            gdpr_consent_version = UNSET
        else:
            gdpr_consent_version = self.gdpr_consent_version

        policy_consent = self.policy_consent

        policy_consent_version: None | str | Unset
        if isinstance(self.policy_consent_version, Unset):
            policy_consent_version = UNSET
        else:
            policy_consent_version = self.policy_consent_version

        statute_consent = self.statute_consent

        statute_consent_version: None | str | Unset
        if isinstance(self.statute_consent_version, Unset):
            statute_consent_version = UNSET
        else:
            statute_consent_version = self.statute_consent_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if declared_existing_member is not UNSET:
            field_dict["declared_existing_member"] = declared_existing_member
        if gdpr_consent is not UNSET:
            field_dict["gdpr_consent"] = gdpr_consent
        if gdpr_consent_version is not UNSET:
            field_dict["gdpr_consent_version"] = gdpr_consent_version
        if policy_consent is not UNSET:
            field_dict["policy_consent"] = policy_consent
        if policy_consent_version is not UNSET:
            field_dict["policy_consent_version"] = policy_consent_version
        if statute_consent is not UNSET:
            field_dict["statute_consent"] = statute_consent
        if statute_consent_version is not UNSET:
            field_dict["statute_consent_version"] = statute_consent_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        declared_existing_member = d.pop("declared_existing_member", UNSET)

        gdpr_consent = d.pop("gdpr_consent", UNSET)

        def _parse_gdpr_consent_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        gdpr_consent_version = _parse_gdpr_consent_version(d.pop("gdpr_consent_version", UNSET))

        policy_consent = d.pop("policy_consent", UNSET)

        def _parse_policy_consent_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        policy_consent_version = _parse_policy_consent_version(d.pop("policy_consent_version", UNSET))

        statute_consent = d.pop("statute_consent", UNSET)

        def _parse_statute_consent_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        statute_consent_version = _parse_statute_consent_version(d.pop("statute_consent_version", UNSET))

        consent_create = cls(
            declared_existing_member=declared_existing_member,
            gdpr_consent=gdpr_consent,
            gdpr_consent_version=gdpr_consent_version,
            policy_consent=policy_consent,
            policy_consent_version=policy_consent_version,
            statute_consent=statute_consent,
            statute_consent_version=statute_consent_version,
        )

        consent_create.additional_properties = d
        return consent_create

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
