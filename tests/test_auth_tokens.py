"""Tests for `celine.sdk.auth.jwt` verification — docs/specifications/identity.md.

Every token here is really signed and really verified: the only thing replaced
is the JWKS fetch (conftest). A test that passes because verification was
stubbed out would be evidence of nothing.
"""

from __future__ import annotations

import pytest

from celine.sdk.auth.jwt import JwtUser, get_expected_audiences
from celine.sdk.settings.models import OidcSettings

from conftest import ISSUER


class TestVerification:
    # @verifies REQ-0020
    def test_a_genuine_token_parses(self, oidc, make_token):
        token = make_token({"email": "a@test", "preferred_username": "alice"})
        user = JwtUser.from_token(token, oidc)
        assert user.sub == "user-123"
        assert user.email == "a@test"
        assert user.iss == ISSUER
        assert user.token == token

    # @verifies REQ-0023
    def test_a_token_signed_by_a_foreign_key_is_rejected(
        self, oidc, make_token, foreign_key
    ):
        """Claims are perfect; only the signature is not the issuer's. This is the
        test that proves verification is live rather than stubbed.
        """
        token = make_token(key=foreign_key)
        with pytest.raises(Exception) as exc:
            JwtUser.from_token(token, oidc)
        assert "signature" in str(exc.value).lower()

    # @verifies REQ-0022
    def test_an_expired_token_is_rejected(self, oidc, make_token):
        with pytest.raises(Exception) as exc:
            JwtUser.from_token(make_token(expires_in=-120), oidc)
        assert "expired" in str(exc.value).lower()

    # @verifies REQ-0022
    def test_expiry_allows_thirty_seconds_of_clock_skew(self, oidc, make_token):
        """A service whose clock runs a few seconds ahead of Keycloak must not
        start refusing tokens that the issuer still considers valid.
        """
        assert JwtUser.from_token(make_token(expires_in=-10), oidc).sub == "user-123"

    # @verifies REQ-0020
    def test_a_token_not_yet_valid_is_rejected(self, oidc, make_token):
        with pytest.raises(Exception):
            JwtUser.from_token(make_token(not_before=300), oidc)

    # @verifies REQ-0024
    def test_a_token_from_another_issuer_is_rejected(self, oidc, make_token):
        token = make_token(issuer="https://auth.elsewhere/realms/other")
        with pytest.raises(Exception) as exc:
            JwtUser.from_token(token, oidc)
        assert "issuer" in str(exc.value).lower()

    # @verifies REQ-0025
    def test_an_authorization_header_value_is_accepted(self, oidc, make_token):
        token = make_token()
        assert JwtUser.from_token(f"Bearer {token}", oidc).sub == "user-123"
        assert JwtUser.from_token(f"bearer {token}", oidc).sub == "user-123"

    # @verifies REQ-0027
    def test_a_token_without_a_subject_is_refused(self, oidc, make_token):
        with pytest.raises(ValueError, match="sub"):
            JwtUser.from_token(make_token(sub=None), oidc)

    # @verifies REQ-0028
    @pytest.mark.parametrize("empty", ["", "   ", None])
    def test_an_empty_token_is_refused_before_any_fetch(self, oidc, monkeypatch, empty):
        """An unauthenticated request must not be able to make this process reach
        out to the identity provider, so the JWKS seam is replaced with one that
        fails the test if it is touched at all.
        """

        def _explode(jwks_uri):  # pragma: no cover - asserts by not running
            raise AssertionError("JWKS was fetched for an empty token")

        monkeypatch.setattr("celine.sdk.auth.jwt._get_jwks_client", _explode)
        with pytest.raises(ValueError):
            JwtUser.from_token(empty, oidc)


class TestJwksClient:
    # @verifies REQ-0021
    def test_the_jwks_client_is_memoised_per_uri(self, real_get_jwks_client):
        """A service verifying thousands of requests must fetch the key set once.
        Constructing the client does not fetch anything — the memoisation is what
        keeps the fetch from happening per request.
        """
        first = real_get_jwks_client("https://auth.test/a/certs")
        again = real_get_jwks_client("https://auth.test/a/certs")
        other = real_get_jwks_client("https://auth.test/b/certs")
        assert first is again
        assert first is not other

    # @verifies REQ-0021
    def test_the_key_set_itself_is_cached(self, real_get_jwks_client):
        client = real_get_jwks_client("https://auth.test/c/certs")
        assert client.jwk_set_cache is not None


class TestAudience:
    # @verifies REQ-0026
    def test_audience_is_enforced_when_configured(self, make_token):
        oidc = OidcSettings(base_url=ISSUER, jwks_uri="https://x/jwks", audience="api")
        assert JwtUser.from_token(make_token({"aud": "api"}), oidc).sub == "user-123"
        with pytest.raises(Exception):
            JwtUser.from_token(make_token({"aud": "other-api"}), oidc)

    # @verifies REQ-0026
    def test_audience_is_not_checked_when_unset(self, oidc, make_token):
        """The permissive default, pinned deliberately: a token minted for another
        service parses here when no audience is configured.
        """
        user = JwtUser.from_token(make_token({"aud": "someone-elses-api"}), oidc)
        assert user.aud == "someone-elses-api"

    # @verifies REQ-0026
    def test_expected_audiences_is_none_when_nothing_is_configured(self):
        assert get_expected_audiences(OidcSettings()) is None

    # @verifies REQ-0026
    def test_expected_audiences_folds_in_the_client_id(self):
        s = OidcSettings(audience="api", client_id="svc")
        assert get_expected_audiences(s) == ["api", "svc"]
        assert get_expected_audiences(OidcSettings(client_id="svc")) == ["svc"]
        assert get_expected_audiences(
            OidcSettings(
                audience="api", client_id="svc", include_client_id_as_audience=False
            )
        ) == ["api"]
        assert get_expected_audiences(
            OidcSettings(audience="api", client_id="api")
        ) == ["api"]

    # @verifies REQ-0026
    def test_from_token_does_not_use_the_expected_audiences_helper(self, make_token):
        """The trap: `include_client_id_as_audience` and `allowed_audiences` look
        like verification settings, and `from_token` ignores both — it checks
        `audience` alone. A service relying on them is not checking what it thinks
        it is checking.
        """
        oidc = OidcSettings(
            base_url=ISSUER,
            jwks_uri="https://x/jwks",
            audience=None,
            client_id="svc",
            include_client_id_as_audience=True,
            allowed_audiences="other",
        )
        assert get_expected_audiences(oidc) == ["svc"]
        # Audience "wrong" is accepted anyway, because `audience` is unset.
        assert JwtUser.from_token(make_token({"aud": "wrong"}), oidc).aud == "wrong"


class TestOrganizations:
    # @verifies REQ-0029
    def test_memberships_are_parsed_from_the_claim(self, oidc, make_token):
        token = make_token(
            {
                "organization": {
                    "example_rec": {"type": ["rec"], "attributes": {"tier": ["gold"]}},
                    "example_dso": {"type": ["dso"]},
                }
            }
        )
        user = JwtUser.from_token(token, oidc)
        assert sorted(user.organization_aliases) == ["example_dso", "example_rec"]
        rec = user.get_organization("example_rec")
        assert rec is not None
        assert rec.type == "rec"
        assert rec.is_type("rec") and not rec.is_type("dso")
        assert rec.get_attribute("tier") == ["gold"]
        assert rec.has_attribute("tier", "gold")
        assert rec.get_attribute("absent") == []
        assert user.is_member_of("example_dso")
        assert not user.is_member_of("someone-else")
        assert user.get_organization("someone-else") is None

    # @verifies REQ-0029
    def test_a_scalar_attribute_is_normalised_to_a_list(self, oidc, make_token):
        token = make_token({"organization": {"rec": {"attributes": {"tier": "gold"}}}})
        org = JwtUser.from_token(token, oidc).get_organization("rec")
        assert org.get_attribute("tier") == ["gold"]

    # @verifies REQ-0029
    def test_an_absent_or_unusable_claim_yields_no_memberships(self, oidc, make_token):
        assert JwtUser.from_token(make_token(), oidc).organizations == []
        token = make_token({"organization": "not-a-mapping"})
        assert JwtUser.from_token(token, oidc).organizations == []

    # @verifies REQ-0029
    def test_a_membership_without_a_type_has_none(self, oidc, make_token):
        token = make_token({"organization": {"rec": {"id": "abc"}}})
        assert JwtUser.from_token(token, oidc).get_organization("rec").type is None


class TestClaimHelpers:
    # @verifies REQ-0032
    def test_roles_read_a_list_or_a_bare_string(self, oidc, make_token):
        user = JwtUser.from_token(make_token({"roles": ["admin", "reader"]}), oidc)
        assert user.has_role("admin") and not user.has_role("writer")
        single = JwtUser.from_token(make_token({"roles": "admin"}), oidc)
        assert single.has_role("admin") and not single.has_role("reader")
        assert not JwtUser.from_token(make_token({"roles": 42}), oidc).has_role("admin")

    # @verifies REQ-0032
    def test_scopes_read_a_space_separated_string_or_a_list(self, oidc, make_token):
        user = JwtUser.from_token(make_token({"scope": "read write"}), oidc)
        assert user.has_scope("read") and not user.has_scope("delete")
        listed = JwtUser.from_token(make_token({"scope": ["read"]}), oidc)
        assert listed.has_scope("read")

    # @verifies REQ-0032
    def test_a_display_name_always_resolves(self, oidc, make_token):
        full = JwtUser.from_token(
            make_token({"name": "Alice", "preferred_username": "alice"}), oidc
        )
        assert full.display_name == "Alice"
        username_only = JwtUser.from_token(
            make_token({"preferred_username": "alice"}), oidc
        )
        assert username_only.display_name == "alice"
        assert username_only.get_username() == "alice"
        bare = JwtUser.from_token(make_token(), oidc)
        assert bare.display_name == "user-user-123"
        assert bare.get_username() == "user-user-123"

    # @verifies REQ-0032
    def test_custom_claims_are_reachable(self, oidc, make_token):
        user = JwtUser.from_token(make_token({"community": "rec-1"}), oidc)
        assert user.get_claim("community") == "rec-1"
        assert user.get_claim("absent", "fallback") == "fallback"
        assert user.to_dict()["community"] == "rec-1"
        assert user.to_dict()["sub"] == "user-123"

    # @verifies REQ-0033
    def test_a_parsed_token_reports_its_own_expiry(self, oidc, make_token):
        user = JwtUser.from_token(make_token(expires_in=300), oidc)
        assert not user.is_expired()
        assert user.is_valid()
        stale = JwtUser.from_token(make_token(expires_in=-10), oidc)
        assert stale.is_expired()
        assert not stale.is_valid()

    # @verifies REQ-0033
    def test_a_token_without_an_expiry_is_not_expired(self):
        assert not JwtUser(sub="s").is_expired()

    # @verifies REQ-0031
    def test_the_service_account_flag_reads_the_verified_claims(self, oidc, make_token):
        svc = JwtUser.from_token(
            make_token({"preferred_username": "service-account-dt"}), oidc
        )
        assert svc.is_service_account
        human = JwtUser.from_token(make_token({"email": "a@test"}), oidc)
        assert not human.is_service_account
