from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.updated_field import UpdatedField
from ..models.verification_outcome import VerificationOutcome

T = TypeVar("T", bound="ParticipantUpdateResponse")


@_attrs_define
class ParticipantUpdateResponse:
    """The account after `PATCH /participants/{community}/{key}`.

    `user_id` and `username` as on every other route: the Keycloak uuid, and the
    name the account authenticates as, which this route never changes.

        Attributes:
            changed (list[UpdatedField]): The fields this call wrote. Empty when every value given was already the
                account's: nothing was written and nothing sent
            email (None | str):
            email_verified (bool): False after an address change, until the person follows the link
            first_name (None | str):
            last_name (None | str):
            user_id (str): The Keycloak uuid of the account (not the registry's user_id)
            username (str): Unchanged by this route, always
            verification (VerificationOutcome): What an update did about verifying an address.

                Mirrors `celine.provisioning.invitation.VerificationOutcome`.
    """

    changed: list[UpdatedField]
    email: None | str
    email_verified: bool
    first_name: None | str
    last_name: None | str
    user_id: str
    username: str
    verification: VerificationOutcome
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        changed = []
        for changed_item_data in self.changed:
            changed_item = changed_item_data.value
            changed.append(changed_item)

        email: None | str
        email = self.email

        email_verified = self.email_verified

        first_name: None | str
        first_name = self.first_name

        last_name: None | str
        last_name = self.last_name

        user_id = self.user_id

        username = self.username

        verification = self.verification.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "changed": changed,
                "email": email,
                "email_verified": email_verified,
                "first_name": first_name,
                "last_name": last_name,
                "user_id": user_id,
                "username": username,
                "verification": verification,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        changed = []
        _changed = d.pop("changed")
        for changed_item_data in _changed:
            changed_item = UpdatedField(changed_item_data)

            changed.append(changed_item)

        def _parse_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        email = _parse_email(d.pop("email"))

        email_verified = d.pop("email_verified")

        def _parse_first_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        first_name = _parse_first_name(d.pop("first_name"))

        def _parse_last_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_name = _parse_last_name(d.pop("last_name"))

        user_id = d.pop("user_id")

        username = d.pop("username")

        verification = VerificationOutcome(d.pop("verification"))

        participant_update_response = cls(
            changed=changed,
            email=email,
            email_verified=email_verified,
            first_name=first_name,
            last_name=last_name,
            user_id=user_id,
            username=username,
            verification=verification,
        )

        participant_update_response.additional_properties = d
        return participant_update_response

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
