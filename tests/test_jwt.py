"""Tests for celine.sdk.auth.jwt — the two levels of grant, organization parsing, subject type."""

import pytest

import celine.sdk.auth as auth_pkg
import celine.sdk.auth.jwt as jwt_module
from celine.sdk.auth.jwt import (
    PLATFORM_ADMIN_ROLE,
    Grants,
    Organization,
    is_platform_admin,
    is_service_account,
    organization_aliases,
    organization_groups,
    realm_roles,
)


# ---------------------------------------------------------------------------
# is_service_account
# ---------------------------------------------------------------------------


class TestIsServiceAccount:
    # @verifies REQ-0031
    def test_service_account_by_username(self):
        claims = {"preferred_username": "service-account-svc-digital-twin"}
        assert is_service_account(claims) is True

    # @verifies REQ-0031
    def test_service_account_by_gty(self):
        claims = {"gty": "client-credentials"}
        assert is_service_account(claims) is True

    # @verifies REQ-0031
    def test_service_account_by_client_id_no_email(self):
        claims = {"client_id": "svc-digital-twin"}
        assert is_service_account(claims) is True

    # @verifies REQ-0031
    def test_user_with_email(self):
        claims = {
            "email": "user@example.com",
            "preferred_username": "user",
            "scope": "openid profile",
        }
        assert is_service_account(claims) is False

    # @verifies REQ-0031
    def test_user_with_realm_groups(self):
        claims = {
            "groups": ["/viewers"],
            "preferred_username": "user",
        }
        assert is_service_account(claims) is False

    # @verifies REQ-0031
    def test_user_with_org_groups_no_realm_groups(self):
        """User with org-level groups but no realm-level groups."""
        claims = {
            "scope": "openid organization:* email groups profile",
            "email": "ah-00003@celine.localhost",
            "preferred_username": "ah-00003",
            "organization": {
                "example_rec": {
                    "type": ["rec"],
                    "groups": ["/viewers"],
                }
            },
        }
        assert is_service_account(claims) is False

    # @verifies REQ-0031
    def test_user_with_human_username(self):
        claims = {"preferred_username": "john.doe"}
        assert is_service_account(claims) is False

    # @verifies REQ-0031
    def test_real_user_token(self):
        """Full token from Keycloak oauth2-proxy — must be classified as user."""
        claims = {
            "iss": "http://keycloak.celine.localhost/realms/celine",
            "aud": ["oauth2_proxy", "svc-digital-twin"],
            "sub": "1e891aa0-4a9b-4a46-a4ea-d49e7011311c",
            "typ": "Bearer",
            "azp": "oauth2_proxy",
            "scope": "openid organization:* email groups profile",
            "email_verified": True,
            "organization": {
                "example_rec": {
                    "type": ["rec"],
                    "groups": ["/viewers"],
                }
            },
            "preferred_username": "ah-00003",
            "email": "ah-00003@celine.localhost",
        }
        assert is_service_account(claims) is False

    # @verifies REQ-0031
    def test_real_service_token(self):
        """Service account token from client credentials grant."""
        claims = {
            "iss": "http://keycloak.celine.localhost/realms/celine",
            "sub": "abc-service-uuid",
            "azp": "svc-digital-twin",
            "scope": "digital-twin.admin dataset.query",
            "preferred_username": "service-account-svc-digital-twin",
        }
        assert is_service_account(claims) is True

    # @verifies REQ-0031
    def test_a_keycloak_client_credentials_token_without_the_service_account_scope(self):
        """Measured on the celine dev realm, Keycloak 26.7.3, 2026-09-14.

        The sync assigns exactly the declared scopes, so Keycloak's built-in
        `service_account` scope is absent: no `preferred_username`, no `client_id`.
        """
        claims = {
            "exp": 1789401714,
            "iat": 1789401414,
            "jti": "trrtcc:9d3dab58-9f8e-b9ad-2a2c-380dd8312b0d",
            "iss": "http://keycloak.celine.localhost/realms/celine",
            "aud": ["svc-digital-twin", "svc-onboarding"],
            "sub": "447989f5-9e75-459b-a77e-75cb515c85b3",
            "typ": "Bearer",
            "azp": "svc-community",
            "scope": "community.read onboarding.members.invite",
        }
        assert is_service_account(claims) is True

    # @verifies REQ-0031
    @pytest.mark.parametrize("jti", ["onrtro:5f0e", "onrtrt:5f0e", "onrtac:5f0e"])
    def test_a_keycloak_user_grant_stripped_of_identity_claims_is_not_a_service(self, jti):
        """Only the client-credentials marker counts; `azp` without a session is not enough."""
        claims = {"jti": jti, "azp": "some-client", "sub": "u", "scope": "community.read"}
        assert is_service_account(claims) is False

    # @verifies REQ-0031
    def test_a_measured_keycloak_user_token_stays_a_user(self):
        """Password grant through oauth2_proxy on the same realm, same day."""
        claims = {
            "jti": "onrtro:1c7a",
            "azp": "oauth2_proxy",
            "sid": "8f1e",
            "sub": "11111111-1111-1111-1111-111111111111",
            "preferred_username": "admin",
            "email": "admin@celine.localhost",
            "groups": ["/admins"],
            "scope": "openid email profile",
        }
        assert is_service_account(claims) is False

    # @verifies REQ-0031
    @pytest.mark.parametrize("jti", ["trrtcc", "cc:abc", "TRRTCC:abc", 42, None, "a-random-uuid"])
    def test_a_jti_that_is_not_keycloaks_marker_grants_nothing(self, jti):
        assert is_service_account({"jti": jti, "azp": "x"}) is False

    # @verifies REQ-0031
    def test_empty_claims(self):
        assert is_service_account({}) is False


# ---------------------------------------------------------------------------
# Organization parsing, and reading the two group levels apart
# ---------------------------------------------------------------------------


class TestOrganizationClaim:
    # The shape a real KC 26.4 token carries, copied from the celine realm:
    # `type` flattened, `groups` with a leading slash, no `attributes` key.
    REAL = {
        "example-renewable-community": {
            "id": "0f4ba6e3-0f1c-43a6-a117-4eb88863bb02",
            "type": ["rec"],
            "groups": ["/managers"],
        }
    }

    # @verifies REQ-0040
    def test_flattened_type_and_groups(self):
        org = Organization._from_claim("example-renewable-community", self.REAL[
            "example-renewable-community"
        ])
        assert org.alias == "example-renewable-community"
        assert org.type == "rec"
        assert org.id == "0f4ba6e3-0f1c-43a6-a117-4eb88863bb02"
        assert org.groups == ["managers"]

    # @verifies REQ-0040
    def test_nested_attributes_still_give_a_type(self):
        org = Organization._from_claim("set", {"attributes": {"type": ["dso"]}})
        assert org.type == "dso"
        assert org.has_attribute("type", "dso")

    # @verifies REQ-0040
    def test_flattened_type_wins_over_nested(self):
        org = Organization._from_claim(
            "set", {"type": ["rec"], "attributes": {"type": ["dso"]}}
        )
        assert org.type == "rec"

    # @verifies REQ-0040
    def test_absent_id_and_groups_are_empty_not_an_error(self):
        org = Organization._from_claim("set", {"type": ["dso"]})
        assert org.id is None
        assert org.groups == []

    # @verifies REQ-0040
    def test_malformed_entry_yields_a_bare_membership(self):
        org = Organization._from_claim("set", "not-a-dict")
        assert org.alias == "set"
        assert org.type is None
        assert org.id is None
        assert org.groups == []


class TestTwoLevelsOfGrant:
    """REQ-0042: a platform grant is the realm role `platform-admin`; an organization's
    groups count only inside that organization; a realm group grants nothing.

    The `REAL_*` claim sets copy the shapes Keycloak 26.7.3 issued through
    `oauth2_proxy` (scope `openid email profile organization:*`) on the local celine
    realm, 2026-10-03, with organization aliases replaced by generic ones.
    """

    # Today's dev `admin`: realm group `/admins` written twice (the `groups` scope
    # mapper with the full path, the client-level mapper without), realm role `admin`
    # through that group, and `admins` inside several organizations.
    REAL_REALM_GROUP_ADMIN = {
        "jti": "onrtro:1c7a",
        "azp": "oauth2_proxy",
        "sid": "8f1e",
        "sub": "11111111-1111-1111-1111-111111111111",
        "preferred_username": "admin",
        "email": "admin@celine.localhost",
        "groups": ["/admins", "admins"],
        "realm_access": {"roles": ["admin"]},
        "organization": {
            "example_rec": {"type": ["rec"], "groups": ["/admins"]},
            "example_dso": {"type": ["dso"], "groups": ["/admins"]},
            "example-dso": {
                "type": ["dso"],
                "groups": ["/connector.consent.holder.read", "/connector.provider.read"],
            },
        },
    }

    # An organization-only user (dev `e2e-mgr`): no `groups` claim at all, Keycloak's
    # default realm roles.
    REAL_ORG_MANAGER = {
        "jti": "onrtro:2d8b",
        "azp": "oauth2_proxy",
        "sid": "9a2f",
        "sub": "22222222-2222-2222-2222-222222222222",
        "preferred_username": "e2e-mgr",
        "email": "e2e-mgr@example.test",
        "realm_access": {
            "roles": ["default-roles-celine", "offline_access", "uma_authorization"]
        },
        "organization": {"example-rec": {"type": ["rec"], "groups": ["/managers"]}},
    }

    # An organization's own `admins`, no realm group, default realm roles.
    ORG_ADMIN = {
        "sub": "33333333-3333-3333-3333-333333333333",
        "email": "rec-admin@example.test",
        "realm_access": {
            "roles": ["default-roles-celine", "offline_access", "uma_authorization"]
        },
        "organization": {"example-rec": {"type": ["rec"], "groups": ["/admins"]}},
    }

    # The target shape: the realm role, and organization groups beside it.
    PLATFORM_ADMIN = {
        "sub": "44444444-4444-4444-4444-444444444444",
        "email": "platform@example.test",
        "realm_access": {
            "roles": [
                "default-roles-celine",
                "platform-admin",
                "offline_access",
                "uma_authorization",
            ]
        },
        "organization": {"example-rec": {"type": ["rec"], "groups": ["/viewers"]}},
    }

    # @verifies REQ-0042
    def test_the_platform_role_is_named_platform_admin(self):
        assert PLATFORM_ADMIN_ROLE == "platform-admin"

    # @verifies REQ-0042
    def test_a_platform_admin_role_holder_is_a_platform_admin(self):
        assert is_platform_admin(self.PLATFORM_ADMIN) is True
        grants = Grants.from_claims(self.PLATFORM_ADMIN)
        assert grants.is_platform_admin is True
        assert PLATFORM_ADMIN_ROLE in grants.platform

    # @verifies REQ-0042
    def test_an_organizations_admins_member_is_not_a_platform_admin(self):
        assert is_platform_admin(self.ORG_ADMIN) is False
        grants = Grants.from_claims(self.ORG_ADMIN)
        assert grants.is_platform_admin is False
        assert grants.in_org("example-rec") == frozenset({"admins"})
        assert "admins" not in grants.platform

    # @verifies REQ-0042
    def test_todays_realm_group_admin_is_not_a_platform_admin(self):
        """`/admins` and `admins` in `groups`, realm role `admin`: none of it is the grant."""
        claims = self.REAL_REALM_GROUP_ADMIN
        assert is_platform_admin(claims) is False
        grants = Grants.from_claims(claims)
        assert grants.platform == frozenset({"admin"})
        assert not grants.is_platform_admin

    # @verifies REQ-0042
    @pytest.mark.parametrize(
        "groups",
        [["/admins"], ["admins"], ["/admins", "admins"], ["/platform-admin"], ["platform-admin"]],
    )
    def test_a_realm_group_grants_nothing(self, groups):
        claims = {"sub": "u", "groups": groups}
        assert is_platform_admin(claims) is False
        assert realm_roles(claims) == []
        grants = Grants.from_claims(claims)
        assert grants.platform == frozenset()
        assert grants.aliases == []

    # @verifies REQ-0042
    def test_an_organization_group_named_platform_admin_is_not_the_role(self):
        claims = {"organization": {"example-rec": {"groups": ["/platform-admin"]}}}
        assert is_platform_admin(claims) is False
        assert Grants.from_claims(claims).in_org("example-rec") == frozenset(
            {"platform-admin"}
        )

    # @verifies REQ-0042
    def test_a_role_anywhere_but_realm_access_is_not_a_platform_grant(self):
        claims = {
            "roles": ["platform-admin"],
            "resource_access": {"some-client": {"roles": ["platform-admin"]}},
            "groups": ["platform-admin"],  # what a microprofile-jwt mapper writes
        }
        assert realm_roles(claims) == []
        assert is_platform_admin(claims) is False

    # @verifies REQ-0042
    @pytest.mark.parametrize(
        "claims",
        [
            {},
            {"realm_access": None},
            {"realm_access": "platform-admin"},
            {"realm_access": ["platform-admin"]},
            {"realm_access": {}},
            {"realm_access": {"roles": "platform-admin"}},
            {"realm_access": {"roles": None}},
            {"realm_access": {"roles": [42, None, ""]}},
        ],
    )
    def test_a_missing_or_malformed_realm_access_yields_no_roles(self, claims):
        assert realm_roles(claims) == []
        assert is_platform_admin(claims) is False
        assert Grants.from_claims(claims).platform == frozenset()

    # @verifies REQ-0042
    def test_realm_roles_are_deduplicated_in_order_skipping_non_strings(self):
        claims = {"realm_access": {"roles": ["a", 1, "platform-admin", "a", None]}}
        assert realm_roles(claims) == ["a", "platform-admin"]

    # @verifies REQ-0042
    def test_organization_groups_are_scoped_to_one_alias(self):
        claims = self.REAL_REALM_GROUP_ADMIN
        assert organization_groups(claims, "example_rec") == ["admins"]
        assert organization_groups(claims, "example-dso") == [
            "connector.consent.holder.read",
            "connector.provider.read",
        ]
        assert organization_groups(claims, "example-rec") == []
        grants = Grants.from_claims(self.REAL_ORG_MANAGER)
        assert grants.in_org("example-rec") == frozenset({"managers"})
        assert grants.in_org("example_rec") == frozenset()

    # @verifies REQ-0042
    def test_an_organization_path_is_not_read_as_a_realm_path(self):
        """Organization group paths are `/admins`, the same string as the realm group."""
        claims = {"organization": {"example-rec": {"groups": ["/admins"]}}}
        assert realm_roles(claims) == []
        assert Grants.from_claims(claims).platform == frozenset()

    # @verifies REQ-0042
    def test_grants_offer_no_flat_list_and_cannot_be_changed(self):
        grants = Grants.from_claims(self.REAL_REALM_GROUP_ADMIN)
        assert grants.aliases == ["example-dso", "example_dso", "example_rec"]
        with pytest.raises(TypeError):
            grants.organizations["example-rec"] = frozenset({"admins"})  # type: ignore[index]
        public = {n for n in dir(grants) if not n.startswith("_")}
        assert public == {
            "aliases",
            "from_claims",
            "in_org",
            "is_platform_admin",
            "organizations",
            "platform",
        }

    # @verifies REQ-0042
    def test_grants_of_unusable_claims_are_empty(self):
        for claims in ({}, {"organization": "nope"}, {"organization": {"x": "nope"}}):
            grants = Grants.from_claims(claims)
            assert grants.platform == frozenset()
            assert grants.in_org("x") == frozenset()
        assert Grants.from_claims(None).platform == frozenset()  # type: ignore[arg-type]

    # @verifies REQ-0042
    def test_organization_aliases_are_sorted(self):
        assert organization_aliases(self.REAL_REALM_GROUP_ADMIN) == [
            "example-dso",
            "example_dso",
            "example_rec",
        ]
        assert organization_aliases({}) == []
        assert organization_aliases({"organization": "nope"}) == []

    # @verifies REQ-0042
    def test_claims_of_the_wrong_shape_are_tolerated(self):
        assert organization_groups({"organization": "nope"}, "rec-a") == []
        assert organization_groups({"organization": {"rec-a": "nope"}}, "rec-a") == []
        assert organization_groups({"organization": {"rec-a": {"groups": "x"}}}, "rec-a") == []

    # @verifies REQ-0042
    @pytest.mark.parametrize("module", [jwt_module, auth_pkg])
    @pytest.mark.parametrize("name", ["extract_groups", "realm_groups", "_merged_groups"])
    def test_the_level_merging_readers_are_gone(self, module, name):
        assert not hasattr(module, name)

    # @verifies REQ-0042
    @pytest.mark.parametrize(
        "name",
        [
            "PLATFORM_ADMIN_ROLE",
            "Grants",
            "is_platform_admin",
            "realm_roles",
            "organization_groups",
            "organization_aliases",
        ],
    )
    def test_the_readers_are_exported_by_the_auth_package(self, name):
        assert name in auth_pkg.__all__
        assert getattr(auth_pkg, name) is getattr(jwt_module, name)

    # @verifies REQ-0031
    def test_an_organization_only_user_is_still_a_user(self):
        stripped = {k: v for k, v in self.REAL_ORG_MANAGER.items() if k not in (
            "email", "preferred_username")}
        assert is_service_account(stripped) is False

    # @verifies REQ-0031
    def test_realm_roles_alone_do_not_make_a_human(self):
        """A client-credentials token can carry default realm roles; that is not a person."""
        claims = {
            "jti": "trrtcc:9d3d",
            "azp": "svc-example",
            "sub": "s",
            "realm_access": {"roles": ["default-roles-celine", "offline_access"]},
        }
        assert is_service_account(claims) is True
