from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.locale import Locale
from ..types import UNSET, Unset

T = TypeVar("T", bound="ParticipantUpsert")


@_attrs_define
class ParticipantUpsert:
    """The body of `PUT /participants/{community}/{key}`.

    **The email transits and is stored nowhere.** Not here — this service keeps
    no state at all — and not in the registry, which has no email column and is
    gaining none. It is on the account in Keycloak, which is where the address a
    person logs in with belongs.

    It is required because it is the only thing that can find an account this
    platform did not name. A participant who already has a login authenticates
    under whatever convention created it, and the address is the one identifier
    every writer agrees on.

    **A plain string, not `EmailStr`.** The address belongs to the submission
    `../onboarding` already validated and accepted; re-deciding here whether it
    is well formed would mean a person who has been approved cannot be given a
    login because two libraries disagree about their address. Non-empty is the
    whole check, and it exists so a missing value fails here rather than
    creating an account named the empty string.

        Attributes:
            email (str): The participant's address; used to find or create the account
            first_name (None | str | Unset): Given name, optional
            invite (bool | Unset): Email the participant a link to set their password — only if the account was created in
                this call or has no password. The outcome is in `invitation`; the upsert never fails because of it. Default:
                False.
            last_name (None | str | Unset): Family name, optional
            locale (Locale | None | Unset): The participant's language, used for Keycloak's emails. Written on creation, and
                on an existing account only if it has none. Needs internationalization enabled on the realm, or Keycloak drops
                it.
    """

    email: str
    first_name: None | str | Unset = UNSET
    invite: bool | Unset = False
    last_name: None | str | Unset = UNSET
    locale: Locale | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        invite = self.invite

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        locale: None | str | Unset
        if isinstance(self.locale, Unset):
            locale = UNSET
        elif isinstance(self.locale, Locale):
            locale = self.locale.value
        else:
            locale = self.locale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if invite is not UNSET:
            field_dict["invite"] = invite
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if locale is not UNSET:
            field_dict["locale"] = locale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        invite = d.pop("invite", UNSET)

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        def _parse_locale(data: object) -> Locale | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                locale_type_0 = Locale(data)

                return locale_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Locale | None | Unset, data)

        locale = _parse_locale(d.pop("locale", UNSET))

        participant_upsert = cls(
            email=email,
            first_name=first_name,
            invite=invite,
            last_name=last_name,
            locale=locale,
        )

        participant_upsert.additional_properties = d
        return participant_upsert

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
