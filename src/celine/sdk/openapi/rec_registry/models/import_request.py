from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.registry_bundle_in import RegistryBundleIn


T = TypeVar("T", bound="ImportRequest")


@_attrs_define
class ImportRequest:
    """Import request payload.

    Attributes:
        bundle (RegistryBundleIn): Complete registry bundle for import.

            Matches v0.4 structure.
        dry_run (bool | Unset):  Default: False.
        force (bool | Unset):  Default: False.
    """

    bundle: RegistryBundleIn
    dry_run: bool | Unset = False
    force: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bundle = self.bundle.to_dict()

        dry_run = self.dry_run

        force = self.force

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bundle": bundle,
            }
        )
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if force is not UNSET:
            field_dict["force"] = force

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.registry_bundle_in import RegistryBundleIn

        d = dict(src_dict)
        bundle = RegistryBundleIn.from_dict(d.pop("bundle"))

        dry_run = d.pop("dry_run", UNSET)

        force = d.pop("force", UNSET)

        import_request = cls(
            bundle=bundle,
            dry_run=dry_run,
            force=force,
        )

        import_request.additional_properties = d
        return import_request

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
