from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DidsBatchRequest")


@_attrs_define
class DidsBatchRequest:
    """Members to resolve by their dataspace DID.

    Bounded by the same constant as its two siblings, for the same reason: a
    caller naming ten thousand DIDs in one request has a dump of the registry
    rather than a lookup.

    A DID is the identifier a consent record is written in, so the set the
    caller holds is the set of people who consented — and this endpoint turns
    that into the supply points they hold. Which makes the bound the same
    security decision it is on the other two.

        Attributes:
            dids (list[str]):
    """

    dids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dids = self.dids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dids": dids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dids = cast(list[str], d.pop("dids"))

        dids_batch_request = cls(
            dids=dids,
        )

        dids_batch_request.additional_properties = d
        return dids_batch_request

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
