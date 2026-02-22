from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.engine_result_out import EngineResultOut
    from ..models.nudge_created_item import NudgeCreatedItem


T = TypeVar("T", bound="IngestOkResponse")


@_attrs_define
class IngestOkResponse:
    """
    Attributes:
        created (list[NudgeCreatedItem]):
        suppressed (list[EngineResultOut]):
        status (str | Unset):  Default: 'ok'.
    """

    created: list[NudgeCreatedItem]
    suppressed: list[EngineResultOut]
    status: str | Unset = "ok"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created = []
        for created_item_data in self.created:
            created_item = created_item_data.to_dict()
            created.append(created_item)

        suppressed = []
        for suppressed_item_data in self.suppressed:
            suppressed_item = suppressed_item_data.to_dict()
            suppressed.append(suppressed_item)

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created": created,
                "suppressed": suppressed,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.engine_result_out import EngineResultOut
        from ..models.nudge_created_item import NudgeCreatedItem

        d = dict(src_dict)
        created = []
        _created = d.pop("created")
        for created_item_data in _created:
            created_item = NudgeCreatedItem.from_dict(created_item_data)

            created.append(created_item)

        suppressed = []
        _suppressed = d.pop("suppressed")
        for suppressed_item_data in _suppressed:
            suppressed_item = EngineResultOut.from_dict(suppressed_item_data)

            suppressed.append(suppressed_item)

        status = d.pop("status", UNSET)

        ingest_ok_response = cls(
            created=created,
            suppressed=suppressed,
            status=status,
        )

        ingest_ok_response.additional_properties = d
        return ingest_ok_response

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
