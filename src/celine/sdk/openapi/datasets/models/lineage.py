from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.lineage_facets_type_0 import LineageFacetsType0


T = TypeVar("T", bound="Lineage")


@_attrs_define
class Lineage:
    """
    Attributes:
        created_at (None | str | Unset):
        facets (LineageFacetsType0 | None | Unset):
        last_lifecycle_state (None | str | Unset):
        last_modified_at (None | str | Unset):
        name (None | str | Unset):
        namespace (None | str | Unset):
        source_name (None | str | Unset):
        tags (list[str] | None | Unset):
        updated_at (None | str | Unset):
    """

    created_at: None | str | Unset = UNSET
    facets: LineageFacetsType0 | None | Unset = UNSET
    last_lifecycle_state: None | str | Unset = UNSET
    last_modified_at: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    namespace: None | str | Unset = UNSET
    source_name: None | str | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.lineage_facets_type_0 import LineageFacetsType0

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        facets: dict[str, Any] | None | Unset
        if isinstance(self.facets, Unset):
            facets = UNSET
        elif isinstance(self.facets, LineageFacetsType0):
            facets = self.facets.to_dict()
        else:
            facets = self.facets

        last_lifecycle_state: None | str | Unset
        if isinstance(self.last_lifecycle_state, Unset):
            last_lifecycle_state = UNSET
        else:
            last_lifecycle_state = self.last_lifecycle_state

        last_modified_at: None | str | Unset
        if isinstance(self.last_modified_at, Unset):
            last_modified_at = UNSET
        else:
            last_modified_at = self.last_modified_at

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        namespace: None | str | Unset
        if isinstance(self.namespace, Unset):
            namespace = UNSET
        else:
            namespace = self.namespace

        source_name: None | str | Unset
        if isinstance(self.source_name, Unset):
            source_name = UNSET
        else:
            source_name = self.source_name

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if facets is not UNSET:
            field_dict["facets"] = facets
        if last_lifecycle_state is not UNSET:
            field_dict["lastLifecycleState"] = last_lifecycle_state
        if last_modified_at is not UNSET:
            field_dict["lastModifiedAt"] = last_modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if source_name is not UNSET:
            field_dict["sourceName"] = source_name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lineage_facets_type_0 import LineageFacetsType0

        d = dict(src_dict)

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_facets(data: object) -> LineageFacetsType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                facets_type_0 = LineageFacetsType0.from_dict(data)

                return facets_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LineageFacetsType0 | None | Unset, data)

        facets = _parse_facets(d.pop("facets", UNSET))

        def _parse_last_lifecycle_state(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_lifecycle_state = _parse_last_lifecycle_state(d.pop("lastLifecycleState", UNSET))

        def _parse_last_modified_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_modified_at = _parse_last_modified_at(d.pop("lastModifiedAt", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_namespace(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        namespace = _parse_namespace(d.pop("namespace", UNSET))

        def _parse_source_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_name = _parse_source_name(d.pop("sourceName", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updatedAt", UNSET))

        lineage = cls(
            created_at=created_at,
            facets=facets,
            last_lifecycle_state=last_lifecycle_state,
            last_modified_at=last_modified_at,
            name=name,
            namespace=namespace,
            source_name=source_name,
            tags=tags,
            updated_at=updated_at,
        )

        lineage.additional_properties = d
        return lineage

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
