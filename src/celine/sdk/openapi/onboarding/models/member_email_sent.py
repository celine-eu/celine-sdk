from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.member_email_sent_kind import MemberEmailSentKind

T = TypeVar("T", bound="MemberEmailSent")


@_attrs_define
class MemberEmailSent:
    """A `200`: the email went out, or dev email mode held it back.

    Attributes:
        code (str):
        kind (MemberEmailSentKind):
        lifespan_seconds (int):
    """

    code: str
    kind: MemberEmailSentKind
    lifespan_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        kind = self.kind.value

        lifespan_seconds = self.lifespan_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "kind": kind,
                "lifespanSeconds": lifespan_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        kind = MemberEmailSentKind(d.pop("kind"))

        lifespan_seconds = d.pop("lifespanSeconds")

        member_email_sent = cls(
            code=code,
            kind=kind,
            lifespan_seconds=lifespan_seconds,
        )

        member_email_sent.additional_properties = d
        return member_email_sent

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
