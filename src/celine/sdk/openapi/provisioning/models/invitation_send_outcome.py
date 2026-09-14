from enum import Enum


class InvitationSendOutcome(str, Enum):
    NOT_ON_DEV_LIST = "not_on_dev_list"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
