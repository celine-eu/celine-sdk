from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationKindPreferenceOut")


@_attrs_define
class NotificationKindPreferenceOut:
    """
    Attributes:
        kind (str):
        label (str):
        description (str):
        cadence (str):
        enabled (bool):
        editable (bool | Unset):  Default: True.
    """

    kind: str
    label: str
    description: str
    cadence: str
    enabled: bool
    editable: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        label = self.label

        description = self.description

        cadence = self.cadence

        enabled = self.enabled

        editable = self.editable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "label": label,
                "description": description,
                "cadence": cadence,
                "enabled": enabled,
            }
        )
        if editable is not UNSET:
            field_dict["editable"] = editable

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind")

        label = d.pop("label")

        description = d.pop("description")

        cadence = d.pop("cadence")

        enabled = d.pop("enabled")

        editable = d.pop("editable", UNSET)

        notification_kind_preference_out = cls(
            kind=kind,
            label=label,
            description=description,
            cadence=cadence,
            enabled=enabled,
            editable=editable,
        )

        notification_kind_preference_out.additional_properties = d
        return notification_kind_preference_out

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
