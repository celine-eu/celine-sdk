from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery_point import DeliveryPoint
    from ..models.user_member_detail_extra import UserMemberDetailExtra


T = TypeVar("T", bound="UserMemberDetail")


@_attrs_define
class UserMemberDetail:
    """
    Attributes:
        area (str):
        key (str):
        name (str):
        role (str):
        status (str):
        created_at (None | str | Unset):
        delivery_points (list[DeliveryPoint] | Unset):
        extra (UserMemberDetailExtra | Unset):
        updated_at (None | str | Unset):
    """

    area: str
    key: str
    name: str
    role: str
    status: str
    created_at: None | str | Unset = UNSET
    delivery_points: list[DeliveryPoint] | Unset = UNSET
    extra: UserMemberDetailExtra | Unset = UNSET
    updated_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        area = self.area

        key = self.key

        name = self.name

        role = self.role

        status = self.status

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        else:
            created_at = self.created_at

        delivery_points: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.delivery_points, Unset):
            delivery_points = []
            for delivery_points_item_data in self.delivery_points:
                delivery_points_item = delivery_points_item_data.to_dict()
                delivery_points.append(delivery_points_item)

        extra: dict[str, Any] | Unset = UNSET
        if not isinstance(self.extra, Unset):
            extra = self.extra.to_dict()

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "area": area,
                "key": key,
                "name": name,
                "role": role,
                "status": status,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if delivery_points is not UNSET:
            field_dict["delivery_points"] = delivery_points
        if extra is not UNSET:
            field_dict["extra"] = extra
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.delivery_point import DeliveryPoint
        from ..models.user_member_detail_extra import UserMemberDetailExtra

        d = dict(src_dict)
        area = d.pop("area")

        key = d.pop("key")

        name = d.pop("name")

        role = d.pop("role")

        status = d.pop("status")

        def _parse_created_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        _delivery_points = d.pop("delivery_points", UNSET)
        delivery_points: list[DeliveryPoint] | Unset = UNSET
        if _delivery_points is not UNSET:
            delivery_points = []
            for delivery_points_item_data in _delivery_points:
                delivery_points_item = DeliveryPoint.from_dict(delivery_points_item_data)

                delivery_points.append(delivery_points_item)

        _extra = d.pop("extra", UNSET)
        extra: UserMemberDetailExtra | Unset
        if isinstance(_extra, Unset):
            extra = UNSET
        else:
            extra = UserMemberDetailExtra.from_dict(_extra)

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        user_member_detail = cls(
            area=area,
            key=key,
            name=name,
            role=role,
            status=status,
            created_at=created_at,
            delivery_points=delivery_points,
            extra=extra,
            updated_at=updated_at,
        )

        user_member_detail.additional_properties = d
        return user_member_detail

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
