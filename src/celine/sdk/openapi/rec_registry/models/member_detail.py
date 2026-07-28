from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery_point import DeliveryPoint
    from ..models.member_detail_extra import MemberDetailExtra


T = TypeVar("T", bound="MemberDetail")


@_attrs_define
class MemberDetail:
    """
    Attributes:
        id (str):
        key (str):
        user_id (str):
        name (str):
        role (str):
        area (str):
        status (str):
        delivery_points (list[DeliveryPoint] | Unset):
        extra (MemberDetailExtra | Unset):
        created_at (None | str | Unset):
        updated_at (None | str | Unset):
    """

    id: str
    key: str
    user_id: str
    name: str
    role: str
    area: str
    status: str
    delivery_points: list[DeliveryPoint] | Unset = UNSET
    extra: MemberDetailExtra | Unset = UNSET
    created_at: None | str | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        key = self.key

        user_id = self.user_id

        name = self.name

        role = self.role

        area = self.area

        status = self.status

        delivery_points: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.delivery_points, Unset):
            delivery_points = []
            for delivery_points_item_data in self.delivery_points:
                delivery_points_item = delivery_points_item_data.to_dict()
                delivery_points.append(delivery_points_item)

        extra: dict[str, Any] | Unset = UNSET
        if not isinstance(self.extra, Unset):
            extra = self.extra.to_dict()

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "key": key,
                "user_id": user_id,
                "name": name,
                "role": role,
                "area": area,
                "status": status,
            }
        )
        if delivery_points is not UNSET:
            field_dict["delivery_points"] = delivery_points
        if extra is not UNSET:
            field_dict["extra"] = extra
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delivery_point import DeliveryPoint
        from ..models.member_detail_extra import MemberDetailExtra

        d = dict(src_dict)
        id = d.pop("id")

        key = d.pop("key")

        user_id = d.pop("user_id")

        name = d.pop("name")

        role = d.pop("role")

        area = d.pop("area")

        status = d.pop("status")

        _delivery_points = d.pop("delivery_points", UNSET)
        delivery_points: list[DeliveryPoint] | Unset = UNSET
        if _delivery_points is not UNSET:
            delivery_points = []
            for delivery_points_item_data in _delivery_points:
                delivery_points_item = DeliveryPoint.from_dict(delivery_points_item_data)

                delivery_points.append(delivery_points_item)

        _extra = d.pop("extra", UNSET)
        extra: MemberDetailExtra | Unset
        if isinstance(_extra, Unset):
            extra = UNSET
        else:
            extra = MemberDetailExtra.from_dict(_extra)

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        member_detail = cls(
            id=id,
            key=key,
            user_id=user_id,
            name=name,
            role=role,
            area=area,
            status=status,
            delivery_points=delivery_points,
            extra=extra,
            created_at=created_at,
            updated_at=updated_at,
        )

        member_detail.additional_properties = d
        return member_detail

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
