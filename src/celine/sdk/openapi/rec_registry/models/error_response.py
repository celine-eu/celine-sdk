from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_code import ErrorCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """The body of a refusal that carries a code.

    Attributes:
        detail (str): A sentence for people. Its wording is not part of the API; branch on `code`.
        code (ErrorCode | None | Unset): The rule the request broke, from a closed list (REQ-0073). Absent only on a
            refusal no requirement has given a code yet.
    """

    detail: str
    code: ErrorCode | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        code: None | str | Unset
        if isinstance(self.code, Unset):
            code = UNSET
        elif isinstance(self.code, ErrorCode):
            code = self.code.value
        else:
            code = self.code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )
        if code is not UNSET:
            field_dict["code"] = code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail")

        def _parse_code(data: object) -> ErrorCode | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                code_type_0 = ErrorCode(data)

                return code_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ErrorCode | None | Unset, data)

        code = _parse_code(d.pop("code", UNSET))

        error_response = cls(
            detail=detail,
            code=code,
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
