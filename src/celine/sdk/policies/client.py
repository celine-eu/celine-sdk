# src/celine/sdk/policies/client.py
"""
Authorization client wrapper around the generated OpenAPI client.

This provides a simplified, high-level interface for authorization
while using the generated celine.sdk.openapi.policies client underneath.
"""
from __future__ import annotations

import logging
from typing import Optional

from httpx import Timeout

from celine.sdk.openapi.policies import Client
from celine.sdk.openapi.policies.api.authorization import authorize_authorize_post
from celine.sdk.openapi.policies.models import (
    Action,
    AuthorizeRequest,
    AuthorizeResponse,
    Resource,
    ResourceType,
    Attributes,
)
from celine.sdk.openapi.policies.models.http_validation_error import HTTPValidationError
from celine.sdk.openapi.policies.types import UNSET

logger = logging.getLogger(__name__)


class AuthorizationError(Exception):
    """Exception raised when authorization evaluation fails."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class AuthorizationClient:
    """
    High-level client for authorization using the policies service.

    This wraps the generated OpenAPI client to provide a simpler interface
    while handling common patterns like error handling and logging.

    Usage:
        client = AuthorizationClient(base_url="http://policies:8000")

        allowed = await client.authorize(
            action="read",
            resource_type="dataset",
            resource_id="my_dataset",
            resource_attributes={"access_level": "internal"},
            authorization_header="Bearer token123"
        )

        if allowed:
            # Grant access
            pass
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        raise_on_unexpected_status: bool = False,
    ):
        """
        Initialize the authorization client.

        Args:
            base_url: Base URL of the policies service (e.g., "http://policies:8000")
            timeout: Request timeout in seconds
            raise_on_unexpected_status: Whether to raise on unexpected HTTP status
        """
        self._client = Client(
            base_url=base_url,
            timeout=Timeout(timeout),
            raise_on_unexpected_status=raise_on_unexpected_status,
        )

        logger.debug(f"AuthorizationClient initialized with base_url: {base_url}")

    async def authorize(
        self,
        *,
        action: str,
        resource_type: str,
        resource_id: str,
        resource_attributes: Optional[dict] = None,
        authorization_header: Optional[str] = None,
        x_request_id: Optional[str] = None,
        x_source_service: Optional[str] = None,
    ) -> bool:
        """
        Authorize a resource action.

        This is a convenience method that builds the request, calls the API,
        and returns a simple boolean result.

        Args:
            action: Action name (e.g., "read", "write")
            resource_type: Resource type (e.g., "dataset", "dt", "pipeline")
            resource_id: Resource identifier
            resource_attributes: Optional resource metadata (e.g., access_level, namespace)
            authorization_header: Optional JWT token (e.g., "Bearer token123")
            x_request_id: Optional request ID for tracing
            x_source_service: Optional source service identifier

        Returns:
            True if allowed, False if denied

        Raises:
            AuthorizationError: If the request fails
        """
        try:
            response = await self.authorize_detailed(
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                resource_attributes=resource_attributes,
                authorization_header=authorization_header,
                x_request_id=x_request_id,
                x_source_service=x_source_service,
            )

            return response.allowed

        except AuthorizationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during authorization: {e}")
            raise AuthorizationError(f"Authorization request failed: {e}") from e

    async def authorize_detailed(
        self,
        *,
        action: str,
        resource_type: str,
        resource_id: str,
        resource_attributes: Optional[dict] = None,
        authorization_header: Optional[str] = None,
        x_request_id: Optional[str] = None,
        x_source_service: Optional[str] = None,
    ) -> AuthorizeResponse:
        """
        Authorize a resource action and return the full response.

        This method returns the complete AuthorizeResponse object which includes
        the allowed field, request_id, and optional reason.

        Args:
            action: Action name (e.g., "read", "write")
            resource_type: Resource type (e.g., "dataset", "dt", "pipeline")
            resource_id: Resource identifier
            resource_attributes: Optional resource metadata
            authorization_header: Optional JWT token (e.g., "Bearer token123")
            x_request_id: Optional request ID for tracing
            x_source_service: Optional source service identifier

        Returns:
            AuthorizeResponse with allowed, request_id, and reason fields

        Raises:
            AuthorizationError: If the request fails
        """
        # Build the request
        request = self._build_authorize_request(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_attributes=resource_attributes,
        )

        logger.debug(
            "Authorizing resource",
            extra={
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
            },
        )

        # Call the API
        try:
            response = await authorize_authorize_post.asyncio(
                client=self._client,
                body=request,
                x_request_id=x_request_id or UNSET,
                x_source_service=x_source_service or UNSET,
                authorization=authorization_header or UNSET,
            )

            if response is None:
                raise AuthorizationError("Authorization request returned no response")
            if isinstance(response, HTTPValidationError):
                raise AuthorizationError("Authorization request failed")

            # Handle validation errors
            if hasattr(response, "reason"):
                # This is an HTTPValidationError
                raise AuthorizationError(
                    f"Validation error: {response.reason}",
                    status_code=422,
                )

            logger.debug(
                f"Authorization result: {response.allowed}",
                extra={
                    "resource_id": resource_id,
                    "allowed": response.allowed,
                    "reason": response.reason if response.reason != UNSET else None,
                    "request_id": response.request_id,
                },
            )

            return response

        except Exception as e:
            logger.error(
                f"Authorization request failed for {resource_type}/{resource_id}: {e}"
            )
            raise AuthorizationError(
                f"Failed to authorize {resource_type}/{resource_id}: {e}"
            ) from e

    def _build_authorize_request(
        self,
        *,
        action: str,
        resource_type: str,
        resource_id: str,
        resource_attributes: Optional[dict] = None,
    ) -> AuthorizeRequest:
        """
        Build an AuthorizeRequest from simple parameters.

        Args:
            action: Action name
            resource_type: Resource type
            resource_id: Resource identifier
            resource_attributes: Optional resource metadata

        Returns:
            AuthorizeRequest ready to send to the API
        """
        # Build Action
        action_obj = Action(name=action)

        # Build Resource
        try:
            resource_type_enum = ResourceType(resource_type)
        except ValueError:
            # If resource type not in enum, log warning but continue
            logger.warning(
                f"Resource type '{resource_type}' not in ResourceType enum, "
                f"using it anyway"
            )
            # Use the first enum value as default, the API will handle it
            resource_type_enum = ResourceType.DATASET

        # Build attributes if provided
        attributes = UNSET
        if resource_attributes:
            attr_obj = Attributes()
            for key, value in resource_attributes.items():
                attr_obj[key] = value
            attributes = attr_obj

        resource_obj = Resource(
            id=resource_id,
            type_=resource_type_enum,
            attributes=attributes,
        )

        return AuthorizeRequest(
            action=action_obj,
            resource=resource_obj,
        )

    async def __aenter__(self):
        """Async context manager entry."""
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        """Async context manager exit."""
        await self._client.__aexit__(*args, **kwargs)


# Convenience function for quick authorization checks
async def authorize(
    *,
    base_url: str,
    action: str,
    resource_type: str,
    resource_id: str,
    resource_attributes: Optional[dict] = None,
    authorization_header: Optional[str] = None,
    timeout: float = 5.0,
) -> bool:
    """
    Convenience function for quick authorization checks.

    This creates a temporary client and performs authorization in one call.
    For repeated calls, use AuthorizationClient directly to reuse the client.

    Args:
        base_url: Base URL of the policies service
        action: Action name (e.g., "read", "write")
        resource_type: Resource type (e.g., "dataset", "dt")
        resource_id: Resource identifier
        resource_attributes: Optional resource metadata
        authorization_header: Optional JWT token
        timeout: Request timeout in seconds

    Returns:
        True if allowed, False if denied

    Raises:
        AuthorizationError: If the request fails
    """
    client = AuthorizationClient(base_url=base_url, timeout=timeout)

    async with client:
        return await client.authorize(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_attributes=resource_attributes,
            authorization_header=authorization_header,
        )
