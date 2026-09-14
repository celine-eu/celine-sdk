from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.error_detail import ErrorDetail


T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """`{"detail": {"code": "...", "message": "..."}}`.

    `detail` stays the top-level key, so a consumer that already reads
    `detail` keeps finding it; it is an object rather than a string.

        Attributes:
            detail (ErrorDetail): `detail` in every error body except `422`, which is FastAPI's own list.

                `message` is the service's sentence, naming the member or the scope. It is
                for a log or an operator, and it is not a contract.

                **`code` is a string, not an enum, on purpose.** A generated client turns an
                enum into a strict type that raises on a value it has never seen, so every
                new code would break every consumer that has not regenerated — on the error
                path, where a crash hides the refusal it was meant to report. The codes are
                listed in the description and in `docs/api-reference.md`.
    """

    detail: ErrorDetail
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_detail import ErrorDetail

        d = dict(src_dict)
        detail = ErrorDetail.from_dict(d.pop("detail"))

        error_response = cls(
            detail=detail,
        )

        error_response.additional_properties = d
        return error_response

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
