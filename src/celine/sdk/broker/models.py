from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PipelineRunEvent(BaseModel):
    
    namespace: str = Field(..., description="Pipeline namespace")
    flow: Optional[str] = Field(..., description="Pipeline flow")
    status: str = Field(
        ..., description="Run status: started | completed | failed | ..."
    )
    run_id: str = Field(..., description="Unique run identifier (UUID)")
    timestamp: str = Field(..., description="Event business timestamp")
    duration_ms: Optional[int] = Field(
        default=0, description="Duration in milliseconds (0 when status=started)"
    )
    error: Optional[str] = Field(default=None, description="Error message")
    created: Optional[datetime] = Field(
        default=None, description="Internal ingestion timestamp"
    )
    correlation_id: Optional[str] = Field(
        default=None, description="Tracking id"
    )
