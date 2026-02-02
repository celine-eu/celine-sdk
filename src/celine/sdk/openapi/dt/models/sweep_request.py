from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sweep_request_parameter_sets_item import SweepRequestParameterSetsItem


T = TypeVar("T", bound="SweepRequest")


@_attrs_define
class SweepRequest:
    """
    Attributes:
        parameter_sets (list[SweepRequestParameterSetsItem]):
        scenario_id (str):
        include_baseline (bool | Unset):  Default: True.
    """

    parameter_sets: list[SweepRequestParameterSetsItem]
    scenario_id: str
    include_baseline: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        parameter_sets = []
        for parameter_sets_item_data in self.parameter_sets:
            parameter_sets_item = parameter_sets_item_data.to_dict()
            parameter_sets.append(parameter_sets_item)

        scenario_id = self.scenario_id

        include_baseline = self.include_baseline

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "parameter_sets": parameter_sets,
                "scenario_id": scenario_id,
            }
        )
        if include_baseline is not UNSET:
            field_dict["include_baseline"] = include_baseline

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sweep_request_parameter_sets_item import SweepRequestParameterSetsItem

        d = dict(src_dict)
        parameter_sets = []
        _parameter_sets = d.pop("parameter_sets")
        for parameter_sets_item_data in _parameter_sets:
            parameter_sets_item = SweepRequestParameterSetsItem.from_dict(parameter_sets_item_data)

            parameter_sets.append(parameter_sets_item)

        scenario_id = d.pop("scenario_id")

        include_baseline = d.pop("include_baseline", UNSET)

        sweep_request = cls(
            parameter_sets=parameter_sets,
            scenario_id=scenario_id,
            include_baseline=include_baseline,
        )

        sweep_request.additional_properties = d
        return sweep_request

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
