from enum import Enum


class InvitationIntent(str, Enum):
    INVITATION = "invitation"
    PASSWORD_RESET = "password_reset"

    def __str__(self) -> str:
        return str(self.value)
