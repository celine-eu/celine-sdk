from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.propagation_step import PropagationStep
from ..types import UNSET, Unset

T = TypeVar("T", bound="RevisionRetryRequest")


@_attrs_define
class RevisionRetryRequest:
    """
    Attributes:
        step (None | PropagationStep | Unset):
    """

    step: None | PropagationStep | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step: None | str | Unset
        if isinstance(self.step, Unset):
            step = UNSET
        elif isinstance(self.step, PropagationStep):
            step = self.step.value
        else:
            step = self.step

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if step is not UNSET:
            field_dict["step"] = step

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_step(data: object) -> None | PropagationStep | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                step_type_0 = PropagationStep(data)

                return step_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PropagationStep | Unset, data)

        step = _parse_step(d.pop("step", UNSET))

        revision_retry_request = cls(
            step=step,
        )

        revision_retry_request.additional_properties = d
        return revision_retry_request

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
