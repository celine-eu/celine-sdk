from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.acceptance_read import AcceptanceRead


T = TypeVar("T", bound="AcceptancesResponse")


@_attrs_define
class AcceptancesResponse:
    """The member's own application's acceptances. Nothing else of the application.

    ``submission_id`` is ``None`` when the member has no approved application in the
    community their token names — preregistered, or never applied — and the list is
    empty: an answer, not an error, so the reader asks.

        Attributes:
            acceptances (list[AcceptanceRead] | Unset):
            rec_slug (None | str | Unset):
            submission_id (None | str | Unset):
    """

    acceptances: list[AcceptanceRead] | Unset = UNSET
    rec_slug: None | str | Unset = UNSET
    submission_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        acceptances: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.acceptances, Unset):
            acceptances = []
            for acceptances_item_data in self.acceptances:
                acceptances_item = acceptances_item_data.to_dict()
                acceptances.append(acceptances_item)

        rec_slug: None | str | Unset
        if isinstance(self.rec_slug, Unset):
            rec_slug = UNSET
        else:
            rec_slug = self.rec_slug

        submission_id: None | str | Unset
        if isinstance(self.submission_id, Unset):
            submission_id = UNSET
        else:
            submission_id = self.submission_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if acceptances is not UNSET:
            field_dict["acceptances"] = acceptances
        if rec_slug is not UNSET:
            field_dict["rec_slug"] = rec_slug
        if submission_id is not UNSET:
            field_dict["submission_id"] = submission_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.acceptance_read import AcceptanceRead

        d = dict(src_dict)
        _acceptances = d.pop("acceptances", UNSET)
        acceptances: list[AcceptanceRead] | Unset = UNSET
        if _acceptances is not UNSET:
            acceptances = []
            for acceptances_item_data in _acceptances:
                acceptances_item = AcceptanceRead.from_dict(acceptances_item_data)

                acceptances.append(acceptances_item)

        def _parse_rec_slug(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rec_slug = _parse_rec_slug(d.pop("rec_slug", UNSET))

        def _parse_submission_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        submission_id = _parse_submission_id(d.pop("submission_id", UNSET))

        acceptances_response = cls(
            acceptances=acceptances,
            rec_slug=rec_slug,
            submission_id=submission_id,
        )

        acceptances_response.additional_properties = d
        return acceptances_response

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
