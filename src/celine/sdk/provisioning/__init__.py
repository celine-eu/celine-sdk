"""Provisioning API wrapper.

The only writer of participant accounts in the celine realm. Every other way of
making a login — a service holding its own Keycloak grant, a hand-run CLI —
is what this service replaced; see celine-policies `docs/decisions/ADR-0007`.

**It has no public route and must not be given one.** It holds realm-wide
Keycloak administration and is safe to hold it only because nothing outside the
network can reach it. Reach it by service name on the internal network.

    from celine.sdk.auth import OidcClientCredentialsProvider
    from celine.sdk.provisioning import ProvisioningClient

    client = ProvisioningClient(
        base_url="http://provisioning:8010",
        token_provider=OidcClientCredentialsProvider(...),
    )

    account = await client.ensure_participant(
        "greenland", submission.ref, email=submission.email
    )
    # account.username is what the registry's Member.user_id must be set to,
    # and account.user_id is the Keycloak uuid.

    try:
        await client.send_invitation("greenland", member_key, intent="password_reset")
    except ProvisioningApiError as exc:
        if exc.code == "no_password":  # never set one: send intent="invitation"
            ...
"""

from celine.sdk.provisioning.client import ProvisioningClient, SendIntent
from celine.sdk.provisioning.errors import ProvisioningApiError, ReconcileDivergence

__all__ = [
    "ProvisioningClient",
    "ProvisioningApiError",
    "ReconcileDivergence",
    "SendIntent",
]
