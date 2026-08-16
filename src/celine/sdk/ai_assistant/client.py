"""AI Assistant API wrapper.

Delegates to the generated client in ``celine.sdk.openapi.ai_assistant``, which
is what keeps the routes honest: a path this service renames disappears from the
generated package, and this module then fails to import rather than returning
404s at runtime.

**Two methods deliberately do not delegate**, and both would be broken by doing
so:

- ``chat_stream`` consumes a server-sent event stream. The generated client
  reads a whole response before returning; there is no streaming entry point.
- ``get_attachment_raw`` downloads a file. The generated operation calls
  ``response.json()`` on the body, which is wrong for bytes.

They use ``httpx`` directly, against the same base URL and bearer token.

The wrapper existed as hand-written httpx throughout because the generated
package did not exist: ``services.yaml`` pointed at ``/ai-assistant`` while the
platform routes this service at ``/assistant``, so every ``task gen`` fetched an
empty body and skipped it. Fixed 2026-08-15.

A failing request raises ``celine.sdk.openapi.ai_assistant.errors.UnexpectedStatus``
on the delegated methods, and ``httpx.HTTPStatusError`` on the two above.

Example — per-request usage (FastAPI):
    client = AssistantClient(base_url="http://ai-assistant:8000")

    @app.get("/api/conversations")
    async def conversations(token: str = Depends(get_token)):
        return await client.list_conversations(token=token)

Example — streaming chat:
    async for event in client.chat_stream(payload, token=token):
        print(event["type"], event["data"])
"""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

import httpx

from celine.sdk.openapi.ai_assistant import AuthenticatedClient
from celine.sdk.openapi.ai_assistant.api.default import (
    conversation_messages_conversations_conversation_id_messages_get as _conversation_messages,
    delete_attachment_attachments_attachment_id_delete as _delete_attachment,
    delete_conversation_conversations_conversation_id_delete as _delete_conversation,
    get_user_user_get as _get_user,
    health_health_get as _health,
    list_attachments_attachments_get as _list_attachments,
    list_conversations_conversations_get as _list_conversations,
    upload_user_upload_post as _upload,
)
from celine.sdk.openapi.ai_assistant.errors import UnexpectedStatus
from celine.sdk.openapi.ai_assistant.models import BodyUploadUserUploadPost
from celine.sdk.openapi.ai_assistant.types import File, Response

__all__ = ["AssistantClient"]


def _checked(response: Response[Any]) -> Response[Any]:
    """Raise on failure, and tolerate any success the spec did not enumerate.

    The generated client's own `raise_on_unexpected_status` treats *any*
    undeclared status as an error, including a successful one: these routes
    declare `200` and `422`, so a service answering `204 No Content` to a delete
    — which is the conventional answer — would raise. The previous hand-written
    wrapper used `raise_for_status()` and accepted it.

    So the check is on failure, not on undeclared-ness. A `422` raises here too
    rather than returning a parsed `HTTPValidationError` where callers expect a
    dictionary.
    """
    if response.status_code >= 400:
        raise UnexpectedStatus(response.status_code, response.content)
    return response


def _as_dict(parsed: Any) -> Any:
    """Return generated models as plain dictionaries.

    The routes that carry a response model (`/user`, `/health`) would otherwise
    change this wrapper's return type from `dict` to a generated class, which is
    a surface change for every caller.
    """
    to_dict = getattr(parsed, "to_dict", None)
    return to_dict() if callable(to_dict) else parsed


class AssistantClient:
    """User-scoped AI Assistant API client.

    Designed for per-request token usage: initialise once, pass the caller's
    token on each call.

    Args:
        base_url: Base URL of the AI Assistant API.
        default_token: Default bearer token when none provided per-call.
        timeout: Request timeout in seconds (default: 30.0).
        verify_ssl: Verify SSL certificates (default: True).
    """

    def __init__(
        self,
        base_url: str,
        *,
        default_token: Optional[str] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True,
    ):
        self._base_url = base_url.rstrip("/")
        self._default_token = default_token
        self._timeout = httpx.Timeout(timeout)
        self._verify_ssl = verify_ssl

    def _resolve_token(self, token: Optional[str]) -> str:
        actual = token or self._default_token
        if actual is None:
            raise ValueError("No token provided and no default_token set")
        return actual

    def _client(self, token: Optional[str]) -> AuthenticatedClient:
        """A generated client bound to this call's token."""
        return AuthenticatedClient(
            base_url=self._base_url,
            token=self._resolve_token(token),
            timeout=self._timeout,
            verify_ssl=self._verify_ssl,
        )

    def _raw_client(self, token: Optional[str]) -> httpx.AsyncClient:
        """A plain httpx client, for the streaming and binary paths only."""
        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            verify=self._verify_ssl,
            headers={"Authorization": f"Bearer {self._resolve_token(token)}"},
        )

    # ── Chat (SSE streaming) ────────────────────────────────────────────

    async def chat_stream(
        self,
        payload: dict[str, Any],
        *,
        token: Optional[str] = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream a chat completion as parsed SSE events.

        Not delegated: the generated client has no streaming entry point.

        Args:
            payload: JSON body for ``POST /chat`` (model-defined schema).
            token: Bearer token override.

        Yields:
            ``{"type": "<event-type>", "data": <parsed-json>}`` for each
            SSE frame.  If the ``data`` line is not valid JSON the raw
            string is returned as-is in the ``data`` key.
        """
        async with self._raw_client(token) as client:
            async with client.stream("POST", "/chat", json=payload) as response:
                response.raise_for_status()
                event_type: Optional[str] = None
                async for line in response.aiter_lines():
                    if line.startswith("event:"):
                        event_type = line[len("event:"):].strip()
                    elif line.startswith("data:"):
                        raw = line[len("data:"):].strip()
                        try:
                            data = json.loads(raw)
                        except (json.JSONDecodeError, ValueError):
                            data = raw
                        yield {"type": event_type or "message", "data": data}
                        event_type = None
                    elif line == "":
                        # SSE blank-line delimiter — reset for next event
                        event_type = None

    # ── File upload ─────────────────────────────────────────────────────

    async def upload(
        self,
        file_path: str | Path,
        *,
        filename: Optional[str] = None,
        content_type: str = "application/octet-stream",
        token: Optional[str] = None,
    ) -> dict[str, Any]:
        """Upload a file via ``POST /upload`` (multipart/form-data).

        Args:
            file_path: Local path to the file to upload.
            filename: Override the filename sent in the multipart header.
            content_type: MIME type of the file.
            token: Bearer token override.

        Returns:
            Parsed JSON response from the server.
        """
        path = Path(file_path)
        body = BodyUploadUserUploadPost(
            file=File(
                payload=BytesIO(path.read_bytes()),
                file_name=filename or path.name,
                mime_type=content_type,
            )
        )
        response = _checked(
            await _upload.asyncio_detailed(client=self._client(token), body=body)
        )
        return _as_dict(response.parsed)

    # ── Conversations ───────────────────────────────────────────────────

    async def list_conversations(
        self, *, token: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """List conversations for the authenticated user."""
        response = _checked(await _list_conversations.asyncio_detailed(client=self._client(token)))
        return _as_dict(response.parsed)

    async def get_conversation_messages(
        self,
        conversation_id: str,
        *,
        token: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Retrieve messages for a conversation."""
        response = _checked(
            await _conversation_messages.asyncio_detailed(
                conversation_id, client=self._client(token)
            )
        )
        return _as_dict(response.parsed)

    async def delete_conversation(
        self,
        conversation_id: str,
        *,
        token: Optional[str] = None,
    ) -> None:
        """Delete a conversation."""
        _checked(
            await _delete_conversation.asyncio_detailed(
                conversation_id, client=self._client(token)
            )
        )

    # ── Attachments ─────────────────────────────────────────────────────

    async def list_attachments(
        self, *, token: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """List attachments for the authenticated user."""
        response = _checked(await _list_attachments.asyncio_detailed(client=self._client(token)))
        return _as_dict(response.parsed)

    async def get_attachment_raw(
        self,
        attachment_id: str,
        *,
        token: Optional[str] = None,
    ) -> bytes:
        """Download the raw file content of an attachment.

        Not delegated: the generated operation parses the body as JSON, which
        would corrupt or reject a file.

        Returns:
            Raw bytes of the attachment file.
        """
        async with self._raw_client(token) as client:
            response = await client.get(f"/attachments/{attachment_id}/raw")
            response.raise_for_status()
            return response.content

    async def delete_attachment(
        self,
        attachment_id: str,
        *,
        token: Optional[str] = None,
    ) -> None:
        """Delete an attachment."""
        _checked(
            await _delete_attachment.asyncio_detailed(
                attachment_id, client=self._client(token)
            )
        )

    # ── User / Health ───────────────────────────────────────────────────

    async def get_user(self, *, token: Optional[str] = None) -> dict[str, Any]:
        """Get authenticated user info."""
        response = _checked(await _get_user.asyncio_detailed(client=self._client(token)))
        return _as_dict(response.parsed)

    async def health(self, *, token: Optional[str] = None) -> dict[str, Any]:
        """Check service health."""
        response = _checked(await _health.asyncio_detailed(client=self._client(token)))
        return _as_dict(response.parsed)
