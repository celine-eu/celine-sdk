from enum import Enum


class DocumentType(str, Enum):
    GDPR_FORM = "gdpr_form"
    ID_CARD = "id_card"
    OTHER = "other"
    POLICY_DOC = "policy_doc"
    STATUTE_DOC = "statute_doc"
    UTILITY_BILL = "utility_bill"

    def __str__(self) -> str:
        return str(self.value)
