from enum import Enum


class InvitationOutcome(str, Enum):
    ACCOUNT_DISABLED = "account_disabled"
    COOLDOWN = "cooldown"
    HAS_PASSWORD = "has_password"
    NOT_ON_DEV_LIST = "not_on_dev_list"
    NOT_REQUESTED = "not_requested"
    NO_EMAIL = "no_email"
    SEND_FAILED = "send_failed"
    SENT = "sent"

    def __str__(self) -> str:
        return str(self.value)
