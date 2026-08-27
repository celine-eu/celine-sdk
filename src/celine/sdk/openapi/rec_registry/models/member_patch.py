from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.member_patch_extra_type_0 import MemberPatchExtraType0


T = TypeVar("T", bound="MemberPatch")


@_attrs_define
class MemberPatch:
    """Partial update. Absent fields are left alone, never cleared.

    `delivery_points` is deliberately absent: it is a JSONB list, and a patch
    that happened to omit it would otherwise read as "this member now has none".
    It has its own sub-resource.

        Attributes:
            area (None | str | Unset):
            did (None | str | Unset):
            extra (MemberPatchExtraType0 | None | Unset):
            name (None | str | Unset):
            role (None | str | Unset):
            status (None | str | Unset):
            type_ (None | str | Unset):
            user_id (None | str | Unset):
    """

    area: None | str | Unset = UNSET
    did: None | str | Unset = UNSET
    extra: MemberPatchExtraType0 | None | Unset = UNSET
    name: None | str | Unset = UNSET
    role: None | str | Unset = UNSET
    status: None | str | Unset = UNSET
    type_: None | str | Unset = UNSET
    user_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.member_patch_extra_type_0 import MemberPatchExtraType0

        area: None | str | Unset
        if isinstance(self.area, Unset):
            area = UNSET
        else:
            area = self.area

        did: None | str | Unset
        if isinstance(self.did, Unset):
            did = UNSET
        else:
            did = self.did

        extra: dict[str, Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, MemberPatchExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        role: None | str | Unset
        if isinstance(self.role, Unset):
            role = UNSET
        else:
            role = self.role

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        type_: None | str | Unset
        if isinstance(self.type_, Unset):
            type_ = UNSET
        else:
            type_ = self.type_

        user_id: None | str | Unset
        if isinstance(self.user_id, Unset):
            user_id = UNSET
        else:
            user_id = self.user_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if area is not UNSET:
            field_dict["area"] = area
        if did is not UNSET:
            field_dict["did"] = did
        if extra is not UNSET:
            field_dict["extra"] = extra
        if name is not UNSET:
            field_dict["name"] = name
        if role is not UNSET:
            field_dict["role"] = role
        if status is not UNSET:
            field_dict["status"] = status
        if type_ is not UNSET:
            field_dict["type"] = type_
        if user_id is not UNSET:
            field_dict["user_id"] = user_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.member_patch_extra_type_0 import MemberPatchExtraType0

        d = dict(src_dict)

        def _parse_area(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        area = _parse_area(d.pop("area", UNSET))

        def _parse_did(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        did = _parse_did(d.pop("did", UNSET))

        def _parse_extra(data: object) -> MemberPatchExtraType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = MemberPatchExtraType0.from_dict(data)

                return extra_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MemberPatchExtraType0 | None | Unset, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        role = _parse_role(d.pop("role", UNSET))

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_type_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        type_ = _parse_type_(d.pop("type", UNSET))

        def _parse_user_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_id = _parse_user_id(d.pop("user_id", UNSET))

        member_patch = cls(
            area=area,
            did=did,
            extra=extra,
            name=name,
            role=role,
            status=status,
            type_=type_,
            user_id=user_id,
        )

        member_patch.additional_properties = d
        return member_patch

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
