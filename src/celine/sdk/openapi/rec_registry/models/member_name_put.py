from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MemberNamePut")


@_attrs_define
class MemberNamePut:
    """A member's name, and nothing else (`PUT …/members/{key}/name`, REQ-0083).

    The one key is required and may not be `null`; any other key is `422`, so
    the narrow `members.name.write` grant cannot carry an identity rewrite.

        Attributes:
            name (str): The member's display name.
    """

    name: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        member_name_put = cls(
            name=name,
        )

        return member_name_put
