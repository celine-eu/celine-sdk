from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.area_in_geometry_type_0 import AreaInGeometryType0
    from ..models.location_in import LocationIn


T = TypeVar("T", bound="AreaIn")


@_attrs_define
class AreaIn:
    """Community area definition.

    Attributes:
        name (str):
        geometry (AreaInGeometryType0 | None | Unset):
        location (LocationIn | None | Unset):
        topology (list[str] | Unset):
    """

    name: str
    geometry: AreaInGeometryType0 | None | Unset = UNSET
    location: LocationIn | None | Unset = UNSET
    topology: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.area_in_geometry_type_0 import AreaInGeometryType0
        from ..models.location_in import LocationIn

        name = self.name

        geometry: dict[str, Any] | None | Unset
        if isinstance(self.geometry, Unset):
            geometry = UNSET
        elif isinstance(self.geometry, AreaInGeometryType0):
            geometry = self.geometry.to_dict()
        else:
            geometry = self.geometry

        location: dict[str, Any] | None | Unset
        if isinstance(self.location, Unset):
            location = UNSET
        elif isinstance(self.location, LocationIn):
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
        if geometry is not UNSET:
            field_dict["geometry"] = geometry
        if location is not UNSET:
            field_dict["location"] = location
        if topology is not UNSET:
            field_dict["topology"] = topology

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.area_in_geometry_type_0 import AreaInGeometryType0
        from ..models.location_in import LocationIn

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_geometry(data: object) -> AreaInGeometryType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0 = AreaInGeometryType0.from_dict(data)

                return geometry_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AreaInGeometryType0 | None | Unset, data)

        geometry = _parse_geometry(d.pop("geometry", UNSET))

        def _parse_location(data: object) -> LocationIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = LocationIn.from_dict(data)

                return location_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LocationIn | None | Unset, data)

        location = _parse_location(d.pop("location", UNSET))

        topology = cast(list[str], d.pop("topology", UNSET))

        area_in = cls(
            name=name,
            geometry=geometry,
            location=location,
            topology=topology,
        )

        area_in.additional_properties = d
        return area_in

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
