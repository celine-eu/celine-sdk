from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.topology_node_in_area_type_0 import TopologyNodeInAreaType0


T = TypeVar("T", bound="TopologyNodeIn")


@_attrs_define
class TopologyNodeIn:
    """Grid topology node (substation, transformer, etc.).

    Attributes:
        id (str):
        type_ (str):
        name (None | str | Unset):
        operator_id (None | str | Unset):
        parent (None | str | Unset):
        area (None | TopologyNodeInAreaType0 | Unset):
    """

    id: str
    type_: str
    name: None | str | Unset = UNSET
    operator_id: None | str | Unset = UNSET
    parent: None | str | Unset = UNSET
    area: None | TopologyNodeInAreaType0 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.topology_node_in_area_type_0 import TopologyNodeInAreaType0

        id = self.id

        type_ = self.type_

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        operator_id: None | str | Unset
        if isinstance(self.operator_id, Unset):
            operator_id = UNSET
        else:
            operator_id = self.operator_id

        parent: None | str | Unset
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        area: dict[str, Any] | None | Unset
        if isinstance(self.area, Unset):
            area = UNSET
        elif isinstance(self.area, TopologyNodeInAreaType0):
            area = self.area.to_dict()
        else:
            area = self.area

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if operator_id is not UNSET:
            field_dict["operator_id"] = operator_id
        if parent is not UNSET:
            field_dict["parent"] = parent
        if area is not UNSET:
            field_dict["area"] = area

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.topology_node_in_area_type_0 import TopologyNodeInAreaType0

        d = dict(src_dict)
        id = d.pop("id")

        type_ = d.pop("type")

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_operator_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        operator_id = _parse_operator_id(d.pop("operator_id", UNSET))

        def _parse_parent(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent = _parse_parent(d.pop("parent", UNSET))

        def _parse_area(data: object) -> None | TopologyNodeInAreaType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                area_type_0 = TopologyNodeInAreaType0.from_dict(data)

                return area_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | TopologyNodeInAreaType0 | Unset, data)

        area = _parse_area(d.pop("area", UNSET))

        topology_node_in = cls(
            id=id,
            type_=type_,
            name=name,
            operator_id=operator_id,
            parent=parent,
            area=area,
        )

        topology_node_in.additional_properties = d
        return topology_node_in

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
