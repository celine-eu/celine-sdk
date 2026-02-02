from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.resource_type import ResourceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attributes import Attributes


T = TypeVar("T", bound="Resource")


@_attrs_define
class Resource:
    """Represents the resource being accessed.

    Attributes:
        id (str): Resource identifier
        type_ (ResourceType): Types of resources that can be authorized.
        attributes (Attributes | Unset): Resource-specific attributes
    """

    id: str
    type_: ResourceType
    attributes: Attributes | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_.value

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.attributes import Attributes

        d = dict(src_dict)
        id = d.pop("id")

        type_ = ResourceType(d.pop("type"))

        _attributes = d.pop("attributes", UNSET)
        attributes: Attributes | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = Attributes.from_dict(_attributes)

        resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        resource.additional_properties = d
        return resource

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
