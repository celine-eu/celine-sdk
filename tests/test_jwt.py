"""Tests for celine.sdk.auth.jwt — extract_groups and is_service_account."""

import pytest

from celine.sdk.auth.jwt import extract_groups, is_service_account


# ---------------------------------------------------------------------------
# extract_groups
# ---------------------------------------------------------------------------


class TestExtractGroups:
    # @verifies REQ-0030
    def test_empty_claims(self):
        assert extract_groups({}) == []

    # @verifies REQ-0030
    def test_realm_groups_only(self):
        claims = {"groups": ["/admins", "/viewers"]}
        assert extract_groups(claims) == ["admins", "viewers"]

    # @verifies REQ-0030
    def test_org_groups_only(self):
        claims = {
            "organization": {
                "example_rec": {
                    "type": ["rec"],
                    "groups": ["/viewers"],
                }
            }
        }
        assert extract_groups(claims) == ["viewers"]

    # @verifies REQ-0030
    def test_multiple_orgs(self):
        claims = {
            "organization": {
                "rec_a": {"type": ["rec"], "groups": ["/viewers"]},
                "rec_b": {"type": ["rec"], "groups": ["/managers"]},
            }
        }
        result = extract_groups(claims)
        assert "viewers" in result
        assert "managers" in result

    # @verifies REQ-0030
    def test_realm_and_org_merged(self):
        claims = {
            "groups": ["/admins"],
            "organization": {
                "rec_a": {"type": ["rec"], "groups": ["/viewers"]},
            },
        }
        result = extract_groups(claims)
        assert result == ["admins", "viewers"]

    # @verifies REQ-0030
    def test_deduplication(self):
        claims = {
            "groups": ["/viewers"],
            "organization": {
                "rec_a": {"groups": ["/viewers"]},
            },
        }
        result = extract_groups(claims)
        assert result == ["viewers"]

    # @verifies REQ-0030
    def test_slash_stripping(self):
        claims = {"groups": ["/admins", "viewers", "///editors"]}
        result = extract_groups(claims)
        assert result == ["admins", "viewers", "editors"]

    # @verifies REQ-0030
    def test_non_list_groups_ignored(self):
        claims = {"groups": "not-a-list"}
        assert extract_groups(claims) == []

    # @verifies REQ-0030
    def test_non_string_entries_skipped(self):
        claims = {"groups": ["/viewers", 42, None, "/admins"]}
        assert extract_groups(claims) == ["viewers", "admins"]

    # @verifies REQ-0030
    def test_org_without_groups_key(self):
        claims = {
            "organization": {
                "rec_a": {"type": ["rec"]},
            }
        }
        assert extract_groups(claims) == []

    # @verifies REQ-0030
    def test_org_non_dict_data_ignored(self):
        claims = {"organization": {"rec_a": "not-a-dict"}}
        assert extract_groups(claims) == []

    # @verifies REQ-0030
    def test_real_token_structure(self):
        """Token structure from a Keycloak oauth2-proxy user."""
        claims = {
            "sub": "1e891aa0-4a9b-4a46-a4ea-d49e7011311c",
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
        assert extract_groups(claims) == ["viewers"]


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
    def test_empty_claims(self):
        assert is_service_account({}) is False
