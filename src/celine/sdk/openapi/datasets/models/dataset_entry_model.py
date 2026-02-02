from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.backend_config import BackendConfig
    from ..models.lineage import Lineage
    from ..models.tags import Tags


T = TypeVar("T", bound="DatasetEntryModel")


@_attrs_define
class DatasetEntryModel:
    """
    Attributes:
        backend_type (str):
        dataset_id (str):
        title (str):
        access_level (None | str | Unset):
        backend_config (BackendConfig | Unset): Backend configuration block for dataset storage.
        description (None | str | Unset):
        expose (bool | Unset):  Default: False.
        landing_page (None | str | Unset):
        language_uris (list[str] | None | Unset):
        license_uri (None | str | Unset):
        lineage (Lineage | None | Unset):
        ontology_path (None | str | Unset):
        publisher_uri (None | str | Unset):
        rights_holder_uri (None | str | Unset):
        schema_override_path (None | str | Unset):
        spatial_uris (list[str] | None | Unset):
        tags (None | Tags | Unset):
    """

    backend_type: str
    dataset_id: str
    title: str
    access_level: None | str | Unset = UNSET
    backend_config: BackendConfig | Unset = UNSET
    description: None | str | Unset = UNSET
    expose: bool | Unset = False
    landing_page: None | str | Unset = UNSET
    language_uris: list[str] | None | Unset = UNSET
    license_uri: None | str | Unset = UNSET
    lineage: Lineage | None | Unset = UNSET
    ontology_path: None | str | Unset = UNSET
    publisher_uri: None | str | Unset = UNSET
    rights_holder_uri: None | str | Unset = UNSET
    schema_override_path: None | str | Unset = UNSET
    spatial_uris: list[str] | None | Unset = UNSET
    tags: None | Tags | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.lineage import Lineage
        from ..models.tags import Tags

        backend_type = self.backend_type

        dataset_id = self.dataset_id

        title = self.title

        access_level: None | str | Unset
        if isinstance(self.access_level, Unset):
            access_level = UNSET
        else:
            access_level = self.access_level

        backend_config: dict[str, Any] | Unset = UNSET
        if not isinstance(self.backend_config, Unset):
            backend_config = self.backend_config.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        expose = self.expose

        landing_page: None | str | Unset
        if isinstance(self.landing_page, Unset):
            landing_page = UNSET
        else:
            landing_page = self.landing_page

        language_uris: list[str] | None | Unset
        if isinstance(self.language_uris, Unset):
            language_uris = UNSET
        elif isinstance(self.language_uris, list):
            language_uris = self.language_uris

        else:
            language_uris = self.language_uris

        license_uri: None | str | Unset
        if isinstance(self.license_uri, Unset):
            license_uri = UNSET
        else:
            license_uri = self.license_uri

        lineage: dict[str, Any] | None | Unset
        if isinstance(self.lineage, Unset):
            lineage = UNSET
        elif isinstance(self.lineage, Lineage):
            lineage = self.lineage.to_dict()
        else:
            lineage = self.lineage

        ontology_path: None | str | Unset
        if isinstance(self.ontology_path, Unset):
            ontology_path = UNSET
        else:
            ontology_path = self.ontology_path

        publisher_uri: None | str | Unset
        if isinstance(self.publisher_uri, Unset):
            publisher_uri = UNSET
        else:
            publisher_uri = self.publisher_uri

        rights_holder_uri: None | str | Unset
        if isinstance(self.rights_holder_uri, Unset):
            rights_holder_uri = UNSET
        else:
            rights_holder_uri = self.rights_holder_uri

        schema_override_path: None | str | Unset
        if isinstance(self.schema_override_path, Unset):
            schema_override_path = UNSET
        else:
            schema_override_path = self.schema_override_path

        spatial_uris: list[str] | None | Unset
        if isinstance(self.spatial_uris, Unset):
            spatial_uris = UNSET
        elif isinstance(self.spatial_uris, list):
            spatial_uris = self.spatial_uris

        else:
            spatial_uris = self.spatial_uris

        tags: dict[str, Any] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, Tags):
            tags = self.tags.to_dict()
        else:
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backend_type": backend_type,
                "dataset_id": dataset_id,
                "title": title,
            }
        )
        if access_level is not UNSET:
            field_dict["access_level"] = access_level
        if backend_config is not UNSET:
            field_dict["backend_config"] = backend_config
        if description is not UNSET:
            field_dict["description"] = description
        if expose is not UNSET:
            field_dict["expose"] = expose
        if landing_page is not UNSET:
            field_dict["landing_page"] = landing_page
        if language_uris is not UNSET:
            field_dict["language_uris"] = language_uris
        if license_uri is not UNSET:
            field_dict["license_uri"] = license_uri
        if lineage is not UNSET:
            field_dict["lineage"] = lineage
        if ontology_path is not UNSET:
            field_dict["ontology_path"] = ontology_path
        if publisher_uri is not UNSET:
            field_dict["publisher_uri"] = publisher_uri
        if rights_holder_uri is not UNSET:
            field_dict["rights_holder_uri"] = rights_holder_uri
        if schema_override_path is not UNSET:
            field_dict["schema_override_path"] = schema_override_path
        if spatial_uris is not UNSET:
            field_dict["spatial_uris"] = spatial_uris
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backend_config import BackendConfig
        from ..models.lineage import Lineage
        from ..models.tags import Tags

        d = dict(src_dict)
        backend_type = d.pop("backend_type")

        dataset_id = d.pop("dataset_id")

        title = d.pop("title")

        def _parse_access_level(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        access_level = _parse_access_level(d.pop("access_level", UNSET))

        _backend_config = d.pop("backend_config", UNSET)
        backend_config: BackendConfig | Unset
        if isinstance(_backend_config, Unset):
            backend_config = UNSET
        else:
            backend_config = BackendConfig.from_dict(_backend_config)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        expose = d.pop("expose", UNSET)

        def _parse_landing_page(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        landing_page = _parse_landing_page(d.pop("landing_page", UNSET))

        def _parse_language_uris(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                language_uris_type_0 = cast(list[str], data)

                return language_uris_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        language_uris = _parse_language_uris(d.pop("language_uris", UNSET))

        def _parse_license_uri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        license_uri = _parse_license_uri(d.pop("license_uri", UNSET))

        def _parse_lineage(data: object) -> Lineage | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                lineage_type_0 = Lineage.from_dict(data)

                return lineage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Lineage | None | Unset, data)

        lineage = _parse_lineage(d.pop("lineage", UNSET))

        def _parse_ontology_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ontology_path = _parse_ontology_path(d.pop("ontology_path", UNSET))

        def _parse_publisher_uri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        publisher_uri = _parse_publisher_uri(d.pop("publisher_uri", UNSET))

        def _parse_rights_holder_uri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rights_holder_uri = _parse_rights_holder_uri(d.pop("rights_holder_uri", UNSET))

        def _parse_schema_override_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        schema_override_path = _parse_schema_override_path(d.pop("schema_override_path", UNSET))

        def _parse_spatial_uris(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                spatial_uris_type_0 = cast(list[str], data)

                return spatial_uris_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        spatial_uris = _parse_spatial_uris(d.pop("spatial_uris", UNSET))

        def _parse_tags(data: object) -> None | Tags | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tags_type_0 = Tags.from_dict(data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Tags | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        dataset_entry_model = cls(
            backend_type=backend_type,
            dataset_id=dataset_id,
            title=title,
            access_level=access_level,
            backend_config=backend_config,
            description=description,
            expose=expose,
            landing_page=landing_page,
            language_uris=language_uris,
            license_uri=license_uri,
            lineage=lineage,
            ontology_path=ontology_path,
            publisher_uri=publisher_uri,
            rights_holder_uri=rights_holder_uri,
            schema_override_path=schema_override_path,
            spatial_uris=spatial_uris,
            tags=tags,
        )

        dataset_entry_model.additional_properties = d
        return dataset_entry_model

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
