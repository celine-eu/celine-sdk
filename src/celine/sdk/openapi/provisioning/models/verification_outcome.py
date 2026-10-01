from enum import Enum


class VerificationOutcome(str, Enum):
    NOT_ON_DEV_LIST = "not_on_dev_list"
    NOT_REQUESTED = "not_requested"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
