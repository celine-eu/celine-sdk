from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AcceptanceRead")


@_attrs_define
class AcceptanceRead:
    """One document the member accepted at application, as it was shown to them.

    ``slot`` is onboarding's; ``legal_slot`` is the legal host's (`gdpr` is `privacy`),
    so a reader matches it against `current.json` without knowing onboarding's names.
    ``terms_clauses`` is the specific approval of the terms' clauses, on the terms' own
    document: its own entry, never implied by ``terms``.

        Attributes:
            legal_slot (str):
            slot (str):
            version (str):
            accepted_at (datetime.datetime | None | Unset):
            sha256 (None | str | Unset):
            url (None | str | Unset):
    """

    legal_slot: str
    slot: str
    version: str
    accepted_at: datetime.datetime | None | Unset = UNSET
    sha256: None | str | Unset = UNSET
    url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        legal_slot = self.legal_slot

        slot = self.slot

        version = self.version

        accepted_at: None | str | Unset
        if isinstance(self.accepted_at, Unset):
            accepted_at = UNSET
        elif isinstance(self.accepted_at, datetime.datetime):
            accepted_at = self.accepted_at.isoformat()
        else:
            accepted_at = self.accepted_at

        sha256: None | str | Unset
        if isinstance(self.sha256, Unset):
            sha256 = UNSET
        else:
            sha256 = self.sha256

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "legal_slot": legal_slot,
                "slot": slot,
                "version": version,
            }
        )
        if accepted_at is not UNSET:
            field_dict["accepted_at"] = accepted_at
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        legal_slot = d.pop("legal_slot")

        slot = d.pop("slot")

        version = d.pop("version")

        def _parse_accepted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                accepted_at_type_0 = isoparse(data)

                return accepted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        accepted_at = _parse_accepted_at(d.pop("accepted_at", UNSET))

        def _parse_sha256(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sha256 = _parse_sha256(d.pop("sha256", UNSET))

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        acceptance_read = cls(
            legal_slot=legal_slot,
            slot=slot,
            version=version,
            accepted_at=accepted_at,
            sha256=sha256,
            url=url,
        )

        acceptance_read.additional_properties = d
        return acceptance_read

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
