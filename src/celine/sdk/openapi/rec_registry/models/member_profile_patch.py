from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MemberProfilePatch")


@_attrs_define
class MemberProfilePatch:
    """A member's role and area, and nothing else (REQ-0070).

    At least one of the two, and no other key: a body that could carry a
    `user_id` would hand the narrower `members.profile.write` grant the identity
    rewrite REQ-0022 exists to stop. Absent fields are left alone; neither may
    be sent as `null`, since a member always has both.

    The values are checked against their sets by the route, with a coded `422`
    (`invalid_role`, `unknown_area`; REQ-0066), not here — a validation error
    here has no `code`.

        Attributes:
            area (str | Unset): A key of the community's `areas`.
            role (str | Unset): One of consumer, prosumer, producer, operator, admin.
    """

    area: str | Unset = UNSET
    role: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        area = self.area

        role = self.role

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if area is not UNSET:
            field_dict["area"] = area
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        area = d.pop("area", UNSET)

        role = d.pop("role", UNSET)

        member_profile_patch = cls(
            area=area,
            role=role,
        )

        return member_profile_patch
