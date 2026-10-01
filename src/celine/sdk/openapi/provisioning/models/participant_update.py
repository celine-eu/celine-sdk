from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParticipantUpdate")


@_attrs_define
class ParticipantUpdate:
    """The body of `PATCH /participants/{community}/{key}`.

    At least one field; an empty body, or one with only `null`s, is `422`.
    **No `username`**: the account keeps the one it has, and a body naming one
    (or any other field) is refused `422` rather than silently ignored.

    The address is a plain string, for the reason `ParticipantUpsert` gives.

        Attributes:
            email (None | str | Unset): The new address. A change resets `email_verified` and emails a verification link to
                this address only; the same address (ignoring case) is not a change. `409 email_taken` if another account holds
                it
            first_name (None | str | Unset): Given name; omitted, it is not touched
            last_name (None | str | Unset): Family name; omitted, it is not touched
    """

    email: None | str | Unset = UNSET
    first_name: None | str | Unset = UNSET
    last_name: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        participant_update = cls(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        return participant_update
