from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.delivery_point_schema import DeliveryPointSchema
    from ..models.user_member_detail_schema_extra_type_0 import UserMemberDetailSchemaExtraType0


T = TypeVar("T", bound="UserMemberDetailSchema")


@_attrs_define
class UserMemberDetailSchema:
    """
    Attributes:
        area (str):
        key (str):
        name (str):
        role (str):
        status (str):
        created_at (None | str | Unset):
        delivery_points (list[DeliveryPointSchema] | None | Unset):
        extra (None | Unset | UserMemberDetailSchemaExtraType0):
        updated_at (None | str | Unset):
    """

    area: str
    key: str
    name: str
    role: str
    status: str
    created_at: None | str | Unset = UNSET
    delivery_points: list[DeliveryPointSchema] | None | Unset = UNSET
    extra: None | Unset | UserMemberDetailSchemaExtraType0 = UNSET
    updated_at: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.user_member_detail_schema_extra_type_0 import UserMemberDetailSchemaExtraType0

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

        delivery_points: list[dict[str, Any]] | None | Unset
        if isinstance(self.delivery_points, Unset):
            delivery_points = UNSET
        elif isinstance(self.delivery_points, list):
            delivery_points = []
            for delivery_points_type_0_item_data in self.delivery_points:
                delivery_points_type_0_item = delivery_points_type_0_item_data.to_dict()
                delivery_points.append(delivery_points_type_0_item)

        else:
            delivery_points = self.delivery_points

        extra: dict[str, Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, UserMemberDetailSchemaExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

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
        from ..models.delivery_point_schema import DeliveryPointSchema
        from ..models.user_member_detail_schema_extra_type_0 import UserMemberDetailSchemaExtraType0

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

        def _parse_delivery_points(data: object) -> list[DeliveryPointSchema] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                delivery_points_type_0 = []
                _delivery_points_type_0 = data
                for delivery_points_type_0_item_data in _delivery_points_type_0:
                    delivery_points_type_0_item = DeliveryPointSchema.from_dict(delivery_points_type_0_item_data)

                    delivery_points_type_0.append(delivery_points_type_0_item)

                return delivery_points_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[DeliveryPointSchema] | None | Unset, data)

        delivery_points = _parse_delivery_points(d.pop("delivery_points", UNSET))

        def _parse_extra(data: object) -> None | Unset | UserMemberDetailSchemaExtraType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = UserMemberDetailSchemaExtraType0.from_dict(data)

                return extra_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | Unset | UserMemberDetailSchemaExtraType0, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        def _parse_updated_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        user_member_detail_schema = cls(
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

        user_member_detail_schema.additional_properties = d
        return user_member_detail_schema

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
