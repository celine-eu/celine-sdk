from enum import Enum


class DatasetFilterRequestAccessLevel(str, Enum):
    INTERNAL = "internal"
    OPEN = "open"
    RESTRICTED = "restricted"

    def __str__(self) -> str:
        return str(self.value)
