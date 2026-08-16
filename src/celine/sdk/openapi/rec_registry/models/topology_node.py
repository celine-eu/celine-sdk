from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.topology_node_area import TopologyNodeArea


T = TypeVar("T", bound="TopologyNode")


@_attrs_define
class TopologyNode:
    """
    Attributes:
        id (str):
        type_ (str):
        area (TopologyNodeArea | Unset):
        name (None | str | Unset):
        operator (None | str | Unset):
        parent (None | str | Unset):
    """

    id: str
    type_: str
    area: TopologyNodeArea | Unset = UNSET
    name: None | str | Unset = UNSET
    operator: None | str | Unset = UNSET
    parent: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        area: dict[str, Any] | Unset = UNSET
        if not isinstance(self.area, Unset):
            area = self.area.to_dict()

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        operator: None | str | Unset
        if isinstance(self.operator, Unset):
            operator = UNSET
        else:
            operator = self.operator

        parent: None | str | Unset
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )
        if area is not UNSET:
            field_dict["area"] = area
        if name is not UNSET:
            field_dict["name"] = name
        if operator is not UNSET:
            field_dict["operator"] = operator
        if parent is not UNSET:
            field_dict["parent"] = parent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.topology_node_area import TopologyNodeArea

        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        _area = d.pop("area", UNSET)
        area: TopologyNodeArea | Unset
        if isinstance(_area, Unset):
            area = UNSET
        else:
            area = TopologyNodeArea.from_dict(_area)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_operator(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        operator = _parse_operator(d.pop("operator", UNSET))

        def _parse_parent(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent = _parse_parent(d.pop("parent", UNSET))

        topology_node = cls(
            id=id,
            type_=type_,
            area=area,
            name=name,
            operator=operator,
            parent=parent,
        )

        topology_node.additional_properties = d
        return topology_node

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
