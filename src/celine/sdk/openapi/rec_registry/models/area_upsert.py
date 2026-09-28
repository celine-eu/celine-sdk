from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.area_boundary_in import AreaBoundaryIn
    from ..models.area_upsert_geometry_type_0 import AreaUpsertGeometryType0
    from ..models.location import Location


T = TypeVar("T", bound="AreaUpsert")


@_attrs_define
class AreaUpsert:
    """Create or replace one area of a community.

    One primary substation (REQ-0067): `boundary` references it and `topology`
    lists exactly one node id, `boundary.id`, a `primary_substation` node of
    the community's topology. Anything else — no boundary, a list of them or a
    malformed one included — is `422 invalid_area_boundary`; `boundary`
    accepts anything in the model only so that each of those is refused with
    that code rather than as a validation error.

        Attributes:
            name (str):
            boundary (AreaBoundaryIn | Unset): The primary-substation boundary an area references (REQ-0067, schema v0.7).

                `source` names the boundary dataset (`gse_cabine_primarie`), `id` the
                substation code within it (`cod_ac`). Both are plain strings so that a wrong
                value is refused with the code `invalid_area_boundary` rather than as a
                validation error (REQ-0073); the registry never checks `id` against the
                dataset, which it cannot read.
            geometry (AreaUpsertGeometryType0 | None | Unset):
            location (Location | None | Unset):
            topology (list[str] | Unset): Exactly one node id: `boundary.id`.
    """

    name: str
    boundary: AreaBoundaryIn | Unset = UNSET
    geometry: AreaUpsertGeometryType0 | None | Unset = UNSET
    location: Location | None | Unset = UNSET
    topology: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.area_upsert_geometry_type_0 import AreaUpsertGeometryType0
        from ..models.location import Location

        name = self.name

        boundary: dict[str, Any] | Unset = UNSET
        if not isinstance(self.boundary, Unset):
            boundary = self.boundary.to_dict()

        geometry: dict[str, Any] | None | Unset
        if isinstance(self.geometry, Unset):
            geometry = UNSET
        elif isinstance(self.geometry, AreaUpsertGeometryType0):
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
        from ..models.area_boundary_in import AreaBoundaryIn
        from ..models.area_upsert_geometry_type_0 import AreaUpsertGeometryType0
        from ..models.location import Location

        d = dict(src_dict)
        name = d.pop("name")

        _boundary = d.pop("boundary", UNSET)
        boundary: AreaBoundaryIn | Unset
        if isinstance(_boundary, Unset):
            boundary = UNSET
        else:
            boundary = AreaBoundaryIn.from_dict(_boundary)

        def _parse_geometry(data: object) -> AreaUpsertGeometryType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                geometry_type_0 = AreaUpsertGeometryType0.from_dict(data)

                return geometry_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AreaUpsertGeometryType0 | None | Unset, data)

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

        area_upsert = cls(
            name=name,
            boundary=boundary,
            geometry=geometry,
            location=location,
            topology=topology,
        )

        area_upsert.additional_properties = d
        return area_upsert

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
