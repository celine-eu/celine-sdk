from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.asset_in import AssetIn
    from ..models.community_in import CommunityIn
    from ..models.context_in import ContextIn
    from ..models.membership_in import MembershipIn
    from ..models.meter_in import MeterIn
    from ..models.participant_in import ParticipantIn
    from ..models.site_in import SiteIn


T = TypeVar("T", bound="RegistryBundleIn")


@_attrs_define
class RegistryBundleIn:
    """
    Attributes:
        community (CommunityIn):
        assets (list[AssetIn] | Unset):
        context (ContextIn | None | Unset):
        memberships (list[MembershipIn] | Unset):
        meters (list[MeterIn] | Unset):
        participants (list[ParticipantIn] | Unset):
        sites (list[SiteIn] | Unset):
    """

    community: CommunityIn
    assets: list[AssetIn] | Unset = UNSET
    context: ContextIn | None | Unset = UNSET
    memberships: list[MembershipIn] | Unset = UNSET
    meters: list[MeterIn] | Unset = UNSET
    participants: list[ParticipantIn] | Unset = UNSET
    sites: list[SiteIn] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.context_in import ContextIn

        community = self.community.to_dict()

        assets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.assets, Unset):
            assets = []
            for assets_item_data in self.assets:
                assets_item = assets_item_data.to_dict()
                assets.append(assets_item)

        context: dict[str, Any] | None | Unset
        if isinstance(self.context, Unset):
            context = UNSET
        elif isinstance(self.context, ContextIn):
            context = self.context.to_dict()
        else:
            context = self.context

        memberships: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.memberships, Unset):
            memberships = []
            for memberships_item_data in self.memberships:
                memberships_item = memberships_item_data.to_dict()
                memberships.append(memberships_item)

        meters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.meters, Unset):
            meters = []
            for meters_item_data in self.meters:
                meters_item = meters_item_data.to_dict()
                meters.append(meters_item)

        participants: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.participants, Unset):
            participants = []
            for participants_item_data in self.participants:
                participants_item = participants_item_data.to_dict()
                participants.append(participants_item)

        sites: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sites, Unset):
            sites = []
            for sites_item_data in self.sites:
                sites_item = sites_item_data.to_dict()
                sites.append(sites_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "community": community,
            }
        )
        if assets is not UNSET:
            field_dict["assets"] = assets
        if context is not UNSET:
            field_dict["context"] = context
        if memberships is not UNSET:
            field_dict["memberships"] = memberships
        if meters is not UNSET:
            field_dict["meters"] = meters
        if participants is not UNSET:
            field_dict["participants"] = participants
        if sites is not UNSET:
            field_dict["sites"] = sites

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.asset_in import AssetIn
        from ..models.community_in import CommunityIn
        from ..models.context_in import ContextIn
        from ..models.membership_in import MembershipIn
        from ..models.meter_in import MeterIn
        from ..models.participant_in import ParticipantIn
        from ..models.site_in import SiteIn

        d = dict(src_dict)
        community = CommunityIn.from_dict(d.pop("community"))

        _assets = d.pop("assets", UNSET)
        assets: list[AssetIn] | Unset = UNSET
        if _assets is not UNSET:
            assets = []
            for assets_item_data in _assets:
                assets_item = AssetIn.from_dict(assets_item_data)

                assets.append(assets_item)

        def _parse_context(data: object) -> ContextIn | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                context_type_0 = ContextIn.from_dict(data)

                return context_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ContextIn | None | Unset, data)

        context = _parse_context(d.pop("context", UNSET))

        _memberships = d.pop("memberships", UNSET)
        memberships: list[MembershipIn] | Unset = UNSET
        if _memberships is not UNSET:
            memberships = []
            for memberships_item_data in _memberships:
                memberships_item = MembershipIn.from_dict(memberships_item_data)

                memberships.append(memberships_item)

        _meters = d.pop("meters", UNSET)
        meters: list[MeterIn] | Unset = UNSET
        if _meters is not UNSET:
            meters = []
            for meters_item_data in _meters:
                meters_item = MeterIn.from_dict(meters_item_data)

                meters.append(meters_item)

        _participants = d.pop("participants", UNSET)
        participants: list[ParticipantIn] | Unset = UNSET
        if _participants is not UNSET:
            participants = []
            for participants_item_data in _participants:
                participants_item = ParticipantIn.from_dict(participants_item_data)

                participants.append(participants_item)

        _sites = d.pop("sites", UNSET)
        sites: list[SiteIn] | Unset = UNSET
        if _sites is not UNSET:
            sites = []
            for sites_item_data in _sites:
                sites_item = SiteIn.from_dict(sites_item_data)

                sites.append(sites_item)

        registry_bundle_in = cls(
            community=community,
            assets=assets,
            context=context,
            memberships=memberships,
            meters=meters,
            participants=participants,
            sites=sites,
        )

        registry_bundle_in.additional_properties = d
        return registry_bundle_in

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
