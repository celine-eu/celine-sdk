from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MemberRolePut")


@_attrs_define
class MemberRolePut:
    """A member's role, and nothing else (`PUT …/members/{key}/role`, REQ-0083).

    Checked against its set by the route, with the coded `422 invalid_role`
    the general `PATCH` answers (REQ-0066), not here.

        Attributes:
            role (str): One of consumer, prosumer, producer, operator, admin.
    """

    role: str

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = d.pop("role")

        member_role_put = cls(
            role=role,
        )

        return member_role_put
