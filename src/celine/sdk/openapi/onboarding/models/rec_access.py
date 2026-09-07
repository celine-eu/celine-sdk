from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RecAccess")


@_attrs_define
class RecAccess:
    """
    Attributes:
        capabilities (list[str]):
        name (str):
        organization (None | str):
        slug (str):
    """

    capabilities: list[str]
    name: str
    organization: None | str
    slug: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        capabilities = self.capabilities

        name = self.name

        organization: None | str
        organization = self.organization

        slug = self.slug

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "capabilities": capabilities,
                "name": name,
                "organization": organization,
                "slug": slug,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        capabilities = cast(list[str], d.pop("capabilities"))

        name = d.pop("name")

        def _parse_organization(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        organization = _parse_organization(d.pop("organization"))

        slug = d.pop("slug")

        rec_access = cls(
            capabilities=capabilities,
            name=name,
            organization=organization,
            slug=slug,
        )

        rec_access.additional_properties = d
        return rec_access

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
