from enum import Enum


class PropagationStep(str, Enum):
    ACCOUNT_PROFILE = "account_profile"
    CONSENT_KEYS = "consent_keys"
    IDENTITY_MAPPING = "identity_mapping"
    INVITATION = "invitation"
    REGISTRY_DELIVERY_POINT = "registry_delivery_point"
    REGISTRY_NAME = "registry_name"

    def __str__(self) -> str:
        return str(self.value)
