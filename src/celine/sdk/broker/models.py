from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PipelineRunEvent(BaseModel):
    pipeline: str = Field(..., description="Pipeline identifier")
    status: str = Field(
        ..., description="Run status: started | completed | failed | ..."
    )
    run_id: str = Field(..., description="Unique run identifier (UUID)")
    timestamp: str = Field(..., description="Event business timestamp")
    duration_ms: Optional[int] = Field(
        default=0, description="Duration in milliseconds (0 when status=started)"
    )
    error: Optional[str] = Field(default=None, description="Error message")
    received_on: Optional[datetime] = Field(
        default=None, description="Internal ingestion timestamp"
    )
