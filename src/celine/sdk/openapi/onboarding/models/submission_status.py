from enum import Enum


class SubmissionStatus(str, Enum):
    APPROVED = "approved"
    DRAFT = "draft"
    REJECTED = "rejected"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"

    def __str__(self) -> str:
        return str(self.value)
