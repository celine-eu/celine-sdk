from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.invitation_intent import InvitationIntent

T = TypeVar("T", bound="InvitationRequest")


@_attrs_define
class InvitationRequest:
    """The body of `POST /participants/{community}/{key}/invitation`.

    Attributes:
        intent (InvitationIntent): Which email the caller of `POST .../invitation` asks for.

            Explicit, and required, so the email is always the button a person pressed
            (requester, 2026-09-14, A2: "do not trick the user"). The service checks it
            against the account in the same call that sends and refuses a mismatch.
    """

    intent: InvitationIntent
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        intent = self.intent.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "intent": intent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        intent = InvitationIntent(d.pop("intent"))

        invitation_request = cls(
            intent=intent,
        )

        invitation_request.additional_properties = d
        return invitation_request

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
