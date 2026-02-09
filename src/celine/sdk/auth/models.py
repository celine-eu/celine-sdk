"""Authentication models."""
from __future__ import annotations

from dataclasses import dataclass
import time


@dataclass
class AccessToken:
    """Access token with metadata."""
    access_token: str
    expires_at: float
    refresh_token: str | None = None
    token_type: str = "Bearer"

    def is_valid(self, leeway: int = 30) -> bool:
        """Check if token is still valid with leeway."""
        return time.time() < (self.expires_at - leeway)
    
    def to_header(self) -> str:
        """Get Authorization header value."""
        return f"{self.token_type} {self.access_token}"
