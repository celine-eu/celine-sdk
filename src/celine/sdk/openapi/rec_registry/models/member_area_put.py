from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MemberAreaPut")


@_attrs_define
class MemberAreaPut:
    """A member's area, and nothing else (`PUT …/members/{key}/area`, REQ-0083).

    Checked against the community's areas by the route, with the coded
    `422 unknown_area` the general `PATCH` answers (REQ-0066), not here.

        Attributes:
            area (str): A key of the community's `areas`.
    """

    area: str

    def to_dict(self) -> dict[str, Any]:
        area = self.area

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "area": area,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        area = d.pop("area")

        member_area_put = cls(
            area=area,
        )

        return member_area_put
