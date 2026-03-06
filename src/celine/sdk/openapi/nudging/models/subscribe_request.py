from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.web_push_subscription_in import WebPushSubscriptionIn


T = TypeVar("T", bound="SubscribeRequest")


@_attrs_define
class SubscribeRequest:
    """user_id is derived from the JWT – not accepted from the caller.

    Attributes:
        subscription (WebPushSubscriptionIn):
        community_id (None | str | Unset): Optional community scope for the subscription
    """

    subscription: WebPushSubscriptionIn
    community_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        subscription = self.subscription.to_dict()

        community_id: None | str | Unset
        if isinstance(self.community_id, Unset):
            community_id = UNSET
        else:
            community_id = self.community_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "subscription": subscription,
            }
        )
        if community_id is not UNSET:
            field_dict["community_id"] = community_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.web_push_subscription_in import WebPushSubscriptionIn

        d = dict(src_dict)
        subscription = WebPushSubscriptionIn.from_dict(d.pop("subscription"))

        def _parse_community_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        community_id = _parse_community_id(d.pop("community_id", UNSET))

        subscribe_request = cls(
            subscription=subscription,
            community_id=community_id,
        )

        subscribe_request.additional_properties = d
        return subscribe_request

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
