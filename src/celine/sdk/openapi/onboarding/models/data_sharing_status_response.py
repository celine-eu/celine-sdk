from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.sharing_state import SharingState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_sharing_status_response_identity_type_0 import DataSharingStatusResponseIdentityType0
    from ..models.data_sharing_status_response_offers_item import DataSharingStatusResponseOffersItem


T = TypeVar("T", bound="DataSharingStatusResponse")


@_attrs_define
class DataSharingStatusResponse:
    """Every offer this member's community publishes, with their decision on it.

    ``has_identity`` and ``offers`` are the shape `../celine-webapp` already
    serves to its frontend, kept so a relocation costs the UI nothing. ``state``
    is additive and says *why* `has_identity` is false — "your community is not
    in a dataspace" and "you have no credential yet" need different sentences and
    used to get the same one.

    ``identity`` carries the member's DID, their credential's role, and its
    issued/expires dates — enough to quote to a REC manager looking them up, and
    the only way a member learns a DID that was minted on their behalf. ``None``
    unless `state` is `ok`.

    **No credential is ever in here.** Not the `vc_jws`, which authenticates as
    the member, and not in any field added later.

        Attributes:
            has_identity (bool):
            state (SharingState): Why a member can or cannot decide anything, in one word.

                The states exist because collapsing them is what made the feature useless:
                a preregistered member reached the sharing screen and was told they had no
                dataspace identity, which was true and unactionable. Each of these has a
                different thing to say and a different thing to do next.
            identity (DataSharingStatusResponseIdentityType0 | None | Unset):
            offers (list[DataSharingStatusResponseOffersItem] | Unset):
    """

    has_identity: bool
    state: SharingState
    identity: DataSharingStatusResponseIdentityType0 | None | Unset = UNSET
    offers: list[DataSharingStatusResponseOffersItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.data_sharing_status_response_identity_type_0 import DataSharingStatusResponseIdentityType0

        has_identity = self.has_identity

        state = self.state.value

        identity: dict[str, Any] | None | Unset
        if isinstance(self.identity, Unset):
            identity = UNSET
        elif isinstance(self.identity, DataSharingStatusResponseIdentityType0):
            identity = self.identity.to_dict()
        else:
            identity = self.identity

        offers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.offers, Unset):
            offers = []
            for offers_item_data in self.offers:
                offers_item = offers_item_data.to_dict()
                offers.append(offers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_identity": has_identity,
                "state": state,
            }
        )
        if identity is not UNSET:
            field_dict["identity"] = identity
        if offers is not UNSET:
            field_dict["offers"] = offers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_sharing_status_response_identity_type_0 import DataSharingStatusResponseIdentityType0
        from ..models.data_sharing_status_response_offers_item import DataSharingStatusResponseOffersItem

        d = dict(src_dict)
        has_identity = d.pop("has_identity")

        state = SharingState(d.pop("state"))

        def _parse_identity(data: object) -> DataSharingStatusResponseIdentityType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                identity_type_0 = DataSharingStatusResponseIdentityType0.from_dict(data)

                return identity_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DataSharingStatusResponseIdentityType0 | None | Unset, data)

        identity = _parse_identity(d.pop("identity", UNSET))

        _offers = d.pop("offers", UNSET)
        offers: list[DataSharingStatusResponseOffersItem] | Unset = UNSET
        if _offers is not UNSET:
            offers = []
            for offers_item_data in _offers:
                offers_item = DataSharingStatusResponseOffersItem.from_dict(offers_item_data)

                offers.append(offers_item)

        data_sharing_status_response = cls(
            has_identity=has_identity,
            state=state,
            identity=identity,
            offers=offers,
        )

        data_sharing_status_response.additional_properties = d
        return data_sharing_status_response

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
