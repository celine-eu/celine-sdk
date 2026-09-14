from enum import Enum


class InvitationOutcome(str, Enum):
    ACCOUNT_DISABLED = "account_disabled"
    HAS_PASSWORD = "has_password"
    NOT_ON_DEV_LIST = "not_on_dev_list"
    NOT_REQUESTED = "not_requested"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
