from enum import Enum


class ErrorCode(str, Enum):
    AREA_IN_USE = "area_in_use"
    ASSET_KEY_TAKEN = "asset_key_taken"
    ASSET_KEY_TOO_LONG = "asset_key_too_long"
    ASSET_NOT_FOUND = "asset_not_found"
    COMMUNITY_NOT_FOUND = "community_not_found"
    DID_TAKEN = "did_taken"
    INVALID_STATUS = "invalid_status"
    MEMBER_KEY_TAKEN = "member_key_taken"
    MEMBER_NOT_FOUND = "member_not_found"
    SENSOR_HELD = "sensor_held"
    USER_ID_TAKEN = "user_id_taken"

    def __str__(self) -> str:
        return str(self.value)
