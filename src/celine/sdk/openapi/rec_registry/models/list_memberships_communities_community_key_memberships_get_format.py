from enum import Enum


class ListMembershipsCommunitiesCommunityKeyMembershipsGetFormat(str, Enum):
    JSON = "json"
    JSONLD = "jsonld"

    def __str__(self) -> str:
        return str(self.value)
