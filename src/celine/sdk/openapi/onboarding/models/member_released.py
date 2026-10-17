from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.release_step import ReleaseStep


T = TypeVar("T", bound="MemberReleased")


@_attrs_define
class MemberReleased:
    """
    Attributes:
        community (str):
        member_key (str):
        source (str):
        state (str):
        steps (list[ReleaseStep]):
    """

    community: str
    member_key: str
    source: str
    state: str
    steps: list[ReleaseStep]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community = self.community

        member_key = self.member_key

        source = self.source

        state = self.state

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community": community,
                "memberKey": member_key,
                "source": source,
                "state": state,
                "steps": steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.release_step import ReleaseStep

        d = dict(src_dict)
        community = d.pop("community")

        member_key = d.pop("memberKey")

        source = d.pop("source")

        state = d.pop("state")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = ReleaseStep.from_dict(steps_item_data)

            steps.append(steps_item)

        member_released = cls(
            community=community,
            member_key=member_key,
            source=source,
            state=state,
            steps=steps,
        )

        member_released.additional_properties = d
        return member_released

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
