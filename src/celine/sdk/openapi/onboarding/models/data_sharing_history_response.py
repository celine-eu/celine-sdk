from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sharing_state import SharingState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_sharing_history_response_events_item import DataSharingHistoryResponseEventsItem


T = TypeVar("T", bound="DataSharingHistoryResponse")


@_attrs_define
class DataSharingHistoryResponse:
    """The member's own record of what happened with their data.

    Attributes:
        has_identity (bool):
        state (SharingState): Why a member can or cannot decide anything, in one word.

            The states exist because collapsing them is what made the feature useless:
            a preregistered member reached the sharing screen and was told they had no
            dataspace identity, which was true and unactionable. Each of these has a
            different thing to say and a different thing to do next.
        events (list[DataSharingHistoryResponseEventsItem] | Unset):
    """

    has_identity: bool
    state: SharingState
    events: list[DataSharingHistoryResponseEventsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_identity = self.has_identity

        state = self.state.value

        events: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()
                events.append(events_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_identity": has_identity,
                "state": state,
            }
        )
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_sharing_history_response_events_item import DataSharingHistoryResponseEventsItem

        d = dict(src_dict)
        has_identity = d.pop("has_identity")

        state = SharingState(d.pop("state"))

        _events = d.pop("events", UNSET)
        events: list[DataSharingHistoryResponseEventsItem] | Unset = UNSET
        if _events is not UNSET:
            events = []
            for events_item_data in _events:
                events_item = DataSharingHistoryResponseEventsItem.from_dict(events_item_data)

                events.append(events_item)

        data_sharing_history_response = cls(
            has_identity=has_identity,
            state=state,
            events=events,
        )

        data_sharing_history_response.additional_properties = d
        return data_sharing_history_response

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
