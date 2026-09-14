from enum import Enum


class SubmissionUpdateLocaleType0(str, Enum):
    EN = "en"
    ES = "es"
    IT = "it"

    def __str__(self) -> str:
        return str(self.value)
