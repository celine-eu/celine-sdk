from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.suggestion_respond_request_response import SuggestionRespondRequestResponse
from ..types import UNSET, Unset

T = TypeVar("T", bound="SuggestionRespondRequest")


@_attrs_define
class SuggestionRespondRequest:
    """
    Attributes:
        response (SuggestionRespondRequestResponse):
        period_end (None | str | Unset):
        period_start (None | str | Unset):
        reward_points (int | None | Unset):
    """

    response: SuggestionRespondRequestResponse
    period_end: None | str | Unset = UNSET
    period_start: None | str | Unset = UNSET
    reward_points: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response = self.response.value

        period_end: None | str | Unset
        if isinstance(self.period_end, Unset):
            period_end = UNSET
        else:
            period_end = self.period_end

        period_start: None | str | Unset
        if isinstance(self.period_start, Unset):
            period_start = UNSET
        else:
            period_start = self.period_start

        reward_points: int | None | Unset
        if isinstance(self.reward_points, Unset):
            reward_points = UNSET
        else:
            reward_points = self.reward_points

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "response": response,
            }
        )
        if period_end is not UNSET:
            field_dict["period_end"] = period_end
        if period_start is not UNSET:
            field_dict["period_start"] = period_start
        if reward_points is not UNSET:
            field_dict["reward_points"] = reward_points

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        response = SuggestionRespondRequestResponse(d.pop("response"))

        def _parse_period_end(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        period_end = _parse_period_end(d.pop("period_end", UNSET))

        def _parse_period_start(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        period_start = _parse_period_start(d.pop("period_start", UNSET))

        def _parse_reward_points(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        reward_points = _parse_reward_points(d.pop("reward_points", UNSET))

        suggestion_respond_request = cls(
            response=response,
            period_end=period_end,
            period_start=period_start,
            reward_points=reward_points,
        )

        suggestion_respond_request.additional_properties = d
        return suggestion_respond_request

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
