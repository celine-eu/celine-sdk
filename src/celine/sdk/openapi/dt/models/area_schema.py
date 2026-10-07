from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.area_boundary_schema import AreaBoundarySchema
    from ..models.area_schema_geometry_type_0 import AreaSchemaGeometryType0
    from ..models.location_schema import LocationSchema


T = TypeVar("T", bound="AreaSchema")


@_attrs_define
class AreaSchema:
    """
    Attributes:
        name (str):
        boundary (AreaBoundarySchema | None | Unset):
        geometry (AreaSchemaGeometryType0 | None | Unset):
        location (LocationSchema | None | Unset):
        topology (list[str] | None | Unset):
    """

    name: str
    boundary: AreaBoundarySchema | None | Unset = UNSET
    geometry: AreaSchemaGeometryType0 | None | Unset = UNSET
    location: LocationSchema | None | Unset = UNSET
    topology: list[str] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.area_boundary_schema import AreaBoundarySchema
        from ..models.area_schema_geometry_type_0 import AreaSchemaGeometryType0
        from ..models.location_schema import LocationSchema

        name = self.name

        boundary: dict[str, Any] | None | Unset
        if isinstance(self.boundary, Unset):
            boundary = UNSET
        elif isinstance(self.boundary, AreaBoundarySchema):
            boundary = self.boundary.to_dict()
        else:
            boundary = self.boundary

        geometry: dict[str, Any] | None | Unset
        if isinstance(self.geometry, Unset):
            geometry = UNSET
        elif isinstance(self.geometry, AreaSchemaGeometryType0):
            geometry = self.geometry.to_dict()
        else:
            geometry = self.geometry

        location: dict[str, Any] | None | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, LocationSchema):
            location = self.location.to_dict()
        else:
            location = self.location

        topology: list[str] | None | Unset
        if isinstance(self.topology, Unset):
            topology = UNSET
        elif isinstance(self.topology, list):
            topology = self.topology

        else:
            topology = self.topology

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if boundary is not UNSET:
            field_dict["boundary"] = boundary
        if geometry is not UNSET:
            field_dict["geometry"] = geometry
        if location is not UNSET:
            field_dict["location"] = location
        if topology is not UNSET:
            field_dict["topology"] = topology

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.area_boundary_schema import AreaBoundarySchema
        from ..models.area_schema_geometry_type_0 import AreaSchemaGeometryType0
        from ..models.location_schema import LocationSchema

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_boundary(data: object) -> AreaBoundarySchema | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                boundary_type_0 = AreaBoundarySchema.from_dict(data)

                return boundary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AreaBoundarySchema | None | Unset, data)

        boundary = _parse_boundary(d.pop("boundary", UNSET))

        def _parse_geometry(data: object) -> AreaSchemaGeometryType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0 = AreaSchemaGeometryType0.from_dict(data)

                return geometry_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AreaSchemaGeometryType0 | None | Unset, data)

        geometry = _parse_geometry(d.pop("geometry", UNSET))

        def _parse_location(data: object) -> LocationSchema | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = LocationSchema.from_dict(data)

                return location_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LocationSchema | None | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        def _parse_topology(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                topology_type_0 = cast(list[str], data)

                return topology_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        topology = _parse_topology(d.pop("topology", UNSET))

        area_schema = cls(
            name=name,
            boundary=boundary,
            geometry=geometry,
            location=location,
            topology=topology,
        )

        area_schema.additional_properties = d
        return area_schema

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
