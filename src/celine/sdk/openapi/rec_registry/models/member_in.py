from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_collection_in import AssetCollectionIn
    from ..models.delivery_point_in import DeliveryPointIn


T = TypeVar("T", bound="MemberIn")


@_attrs_define
class MemberIn:
    """Community member.

    Attributes:
        area (str):
        name (str):
        role (str):
        status (str):
        user_id (str):
        assets (AssetCollectionIn | Unset): Collection of assets organized by type.
        delivery_points (list[DeliveryPointIn] | Unset):
        type_ (None | str | Unset):
    """

    area: str
    name: str
    role: str
    status: str
    user_id: str
    assets: AssetCollectionIn | Unset = UNSET
    delivery_points: list[DeliveryPointIn] | Unset = UNSET
    type_: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area

        name = self.name

        role = self.role

        status = self.status

        user_id = self.user_id

        assets: dict[str, Any] | Unset = UNSET
        if not isinstance(self.assets, Unset):
            assets = self.assets.to_dict()

        delivery_points: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.delivery_points, Unset):
            delivery_points = []
            for delivery_points_item_data in self.delivery_points:
                delivery_points_item = delivery_points_item_data.to_dict()
                delivery_points.append(delivery_points_item)

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "name": name,
                "role": role,
                "status": status,
                "user_id": user_id,
            }
        )
        if assets is not UNSET:
            field_dict["assets"] = assets
        if delivery_points is not UNSET:
            field_dict["delivery_points"] = delivery_points
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_collection_in import AssetCollectionIn
        from ..models.delivery_point_in import DeliveryPointIn

        d = dict(src_dict)
        area = d.pop("area")

        name = d.pop("name")

        role = d.pop("role")

        status = d.pop("status")

        user_id = d.pop("user_id")

        _assets = d.pop("assets", UNSET)
        assets: AssetCollectionIn | Unset
        if isinstance(_assets, Unset):
            assets = UNSET
        else:
            assets = AssetCollectionIn.from_dict(_assets)

        _delivery_points = d.pop("delivery_points", UNSET)
        delivery_points: list[DeliveryPointIn] | Unset = UNSET
        if _delivery_points is not UNSET:
            delivery_points = []
            for delivery_points_item_data in _delivery_points:
                delivery_points_item = DeliveryPointIn.from_dict(delivery_points_item_data)

                delivery_points.append(delivery_points_item)

        def _parse_type_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        member_in = cls(
            area=area,
            name=name,
            role=role,
            status=status,
            user_id=user_id,
            assets=assets,
            delivery_points=delivery_points,
            type_=type_,
        )

        member_in.additional_properties = d
        return member_in

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
