from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.by_status import ByStatus


T = TypeVar("T", bound="RecStats")


@_attrs_define
class RecStats:
    """
    Attributes:
        by_status (ByStatus):
        rec_slug (str):
        submissions_with_failed_steps (int):
    """

    by_status: ByStatus
    rec_slug: str
    submissions_with_failed_steps: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        by_status = self.by_status.to_dict()

        rec_slug = self.rec_slug

        submissions_with_failed_steps = self.submissions_with_failed_steps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "by_status": by_status,
                "rec_slug": rec_slug,
                "submissions_with_failed_steps": submissions_with_failed_steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.by_status import ByStatus

        d = dict(src_dict)
        by_status = ByStatus.from_dict(d.pop("by_status"))

        rec_slug = d.pop("rec_slug")

        submissions_with_failed_steps = d.pop("submissions_with_failed_steps")

        rec_stats = cls(
            by_status=by_status,
            rec_slug=rec_slug,
            submissions_with_failed_steps=submissions_with_failed_steps,
        )

        rec_stats.additional_properties = d
        return rec_stats

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
