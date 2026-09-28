from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AreaRename")


@_attrs_define
class AreaRename:
    """Move an area to a new key, with its members (REQ-0079).

    `new_key` only; any other key is `422`. A key that is not an area key —
    letters, digits, `-` and `_`, starting with a letter or digit, at most 128
    characters — is refused `422 invalid_area_key`.

        Attributes:
            new_key (str): The key the area is moved to.
    """

    new_key: str

    def to_dict(self) -> dict[str, Any]:
        new_key = self.new_key

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "new_key": new_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        new_key = d.pop("new_key")

        area_rename = cls(
            new_key=new_key,
        )

        return area_rename
