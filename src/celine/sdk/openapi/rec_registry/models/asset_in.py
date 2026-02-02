from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_in_datasets_item import AssetInDatasetsItem
    from ..models.ref import Ref


T = TypeVar("T", bound="AssetIn")


@_attrs_define
class AssetIn:
    """
    Attributes:
        key (str):
        owner (Ref): Generic reference object used in Greenland bundles.
            Example: {"kind":"participant","ref":"p_gl_00002"}
        category (None | str | Unset):
        datasets (list[AssetInDatasetsItem] | Unset):
        iri (None | str | Unset):
        located_at (None | str | Unset):
        name (None | str | Unset):
    """

    key: str
    owner: Ref
    category: None | str | Unset = UNSET
    datasets: list[AssetInDatasetsItem] | Unset = UNSET
    iri: None | str | Unset = UNSET
    located_at: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        owner = self.owner.to_dict()

        category: None | str | Unset
        if isinstance(self.category, Unset):
            category = UNSET
        else:
            category = self.category

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "owner": owner,
            }
        )
        if category is not UNSET:
            field_dict["category"] = category
        if datasets is not UNSET:
            field_dict["datasets"] = datasets
        if iri is not UNSET:
            field_dict["iri"] = iri
        if located_at is not UNSET:
            field_dict["located_at"] = located_at
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_in_datasets_item import AssetInDatasetsItem
        from ..models.ref import Ref

        d = dict(src_dict)
        key = d.pop("key")

        owner = Ref.from_dict(d.pop("owner"))

        def _parse_category(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category = _parse_category(d.pop("category", UNSET))

        _datasets = d.pop("datasets", UNSET)
        datasets: list[AssetInDatasetsItem] | Unset = UNSET
        if _datasets is not UNSET:
            datasets = []
            for datasets_item_data in _datasets:
                datasets_item = AssetInDatasetsItem.from_dict(datasets_item_data)

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

        asset_in = cls(
            key=key,
            owner=owner,
            category=category,
            datasets=datasets,
            iri=iri,
            located_at=located_at,
            name=name,
        )

        asset_in.additional_properties = d
        return asset_in

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
