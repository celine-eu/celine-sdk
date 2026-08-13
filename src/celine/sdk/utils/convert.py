from __future__ import annotations

import sys
from functools import lru_cache
from importlib import import_module
from types import ModuleType
from typing import Any, Mapping, Protocol, TypeGuard, TypeVar, cast, overload
from pydantic import BaseModel

if sys.version_info >= (3, 11):
    from typing import Self
else:  # pragma: no cover - covered by the 3.10 leg of the test matrix
    # `Self` reached `typing` in 3.11. This single import was the *entire*
    # reason this package declared `requires-python >= 3.12`: on 3.10 it raises
    # at module load, and `convert` is imported transitively by most of the SDK,
    # so 2 of 553 submodules failed and took the floor with them. Every
    # dependency this package declares already supports 3.10.
    from typing_extensions import Self


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
