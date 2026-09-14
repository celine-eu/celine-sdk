from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ErrorDetail")


@_attrs_define
class ErrorDetail:
    """`detail` in every error body except `422`, which is FastAPI's own list.

    `message` is the service's sentence, naming the member or the scope. It is
    for a log or an operator, and it is not a contract.

    **`code` is a string, not an enum, on purpose.** A generated client turns an
    enum into a strict type that raises on a value it has never seen, so every
    new code would break every consumer that has not regenerated — on the error
    path, where a crash hides the refusal it was meant to report. The codes are
    listed in the description and in `docs/api-reference.md`.

        Attributes:
            code (str): Stable machine-readable reason: `missing_token`, `invalid_token`, `insufficient_scope`,
                `community_not_found`, `member_not_found`, `account_not_found`, `account_disabled`, `has_password`,
                `no_password`, `no_email`, `cooldown`, `reconcile_diverged`, `registry_unavailable`, `send_failed`,
                `provisioning_failed`. New codes may be added: branch on the HTTP status for one you do not know.
            message (str): A human sentence. Not a contract.
    """

    code: str
    message: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        message = d.pop("message")

        error_detail = cls(
            code=code,
            message=message,
        )

        error_detail.additional_properties = d
        return error_detail

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
