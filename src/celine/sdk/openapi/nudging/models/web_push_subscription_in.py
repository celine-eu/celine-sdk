from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.web_push_keys_in import WebPushKeysIn


T = TypeVar("T", bound="WebPushSubscriptionIn")


@_attrs_define
class WebPushSubscriptionIn:
    """
    Attributes:
        endpoint (str):
        keys (WebPushKeysIn):
    """

    endpoint: str
    keys: WebPushKeysIn
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        endpoint = self.endpoint

        keys = self.keys.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "endpoint": endpoint,
                "keys": keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.web_push_keys_in import WebPushKeysIn

        d = dict(src_dict)
        endpoint = d.pop("endpoint")

        keys = WebPushKeysIn.from_dict(d.pop("keys"))

        web_push_subscription_in = cls(
            endpoint=endpoint,
            keys=keys,
        )

        web_push_subscription_in.additional_properties = d
        return web_push_subscription_in

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
