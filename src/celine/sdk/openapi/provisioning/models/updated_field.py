from enum import Enum


class UpdatedField(str, Enum):
    EMAIL = "email"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"

    def __str__(self) -> str:
        return str(self.value)
