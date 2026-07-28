from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.community_in import CommunityIn
    from ..models.members import Members
    from ..models.metadata_in import MetadataIn


T = TypeVar("T", bound="RegistryBundleIn")


@_attrs_define
class RegistryBundleIn:
    """Complete registry bundle for import.

    Matches v0.4 structure.

        Attributes:
            community (CommunityIn): Community definition.
            version (str | Unset):  Default: '1.0'.
            schema_version (str | Unset):  Default: '1.0'.
            metadata (MetadataIn | None | Unset):
            members (Members | Unset):
    """

    community: CommunityIn
    version: str | Unset = "1.0"
    schema_version: str | Unset = "1.0"
    metadata: MetadataIn | None | Unset = UNSET
    members: Members | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metadata_in import MetadataIn

        community = self.community.to_dict()

        version = self.version

        schema_version = self.schema_version

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, MetadataIn):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        members: dict[str, Any] | Unset = UNSET
        if not isinstance(self.members, Unset):
            members = self.members.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community": community,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if members is not UNSET:
            field_dict["members"] = members

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.community_in import CommunityIn
        from ..models.members import Members
        from ..models.metadata_in import MetadataIn

        d = dict(src_dict)
        community = CommunityIn.from_dict(d.pop("community"))

        version = d.pop("version", UNSET)

        schema_version = d.pop("schema_version", UNSET)

        def _parse_metadata(data: object) -> MetadataIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = MetadataIn.from_dict(data)

                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MetadataIn | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        _members = d.pop("members", UNSET)
        members: Members | Unset
        if isinstance(_members, Unset):
            members = UNSET
        else:
            members = Members.from_dict(_members)

        registry_bundle_in = cls(
            community=community,
            version=version,
            schema_version=schema_version,
            metadata=metadata,
            members=members,
        )

        registry_bundle_in.additional_properties = d
        return registry_bundle_in

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
