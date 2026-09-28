from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SupplyAddress")


@_attrs_define
class SupplyAddress:
    """The supply address the wizard's eligibility step checked (REQ-0018).

    In the shape the geocoder takes: the free-text query, exactly as the
    applicant typed it and the check geocoded it. The server geocodes the same
    text again at submit and at approval to resolve the boundary; nothing the
    browser computed from it (a point, a boundary, an area) is accepted.

        Attributes:
            text (str):
    """

    text: str

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        text = d.pop("text")

        supply_address = cls(
            text=text,
        )

        return supply_address
