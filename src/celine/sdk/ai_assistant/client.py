"""AI Assistant API wrapper.

Manually-authored client using httpx.AsyncClient directly, since the
generated OpenAPI client is not yet available (the service must be running
for ``task gen`` to fetch its OpenAPI spec).

Once ``src/celine/sdk/openapi/ai_assistant/`` is generated, this wrapper
can be updated to delegate to the generated AuthenticatedClient — the
public surface stays the same.

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
from pathlib import Path
from typing import Any, AsyncGenerator, Optional

import httpx

__all__ = ["AssistantClient"]


class AssistantClient:
    """User-scoped AI Assistant API client.

    Uses ``httpx.AsyncClient`` directly (no generated code dependency).

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

    def _build_client(self, token: Optional[str]) -> httpx.AsyncClient:
        """Return a fresh ``httpx.AsyncClient`` with auth headers."""
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

        Args:
            payload: JSON body for ``POST /chat`` (model-defined schema).
            token: Bearer token override.

        Yields:
            ``{"type": "<event-type>", "data": <parsed-json>}`` for each
            SSE frame.  If the ``data`` line is not valid JSON the raw
            string is returned as-is in the ``data`` key.
        """
        async with self._build_client(token) as client:
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
        upload_name = filename or path.name
        async with self._build_client(token) as client:
            with path.open("rb") as fh:
                response = await client.post(
                    "/upload",
                    files={"file": (upload_name, fh, content_type)},
                )
            response.raise_for_status()
            return response.json()

    # ── Conversations ───────────────────────────────────────────────────

    async def list_conversations(
        self, *, token: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """List conversations for the authenticated user."""
        async with self._build_client(token) as client:
            response = await client.get("/conversations")
            response.raise_for_status()
            return response.json()

    async def get_conversation_messages(
        self,
        conversation_id: str,
        *,
        token: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Retrieve messages for a conversation."""
        async with self._build_client(token) as client:
            response = await client.get(f"/conversations/{conversation_id}/messages")
            response.raise_for_status()
            return response.json()

    async def delete_conversation(
        self,
        conversation_id: str,
        *,
        token: Optional[str] = None,
    ) -> None:
        """Delete a conversation."""
        async with self._build_client(token) as client:
            response = await client.delete(f"/conversations/{conversation_id}")
            response.raise_for_status()

    # ── Attachments ─────────────────────────────────────────────────────

    async def list_attachments(
        self, *, token: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """List attachments for the authenticated user."""
        async with self._build_client(token) as client:
            response = await client.get("/attachments")
            response.raise_for_status()
            return response.json()

    async def get_attachment_raw(
        self,
        attachment_id: str,
        *,
        token: Optional[str] = None,
    ) -> bytes:
        """Download the raw file content of an attachment.

        Returns:
            Raw bytes of the attachment file.
        """
        async with self._build_client(token) as client:
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
        async with self._build_client(token) as client:
            response = await client.delete(f"/attachments/{attachment_id}")
            response.raise_for_status()

    # ── User / Health ───────────────────────────────────────────────────

    async def get_user(
        self, *, token: Optional[str] = None
    ) -> dict[str, Any]:
        """Get authenticated user info."""
        async with self._build_client(token) as client:
            response = await client.get("/user")
            response.raise_for_status()
            return response.json()

    async def health(self, *, token: Optional[str] = None) -> dict[str, Any]:
        """Check service health."""
        async with self._build_client(token) as client:
            response = await client.get("/health")
            response.raise_for_status()
            return response.json()
