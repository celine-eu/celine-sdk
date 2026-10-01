from enum import Enum


class ErrorCode(str, Enum):
    AREA_IN_USE = "area_in_use"
    AREA_KEY_TAKEN = "area_key_taken"
    AREA_NOT_FOUND = "area_not_found"
    ASSET_KEY_TAKEN = "asset_key_taken"
    ASSET_KEY_TOO_LONG = "asset_key_too_long"
    ASSET_NOT_FOUND = "asset_not_found"
    COMMUNITY_NOT_FOUND = "community_not_found"
    DELIVERY_POINT_HELD = "delivery_point_held"
    DELIVERY_POINT_LINKED = "delivery_point_linked"
    DID_TAKEN = "did_taken"
    INVALID_AREA_BOUNDARY = "invalid_area_boundary"
    INVALID_AREA_KEY = "invalid_area_key"
    INVALID_ROLE = "invalid_role"
    INVALID_STATUS = "invalid_status"
    MEMBER_KEY_TAKEN = "member_key_taken"
    MEMBER_NOT_FOUND = "member_not_found"
    NOT_A_MEMBER = "not_a_member"
    SENSOR_HELD = "sensor_held"
    TOPOLOGY_NODE_IN_USE = "topology_node_in_use"
    UNKNOWN_AREA = "unknown_area"
    USER_ID_TAKEN = "user_id_taken"

    def __str__(self) -> str:
        return str(self.value)
