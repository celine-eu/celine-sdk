from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BackendConfig")


@_attrs_define
class BackendConfig:
    """Backend configuration block for dataset storage.

    Attributes:
        base_url (None | str | Unset):
        entity_type (None | str | Unset):
        fiware_service (None | str | Unset):
        fiware_service_path (None | str | Unset):
        format_ (None | str | Unset):
        path (None | str | Unset):
        public_url (None | str | Unset):
        size_bytes (int | None | Unset):
        table (None | str | Unset):
    """

    base_url: None | str | Unset = UNSET
    entity_type: None | str | Unset = UNSET
    fiware_service: None | str | Unset = UNSET
    fiware_service_path: None | str | Unset = UNSET
    format_: None | str | Unset = UNSET
    path: None | str | Unset = UNSET
    public_url: None | str | Unset = UNSET
    size_bytes: int | None | Unset = UNSET
    table: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_url: None | str | Unset
        if isinstance(self.base_url, Unset):
            base_url = UNSET
        else:
            base_url = self.base_url

        entity_type: None | str | Unset
        if isinstance(self.entity_type, Unset):
            entity_type = UNSET
        else:
            entity_type = self.entity_type

        fiware_service: None | str | Unset
        if isinstance(self.fiware_service, Unset):
            fiware_service = UNSET
        else:
            fiware_service = self.fiware_service

        fiware_service_path: None | str | Unset
        if isinstance(self.fiware_service_path, Unset):
            fiware_service_path = UNSET
        else:
            fiware_service_path = self.fiware_service_path

        format_: None | str | Unset
        if isinstance(self.format_, Unset):
            format_ = UNSET
        else:
            format_ = self.format_

        path: None | str | Unset
        if isinstance(self.path, Unset):
            path = UNSET
        else:
            path = self.path

        public_url: None | str | Unset
        if isinstance(self.public_url, Unset):
            public_url = UNSET
        else:
            public_url = self.public_url

        size_bytes: int | None | Unset
        if isinstance(self.size_bytes, Unset):
            size_bytes = UNSET
        else:
            size_bytes = self.size_bytes

        table: None | str | Unset
        if isinstance(self.table, Unset):
            table = UNSET
        else:
            table = self.table

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_url is not UNSET:
            field_dict["base_url"] = base_url
        if entity_type is not UNSET:
            field_dict["entity_type"] = entity_type
        if fiware_service is not UNSET:
            field_dict["fiware_service"] = fiware_service
        if fiware_service_path is not UNSET:
            field_dict["fiware_service_path"] = fiware_service_path
        if format_ is not UNSET:
            field_dict["format"] = format_
        if path is not UNSET:
            field_dict["path"] = path
        if public_url is not UNSET:
            field_dict["public_url"] = public_url
        if size_bytes is not UNSET:
            field_dict["size_bytes"] = size_bytes
        if table is not UNSET:
            field_dict["table"] = table

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_base_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base_url = _parse_base_url(d.pop("base_url", UNSET))

        def _parse_entity_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        entity_type = _parse_entity_type(d.pop("entity_type", UNSET))

        def _parse_fiware_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fiware_service = _parse_fiware_service(d.pop("fiware_service", UNSET))

        def _parse_fiware_service_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fiware_service_path = _parse_fiware_service_path(d.pop("fiware_service_path", UNSET))

        def _parse_format_(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        format_ = _parse_format_(d.pop("format", UNSET))

        def _parse_path(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        path = _parse_path(d.pop("path", UNSET))

        def _parse_public_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        public_url = _parse_public_url(d.pop("public_url", UNSET))

        def _parse_size_bytes(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        size_bytes = _parse_size_bytes(d.pop("size_bytes", UNSET))

        def _parse_table(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        table = _parse_table(d.pop("table", UNSET))

        backend_config = cls(
            base_url=base_url,
            entity_type=entity_type,
            fiware_service=fiware_service,
            fiware_service_path=fiware_service_path,
            format_=format_,
            path=path,
            public_url=public_url,
            size_bytes=size_bytes,
            table=table,
        )

        backend_config.additional_properties = d
        return backend_config

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
