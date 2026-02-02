from enum import Enum


class ListCommunitiesCommunitiesGetFormat(str, Enum):
    JSON = "json"
    JSONLD = "jsonld"

    def __str__(self) -> str:
        return str(self.value)
