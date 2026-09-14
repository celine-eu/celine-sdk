from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.invitation_send_outcome import InvitationSendOutcome

T = TypeVar("T", bound="InvitationResponse")


@_attrs_define
class InvitationResponse:
    """What `POST .../invitation` emailed, and for how long the link lasts.

    No credential travels here: the person sets their own through the link
    Keycloak sends. `actions` says which email it was — `UPDATE_PASSWORD` and
    `VERIFY_EMAIL` for an account with no password (an invitation),
    `UPDATE_PASSWORD` alone for one that has a password (a reset).

        Attributes:
            actions (list[str]):
            invitation (InvitationSendOutcome): What `POST .../invitation` did: sent, or refused by the dev list.
            lifespan (int): Seconds the link stays usable
            user_id (str):
            username (str):
    """

    actions: list[str]
    invitation: InvitationSendOutcome
    lifespan: int
    user_id: str
    username: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actions = self.actions

        invitation = self.invitation.value

        lifespan = self.lifespan

        user_id = self.user_id

        username = self.username

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actions": actions,
                "invitation": invitation,
                "lifespan": lifespan,
                "user_id": user_id,
                "username": username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        actions = cast(list[str], d.pop("actions"))

        invitation = InvitationSendOutcome(d.pop("invitation"))

        lifespan = d.pop("lifespan")

        user_id = d.pop("user_id")

        username = d.pop("username")

        invitation_response = cls(
            actions=actions,
            invitation=invitation,
            lifespan=lifespan,
            user_id=user_id,
            username=username,
        )

        invitation_response.additional_properties = d
        return invitation_response

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
