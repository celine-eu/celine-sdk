from enum import Enum


class CommitmentOutStatus(str, Enum):
    CANCELLED = "cancelled"
    COMMITTED = "committed"
    REJECTED = "rejected"
    SETTLED = "settled"

    def __str__(self) -> str:
        return str(self.value)
