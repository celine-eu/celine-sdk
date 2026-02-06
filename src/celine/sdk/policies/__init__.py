"""
Authorization policies client using the generated OpenAPI client.

This module provides a convenient wrapper around the generated
celine.sdk.openapi.policies client for authorization operations.
"""

from celine.sdk.policies.client import AuthorizationClient, AuthorizationError

__all__ = [
    "AuthorizationClient",
    "AuthorizationError",
]
