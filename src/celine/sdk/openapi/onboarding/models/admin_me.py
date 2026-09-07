from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.rec_access import RecAccess


T = TypeVar("T", bound="AdminMe")


@_attrs_define
class AdminMe:
    """
    Attributes:
        email (None | str):
        locale (None | str):
        name (None | str):
        organizations (list[str]):
        preferred_username (None | str):
        realm_groups (list[str]):
        recs (list[RecAccess]):
        sub (str):
        subject_type (str):
    """

    email: None | str
    locale: None | str
    name: None | str
    organizations: list[str]
    preferred_username: None | str
    realm_groups: list[str]
    recs: list[RecAccess]
    sub: str
    subject_type: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email: None | str
        email = self.email

        locale: None | str
        locale = self.locale

        name: None | str
        name = self.name

        organizations = self.organizations

        preferred_username: None | str
        preferred_username = self.preferred_username

        realm_groups = self.realm_groups

        recs = []
        for recs_item_data in self.recs:
            recs_item = recs_item_data.to_dict()
            recs.append(recs_item)

        sub = self.sub

        subject_type = self.subject_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "locale": locale,
                "name": name,
                "organizations": organizations,
                "preferred_username": preferred_username,
                "realm_groups": realm_groups,
                "recs": recs,
                "sub": sub,
                "subject_type": subject_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rec_access import RecAccess

        d = dict(src_dict)

        def _parse_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        email = _parse_email(d.pop("email"))

        def _parse_locale(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        locale = _parse_locale(d.pop("locale"))

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        organizations = cast(list[str], d.pop("organizations"))

        def _parse_preferred_username(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        preferred_username = _parse_preferred_username(d.pop("preferred_username"))

        realm_groups = cast(list[str], d.pop("realm_groups"))

        recs = []
        _recs = d.pop("recs")
        for recs_item_data in _recs:
            recs_item = RecAccess.from_dict(recs_item_data)

            recs.append(recs_item)

        sub = d.pop("sub")

        subject_type = d.pop("subject_type")

        admin_me = cls(
            email=email,
            locale=locale,
            name=name,
            organizations=organizations,
            preferred_username=preferred_username,
            realm_groups=realm_groups,
            recs=recs,
            sub=sub,
            subject_type=subject_type,
        )

        admin_me.additional_properties = d
        return admin_me

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
