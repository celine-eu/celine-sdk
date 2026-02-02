from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.action import Action
    from ..models.authorize_request_context import AuthorizeRequestContext
    from ..models.resource import Resource


T = TypeVar("T", bound="AuthorizeRequest")


@_attrs_define
class AuthorizeRequest:
    """Generic authorization request.

    The JWT token should be passed in the Authorization header.

        Attributes:
            action (Action): Represents the action being performed.
            resource (Resource): Represents the resource being accessed.
            context (AuthorizeRequestContext | Unset): Additional context for policy evaluation
    """

    action: Action
    resource: Resource
    context: AuthorizeRequestContext | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.to_dict()

        resource = self.resource.to_dict()

        context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
                "resource": resource,
            }
        )
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.action import Action
        from ..models.authorize_request_context import AuthorizeRequestContext
        from ..models.resource import Resource

        d = dict(src_dict)
        action = Action.from_dict(d.pop("action"))

        resource = Resource.from_dict(d.pop("resource"))

        _context = d.pop("context", UNSET)
        context: AuthorizeRequestContext | Unset
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = AuthorizeRequestContext.from_dict(_context)

        authorize_request = cls(
            action=action,
            resource=resource,
            context=context,
        )

        authorize_request.additional_properties = d
        return authorize_request

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
