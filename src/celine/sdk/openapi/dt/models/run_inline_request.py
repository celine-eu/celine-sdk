from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parameters import Parameters
    from ..models.scenario import Scenario


T = TypeVar("T", bound="RunInlineRequest")


@_attrs_define
class RunInlineRequest:
    """
    Attributes:
        scenario (Scenario):
        include_result (bool | Unset):  Default: False.
        parameters (Parameters | Unset):
        ttl_hours (int | Unset):  Default: 1.
    """

    scenario: Scenario
    include_result: bool | Unset = False
    parameters: Parameters | Unset = UNSET
    ttl_hours: int | Unset = 1
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scenario = self.scenario.to_dict()

        include_result = self.include_result

        parameters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        ttl_hours = self.ttl_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scenario": scenario,
            }
        )
        if include_result is not UNSET:
            field_dict["include_result"] = include_result
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if ttl_hours is not UNSET:
            field_dict["ttl_hours"] = ttl_hours

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.parameters import Parameters
        from ..models.scenario import Scenario

        d = dict(src_dict)
        scenario = Scenario.from_dict(d.pop("scenario"))

        include_result = d.pop("include_result", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Parameters | Unset
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = Parameters.from_dict(_parameters)

        ttl_hours = d.pop("ttl_hours", UNSET)

        run_inline_request = cls(
            scenario=scenario,
            include_result=include_result,
            parameters=parameters,
            ttl_hours=ttl_hours,
        )

        run_inline_request.additional_properties = d
        return run_inline_request

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
