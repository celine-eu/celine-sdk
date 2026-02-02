from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_simulation_parameters import RunSimulationParameters


T = TypeVar("T", bound="RunSimulationRequest")


@_attrs_define
class RunSimulationRequest:
    """
    Attributes:
        scenario_id (str):
        include_result (bool | Unset):  Default: False.
        parameters (RunSimulationParameters | Unset):
    """

    scenario_id: str
    include_result: bool | Unset = False
    parameters: RunSimulationParameters | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scenario_id = self.scenario_id

        include_result = self.include_result

        parameters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scenario_id": scenario_id,
            }
        )
        if include_result is not UNSET:
            field_dict["include_result"] = include_result
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_simulation_parameters import RunSimulationParameters

        d = dict(src_dict)
        scenario_id = d.pop("scenario_id")

        include_result = d.pop("include_result", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: RunSimulationParameters | Unset
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = RunSimulationParameters.from_dict(_parameters)

        run_simulation_request = cls(
            scenario_id=scenario_id,
            include_result=include_result,
            parameters=parameters,
        )

        run_simulation_request.additional_properties = d
        return run_simulation_request

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
