from enum import Enum


class RevisionCreateField(str, Enum):
    EMAIL = "email"
    FIRST_NAME = "first_name"
    FISCAL_CODE = "fiscal_code"
    LAST_NAME = "last_name"
    POD_CODE = "pod_code"
    SUPPLY_ADDRESS = "supply_address"

    def __str__(self) -> str:
        return str(self.value)
