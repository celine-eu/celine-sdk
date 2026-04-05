from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.suggestion_respond_response_status import SuggestionRespondResponseStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="SuggestionRespondResponse")


@_attrs_define
class SuggestionRespondResponse:
    """
    Attributes:
        reward_points_estimated (int):
        status (SuggestionRespondResponseStatus):
        commitment_id (None | Unset | UUID):
    """

    reward_points_estimated: int
    status: SuggestionRespondResponseStatus
    commitment_id: None | Unset | UUID = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reward_points_estimated = self.reward_points_estimated

        status = self.status.value

        commitment_id: None | str | Unset
        if isinstance(self.commitment_id, Unset):
            commitment_id = UNSET
        elif isinstance(self.commitment_id, UUID):
            commitment_id = str(self.commitment_id)
        else:
            commitment_id = self.commitment_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reward_points_estimated": reward_points_estimated,
                "status": status,
            }
        )
        if commitment_id is not UNSET:
            field_dict["commitment_id"] = commitment_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        reward_points_estimated = d.pop("reward_points_estimated")

        status = SuggestionRespondResponseStatus(d.pop("status"))

        def _parse_commitment_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                commitment_id_type_0 = UUID(data)

                return commitment_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UUID, data)

        commitment_id = _parse_commitment_id(d.pop("commitment_id", UNSET))

        suggestion_respond_response = cls(
            reward_points_estimated=reward_points_estimated,
            status=status,
            commitment_id=commitment_id,
        )

        suggestion_respond_response.additional_properties = d
        return suggestion_respond_response

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
