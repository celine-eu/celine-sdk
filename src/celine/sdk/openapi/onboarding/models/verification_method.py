from enum import Enum


class VerificationMethod(str, Enum):
    OFFLINE = "offline"
    UPLOADED_DOCUMENT = "uploaded-document"

    def __str__(self) -> str:
        return str(self.value)
