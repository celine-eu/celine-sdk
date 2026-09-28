from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.setup_step_out import SetupStepOut
    from ..models.summary import Summary
    from ..models.sync_item import SyncItem


T = TypeVar("T", bound="RegistrySyncOut")


@_attrs_define
class RegistrySyncOut:
    """
    Attributes:
        areas (list[SyncItem]):
        community (str):
        dry_run (bool):
        nodes (list[SyncItem]):
        ok (bool):
        prune (bool):
        rec (str):
        setup (SetupStepOut): The community's set-up through the provisioning reconcile.

            ``status``: ``succeeded``, ``failed`` (with ``reason``), ``skipped`` (no
            provisioning service configured) or ``not_run`` (a dry run).
        summary (Summary):
    """

    areas: list[SyncItem]
    community: str
    dry_run: bool
    nodes: list[SyncItem]
    ok: bool
    prune: bool
    rec: str
    setup: SetupStepOut
    summary: Summary
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        areas = []
        for areas_item_data in self.areas:
            areas_item = areas_item_data.to_dict()
            areas.append(areas_item)

        community = self.community

        dry_run = self.dry_run

        nodes = []
        for nodes_item_data in self.nodes:
            nodes_item = nodes_item_data.to_dict()
            nodes.append(nodes_item)

        ok = self.ok

        prune = self.prune

        rec = self.rec

        setup = self.setup.to_dict()

        summary = self.summary.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "areas": areas,
                "community": community,
                "dry_run": dry_run,
                "nodes": nodes,
                "ok": ok,
                "prune": prune,
                "rec": rec,
                "setup": setup,
                "summary": summary,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.setup_step_out import SetupStepOut
        from ..models.summary import Summary
        from ..models.sync_item import SyncItem

        d = dict(src_dict)
        areas = []
        _areas = d.pop("areas")
        for areas_item_data in _areas:
            areas_item = SyncItem.from_dict(areas_item_data)

            areas.append(areas_item)

        community = d.pop("community")

        dry_run = d.pop("dry_run")

        nodes = []
        _nodes = d.pop("nodes")
        for nodes_item_data in _nodes:
            nodes_item = SyncItem.from_dict(nodes_item_data)

            nodes.append(nodes_item)

        ok = d.pop("ok")

        prune = d.pop("prune")

        rec = d.pop("rec")

        setup = SetupStepOut.from_dict(d.pop("setup"))

        summary = Summary.from_dict(d.pop("summary"))

        registry_sync_out = cls(
            areas=areas,
            community=community,
            dry_run=dry_run,
            nodes=nodes,
            ok=ok,
            prune=prune,
            rec=rec,
            setup=setup,
            summary=summary,
        )

        registry_sync_out.additional_properties = d
        return registry_sync_out

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
