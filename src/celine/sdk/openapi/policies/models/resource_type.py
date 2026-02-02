from enum import Enum


class ResourceType(str, Enum):
    DATASET = "dataset"
    DT = "dt"
    PIPELINE = "pipeline"
    TOPIC = "topic"
    USERDATA = "userdata"

    def __str__(self) -> str:
        return str(self.value)
