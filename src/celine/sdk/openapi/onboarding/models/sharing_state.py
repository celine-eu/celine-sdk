from enum import Enum


class SharingState(str, Enum):
    AMBIGUOUS_COMMUNITY = "ambiguous_community"
    IDENTITY_CONFLICT = "identity_conflict"
    NO_DATASPACE = "no_dataspace"
    NO_IDENTITY = "no_identity"
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
