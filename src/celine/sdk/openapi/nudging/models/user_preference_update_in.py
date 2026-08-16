from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPreferenceUpdateIn")


@_attrs_define
class UserPreferenceUpdateIn:
    """
    Attributes:
        max_per_day (int):
        channel_email (bool | None | Unset):
        email (None | str | Unset):
        enabled_notification_kinds (list[str] | None | Unset):
        lang (None | str | Unset):
    """

    max_per_day: int
    channel_email: bool | None | Unset = UNSET
    email: None | str | Unset = UNSET
    enabled_notification_kinds: list[str] | None | Unset = UNSET
    lang: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        max_per_day = self.max_per_day

        channel_email: bool | None | Unset
        if isinstance(self.channel_email, Unset):
            channel_email = UNSET
        else:
            channel_email = self.channel_email

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        enabled_notification_kinds: list[str] | None | Unset
        if isinstance(self.enabled_notification_kinds, Unset):
            enabled_notification_kinds = UNSET
        elif isinstance(self.enabled_notification_kinds, list):
            enabled_notification_kinds = self.enabled_notification_kinds

        else:
            enabled_notification_kinds = self.enabled_notification_kinds

        lang: None | str | Unset
        if isinstance(self.lang, Unset):
            lang = UNSET
        else:
            lang = self.lang

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "max_per_day": max_per_day,
            }
        )
        if channel_email is not UNSET:
            field_dict["channel_email"] = channel_email
        if email is not UNSET:
            field_dict["email"] = email
        if enabled_notification_kinds is not UNSET:
            field_dict["enabled_notification_kinds"] = enabled_notification_kinds
        if lang is not UNSET:
            field_dict["lang"] = lang

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_per_day = d.pop("max_per_day")

        def _parse_channel_email(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        channel_email = _parse_channel_email(d.pop("channel_email", UNSET))

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_enabled_notification_kinds(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                enabled_notification_kinds_type_0 = cast(list[str], data)

                return enabled_notification_kinds_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        enabled_notification_kinds = _parse_enabled_notification_kinds(d.pop("enabled_notification_kinds", UNSET))

        def _parse_lang(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        lang = _parse_lang(d.pop("lang", UNSET))

        user_preference_update_in = cls(
            max_per_day=max_per_day,
            channel_email=channel_email,
            email=email,
            enabled_notification_kinds=enabled_notification_kinds,
            lang=lang,
        )

        user_preference_update_in.additional_properties = d
        return user_preference_update_in

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
