"""Tests for celine.sdk.auth.jwt — group readers, organization parsing, subject type."""

import pytest

from celine.sdk.auth.jwt import (
    Organization,
    extract_groups,
    is_service_account,
    organization_aliases,
    organization_groups,
    realm_groups,
)


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


# ---------------------------------------------------------------------------
# Organization parsing, and reading the two group levels apart
# ---------------------------------------------------------------------------


class TestOrganizationClaim:
    # The shape a real KC 26.4 token carries, copied from the celine realm:
    # `type` flattened, `groups` with a leading slash, no `attributes` key.
    REAL = {
        "gr-renewable-community": {
            "id": "0f4ba6e3-0f1c-43a6-a117-4eb88863bb02",
            "type": ["rec"],
            "groups": ["/managers"],
        }
    }

    # @verifies REQ-0040
    def test_flattened_type_and_groups(self):
        org = Organization._from_claim("gr-renewable-community", self.REAL[
            "gr-renewable-community"
        ])
        assert org.alias == "gr-renewable-community"
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


class TestRealmAndOrganizationGroups:
    CLAIMS = {
        "groups": ["/viewers", "viewers"],
        "organization": {
            "rec-a": {"type": ["rec"], "groups": ["/managers"]},
            "rec-b": {"type": ["rec"], "groups": ["/participants"]},
        },
    }

    # @verifies REQ-0041
    def test_realm_groups_exclude_organization_groups(self):
        assert realm_groups(self.CLAIMS) == ["viewers"]

    # @verifies REQ-0041
    def test_organization_groups_are_scoped_to_one_alias(self):
        assert organization_groups(self.CLAIMS, "rec-a") == ["managers"]
        assert organization_groups(self.CLAIMS, "rec-b") == ["participants"]
        assert organization_groups(self.CLAIMS, "rec-c") == []

    # @verifies REQ-0041
    def test_extract_groups_still_merges_the_two_levels(self):
        """The contrast REQ-0041 exists for, asserted rather than described.

        `managers` is held in rec-a only. A multi-tenant caller asking about
        rec-b must not see it, and `extract_groups` shows it regardless.
        """
        assert "managers" in extract_groups(self.CLAIMS)
        assert "managers" not in organization_groups(self.CLAIMS, "rec-b")

    # @verifies REQ-0041
    def test_organization_aliases_are_sorted(self):
        assert organization_aliases(self.CLAIMS) == ["rec-a", "rec-b"]

    # @verifies REQ-0041
    def test_claims_of_the_wrong_shape_are_tolerated(self):
        assert realm_groups({}) == []
        assert realm_groups({"groups": "managers"}) == []
        assert organization_groups({"organization": "nope"}, "rec-a") == []
        assert organization_groups({"organization": {"rec-a": "nope"}}, "rec-a") == []
        assert organization_aliases({}) == []
