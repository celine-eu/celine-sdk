from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.document_type import DocumentType

T = TypeVar("T", bound="DocumentRead")


@_attrs_define
class DocumentRead:
    """
    Attributes:
        created_at (datetime.datetime):
        doc_type (DocumentType):
        id (UUID):
        mime_type (str):
        original_filename (str):
        size_bytes (int):
        submission_id (UUID):
    """

    created_at: datetime.datetime
    doc_type: DocumentType
    id: UUID
    mime_type: str
    original_filename: str
    size_bytes: int
    submission_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        doc_type = self.doc_type.value

        id = str(self.id)

        mime_type = self.mime_type

        original_filename = self.original_filename

        size_bytes = self.size_bytes

        submission_id = str(self.submission_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "doc_type": doc_type,
                "id": id,
                "mime_type": mime_type,
                "original_filename": original_filename,
                "size_bytes": size_bytes,
                "submission_id": submission_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        doc_type = DocumentType(d.pop("doc_type"))

        id = UUID(d.pop("id"))

        mime_type = d.pop("mime_type")

        original_filename = d.pop("original_filename")

        size_bytes = d.pop("size_bytes")

        submission_id = UUID(d.pop("submission_id"))

        document_read = cls(
            created_at=created_at,
            doc_type=doc_type,
            id=id,
            mime_type=mime_type,
            original_filename=original_filename,
            size_bytes=size_bytes,
            submission_id=submission_id,
        )

        document_read.additional_properties = d
        return document_read

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
