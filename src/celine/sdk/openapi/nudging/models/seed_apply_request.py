from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.seed_apply_request_overrides_item import SeedApplyRequestOverridesItem
    from ..models.seed_apply_request_preferences_item import SeedApplyRequestPreferencesItem
    from ..models.seed_apply_request_rules_item import SeedApplyRequestRulesItem
    from ..models.seed_apply_request_templates_item import SeedApplyRequestTemplatesItem


T = TypeVar("T", bound="SeedApplyRequest")


@_attrs_define
class SeedApplyRequest:
    """
    Attributes:
        overrides (list[SeedApplyRequestOverridesItem] | Unset):
        preferences (list[SeedApplyRequestPreferencesItem] | Unset):
        rules (list[SeedApplyRequestRulesItem] | Unset):
        templates (list[SeedApplyRequestTemplatesItem] | Unset):
    """

    overrides: list[SeedApplyRequestOverridesItem] | Unset = UNSET
    preferences: list[SeedApplyRequestPreferencesItem] | Unset = UNSET
    rules: list[SeedApplyRequestRulesItem] | Unset = UNSET
    templates: list[SeedApplyRequestTemplatesItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        overrides: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.overrides, Unset):
            overrides = []
            for overrides_item_data in self.overrides:
                overrides_item = overrides_item_data.to_dict()
                overrides.append(overrides_item)

        preferences: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.preferences, Unset):
            preferences = []
            for preferences_item_data in self.preferences:
                preferences_item = preferences_item_data.to_dict()
                preferences.append(preferences_item)

        rules: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rules, Unset):
            rules = []
            for rules_item_data in self.rules:
                rules_item = rules_item_data.to_dict()
                rules.append(rules_item)

        templates: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.templates, Unset):
            templates = []
            for templates_item_data in self.templates:
                templates_item = templates_item_data.to_dict()
                templates.append(templates_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if overrides is not UNSET:
            field_dict["overrides"] = overrides
        if preferences is not UNSET:
            field_dict["preferences"] = preferences
        if rules is not UNSET:
            field_dict["rules"] = rules
        if templates is not UNSET:
            field_dict["templates"] = templates

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.seed_apply_request_overrides_item import SeedApplyRequestOverridesItem
        from ..models.seed_apply_request_preferences_item import SeedApplyRequestPreferencesItem
        from ..models.seed_apply_request_rules_item import SeedApplyRequestRulesItem
        from ..models.seed_apply_request_templates_item import SeedApplyRequestTemplatesItem

        d = dict(src_dict)
        _overrides = d.pop("overrides", UNSET)
        overrides: list[SeedApplyRequestOverridesItem] | Unset = UNSET
        if _overrides is not UNSET:
            overrides = []
            for overrides_item_data in _overrides:
                overrides_item = SeedApplyRequestOverridesItem.from_dict(overrides_item_data)

                overrides.append(overrides_item)

        _preferences = d.pop("preferences", UNSET)
        preferences: list[SeedApplyRequestPreferencesItem] | Unset = UNSET
        if _preferences is not UNSET:
            preferences = []
            for preferences_item_data in _preferences:
                preferences_item = SeedApplyRequestPreferencesItem.from_dict(preferences_item_data)

                preferences.append(preferences_item)

        _rules = d.pop("rules", UNSET)
        rules: list[SeedApplyRequestRulesItem] | Unset = UNSET
        if _rules is not UNSET:
            rules = []
            for rules_item_data in _rules:
                rules_item = SeedApplyRequestRulesItem.from_dict(rules_item_data)

                rules.append(rules_item)

        _templates = d.pop("templates", UNSET)
        templates: list[SeedApplyRequestTemplatesItem] | Unset = UNSET
        if _templates is not UNSET:
            templates = []
            for templates_item_data in _templates:
                templates_item = SeedApplyRequestTemplatesItem.from_dict(templates_item_data)

                templates.append(templates_item)

        seed_apply_request = cls(
            overrides=overrides,
            preferences=preferences,
            rules=rules,
            templates=templates,
        )

        seed_apply_request.additional_properties = d
        return seed_apply_request

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
