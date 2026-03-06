from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SeedApplyResponse")


@_attrs_define
class SeedApplyResponse:
    """
    Attributes:
        overrides (int):
        preferences (int):
        rules (int):
        templates (int):
        status (str | Unset):  Default: 'ok'.
    """

    overrides: int
    preferences: int
    rules: int
    templates: int
    status: str | Unset = "ok"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        overrides = self.overrides

        preferences = self.preferences

        rules = self.rules

        templates = self.templates

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "overrides": overrides,
                "preferences": preferences,
                "rules": rules,
                "templates": templates,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        overrides = d.pop("overrides")

        preferences = d.pop("preferences")

        rules = d.pop("rules")

        templates = d.pop("templates")

        status = d.pop("status", UNSET)

        seed_apply_response = cls(
            overrides=overrides,
            preferences=preferences,
            rules=rules,
            templates=templates,
            status=status,
        )

        seed_apply_response.additional_properties = d
        return seed_apply_response

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
