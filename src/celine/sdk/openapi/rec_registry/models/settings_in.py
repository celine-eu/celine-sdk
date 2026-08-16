from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SettingsIn")


@_attrs_define
class SettingsIn:
    """Operational settings.

    Attributes:
        currency (None | str | Unset):
        energy_unit (None | str | Unset):
        power_unit (None | str | Unset):
        timezone (None | str | Unset):
    """

    currency: None | str | Unset = UNSET
    energy_unit: None | str | Unset = UNSET
    power_unit: None | str | Unset = UNSET
    timezone: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        currency: None | str | Unset
        if isinstance(self.currency, Unset):
            currency = UNSET
        else:
            currency = self.currency

        energy_unit: None | str | Unset
        if isinstance(self.energy_unit, Unset):
            energy_unit = UNSET
        else:
            energy_unit = self.energy_unit

        power_unit: None | str | Unset
        if isinstance(self.power_unit, Unset):
            power_unit = UNSET
        else:
            power_unit = self.power_unit

        timezone: None | str | Unset
        if isinstance(self.timezone, Unset):
            timezone = UNSET
        else:
            timezone = self.timezone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if currency is not UNSET:
            field_dict["currency"] = currency
        if energy_unit is not UNSET:
            field_dict["energy_unit"] = energy_unit
        if power_unit is not UNSET:
            field_dict["power_unit"] = power_unit
        if timezone is not UNSET:
            field_dict["timezone"] = timezone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_currency(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        currency = _parse_currency(d.pop("currency", UNSET))

        def _parse_energy_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        energy_unit = _parse_energy_unit(d.pop("energy_unit", UNSET))

        def _parse_power_unit(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        power_unit = _parse_power_unit(d.pop("power_unit", UNSET))

        def _parse_timezone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        timezone = _parse_timezone(d.pop("timezone", UNSET))

        settings_in = cls(
            currency=currency,
            energy_unit=energy_unit,
            power_unit=power_unit,
            timezone=timezone,
        )

        settings_in.additional_properties = d
        return settings_in

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
