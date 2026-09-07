from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.submission_status import SubmissionStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.submission_update_extra_data_type_0 import SubmissionUpdateExtraDataType0
    from ..models.submission_update_extracted_data_type_0 import SubmissionUpdateExtractedDataType0
    from ..models.submission_update_id_extracted_data_type_0 import SubmissionUpdateIdExtractedDataType0


T = TypeVar("T", bound="SubmissionUpdate")


@_attrs_define
class SubmissionUpdate:
    """
    Attributes:
        data_sharing_consent (bool | None | Unset):
        data_sharing_consent_locale (None | str | Unset):
        data_sharing_consent_offer_ids (list[str] | None | Unset):
        data_sharing_consent_text_sha256 (None | str | Unset):
        data_sharing_consent_text_version (None | str | Unset):
        email (None | str | Unset):
        extra_data (None | SubmissionUpdateExtraDataType0 | Unset):
        extracted_data (None | SubmissionUpdateExtractedDataType0 | Unset):
        first_name (None | str | Unset):
        fiscal_code (None | str | Unset):
        id_extracted_data (None | SubmissionUpdateIdExtractedDataType0 | Unset):
        keep_me_updated (bool | None | Unset):
        last_name (None | str | Unset):
        notes (None | str | Unset):
        phone (None | str | Unset):
        pod_code (None | str | Unset):
        status (None | SubmissionStatus | Unset):
        statute_consent (bool | None | Unset):
        supply_municipality (None | str | Unset):
    """

    data_sharing_consent: bool | None | Unset = UNSET
    data_sharing_consent_locale: None | str | Unset = UNSET
    data_sharing_consent_offer_ids: list[str] | None | Unset = UNSET
    data_sharing_consent_text_sha256: None | str | Unset = UNSET
    data_sharing_consent_text_version: None | str | Unset = UNSET
    email: None | str | Unset = UNSET
    extra_data: None | SubmissionUpdateExtraDataType0 | Unset = UNSET
    extracted_data: None | SubmissionUpdateExtractedDataType0 | Unset = UNSET
    first_name: None | str | Unset = UNSET
    fiscal_code: None | str | Unset = UNSET
    id_extracted_data: None | SubmissionUpdateIdExtractedDataType0 | Unset = UNSET
    keep_me_updated: bool | None | Unset = UNSET
    last_name: None | str | Unset = UNSET
    notes: None | str | Unset = UNSET
    phone: None | str | Unset = UNSET
    pod_code: None | str | Unset = UNSET
    status: None | SubmissionStatus | Unset = UNSET
    statute_consent: bool | None | Unset = UNSET
    supply_municipality: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.submission_update_extra_data_type_0 import SubmissionUpdateExtraDataType0
        from ..models.submission_update_extracted_data_type_0 import SubmissionUpdateExtractedDataType0
        from ..models.submission_update_id_extracted_data_type_0 import SubmissionUpdateIdExtractedDataType0

        data_sharing_consent: bool | None | Unset
        if isinstance(self.data_sharing_consent, Unset):
            data_sharing_consent = UNSET
        else:
            data_sharing_consent = self.data_sharing_consent

        data_sharing_consent_locale: None | str | Unset
        if isinstance(self.data_sharing_consent_locale, Unset):
            data_sharing_consent_locale = UNSET
        else:
            data_sharing_consent_locale = self.data_sharing_consent_locale

        data_sharing_consent_offer_ids: list[str] | None | Unset
        if isinstance(self.data_sharing_consent_offer_ids, Unset):
            data_sharing_consent_offer_ids = UNSET
        elif isinstance(self.data_sharing_consent_offer_ids, list):
            data_sharing_consent_offer_ids = self.data_sharing_consent_offer_ids

        else:
            data_sharing_consent_offer_ids = self.data_sharing_consent_offer_ids

        data_sharing_consent_text_sha256: None | str | Unset
        if isinstance(self.data_sharing_consent_text_sha256, Unset):
            data_sharing_consent_text_sha256 = UNSET
        else:
            data_sharing_consent_text_sha256 = self.data_sharing_consent_text_sha256

        data_sharing_consent_text_version: None | str | Unset
        if isinstance(self.data_sharing_consent_text_version, Unset):
            data_sharing_consent_text_version = UNSET
        else:
            data_sharing_consent_text_version = self.data_sharing_consent_text_version

        email: None | str | Unset
        if isinstance(self.email, Unset):
            email = UNSET
        else:
            email = self.email

        extra_data: dict[str, Any] | None | Unset
        if isinstance(self.extra_data, Unset):
            extra_data = UNSET
        elif isinstance(self.extra_data, SubmissionUpdateExtraDataType0):
            extra_data = self.extra_data.to_dict()
        else:
            extra_data = self.extra_data

        extracted_data: dict[str, Any] | None | Unset
        if isinstance(self.extracted_data, Unset):
            extracted_data = UNSET
        elif isinstance(self.extracted_data, SubmissionUpdateExtractedDataType0):
            extracted_data = self.extracted_data.to_dict()
        else:
            extracted_data = self.extracted_data

        first_name: None | str | Unset
        if isinstance(self.first_name, Unset):
            first_name = UNSET
        else:
            first_name = self.first_name

        fiscal_code: None | str | Unset
        if isinstance(self.fiscal_code, Unset):
            fiscal_code = UNSET
        else:
            fiscal_code = self.fiscal_code

        id_extracted_data: dict[str, Any] | None | Unset
        if isinstance(self.id_extracted_data, Unset):
            id_extracted_data = UNSET
        elif isinstance(self.id_extracted_data, SubmissionUpdateIdExtractedDataType0):
            id_extracted_data = self.id_extracted_data.to_dict()
        else:
            id_extracted_data = self.id_extracted_data

        keep_me_updated: bool | None | Unset
        if isinstance(self.keep_me_updated, Unset):
            keep_me_updated = UNSET
        else:
            keep_me_updated = self.keep_me_updated

        last_name: None | str | Unset
        if isinstance(self.last_name, Unset):
            last_name = UNSET
        else:
            last_name = self.last_name

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        phone: None | str | Unset
        if isinstance(self.phone, Unset):
            phone = UNSET
        else:
            phone = self.phone

        pod_code: None | str | Unset
        if isinstance(self.pod_code, Unset):
            pod_code = UNSET
        else:
            pod_code = self.pod_code

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, SubmissionStatus):
            status = self.status.value
        else:
            status = self.status

        statute_consent: bool | None | Unset
        if isinstance(self.statute_consent, Unset):
            statute_consent = UNSET
        else:
            statute_consent = self.statute_consent

        supply_municipality: None | str | Unset
        if isinstance(self.supply_municipality, Unset):
            supply_municipality = UNSET
        else:
            supply_municipality = self.supply_municipality

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data_sharing_consent is not UNSET:
            field_dict["data_sharing_consent"] = data_sharing_consent
        if data_sharing_consent_locale is not UNSET:
            field_dict["data_sharing_consent_locale"] = data_sharing_consent_locale
        if data_sharing_consent_offer_ids is not UNSET:
            field_dict["data_sharing_consent_offer_ids"] = data_sharing_consent_offer_ids
        if data_sharing_consent_text_sha256 is not UNSET:
            field_dict["data_sharing_consent_text_sha256"] = data_sharing_consent_text_sha256
        if data_sharing_consent_text_version is not UNSET:
            field_dict["data_sharing_consent_text_version"] = data_sharing_consent_text_version
        if email is not UNSET:
            field_dict["email"] = email
        if extra_data is not UNSET:
            field_dict["extra_data"] = extra_data
        if extracted_data is not UNSET:
            field_dict["extracted_data"] = extracted_data
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if fiscal_code is not UNSET:
            field_dict["fiscal_code"] = fiscal_code
        if id_extracted_data is not UNSET:
            field_dict["id_extracted_data"] = id_extracted_data
        if keep_me_updated is not UNSET:
            field_dict["keep_me_updated"] = keep_me_updated
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if notes is not UNSET:
            field_dict["notes"] = notes
        if phone is not UNSET:
            field_dict["phone"] = phone
        if pod_code is not UNSET:
            field_dict["pod_code"] = pod_code
        if status is not UNSET:
            field_dict["status"] = status
        if statute_consent is not UNSET:
            field_dict["statute_consent"] = statute_consent
        if supply_municipality is not UNSET:
            field_dict["supply_municipality"] = supply_municipality

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.submission_update_extra_data_type_0 import SubmissionUpdateExtraDataType0
        from ..models.submission_update_extracted_data_type_0 import SubmissionUpdateExtractedDataType0
        from ..models.submission_update_id_extracted_data_type_0 import SubmissionUpdateIdExtractedDataType0

        d = dict(src_dict)

        def _parse_data_sharing_consent(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        data_sharing_consent = _parse_data_sharing_consent(d.pop("data_sharing_consent", UNSET))

        def _parse_data_sharing_consent_locale(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        data_sharing_consent_locale = _parse_data_sharing_consent_locale(d.pop("data_sharing_consent_locale", UNSET))

        def _parse_data_sharing_consent_offer_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                data_sharing_consent_offer_ids_type_0 = cast(list[str], data)

                return data_sharing_consent_offer_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        data_sharing_consent_offer_ids = _parse_data_sharing_consent_offer_ids(
            d.pop("data_sharing_consent_offer_ids", UNSET)
        )

        def _parse_data_sharing_consent_text_sha256(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        data_sharing_consent_text_sha256 = _parse_data_sharing_consent_text_sha256(
            d.pop("data_sharing_consent_text_sha256", UNSET)
        )

        def _parse_data_sharing_consent_text_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        data_sharing_consent_text_version = _parse_data_sharing_consent_text_version(
            d.pop("data_sharing_consent_text_version", UNSET)
        )

        def _parse_email(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        email = _parse_email(d.pop("email", UNSET))

        def _parse_extra_data(data: object) -> None | SubmissionUpdateExtraDataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_data_type_0 = SubmissionUpdateExtraDataType0.from_dict(data)

                return extra_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SubmissionUpdateExtraDataType0 | Unset, data)

        extra_data = _parse_extra_data(d.pop("extra_data", UNSET))

        def _parse_extracted_data(data: object) -> None | SubmissionUpdateExtractedDataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extracted_data_type_0 = SubmissionUpdateExtractedDataType0.from_dict(data)

                return extracted_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SubmissionUpdateExtractedDataType0 | Unset, data)

        extracted_data = _parse_extracted_data(d.pop("extracted_data", UNSET))

        def _parse_first_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        first_name = _parse_first_name(d.pop("first_name", UNSET))

        def _parse_fiscal_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        fiscal_code = _parse_fiscal_code(d.pop("fiscal_code", UNSET))

        def _parse_id_extracted_data(data: object) -> None | SubmissionUpdateIdExtractedDataType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                id_extracted_data_type_0 = SubmissionUpdateIdExtractedDataType0.from_dict(data)

                return id_extracted_data_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SubmissionUpdateIdExtractedDataType0 | Unset, data)

        id_extracted_data = _parse_id_extracted_data(d.pop("id_extracted_data", UNSET))

        def _parse_keep_me_updated(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        keep_me_updated = _parse_keep_me_updated(d.pop("keep_me_updated", UNSET))

        def _parse_last_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_name = _parse_last_name(d.pop("last_name", UNSET))

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        def _parse_phone(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        phone = _parse_phone(d.pop("phone", UNSET))

        def _parse_pod_code(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        pod_code = _parse_pod_code(d.pop("pod_code", UNSET))

        def _parse_status(data: object) -> None | SubmissionStatus | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = SubmissionStatus(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | SubmissionStatus | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_statute_consent(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        statute_consent = _parse_statute_consent(d.pop("statute_consent", UNSET))

        def _parse_supply_municipality(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        supply_municipality = _parse_supply_municipality(d.pop("supply_municipality", UNSET))

        submission_update = cls(
            data_sharing_consent=data_sharing_consent,
            data_sharing_consent_locale=data_sharing_consent_locale,
            data_sharing_consent_offer_ids=data_sharing_consent_offer_ids,
            data_sharing_consent_text_sha256=data_sharing_consent_text_sha256,
            data_sharing_consent_text_version=data_sharing_consent_text_version,
            email=email,
            extra_data=extra_data,
            extracted_data=extracted_data,
            first_name=first_name,
            fiscal_code=fiscal_code,
            id_extracted_data=id_extracted_data,
            keep_me_updated=keep_me_updated,
            last_name=last_name,
            notes=notes,
            phone=phone,
            pod_code=pod_code,
            status=status,
            statute_consent=statute_consent,
            supply_municipality=supply_municipality,
        )

        submission_update.additional_properties = d
        return submission_update

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
