from enum import Enum


class VerificationMethod(str, Enum):
    OFFLINE = "offline"
    OFFLINE_WITH_EVIDENCE = "offline-with-evidence"
    UPLOADED_DOCUMENT = "uploaded-document"

    def __str__(self) -> str:
        return str(self.value)
