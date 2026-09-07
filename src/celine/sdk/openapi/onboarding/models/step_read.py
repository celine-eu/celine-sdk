from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="StepRead")


@_attrs_define
class StepRead:
    """
    Attributes:
        attempts (int):
        completed_at (datetime.datetime | None):
        detail (None | str):
        external_ref (None | str):
        fail_closed (bool):
        label (str):
        last_error (None | str):
        started_at (datetime.datetime | None):
        status (str):
        step (str):
    """

    attempts: int
    completed_at: datetime.datetime | None
    detail: None | str
    external_ref: None | str
    fail_closed: bool
    label: str
    last_error: None | str
    started_at: datetime.datetime | None
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

        detail: None | str
        detail = self.detail

        external_ref: None | str
        external_ref = self.external_ref

        fail_closed = self.fail_closed

        label = self.label

        last_error: None | str
        last_error = self.last_error

        started_at: None | str
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        status = self.status

        step = self.step

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "attempts": attempts,
                "completed_at": completed_at,
                "detail": detail,
                "external_ref": external_ref,
                "fail_closed": fail_closed,
                "label": label,
                "last_error": last_error,
                "started_at": started_at,
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

        def _parse_detail(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        detail = _parse_detail(d.pop("detail"))

        def _parse_external_ref(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_ref = _parse_external_ref(d.pop("external_ref"))

        fail_closed = d.pop("fail_closed")

        label = d.pop("label")

        def _parse_last_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_error = _parse_last_error(d.pop("last_error"))

        def _parse_started_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        started_at = _parse_started_at(d.pop("started_at"))

        status = d.pop("status")

        step = d.pop("step")

        step_read = cls(
            attempts=attempts,
            completed_at=completed_at,
            detail=detail,
            external_ref=external_ref,
            fail_closed=fail_closed,
            label=label,
            last_error=last_error,
            started_at=started_at,
            status=status,
            step=step,
        )

        step_read.additional_properties = d
        return step_read

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
