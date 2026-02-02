from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.baseline_metrics import BaselineMetrics


T = TypeVar("T", bound="BuildScenarioResponse")


@_attrs_define
class BuildScenarioResponse:
    """
    Attributes:
        config_hash (str):
        created_at (str):
        expires_at (str):
        scenario_id (str):
        simulation_key (str):
        baseline_metrics (BaselineMetrics | Unset):
    """

    config_hash: str
    created_at: str
    expires_at: str
    scenario_id: str
    simulation_key: str
    baseline_metrics: BaselineMetrics | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_hash = self.config_hash

        created_at = self.created_at

        expires_at = self.expires_at

        scenario_id = self.scenario_id

        simulation_key = self.simulation_key

        baseline_metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.baseline_metrics, Unset):
            baseline_metrics = self.baseline_metrics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config_hash": config_hash,
                "created_at": created_at,
                "expires_at": expires_at,
                "scenario_id": scenario_id,
                "simulation_key": simulation_key,
            }
        )
        if baseline_metrics is not UNSET:
            field_dict["baseline_metrics"] = baseline_metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.baseline_metrics import BaselineMetrics

        d = dict(src_dict)
        config_hash = d.pop("config_hash")

        created_at = d.pop("created_at")

        expires_at = d.pop("expires_at")

        scenario_id = d.pop("scenario_id")

        simulation_key = d.pop("simulation_key")

        _baseline_metrics = d.pop("baseline_metrics", UNSET)
        baseline_metrics: BaselineMetrics | Unset
        if isinstance(_baseline_metrics, Unset):
            baseline_metrics = UNSET
        else:
            baseline_metrics = BaselineMetrics.from_dict(_baseline_metrics)

        build_scenario_response = cls(
            config_hash=config_hash,
            created_at=created_at,
            expires_at=expires_at,
            scenario_id=scenario_id,
            simulation_key=simulation_key,
            baseline_metrics=baseline_metrics,
        )

        build_scenario_response.additional_properties = d
        return build_scenario_response

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
