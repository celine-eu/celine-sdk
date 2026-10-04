from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RevisionStepRead")


@_attrs_define
class RevisionStepRead:
    """One propagation target of a revision. Codes and fixed sentences, no values.

    Attributes:
        attempts (int):
        completed_at (datetime.datetime | None):
        error_code (None | str):
        outcome (None | str):
        reason (None | str):
        status (str):
        step (str):
    """

    attempts: int
    completed_at: datetime.datetime | None
    error_code: None | str
    outcome: None | str
    reason: None | str
    status: str
    step: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attempts = self.attempts

        completed_at: None | str
        if isinstance(self.completed_at, datetime.datetime):
            completed_at = self.completed_at.isoformat()
        else:
            completed_at = self.completed_at

        error_code: None | str
        error_code = self.error_code

        outcome: None | str
        outcome = self.outcome

        reason: None | str
        reason = self.reason

        status = self.status

        step = self.step

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempts": attempts,
                "completed_at": completed_at,
                "error_code": error_code,
                "outcome": outcome,
                "reason": reason,
                "status": status,
                "step": step,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempts = d.pop("attempts")

        def _parse_completed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                completed_at_type_0 = isoparse(data)

                return completed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        completed_at = _parse_completed_at(d.pop("completed_at"))

        def _parse_error_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        error_code = _parse_error_code(d.pop("error_code"))

        def _parse_outcome(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        outcome = _parse_outcome(d.pop("outcome"))

        def _parse_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        reason = _parse_reason(d.pop("reason"))

        status = d.pop("status")

        step = d.pop("step")

        revision_step_read = cls(
            attempts=attempts,
            completed_at=completed_at,
            error_code=error_code,
            outcome=outcome,
            reason=reason,
            status=status,
            step=step,
        )

        revision_step_read.additional_properties = d
        return revision_step_read

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
