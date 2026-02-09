# celine/sdk/dt/__init__.py
"""
Digital Twin client — curated wrapper around the generated OpenAPI client.

Provides ``DTClient`` as the main entry point with ``.communities`` and
``.participants`` accessors.

Usage::

    from celine.sdk.auth.static import StaticTokenProvider
    from celine.sdk.dt import DTClient

    dt = DTClient(
        base_url="http://dt:8000",
        token_provider=StaticTokenProvider(jwt_token),
    )

    balance = await dt.communities.energy_balance("rec-folgaria")
    profile = await dt.participants.profile("p-123")
"""
from celine.sdk.dt.client import DTClient
from celine.sdk.dt.community import CommunityClient
from celine.sdk.dt.participant import ParticipantClient

__all__ = [
    "DTClient",
    "CommunityClient",
    "ParticipantClient",
]
