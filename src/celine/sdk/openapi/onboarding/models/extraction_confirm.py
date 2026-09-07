from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extraction_confirm_extracted_data_type_0 import ExtractionConfirmExtractedDataType0


T = TypeVar("T", bound="ExtractionConfirm")


@_attrs_define
class ExtractionConfirm:
    """
    Attributes:
        extracted_data (ExtractionConfirmExtractedDataType0 | None | Unset):
    """

    extracted_data: ExtractionConfirmExtractedDataType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.extraction_confirm_extracted_data_type_0 import ExtractionConfirmExtractedDataType0

        extracted_data: dict[str, Any] | None | Unset
        if isinstance(self.extracted_data, Unset):
            extracted_data = UNSET
        elif isinstance(self.extracted_data, ExtractionConfirmExtractedDataType0):
            extracted_data = self.extracted_data.to_dict()
        else:
            extracted_data = self.extracted_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if extracted_data is not UNSET:
            field_dict["extracted_data"] = extracted_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.extraction_confirm_extracted_data_type_0 import ExtractionConfirmExtractedDataType0

        d = dict(src_dict)

        def _parse_extracted_data(data: object) -> ExtractionConfirmExtractedDataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extracted_data_type_0 = ExtractionConfirmExtractedDataType0.from_dict(data)

                return extracted_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ExtractionConfirmExtractedDataType0 | None | Unset, data)

        extracted_data = _parse_extracted_data(d.pop("extracted_data", UNSET))

        extraction_confirm = cls(
            extracted_data=extracted_data,
        )

        extraction_confirm.additional_properties = d
        return extraction_confirm

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
