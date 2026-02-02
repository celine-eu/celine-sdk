from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.meter_in_datasets_item import MeterInDatasetsItem
    from ..models.ref import Ref


T = TypeVar("T", bound="MeterIn")


@_attrs_define
class MeterIn:
    """
    Attributes:
        key (str):
        owner (Ref): Generic reference object used in Greenland bundles.
            Example: {"kind":"participant","ref":"p_gl_00002"}
        datasets (list[MeterInDatasetsItem] | Unset):
        iri (None | str | Unset):
        located_at (None | str | Unset):
        name (None | str | Unset):
        pod (None | str | Unset):
        sensor_id (None | str | Unset):
    """

    key: str
    owner: Ref
    datasets: list[MeterInDatasetsItem] | Unset = UNSET
    iri: None | str | Unset = UNSET
    located_at: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    pod: None | str | Unset = UNSET
    sensor_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        owner = self.owner.to_dict()

        datasets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.datasets, Unset):
            datasets = []
            for datasets_item_data in self.datasets:
                datasets_item = datasets_item_data.to_dict()
                datasets.append(datasets_item)

        iri: None | str | Unset
        if isinstance(self.iri, Unset):
            iri = UNSET
        else:
            iri = self.iri

        located_at: None | str | Unset
        if isinstance(self.located_at, Unset):
            located_at = UNSET
        else:
            located_at = self.located_at

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        pod: None | str | Unset
        if isinstance(self.pod, Unset):
            pod = UNSET
        else:
            pod = self.pod

        sensor_id: None | str | Unset
        if isinstance(self.sensor_id, Unset):
            sensor_id = UNSET
        else:
            sensor_id = self.sensor_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "owner": owner,
            }
        )
        if datasets is not UNSET:
            field_dict["datasets"] = datasets
        if iri is not UNSET:
            field_dict["iri"] = iri
        if located_at is not UNSET:
            field_dict["located_at"] = located_at
        if name is not UNSET:
            field_dict["name"] = name
        if pod is not UNSET:
            field_dict["pod"] = pod
        if sensor_id is not UNSET:
            field_dict["sensor_id"] = sensor_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.meter_in_datasets_item import MeterInDatasetsItem
        from ..models.ref import Ref

        d = dict(src_dict)
        key = d.pop("key")

        owner = Ref.from_dict(d.pop("owner"))

        _datasets = d.pop("datasets", UNSET)
        datasets: list[MeterInDatasetsItem] | Unset = UNSET
        if _datasets is not UNSET:
            datasets = []
            for datasets_item_data in _datasets:
                datasets_item = MeterInDatasetsItem.from_dict(datasets_item_data)

                datasets.append(datasets_item)

        def _parse_iri(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        iri = _parse_iri(d.pop("iri", UNSET))

        def _parse_located_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        located_at = _parse_located_at(d.pop("located_at", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_pod(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pod = _parse_pod(d.pop("pod", UNSET))

        def _parse_sensor_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        sensor_id = _parse_sensor_id(d.pop("sensor_id", UNSET))

        meter_in = cls(
            key=key,
            owner=owner,
            datasets=datasets,
            iri=iri,
            located_at=located_at,
            name=name,
            pod=pod,
            sensor_id=sensor_id,
        )

        meter_in.additional_properties = d
        return meter_in

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
