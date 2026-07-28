from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ev_charger import EvCharger
    from ..models.heat_pump import HeatPump
    from ..models.load import Load
    from ..models.meter import Meter
    from ..models.pv import Pv
    from ..models.storage import Storage


T = TypeVar("T", bound="AssetCollectionIn")


@_attrs_define
class AssetCollectionIn:
    """Collection of assets organized by type.

    Attributes:
        pv (Pv | Unset):
        storage (Storage | Unset):
        meter (Meter | Unset):
        ev_charger (EvCharger | Unset):
        heat_pump (HeatPump | Unset):
        load (Load | Unset):
    """

    pv: Pv | Unset = UNSET
    storage: Storage | Unset = UNSET
    meter: Meter | Unset = UNSET
    ev_charger: EvCharger | Unset = UNSET
    heat_pump: HeatPump | Unset = UNSET
    load: Load | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pv: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pv, Unset):
            pv = self.pv.to_dict()

        storage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.storage, Unset):
            storage = self.storage.to_dict()

        meter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.meter, Unset):
            meter = self.meter.to_dict()

        ev_charger: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ev_charger, Unset):
            ev_charger = self.ev_charger.to_dict()

        heat_pump: dict[str, Any] | Unset = UNSET
        if not isinstance(self.heat_pump, Unset):
            heat_pump = self.heat_pump.to_dict()

        load: dict[str, Any] | Unset = UNSET
        if not isinstance(self.load, Unset):
            load = self.load.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pv is not UNSET:
            field_dict["pv"] = pv
        if storage is not UNSET:
            field_dict["storage"] = storage
        if meter is not UNSET:
            field_dict["meter"] = meter
        if ev_charger is not UNSET:
            field_dict["ev_charger"] = ev_charger
        if heat_pump is not UNSET:
            field_dict["heat_pump"] = heat_pump
        if load is not UNSET:
            field_dict["load"] = load

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ev_charger import EvCharger
        from ..models.heat_pump import HeatPump
        from ..models.load import Load
        from ..models.meter import Meter
        from ..models.pv import Pv
        from ..models.storage import Storage

        d = dict(src_dict)
        _pv = d.pop("pv", UNSET)
        pv: Pv | Unset
        if isinstance(_pv, Unset):
            pv = UNSET
        else:
            pv = Pv.from_dict(_pv)

        _storage = d.pop("storage", UNSET)
        storage: Storage | Unset
        if isinstance(_storage, Unset):
            storage = UNSET
        else:
            storage = Storage.from_dict(_storage)

        _meter = d.pop("meter", UNSET)
        meter: Meter | Unset
        if isinstance(_meter, Unset):
            meter = UNSET
        else:
            meter = Meter.from_dict(_meter)

        _ev_charger = d.pop("ev_charger", UNSET)
        ev_charger: EvCharger | Unset
        if isinstance(_ev_charger, Unset):
            ev_charger = UNSET
        else:
            ev_charger = EvCharger.from_dict(_ev_charger)

        _heat_pump = d.pop("heat_pump", UNSET)
        heat_pump: HeatPump | Unset
        if isinstance(_heat_pump, Unset):
            heat_pump = UNSET
        else:
            heat_pump = HeatPump.from_dict(_heat_pump)

        _load = d.pop("load", UNSET)
        load: Load | Unset
        if isinstance(_load, Unset):
            load = UNSET
        else:
            load = Load.from_dict(_load)

        asset_collection_in = cls(
            pv=pv,
            storage=storage,
            meter=meter,
            ev_charger=ev_charger,
            heat_pump=heat_pump,
            load=load,
        )

        asset_collection_in.additional_properties = d
        return asset_collection_in

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
