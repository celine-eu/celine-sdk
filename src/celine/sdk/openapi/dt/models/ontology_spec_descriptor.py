from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OntologySpecDescriptor")


@_attrs_define
class OntologySpecDescriptor:
    """Metadata about a single ontology spec, for the listing endpoint.

    Attributes:
        description (str):
        fetcher_ids (list[str]):
        id (str):
    """

    description: str
    fetcher_ids: list[str]
    id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        fetcher_ids = self.fetcher_ids

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "fetcher_ids": fetcher_ids,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        fetcher_ids = cast(list[str], d.pop("fetcher_ids"))

        id = d.pop("id")

        ontology_spec_descriptor = cls(
            description=description,
            fetcher_ids=fetcher_ids,
            id=id,
        )

        ontology_spec_descriptor.additional_properties = d
        return ontology_spec_descriptor

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
