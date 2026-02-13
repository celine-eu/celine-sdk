from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.descriptor_spec_schema_payload_schema_type_0 import DescriptorSpecSchemaPayloadSchemaType0


T = TypeVar("T", bound="DescriptorSpecSchema")


@_attrs_define
class DescriptorSpecSchema:
    """
    Attributes:
        id (str): Fetcher ID (domain-scoped).
        output_mapper (None | str): Payload mapper
        client (str | Unset): Fetcher client Default: 'dataset_api'.
        limit (int | Unset): Query limit Default: 100.
        offset (int | Unset): Query offset Default: 0.
        payload_schema (DescriptorSpecSchemaPayloadSchemaType0 | None | Unset): Payload schema
        query (None | str | Unset): Query Default: ''.
    """

    id: str
    output_mapper: None | str
    client: str | Unset = "dataset_api"
    limit: int | Unset = 100
    offset: int | Unset = 0
    payload_schema: DescriptorSpecSchemaPayloadSchemaType0 | None | Unset = UNSET
    query: None | str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.descriptor_spec_schema_payload_schema_type_0 import DescriptorSpecSchemaPayloadSchemaType0

        id = self.id

        output_mapper: None | str
        output_mapper = self.output_mapper

        client = self.client

        limit = self.limit

        offset = self.offset

        payload_schema: dict[str, Any] | None | Unset
        if isinstance(self.payload_schema, Unset):
            payload_schema = UNSET
        elif isinstance(self.payload_schema, DescriptorSpecSchemaPayloadSchemaType0):
            payload_schema = self.payload_schema.to_dict()
        else:
            payload_schema = self.payload_schema

        query: None | str | Unset
        if isinstance(self.query, Unset):
            query = UNSET
        else:
            query = self.query

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "output_mapper": output_mapper,
            }
        )
        if client is not UNSET:
            field_dict["client"] = client
        if limit is not UNSET:
            field_dict["limit"] = limit
        if offset is not UNSET:
            field_dict["offset"] = offset
        if payload_schema is not UNSET:
            field_dict["payload_schema"] = payload_schema
        if query is not UNSET:
            field_dict["query"] = query

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.descriptor_spec_schema_payload_schema_type_0 import DescriptorSpecSchemaPayloadSchemaType0

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_output_mapper(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        output_mapper = _parse_output_mapper(d.pop("output_mapper"))

        client = d.pop("client", UNSET)

        limit = d.pop("limit", UNSET)

        offset = d.pop("offset", UNSET)

        def _parse_payload_schema(data: object) -> DescriptorSpecSchemaPayloadSchemaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                payload_schema_type_0 = DescriptorSpecSchemaPayloadSchemaType0.from_dict(data)

                return payload_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DescriptorSpecSchemaPayloadSchemaType0 | None | Unset, data)

        payload_schema = _parse_payload_schema(d.pop("payload_schema", UNSET))

        def _parse_query(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        query = _parse_query(d.pop("query", UNSET))

        descriptor_spec_schema = cls(
            id=id,
            output_mapper=output_mapper,
            client=client,
            limit=limit,
            offset=offset,
            payload_schema=payload_schema,
            query=query,
        )

        descriptor_spec_schema.additional_properties = d
        return descriptor_spec_schema

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
