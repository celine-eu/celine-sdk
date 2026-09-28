from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PodListRequest")


@_attrs_define
class PodListRequest:
    """The offer, and nothing else.

    ``recipient_ref`` was dropped (ADR-0010, amended 2026-09-25): the party the
    offer's consent is read for comes from the offer. A caller still sending it
    is not refused — unknown fields are ignored, like any other — so a body
    written for the old contract keeps working, and names nobody.

        Attributes:
            offer_id (str): Consent is purpose-scoped: somebody who agreed to a different offer has not agreed to this one.
    """

    offer_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offer_id = self.offer_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offer_id": offer_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offer_id = d.pop("offer_id")

        pod_list_request = cls(
            offer_id=offer_id,
        )

        pod_list_request.additional_properties = d
        return pod_list_request

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
