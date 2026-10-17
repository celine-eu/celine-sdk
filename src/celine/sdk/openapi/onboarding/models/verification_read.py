from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.verification_method import VerificationMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evidence_digest import EvidenceDigest


T = TypeVar("T", bound="VerificationRead")


@_attrs_define
class VerificationRead:
    """
    Attributes:
        actor_email (None | str):
        actor_sub (None | str):
        actor_type (str):
        created_at (datetime.datetime):
        document_id (None | UUID):
        id (UUID):
        method (VerificationMethod):
        note (None | str):
        evidence (list[EvidenceDigest] | None | Unset):
        last_asserted_at (datetime.datetime | None | Unset):
    """

    actor_email: None | str
    actor_sub: None | str
    actor_type: str
    created_at: datetime.datetime
    document_id: None | UUID
    id: UUID
    method: VerificationMethod
    note: None | str
    evidence: list[EvidenceDigest] | None | Unset = UNSET
    last_asserted_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actor_email: None | str
        actor_email = self.actor_email

        actor_sub: None | str
        actor_sub = self.actor_sub

        actor_type = self.actor_type

        created_at = self.created_at.isoformat()

        document_id: None | str
        if isinstance(self.document_id, UUID):
            document_id = str(self.document_id)
        else:
            document_id = self.document_id

        id = str(self.id)

        method = self.method.value

        note: None | str
        note = self.note

        evidence: list[dict[str, Any]] | None | Unset
        if isinstance(self.evidence, Unset):
            evidence = UNSET
        elif isinstance(self.evidence, list):
            evidence = []
            for evidence_type_0_item_data in self.evidence:
                evidence_type_0_item = evidence_type_0_item_data.to_dict()
                evidence.append(evidence_type_0_item)

        else:
            evidence = self.evidence

        last_asserted_at: None | str | Unset
        if isinstance(self.last_asserted_at, Unset):
            last_asserted_at = UNSET
        elif isinstance(self.last_asserted_at, datetime.datetime):
            last_asserted_at = self.last_asserted_at.isoformat()
        else:
            last_asserted_at = self.last_asserted_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actor_email": actor_email,
                "actor_sub": actor_sub,
                "actor_type": actor_type,
                "created_at": created_at,
                "document_id": document_id,
                "id": id,
                "method": method,
                "note": note,
            }
        )
        if evidence is not UNSET:
            field_dict["evidence"] = evidence
        if last_asserted_at is not UNSET:
            field_dict["last_asserted_at"] = last_asserted_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evidence_digest import EvidenceDigest

        d = dict(src_dict)

        def _parse_actor_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_email = _parse_actor_email(d.pop("actor_email"))

        def _parse_actor_sub(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        actor_sub = _parse_actor_sub(d.pop("actor_sub"))

        actor_type = d.pop("actor_type")

        created_at = isoparse(d.pop("created_at"))

        def _parse_document_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                document_id_type_0 = UUID(data)

                return document_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | UUID, data)

        document_id = _parse_document_id(d.pop("document_id"))

        id = UUID(d.pop("id"))

        method = VerificationMethod(d.pop("method"))

        def _parse_note(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        note = _parse_note(d.pop("note"))

        def _parse_evidence(data: object) -> list[EvidenceDigest] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                evidence_type_0 = []
                _evidence_type_0 = data
                for evidence_type_0_item_data in _evidence_type_0:
                    evidence_type_0_item = EvidenceDigest.from_dict(evidence_type_0_item_data)

                    evidence_type_0.append(evidence_type_0_item)

                return evidence_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[EvidenceDigest] | None | Unset, data)

        evidence = _parse_evidence(d.pop("evidence", UNSET))

        def _parse_last_asserted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_asserted_at_type_0 = isoparse(data)

                return last_asserted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_asserted_at = _parse_last_asserted_at(d.pop("last_asserted_at", UNSET))

        verification_read = cls(
            actor_email=actor_email,
            actor_sub=actor_sub,
            actor_type=actor_type,
            created_at=created_at,
            document_id=document_id,
            id=id,
            method=method,
            note=note,
            evidence=evidence,
            last_asserted_at=last_asserted_at,
        )

        verification_read.additional_properties = d
        return verification_read

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
