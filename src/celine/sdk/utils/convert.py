from __future__ import annotations

from functools import lru_cache
from importlib import import_module
from types import ModuleType
from typing import Any, Mapping, Protocol, Self, TypeGuard, TypeVar, cast, overload
from pydantic import BaseModel


class SupportsToDict(Protocol):
    def to_dict(self) -> Mapping[str, Any]: ...


class SupportsFromDict(Protocol):
    @classmethod
    def from_dict(cls: type[Self], src_dict: Mapping[str, Any]) -> Self: ...


SchemaT = TypeVar("SchemaT", bound=BaseModel)
ClientToT = TypeVar("ClientToT", bound=SupportsToDict)
ClientFromT = TypeVar("ClientFromT", bound=SupportsFromDict)


@overload
def to_schema(client_obj: None, schema_cls: type[SchemaT]) -> None: ...


@overload
def to_schema(client_obj: SupportsToDict, schema_cls: type[SchemaT]) -> SchemaT: ...


@overload
def to_schema(
    client_obj: SupportsToDict | None, schema_cls: type[SchemaT]
) -> SchemaT | None: ...


def to_schema(
    client_obj: SupportsToDict | None, schema_cls: type[SchemaT]
) -> SchemaT | None:
    if client_obj is None:
        return None
    return schema_cls.model_validate(client_obj.to_dict())

def to_client(
    schema_obj: BaseModel | None, client_cls: type[ClientFromT]
) -> ClientFromT | None:
    if schema_obj is None:
        return None
    data = schema_obj.model_dump(mode="json", by_alias=True, exclude_unset=True)
    return client_cls.from_dict(data)
