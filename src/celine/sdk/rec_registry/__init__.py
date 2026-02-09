"""CELINE REC Registry SDK Wrapper.

This module provides a high-level Python interface to the CELINE REC Registry API,
wrapping the auto-generated OpenAPI client with convenient access patterns.

Key Features:
- User-scoped operations via RecRegistryUserClient
- Admin-scoped operations via RecRegistryAdminClient
- Automatic token management with TokenProvider integration
- Async/await support with context managers

Quick Start:

    User Access (with user token):
    
        from celine.sdk.rec_registry import RecRegistryUserClient
        
        async with RecRegistryUserClient(
            base_url="https://registry.example.com",
            token="user-jwt-token"
        ) as client:
            communities = await client.list_communities()
            community = await client.get_community("community-key")
            assets = await client.list_assets("community-key")
    
    Admin Access (with client credentials):
    
        from celine.sdk.rec_registry import RecRegistryAdminClient
        from celine.sdk.auth import OidcClientCredentialsProvider
        
        token_provider = OidcClientCredentialsProvider(
            base_url="https://auth.example.com",
            client_id="admin-client",
            client_secret="secret",
            scope="registry:admin"
        )
        
        async with RecRegistryAdminClient(
            base_url="https://registry.example.com",
            token_provider=token_provider
        ) as admin:
            yaml_data = await admin.export_community("community-key")
            await admin.import_community(yaml_data)
    
    Admin Access (with static admin token):
    
        async with RecRegistryAdminClient(
            base_url="https://registry.example.com",
            token="admin-jwt-token"
        ) as admin:
            yaml_data = await admin.export_community("community-key")
"""

from celine.sdk.rec_registry.client import RecRegistryAdminClient, RecRegistryUserClient

__all__ = [
    "RecRegistryUserClient",
    "RecRegistryAdminClient",
]
