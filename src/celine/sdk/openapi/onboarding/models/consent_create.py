from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ConsentCreate")


@_attrs_define
class ConsentCreate:
    """
    Attributes:
        gdpr_consent (bool):
        gdpr_consent_version (str):
        policy_consent (bool):
        policy_consent_version (str):
        statute_consent (bool):
        statute_consent_version (str):
    """

    gdpr_consent: bool
    gdpr_consent_version: str
    policy_consent: bool
    policy_consent_version: str
    statute_consent: bool
    statute_consent_version: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gdpr_consent = self.gdpr_consent

        gdpr_consent_version = self.gdpr_consent_version

        policy_consent = self.policy_consent

        policy_consent_version = self.policy_consent_version

        statute_consent = self.statute_consent

        statute_consent_version = self.statute_consent_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gdpr_consent": gdpr_consent,
                "gdpr_consent_version": gdpr_consent_version,
                "policy_consent": policy_consent,
                "policy_consent_version": policy_consent_version,
                "statute_consent": statute_consent,
                "statute_consent_version": statute_consent_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gdpr_consent = d.pop("gdpr_consent")

        gdpr_consent_version = d.pop("gdpr_consent_version")

        policy_consent = d.pop("policy_consent")

        policy_consent_version = d.pop("policy_consent_version")

        statute_consent = d.pop("statute_consent")

        statute_consent_version = d.pop("statute_consent_version")

        consent_create = cls(
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
