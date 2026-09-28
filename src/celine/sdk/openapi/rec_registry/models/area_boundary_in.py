from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AreaBoundaryIn")


@_attrs_define
class AreaBoundaryIn:
    """The primary-substation boundary an area references (REQ-0067, schema v0.7).

    `source` names the boundary dataset (`gse_cabine_primarie`), `id` the
    substation code within it (`cod_ac`). Both are plain strings so that a wrong
    value is refused with the code `invalid_area_boundary` rather than as a
    validation error (REQ-0073); the registry never checks `id` against the
    dataset, which it cannot read.

        Attributes:
            id (str): The substation code (`cod_ac`); equal to the id of the area's one `primary_substation` topology node.
                At most 64 characters; a longer one is refused with `invalid_area_boundary`.
            source (str): The boundary dataset: `gse_cabine_primarie`.
    """

    id: str
    source: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        source = self.source

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        source = d.pop("source")

        area_boundary_in = cls(
            id=id,
            source=source,
        )

        return area_boundary_in
