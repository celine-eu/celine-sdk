from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.area_boundary import AreaBoundary
    from ..models.area_geometry_type_0 import AreaGeometryType0
    from ..models.location import Location


T = TypeVar("T", bound="Area")


@_attrs_define
class Area:
    """
    Attributes:
        name (str):
        boundary (AreaBoundary | None | Unset):
        geometry (AreaGeometryType0 | None | Unset):
        location (Location | None | Unset):
        topology (list[str] | Unset):
    """

    name: str
    boundary: AreaBoundary | None | Unset = UNSET
    geometry: AreaGeometryType0 | None | Unset = UNSET
    location: Location | None | Unset = UNSET
    topology: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.area_boundary import AreaBoundary
        from ..models.area_geometry_type_0 import AreaGeometryType0
        from ..models.location import Location

        name = self.name

        boundary: dict[str, Any] | None | Unset
        if isinstance(self.boundary, Unset):
            boundary = UNSET
        elif isinstance(self.boundary, AreaBoundary):
            boundary = self.boundary.to_dict()
        else:
            boundary = self.boundary

        geometry: dict[str, Any] | None | Unset
        if isinstance(self.geometry, Unset):
            geometry = UNSET
        elif isinstance(self.geometry, AreaGeometryType0):
            geometry = self.geometry.to_dict()
        else:
            geometry = self.geometry

        location: dict[str, Any] | None | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, Location):
            location = self.location.to_dict()
        else:
            location = self.location

        topology: list[str] | Unset = UNSET
        if not isinstance(self.topology, Unset):
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
        from ..models.area_boundary import AreaBoundary
        from ..models.area_geometry_type_0 import AreaGeometryType0
        from ..models.location import Location

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_boundary(data: object) -> AreaBoundary | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                boundary_type_0 = AreaBoundary.from_dict(data)

                return boundary_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AreaBoundary | None | Unset, data)

        boundary = _parse_boundary(d.pop("boundary", UNSET))

        def _parse_geometry(data: object) -> AreaGeometryType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0 = AreaGeometryType0.from_dict(data)

                return geometry_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AreaGeometryType0 | None | Unset, data)

        geometry = _parse_geometry(d.pop("geometry", UNSET))

        def _parse_location(data: object) -> Location | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = Location.from_dict(data)

                return location_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(Location | None | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        topology = cast(list[str], d.pop("topology", UNSET))

        area = cls(
            name=name,
            boundary=boundary,
            geometry=geometry,
            location=location,
            topology=topology,
        )

        area.additional_properties = d
        return area

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
