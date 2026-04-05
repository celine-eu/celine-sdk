from enum import Enum


class SuggestionRespondResponseStatus(str, Enum):
    COMMITTED = "committed"
    DECLINED = "declined"

    def __str__(self) -> str:
        return str(self.value)
