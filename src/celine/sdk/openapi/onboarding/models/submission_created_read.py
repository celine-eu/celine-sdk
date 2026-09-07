from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.submission_status import SubmissionStatus

if TYPE_CHECKING:
    from ..models.submission_created_read_extra_data_type_0 import SubmissionCreatedReadExtraDataType0
    from ..models.submission_created_read_extracted_data_type_0 import SubmissionCreatedReadExtractedDataType0
    from ..models.submission_created_read_id_extracted_data_type_0 import SubmissionCreatedReadIdExtractedDataType0


T = TypeVar("T", bound="SubmissionCreatedRead")


@_attrs_define
class SubmissionCreatedRead:
    """
    Attributes:
        created_at (datetime.datetime):
        data_sharing_consent (bool):
        data_sharing_consent_at (datetime.datetime | None):
        data_sharing_consent_locale (None | str):
        data_sharing_consent_offer_ids (list[str] | None):
        data_sharing_consent_text_sha256 (None | str):
        data_sharing_consent_text_version (None | str):
        email (None | str):
        extra_data (None | SubmissionCreatedReadExtraDataType0):
        extracted_data (None | SubmissionCreatedReadExtractedDataType0):
        first_name (None | str):
        fiscal_code (None | str):
        gdpr_consent (bool):
        gdpr_consent_at (datetime.datetime | None):
        gdpr_consent_version (None | str):
        id (UUID):
        id_extracted_data (None | SubmissionCreatedReadIdExtractedDataType0):
        keep_me_updated (bool):
        last_name (None | str):
        notes (None | str):
        phone (None | str):
        phone_verified (bool):
        phone_verified_at (datetime.datetime | None):
        pod_code (None | str):
        policy_consent (bool):
        policy_consent_at (datetime.datetime | None):
        policy_consent_version (None | str):
        rec_slug (str):
        ref (str):
        session_token (str):
        share_provisioned (bool):
        status (SubmissionStatus):
        statute_consent (bool):
        statute_consent_at (datetime.datetime | None):
        statute_consent_version (None | str):
        supply_municipality (None | str):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    data_sharing_consent: bool
    data_sharing_consent_at: datetime.datetime | None
    data_sharing_consent_locale: None | str
    data_sharing_consent_offer_ids: list[str] | None
    data_sharing_consent_text_sha256: None | str
    data_sharing_consent_text_version: None | str
    email: None | str
    extra_data: None | SubmissionCreatedReadExtraDataType0
    extracted_data: None | SubmissionCreatedReadExtractedDataType0
    first_name: None | str
    fiscal_code: None | str
    gdpr_consent: bool
    gdpr_consent_at: datetime.datetime | None
    gdpr_consent_version: None | str
    id: UUID
    id_extracted_data: None | SubmissionCreatedReadIdExtractedDataType0
    keep_me_updated: bool
    last_name: None | str
    notes: None | str
    phone: None | str
    phone_verified: bool
    phone_verified_at: datetime.datetime | None
    pod_code: None | str
    policy_consent: bool
    policy_consent_at: datetime.datetime | None
    policy_consent_version: None | str
    rec_slug: str
    ref: str
    session_token: str
    share_provisioned: bool
    status: SubmissionStatus
    statute_consent: bool
    statute_consent_at: datetime.datetime | None
    statute_consent_version: None | str
    supply_municipality: None | str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.submission_created_read_extra_data_type_0 import SubmissionCreatedReadExtraDataType0
        from ..models.submission_created_read_extracted_data_type_0 import SubmissionCreatedReadExtractedDataType0
        from ..models.submission_created_read_id_extracted_data_type_0 import SubmissionCreatedReadIdExtractedDataType0

        created_at = self.created_at.isoformat()

        data_sharing_consent = self.data_sharing_consent

        data_sharing_consent_at: None | str
        if isinstance(self.data_sharing_consent_at, datetime.datetime):
            data_sharing_consent_at = self.data_sharing_consent_at.isoformat()
        else:
            data_sharing_consent_at = self.data_sharing_consent_at

        data_sharing_consent_locale: None | str
        data_sharing_consent_locale = self.data_sharing_consent_locale

        data_sharing_consent_offer_ids: list[str] | None
        if isinstance(self.data_sharing_consent_offer_ids, list):
            data_sharing_consent_offer_ids = self.data_sharing_consent_offer_ids

        else:
            data_sharing_consent_offer_ids = self.data_sharing_consent_offer_ids

        data_sharing_consent_text_sha256: None | str
        data_sharing_consent_text_sha256 = self.data_sharing_consent_text_sha256

        data_sharing_consent_text_version: None | str
        data_sharing_consent_text_version = self.data_sharing_consent_text_version

        email: None | str
        email = self.email

        extra_data: dict[str, Any] | None
        if isinstance(self.extra_data, SubmissionCreatedReadExtraDataType0):
            extra_data = self.extra_data.to_dict()
        else:
            extra_data = self.extra_data

        extracted_data: dict[str, Any] | None
        if isinstance(self.extracted_data, SubmissionCreatedReadExtractedDataType0):
            extracted_data = self.extracted_data.to_dict()
        else:
            extracted_data = self.extracted_data

        first_name: None | str
        first_name = self.first_name

        fiscal_code: None | str
        fiscal_code = self.fiscal_code

        gdpr_consent = self.gdpr_consent

        gdpr_consent_at: None | str
        if isinstance(self.gdpr_consent_at, datetime.datetime):
            gdpr_consent_at = self.gdpr_consent_at.isoformat()
        else:
            gdpr_consent_at = self.gdpr_consent_at

        gdpr_consent_version: None | str
        gdpr_consent_version = self.gdpr_consent_version

        id = str(self.id)

        id_extracted_data: dict[str, Any] | None
        if isinstance(self.id_extracted_data, SubmissionCreatedReadIdExtractedDataType0):
            id_extracted_data = self.id_extracted_data.to_dict()
        else:
            id_extracted_data = self.id_extracted_data

        keep_me_updated = self.keep_me_updated

        last_name: None | str
        last_name = self.last_name

        notes: None | str
        notes = self.notes

        phone: None | str
        phone = self.phone

        phone_verified = self.phone_verified

        phone_verified_at: None | str
        if isinstance(self.phone_verified_at, datetime.datetime):
            phone_verified_at = self.phone_verified_at.isoformat()
        else:
            phone_verified_at = self.phone_verified_at

        pod_code: None | str
        pod_code = self.pod_code

        policy_consent = self.policy_consent

        policy_consent_at: None | str
        if isinstance(self.policy_consent_at, datetime.datetime):
            policy_consent_at = self.policy_consent_at.isoformat()
        else:
            policy_consent_at = self.policy_consent_at

        policy_consent_version: None | str
        policy_consent_version = self.policy_consent_version

        rec_slug = self.rec_slug

        ref = self.ref

        session_token = self.session_token

        share_provisioned = self.share_provisioned

        status = self.status.value

        statute_consent = self.statute_consent

        statute_consent_at: None | str
        if isinstance(self.statute_consent_at, datetime.datetime):
            statute_consent_at = self.statute_consent_at.isoformat()
        else:
            statute_consent_at = self.statute_consent_at

        statute_consent_version: None | str
        statute_consent_version = self.statute_consent_version

        supply_municipality: None | str
        supply_municipality = self.supply_municipality

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "data_sharing_consent": data_sharing_consent,
                "data_sharing_consent_at": data_sharing_consent_at,
                "data_sharing_consent_locale": data_sharing_consent_locale,
                "data_sharing_consent_offer_ids": data_sharing_consent_offer_ids,
                "data_sharing_consent_text_sha256": data_sharing_consent_text_sha256,
                "data_sharing_consent_text_version": data_sharing_consent_text_version,
                "email": email,
                "extra_data": extra_data,
                "extracted_data": extracted_data,
                "first_name": first_name,
                "fiscal_code": fiscal_code,
                "gdpr_consent": gdpr_consent,
                "gdpr_consent_at": gdpr_consent_at,
                "gdpr_consent_version": gdpr_consent_version,
                "id": id,
                "id_extracted_data": id_extracted_data,
                "keep_me_updated": keep_me_updated,
                "last_name": last_name,
                "notes": notes,
                "phone": phone,
                "phone_verified": phone_verified,
                "phone_verified_at": phone_verified_at,
                "pod_code": pod_code,
                "policy_consent": policy_consent,
                "policy_consent_at": policy_consent_at,
                "policy_consent_version": policy_consent_version,
                "rec_slug": rec_slug,
                "ref": ref,
                "session_token": session_token,
                "share_provisioned": share_provisioned,
                "status": status,
                "statute_consent": statute_consent,
                "statute_consent_at": statute_consent_at,
                "statute_consent_version": statute_consent_version,
                "supply_municipality": supply_municipality,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.submission_created_read_extra_data_type_0 import SubmissionCreatedReadExtraDataType0
        from ..models.submission_created_read_extracted_data_type_0 import SubmissionCreatedReadExtractedDataType0
        from ..models.submission_created_read_id_extracted_data_type_0 import SubmissionCreatedReadIdExtractedDataType0

        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        data_sharing_consent = d.pop("data_sharing_consent")

        def _parse_data_sharing_consent_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_sharing_consent_at_type_0 = isoparse(data)

                return data_sharing_consent_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        data_sharing_consent_at = _parse_data_sharing_consent_at(d.pop("data_sharing_consent_at"))

        def _parse_data_sharing_consent_locale(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        data_sharing_consent_locale = _parse_data_sharing_consent_locale(d.pop("data_sharing_consent_locale"))

        def _parse_data_sharing_consent_offer_ids(data: object) -> list[str] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                data_sharing_consent_offer_ids_type_0 = cast(list[str], data)

                return data_sharing_consent_offer_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None, data)

        data_sharing_consent_offer_ids = _parse_data_sharing_consent_offer_ids(d.pop("data_sharing_consent_offer_ids"))

        def _parse_data_sharing_consent_text_sha256(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        data_sharing_consent_text_sha256 = _parse_data_sharing_consent_text_sha256(
            d.pop("data_sharing_consent_text_sha256")
        )

        def _parse_data_sharing_consent_text_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        data_sharing_consent_text_version = _parse_data_sharing_consent_text_version(
            d.pop("data_sharing_consent_text_version")
        )

        def _parse_email(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        email = _parse_email(d.pop("email"))

        def _parse_extra_data(data: object) -> None | SubmissionCreatedReadExtraDataType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_data_type_0 = SubmissionCreatedReadExtraDataType0.from_dict(data)

                return extra_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SubmissionCreatedReadExtraDataType0, data)

        extra_data = _parse_extra_data(d.pop("extra_data"))

        def _parse_extracted_data(data: object) -> None | SubmissionCreatedReadExtractedDataType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extracted_data_type_0 = SubmissionCreatedReadExtractedDataType0.from_dict(data)

                return extracted_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SubmissionCreatedReadExtractedDataType0, data)

        extracted_data = _parse_extracted_data(d.pop("extracted_data"))

        def _parse_first_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        first_name = _parse_first_name(d.pop("first_name"))

        def _parse_fiscal_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        fiscal_code = _parse_fiscal_code(d.pop("fiscal_code"))

        gdpr_consent = d.pop("gdpr_consent")

        def _parse_gdpr_consent_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                gdpr_consent_at_type_0 = isoparse(data)

                return gdpr_consent_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        gdpr_consent_at = _parse_gdpr_consent_at(d.pop("gdpr_consent_at"))

        def _parse_gdpr_consent_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        gdpr_consent_version = _parse_gdpr_consent_version(d.pop("gdpr_consent_version"))

        id = UUID(d.pop("id"))

        def _parse_id_extracted_data(data: object) -> None | SubmissionCreatedReadIdExtractedDataType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                id_extracted_data_type_0 = SubmissionCreatedReadIdExtractedDataType0.from_dict(data)

                return id_extracted_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SubmissionCreatedReadIdExtractedDataType0, data)

        id_extracted_data = _parse_id_extracted_data(d.pop("id_extracted_data"))

        keep_me_updated = d.pop("keep_me_updated")

        def _parse_last_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_name = _parse_last_name(d.pop("last_name"))

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        def _parse_phone(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        phone = _parse_phone(d.pop("phone"))

        phone_verified = d.pop("phone_verified")

        def _parse_phone_verified_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                phone_verified_at_type_0 = isoparse(data)

                return phone_verified_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        phone_verified_at = _parse_phone_verified_at(d.pop("phone_verified_at"))

        def _parse_pod_code(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        pod_code = _parse_pod_code(d.pop("pod_code"))

        policy_consent = d.pop("policy_consent")

        def _parse_policy_consent_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_consent_at_type_0 = isoparse(data)

                return policy_consent_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        policy_consent_at = _parse_policy_consent_at(d.pop("policy_consent_at"))

        def _parse_policy_consent_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        policy_consent_version = _parse_policy_consent_version(d.pop("policy_consent_version"))

        rec_slug = d.pop("rec_slug")

        ref = d.pop("ref")

        session_token = d.pop("session_token")

        share_provisioned = d.pop("share_provisioned")

        status = SubmissionStatus(d.pop("status"))

        statute_consent = d.pop("statute_consent")

        def _parse_statute_consent_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                statute_consent_at_type_0 = isoparse(data)

                return statute_consent_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        statute_consent_at = _parse_statute_consent_at(d.pop("statute_consent_at"))

        def _parse_statute_consent_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        statute_consent_version = _parse_statute_consent_version(d.pop("statute_consent_version"))

        def _parse_supply_municipality(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        supply_municipality = _parse_supply_municipality(d.pop("supply_municipality"))

        updated_at = isoparse(d.pop("updated_at"))

        submission_created_read = cls(
            created_at=created_at,
            data_sharing_consent=data_sharing_consent,
            data_sharing_consent_at=data_sharing_consent_at,
            data_sharing_consent_locale=data_sharing_consent_locale,
            data_sharing_consent_offer_ids=data_sharing_consent_offer_ids,
            data_sharing_consent_text_sha256=data_sharing_consent_text_sha256,
            data_sharing_consent_text_version=data_sharing_consent_text_version,
            email=email,
            extra_data=extra_data,
            extracted_data=extracted_data,
            first_name=first_name,
            fiscal_code=fiscal_code,
            gdpr_consent=gdpr_consent,
            gdpr_consent_at=gdpr_consent_at,
            gdpr_consent_version=gdpr_consent_version,
            id=id,
            id_extracted_data=id_extracted_data,
            keep_me_updated=keep_me_updated,
            last_name=last_name,
            notes=notes,
            phone=phone,
            phone_verified=phone_verified,
            phone_verified_at=phone_verified_at,
            pod_code=pod_code,
            policy_consent=policy_consent,
            policy_consent_at=policy_consent_at,
            policy_consent_version=policy_consent_version,
            rec_slug=rec_slug,
            ref=ref,
            session_token=session_token,
            share_provisioned=share_provisioned,
            status=status,
            statute_consent=statute_consent,
            statute_consent_at=statute_consent_at,
            statute_consent_version=statute_consent_version,
            supply_municipality=supply_municipality,
            updated_at=updated_at,
        )

        submission_created_read.additional_properties = d
        return submission_created_read

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
