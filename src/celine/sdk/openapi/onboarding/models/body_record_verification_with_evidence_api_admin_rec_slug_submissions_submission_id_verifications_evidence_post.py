from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, Unset

T = TypeVar(
    "T", bound="BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost"
)


@_attrs_define
class BodyRecordVerificationWithEvidenceApiAdminRecSlugSubmissionsSubmissionIdVerificationsEvidencePost:
    """
    Attributes:
        files (list[str]): The evidence the community keeps
        kinds (list[str]): One per file: utility_bill, id_document or other
        note (None | str | Unset):
    """

    files: list[str]
    kinds: list[str]
    note: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        files = self.files

        kinds = self.kinds

        note: None | str | Unset
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
                "kinds": kinds,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        for files_item_element in self.files:
            files.append(("files", (None, str(files_item_element).encode(), "text/plain")))

        for kinds_item_element in self.kinds:
            files.append(("kinds", (None, str(kinds_item_element).encode(), "text/plain")))

        if not isinstance(self.note, Unset):
            if isinstance(self.note, str):
                files.append(("note", (None, str(self.note).encode(), "text/plain")))
            else:
                files.append(("note", (None, str(self.note).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        files = cast(list[str], d.pop("files"))

        kinds = cast(list[str], d.pop("kinds"))

        def _parse_note(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        note = _parse_note(d.pop("note", UNSET))

        body_record_verification_with_evidence_api_admin_rec_slug_submissions_submission_id_verifications_evidence_post = cls(
            files=files,
            kinds=kinds,
            note=note,
        )

        body_record_verification_with_evidence_api_admin_rec_slug_submissions_submission_id_verifications_evidence_post.additional_properties = d
        return body_record_verification_with_evidence_api_admin_rec_slug_submissions_submission_id_verifications_evidence_post

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
