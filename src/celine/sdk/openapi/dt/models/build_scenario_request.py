from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.config import Config


T = TypeVar("T", bound="BuildScenarioRequest")


@_attrs_define
class BuildScenarioRequest:
    """
    Attributes:
        config (Config):
        reuse_existing (bool | Unset):  Default: True.
        ttl_hours (int | Unset):  Default: 24.
    """

    config: Config
    reuse_existing: bool | Unset = True
    ttl_hours: int | Unset = 24
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config = self.config.to_dict()

        reuse_existing = self.reuse_existing

        ttl_hours = self.ttl_hours

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
            }
        )
        if reuse_existing is not UNSET:
            field_dict["reuse_existing"] = reuse_existing
        if ttl_hours is not UNSET:
            field_dict["ttl_hours"] = ttl_hours

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.config import Config

        d = dict(src_dict)
        config = Config.from_dict(d.pop("config"))

        reuse_existing = d.pop("reuse_existing", UNSET)

        ttl_hours = d.pop("ttl_hours", UNSET)

        build_scenario_request = cls(
            config=config,
            reuse_existing=reuse_existing,
            ttl_hours=ttl_hours,
        )

        build_scenario_request.additional_properties = d
        return build_scenario_request

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
