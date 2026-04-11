from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.import_report import ImportReport


T = TypeVar("T", bound="MultiImportReport")


@_attrs_define
class MultiImportReport:
    """Report for a bulk import of multiple bundles.

    Attributes:
        reports (list[ImportReport]):
        dry_run (bool | Unset):  Default: False.
    """

    reports: list[ImportReport]
    dry_run: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reports = []
        for reports_item_data in self.reports:
            reports_item = reports_item_data.to_dict()
            reports.append(reports_item)

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reports": reports,
            }
        )
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.import_report import ImportReport

        d = dict(src_dict)
        reports = []
        _reports = d.pop("reports")
        for reports_item_data in _reports:
            reports_item = ImportReport.from_dict(reports_item_data)

            reports.append(reports_item)

        dry_run = d.pop("dry_run", UNSET)

        multi_import_report = cls(
            reports=reports,
            dry_run=dry_run,
        )

        multi_import_report.additional_properties = d
        return multi_import_report

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
