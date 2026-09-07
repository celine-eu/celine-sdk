from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="EligibilityResponse")


@_attrs_define
class EligibilityResponse:
    """
    Attributes:
        eligible (bool):
        country_code (None | str | Unset):
        lat (float | None | Unset):
        lng (float | None | Unset):
        matched_rule (None | str | Unset):
        matched_value (None | str | Unset):
        municipality (None | str | Unset):
        postal_code (None | str | Unset):
        reason (None | str | Unset):
        state (None | str | Unset):
    """

    eligible: bool
    country_code: None | str | Unset = UNSET
    lat: float | None | Unset = UNSET
    lng: float | None | Unset = UNSET
    matched_rule: None | str | Unset = UNSET
    matched_value: None | str | Unset = UNSET
    municipality: None | str | Unset = UNSET
    postal_code: None | str | Unset = UNSET
    reason: None | str | Unset = UNSET
    state: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        eligible = self.eligible

        country_code: None | str | Unset
        if isinstance(self.country_code, Unset):
            country_code = UNSET
        else:
            country_code = self.country_code

        lat: float | None | Unset
        if isinstance(self.lat, Unset):
            lat = UNSET
        else:
            lat = self.lat

        lng: float | None | Unset
        if isinstance(self.lng, Unset):
            lng = UNSET
        else:
            lng = self.lng

        matched_rule: None | str | Unset
        if isinstance(self.matched_rule, Unset):
            matched_rule = UNSET
        else:
            matched_rule = self.matched_rule

        matched_value: None | str | Unset
        if isinstance(self.matched_value, Unset):
            matched_value = UNSET
        else:
            matched_value = self.matched_value

        municipality: None | str | Unset
        if isinstance(self.municipality, Unset):
            municipality = UNSET
        else:
            municipality = self.municipality

        postal_code: None | str | Unset
        if isinstance(self.postal_code, Unset):
            postal_code = UNSET
        else:
            postal_code = self.postal_code

        reason: None | str | Unset
        if isinstance(self.reason, Unset):
            reason = UNSET
        else:
            reason = self.reason

        state: None | str | Unset
        if isinstance(self.state, Unset):
            state = UNSET
        else:
            state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eligible": eligible,
            }
        )
        if country_code is not UNSET:
            field_dict["country_code"] = country_code
        if lat is not UNSET:
            field_dict["lat"] = lat
        if lng is not UNSET:
            field_dict["lng"] = lng
        if matched_rule is not UNSET:
            field_dict["matched_rule"] = matched_rule
        if matched_value is not UNSET:
            field_dict["matched_value"] = matched_value
        if municipality is not UNSET:
            field_dict["municipality"] = municipality
        if postal_code is not UNSET:
            field_dict["postal_code"] = postal_code
        if reason is not UNSET:
            field_dict["reason"] = reason
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        eligible = d.pop("eligible")

        def _parse_country_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        country_code = _parse_country_code(d.pop("country_code", UNSET))

        def _parse_lat(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        lat = _parse_lat(d.pop("lat", UNSET))

        def _parse_lng(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        lng = _parse_lng(d.pop("lng", UNSET))

        def _parse_matched_rule(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        matched_rule = _parse_matched_rule(d.pop("matched_rule", UNSET))

        def _parse_matched_value(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        matched_value = _parse_matched_value(d.pop("matched_value", UNSET))

        def _parse_municipality(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        municipality = _parse_municipality(d.pop("municipality", UNSET))

        def _parse_postal_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        postal_code = _parse_postal_code(d.pop("postal_code", UNSET))

        def _parse_reason(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reason = _parse_reason(d.pop("reason", UNSET))

        def _parse_state(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        state = _parse_state(d.pop("state", UNSET))

        eligibility_response = cls(
            eligible=eligible,
            country_code=country_code,
            lat=lat,
            lng=lng,
            matched_rule=matched_rule,
            matched_value=matched_value,
            municipality=municipality,
            postal_code=postal_code,
            reason=reason,
            state=state,
        )

        eligibility_response.additional_properties = d
        return eligibility_response

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
