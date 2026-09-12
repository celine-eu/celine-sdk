from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.divergence_model import DivergenceModel


T = TypeVar("T", bound="ReconcileResponse")


@_attrs_define
class ReconcileResponse:
    """What a community sweep did, and what it could not put right.

    `divergences` is empty on a healthy run **and a sweep that ends with any is
    a failure, reported as one**. The check runs after provisioning, so anything
    it finds is something a provisioning call claimed to have done and had not:
    quietly repairing it on the next sweep is how 10 of 45 members ended up
    outside their own organization with nothing saying so.

        Attributes:
            community (str):
            created (int):
            existing (int):
            members (int):
            divergences (list[DivergenceModel] | Unset):
    """

    community: str
    created: int
    existing: int
    members: int
    divergences: list[DivergenceModel] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        community = self.community

        created = self.created

        existing = self.existing

        members = self.members

        divergences: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.divergences, Unset):
            divergences = []
            for divergences_item_data in self.divergences:
                divergences_item = divergences_item_data.to_dict()
                divergences.append(divergences_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community": community,
                "created": created,
                "existing": existing,
                "members": members,
            }
        )
        if divergences is not UNSET:
            field_dict["divergences"] = divergences

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.divergence_model import DivergenceModel

        d = dict(src_dict)
        community = d.pop("community")

        created = d.pop("created")

        existing = d.pop("existing")

        members = d.pop("members")

        _divergences = d.pop("divergences", UNSET)
        divergences: list[DivergenceModel] | Unset = UNSET
        if _divergences is not UNSET:
            divergences = []
            for divergences_item_data in _divergences:
                divergences_item = DivergenceModel.from_dict(divergences_item_data)

                divergences.append(divergences_item)

        reconcile_response = cls(
            community=community,
            created=created,
            existing=existing,
            members=members,
            divergences=divergences,
        )

        reconcile_response.additional_properties = d
        return reconcile_response

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
