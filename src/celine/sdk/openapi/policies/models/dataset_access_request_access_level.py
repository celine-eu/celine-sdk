from enum import Enum


class DatasetAccessRequestAccessLevel(str, Enum):
    INTERNAL = "internal"
    OPEN = "open"
    RESTRICTED = "restricted"

    def __str__(self) -> str:
        return str(self.value)
