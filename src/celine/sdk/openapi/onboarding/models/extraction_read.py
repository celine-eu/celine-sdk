from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.extracted_data import ExtractedData


T = TypeVar("T", bound="ExtractionRead")


@_attrs_define
class ExtractionRead:
    """
    Attributes:
        confirmed_at (datetime.datetime | None):
        confirmed_by_user (bool):
        created_at (datetime.datetime):
        document_id (UUID):
        extracted_data (ExtractedData):
        id (UUID):
    """

    confirmed_at: datetime.datetime | None
    confirmed_by_user: bool
    created_at: datetime.datetime
    document_id: UUID
    extracted_data: ExtractedData
    id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        confirmed_at: None | str
        if isinstance(self.confirmed_at, datetime.datetime):
            confirmed_at = self.confirmed_at.isoformat()
        else:
            confirmed_at = self.confirmed_at

        confirmed_by_user = self.confirmed_by_user

        created_at = self.created_at.isoformat()

        document_id = str(self.document_id)

        extracted_data = self.extracted_data.to_dict()

        id = str(self.id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "confirmed_at": confirmed_at,
                "confirmed_by_user": confirmed_by_user,
                "created_at": created_at,
                "document_id": document_id,
                "extracted_data": extracted_data,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.extracted_data import ExtractedData

        d = dict(src_dict)

        def _parse_confirmed_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                confirmed_at_type_0 = isoparse(data)

                return confirmed_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        confirmed_at = _parse_confirmed_at(d.pop("confirmed_at"))

        confirmed_by_user = d.pop("confirmed_by_user")

        created_at = isoparse(d.pop("created_at"))

        document_id = UUID(d.pop("document_id"))

        extracted_data = ExtractedData.from_dict(d.pop("extracted_data"))

        id = UUID(d.pop("id"))

        extraction_read = cls(
            confirmed_at=confirmed_at,
            confirmed_by_user=confirmed_by_user,
            created_at=created_at,
            document_id=document_id,
            extracted_data=extracted_data,
            id=id,
        )

        extraction_read.additional_properties = d
        return extraction_read

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
