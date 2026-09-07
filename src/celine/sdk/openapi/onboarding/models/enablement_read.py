from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.step_read import StepRead


T = TypeVar("T", bound="EnablementRead")


@_attrs_define
class EnablementRead:
    """
    Attributes:
        state (str):
        steps (list[StepRead]):
        submission_id (UUID):
    """

    state: str
    steps: list[StepRead]
    submission_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        submission_id = str(self.submission_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "steps": steps,
                "submission_id": submission_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.step_read import StepRead

        d = dict(src_dict)
        state = d.pop("state")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = StepRead.from_dict(steps_item_data)

            steps.append(steps_item)

        submission_id = UUID(d.pop("submission_id"))

        enablement_read = cls(
            state=state,
            steps=steps,
            submission_id=submission_id,
        )

        enablement_read.additional_properties = d
        return enablement_read

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
