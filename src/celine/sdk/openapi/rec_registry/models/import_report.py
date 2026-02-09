from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.deleted import Deleted
    from ..models.inserted import Inserted


T = TypeVar("T", bound="ImportReport")


@_attrs_define
class ImportReport:
    """Import operation report.

    Attributes:
        community_key (str):
        deleted (Deleted | Unset):
        inserted (Inserted | Unset):
        warnings (list[str] | Unset):
    """

    community_key: str
    deleted: Deleted | Unset = UNSET
    inserted: Inserted | Unset = UNSET
    warnings: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community_key = self.community_key

        deleted: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deleted, Unset):
            deleted = self.deleted.to_dict()

        inserted: dict[str, Any] | Unset = UNSET
        if not isinstance(self.inserted, Unset):
            inserted = self.inserted.to_dict()

        warnings: list[str] | Unset = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community_key": community_key,
            }
        )
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if inserted is not UNSET:
            field_dict["inserted"] = inserted
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.deleted import Deleted
        from ..models.inserted import Inserted

        d = dict(src_dict)
        community_key = d.pop("community_key")

        _deleted = d.pop("deleted", UNSET)
        deleted: Deleted | Unset
        if isinstance(_deleted, Unset):
            deleted = UNSET
        else:
            deleted = Deleted.from_dict(_deleted)

        _inserted = d.pop("inserted", UNSET)
        inserted: Inserted | Unset
        if isinstance(_inserted, Unset):
            inserted = UNSET
        else:
            inserted = Inserted.from_dict(_inserted)

        warnings = cast(list[str], d.pop("warnings", UNSET))

        import_report = cls(
            community_key=community_key,
            deleted=deleted,
            inserted=inserted,
            warnings=warnings,
        )

        import_report.additional_properties = d
        return import_report

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
