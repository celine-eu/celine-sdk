"""Tests for `celine.sdk.provisioning`.

The seam is `mock_http`: the generated client builds its own `httpx.AsyncClient`,
so the class is what gets replaced, and everything this repository owns — the
status mapping, the detail extraction, the schema conversion — runs against real
responses.

Two things are pinned harder than the rest, because they are what a caller gets
wrong:

- **the `username` in the answer is not the one you sent.** It is read back from
  Keycloak, and an account that already existed may authenticate under a
  convention nobody chose. A caller that stores its own guess creates a second
  account beside the one the participant already signs in with.
- **a refusal is branched on by its `code`.** A 1.2.0+ service answers
  `{"detail": {"code", "message"}}`, and the wrapper must also keep reading an
  older service's string `detail` — which the generated parser, now that the
  error statuses are declared, would crash on.
- **a diverging reconcile is a failure with a payload.** The service answers
  `500` on purpose; the wrapper turns it into `ReconcileDivergence` carrying the
  list, because a `200` with a list nobody reads is the failure mode the whole
  service exists to end.
"""

from __future__ import annotations

import json

import httpx
import pytest

from celine.sdk.openapi.provisioning.models import InvitationIntent
from celine.sdk.openapi.provisioning.schemas import InvitationIntentSchema
from celine.sdk.provisioning import (
    ProvisioningApiError,
    ProvisioningClient,
    ReconcileDivergence,
)

pytestmark = pytest.mark.asyncio


def _client() -> ProvisioningClient:
    return ProvisioningClient("http://provisioning.test", default_token="tok-svc")


def _answer(code: int, payload, headers: dict | None = None):
    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(code, json=payload, headers=headers)

    return handle


def _refusal(code: str, message: str) -> dict:
    """The 1.2.0+ error body."""
    return {"detail": {"code": code, "message": message}}


ACCOUNT = {
    "user_id": "3f1c-uuid",
    "username": "gl-00001",
    "created": True,
    "invitation": "not_requested",
    "invited": False,
}
INVITED = {
    "user_id": "3f1c-uuid",
    "username": "gl-00001",
    "invitation": "sent",
    "actions": ["UPDATE_PASSWORD", "VERIFY_EMAIL"],
    "lifespan": 604800,
}
DISABLED = {"user_id": "3f1c-uuid", "username": "gl-00001", "changed": True}
SWEPT = {
    "community": "greenland",
    "members": 45,
    "created": 2,
    "existing": 43,
    "divergences": [],
}


class TestEnsuringAParticipant:
    async def test_the_account_comes_back_as_a_schema(self, mock_http):
        mock_http(_answer(200, ACCOUNT))

        account = await _client().ensure_participant(
            "greenland", "20260912-a3f9c2", email="a.person@example.org"
        )

        assert account.user_id == "3f1c-uuid"
        assert account.username == "gl-00001"
        assert account.created is True

    async def test_the_username_is_whatever_keycloak_says_not_what_was_sent(
        self, mock_http
    ):
        """The reason this call is synchronous rather than a signal. A caller
        that derives the username from the address it just sent would make a
        second account beside the one this participant already signs in with."""
        mock_http(_answer(200, {**ACCOUNT, "username": "gl-00002", "created": False}))

        account = await _client().ensure_participant(
            "greenland", "k", email="a.person@example.org"
        )

        assert account.username == "gl-00002"
        assert account.created is False

    async def test_the_request_carries_the_address_and_the_keys_in_the_path(
        self, mock_http
    ):
        seen = mock_http(_answer(200, ACCOUNT))

        await _client().ensure_participant(
            "greenland",
            "20260912-a3f9c2",
            email="a.person@example.org",
            first_name="A",
            last_name="Person",
        )

        assert seen[0].method == "PUT"
        assert seen[0].url.path == "/participants/greenland/20260912-a3f9c2"
        assert b"a.person@example.org" in seen[0].content

    async def test_one_authorization_header_and_it_is_the_token(self, mock_http):
        """The service declares `Authorization` as an explicit header parameter,
        so the generated signature offers it too. Passing both would be two
        sources for one credential; the wrapper leaves it UNSET."""
        seen = mock_http(_answer(200, ACCOUNT))

        await _client().ensure_participant("greenland", "k", email="a@example.org")

        assert seen[0].headers.get_list("authorization") == ["Bearer tok-svc"]

    async def test_a_per_call_token_wins_over_the_default(self, mock_http):
        seen = mock_http(_answer(200, ACCOUNT))

        await _client().ensure_participant(
            "greenland", "k", email="a@example.org", token="tok-request"
        )

        assert seen[0].headers["authorization"] == "Bearer tok-request"

    async def test_no_token_anywhere_is_refused_before_the_request(self, mock_http):
        seen = mock_http(_answer(200, ACCOUNT))

        with pytest.raises(ValueError):
            await ProvisioningClient("http://provisioning.test").ensure_participant(
                "greenland", "k", email="a@example.org"
            )

        assert seen == []


class TestTheInvitation:
    async def test_locale_and_invite_travel_in_the_body(self, mock_http):
        seen = mock_http(_answer(200, {**ACCOUNT, "invitation": "sent", "invited": True}))

        await _client().ensure_participant(
            "greenland", "k", email="a@example.org", locale="es", invite=True
        )

        body = json.loads(seen[0].content)
        assert body["locale"] == "es"
        assert body["invite"] is True

    async def test_without_them_no_locale_is_sent_and_invite_is_false(self, mock_http):
        seen = mock_http(_answer(200, ACCOUNT))

        await _client().ensure_participant("greenland", "k", email="a@example.org")

        body = json.loads(seen[0].content)
        assert "locale" not in body
        assert body["invite"] is False

    async def test_a_locale_the_service_would_refuse_is_refused_before_the_request(
        self, mock_http
    ):
        seen = mock_http(_answer(200, ACCOUNT))

        with pytest.raises(ValueError):
            await _client().ensure_participant(
                "greenland", "k", email="a@example.org", locale="fr"
            )

        assert seen == []

    @pytest.mark.parametrize(
        "invitation",
        [
            "not_requested",
            "sent",
            "has_password",
            "no_email",
            "not_on_dev_list",
            "account_disabled",
            "cooldown",
            "send_failed",
        ],
    )
    async def test_the_upsert_says_what_happened_to_the_invitation(
        self, mock_http, invitation
    ):
        """A reason code the consumer shows the operator who approved. It is
        an enum in the schema, so `.value` is the string."""
        mock_http(
            _answer(
                200,
                {**ACCOUNT, "invitation": invitation, "invited": invitation == "sent"},
            )
        )

        account = await _client().ensure_participant(
            "greenland", "k", email="a@example.org", invite=True
        )

        assert account.invitation.value == invitation
        assert account.invited is (invitation == "sent")

    async def test_an_invitation_reports_the_actions_and_the_lifespan(self, mock_http):
        seen = mock_http(_answer(200, INVITED))

        result = await _client().send_invitation(
            "greenland", "gl-00001", intent="invitation"
        )

        assert result.invitation.value == "sent"
        assert result.actions == ["UPDATE_PASSWORD", "VERIFY_EMAIL"]
        assert result.lifespan == 604800
        assert seen[0].method == "POST"
        assert seen[0].url.path == "/participants/greenland/gl-00001/invitation"

    @pytest.mark.parametrize("intent", ["invitation", "password_reset"])
    async def test_the_intent_travels_in_the_body(self, mock_http, intent):
        seen = mock_http(
            _answer(200, {**INVITED, "actions": ["UPDATE_PASSWORD"], "lifespan": 3600})
        )

        await _client().send_invitation("greenland", "gl-00001", intent=intent)

        assert json.loads(seen[0].content) == {"intent": intent}
        assert seen[0].headers["content-type"] == "application/json"

    @pytest.mark.parametrize(
        "intent", [InvitationIntent.PASSWORD_RESET, InvitationIntentSchema.password_reset]
    )
    async def test_either_generated_enum_is_accepted_as_the_intent(self, mock_http, intent):
        seen = mock_http(_answer(200, INVITED))

        await _client().send_invitation("greenland", "gl-00001", intent=intent)

        assert json.loads(seen[0].content) == {"intent": "password_reset"}

    @pytest.mark.parametrize("intent", ["reset", "", None, "INVITATION"])
    async def test_an_intent_the_service_would_refuse_is_refused_before_the_request(
        self, mock_http, intent
    ):
        seen = mock_http(_answer(200, INVITED))

        with pytest.raises(ValueError):
            await _client().send_invitation("greenland", "gl-00001", intent=intent)

        assert seen == []

    async def test_the_intent_is_required(self):
        """No default: a default would be the SDK choosing the email for the
        person who pressed the button."""
        with pytest.raises(TypeError):
            await _client().send_invitation("greenland", "gl-00001")  # type: ignore[call-arg]

    @pytest.mark.parametrize(
        "status,code,intent",
        [
            (404, "member_not_found", "invitation"),
            (404, "account_not_found", "password_reset"),
            (409, "account_disabled", "invitation"),
            (409, "has_password", "invitation"),
            (409, "no_password", "password_reset"),
            (409, "no_email", "password_reset"),
            (502, "send_failed", "invitation"),
        ],
    )
    async def test_a_refused_invitation_raises_with_the_status_and_the_code(
        self, mock_http, status, code, intent
    ):
        mock_http(_answer(status, _refusal(code, "greenland/gl-00001: refused")))

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().send_invitation("greenland", "gl-00001", intent=intent)

        error = excinfo.value
        assert error.status_code == status
        assert error.code == code
        assert error.detail == {"code": code, "message": "greenland/gl-00001: refused"}
        # the sentence stays readable in the exception, for a log
        assert "greenland/gl-00001: refused" in str(error)
        assert code in str(error)
        assert error.retry_after is None

    async def test_a_cooldown_carries_retry_after(self, mock_http):
        mock_http(
            _answer(
                429,
                _refusal("cooldown", "greenland/gl-00001 was emailed less than 300s ago"),
                headers={"Retry-After": "241"},
            )
        )

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().send_invitation("greenland", "gl-00001", intent="invitation")

        assert excinfo.value.status_code == 429
        assert excinfo.value.code == "cooldown"
        assert excinfo.value.retry_after == 241

    @pytest.mark.parametrize("status", [404, 409, 429, 502])
    async def test_an_older_service_string_detail_still_raises_legibly(
        self, mock_http, status
    ):
        """The generated parser now expects `ErrorResponse` on these statuses
        and raises on a string `detail`. The wrapper must not."""
        mock_http(_answer(status, {"detail": "greenland/gl-00001: refused"}))

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().send_invitation("greenland", "gl-00001", intent="invitation")

        assert excinfo.value.status_code == status
        assert excinfo.value.code is None
        assert excinfo.value.detail == "greenland/gl-00001: refused"
        assert "refused" in str(excinfo.value)

    async def test_an_unknown_code_is_passed_through_as_a_string(self, mock_http):
        """`code` is a plain string in the contract, so a code this SDK has never
        seen neither raises nor needs `.value`."""
        mock_http(_answer(409, _refusal("some_future_code", "something new")))

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().send_invitation("greenland", "gl-00001", intent="invitation")

        assert excinfo.value.code == "some_future_code"

    async def test_reset_password_is_gone(self):
        """It handed back a temporary password with no channel to deliver it."""
        assert not hasattr(ProvisioningClient, "reset_password")


class TestTheLifecycleCalls:
    async def test_disabling_reports_whether_it_changed_anything(self, mock_http):
        mock_http(_answer(200, {**DISABLED, "changed": False}))

        result = await _client().disable("greenland", "gl-00001")

        # Already revoked. Not a failure, and it must not be reported as one.
        assert result.changed is False

    async def test_the_disable_route_is_the_one_the_service_declares(self, mock_http):
        # A second `mock_http` in one test does not replace the first — the
        # fixture subclasses whatever `httpx.AsyncClient` currently is, and the
        # inner __init__ puts its own transport back. One handler per test.
        seen = mock_http(_answer(200, DISABLED))

        await _client().disable("greenland", "gl-00001")

        assert seen[0].method == "POST"
        assert seen[0].url.path == "/participants/greenland/gl-00001/disable"


class TestWhatRefusalsMean:
    async def test_a_member_nobody_has_is_404_with_the_service_sentence(
        self, mock_http
    ):
        mock_http(
            _answer(404, _refusal("member_not_found", "greenland has no member 'nobody'"))
        )

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().disable("greenland", "nobody")

        assert excinfo.value.status_code == 404
        assert excinfo.value.code == "member_not_found"
        assert "no member" in str(excinfo.value)

    @pytest.mark.parametrize(
        "code", ["community_not_found", "member_not_found", "account_not_found"]
    )
    async def test_the_code_tells_the_three_404s_apart(self, mock_http, code):
        """Only `account_not_found` means "no account to disable"."""
        mock_http(_answer(404, _refusal(code, "missing")))

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().disable("greenland", "gl-00001")

        assert excinfo.value.code == code

    async def test_a_missing_scope_is_403_and_says_which(self, mock_http):
        """403 and 401 are different on purpose: ask for a grant, or renew a
        credential. Retrying a 403 will never help."""
        mock_http(
            _answer(
                403,
                _refusal(
                    "insufficient_scope",
                    "requires scope 'provisioning.participants.write'",
                ),
            )
        )

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().ensure_participant(
                "greenland", "k", email="a@example.org"
            )

        assert excinfo.value.status_code == 403
        assert excinfo.value.code == "insufficient_scope"
        assert "provisioning.participants.write" in str(excinfo.value)

    async def test_a_dependency_failure_is_502_and_is_the_one_worth_retrying(
        self, mock_http
    ):
        mock_http(
            _answer(
                502,
                _refusal("registry_unavailable", "Could not export from http://registry"),
            )
        )

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().send_invitation("greenland", "gl-00001", intent="invitation")

        assert excinfo.value.status_code == 502
        assert excinfo.value.code == "registry_unavailable"

    async def test_a_body_that_is_not_json_still_raises_something_legible(
        self, mock_http
    ):
        def handle(request: httpx.Request) -> httpx.Response:
            return httpx.Response(502, content=b"<html>bad gateway</html>")

        mock_http(handle)

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().disable("greenland", "gl-00001")

        assert excinfo.value.status_code == 502
        assert excinfo.value.detail is None
        assert excinfo.value.code is None

    async def test_an_html_error_page_on_a_declared_status_does_not_crash_the_parse(
        self, mock_http
    ):
        """A proxy's page on a status the service declares with `ErrorResponse`."""

        def handle(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, content=b"<html>not found</html>")

        mock_http(handle)

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().send_invitation("greenland", "gl-00001", intent="invitation")

        assert excinfo.value.status_code == 404
        assert excinfo.value.code is None

    async def test_a_422_is_raised_without_a_code(self, mock_http):
        mock_http(
            _answer(
                422,
                {"detail": [{"loc": ["body", "intent"], "msg": "Field required", "type": "missing"}]},
            )
        )

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().send_invitation("greenland", "gl-00001", intent="invitation")

        assert excinfo.value.status_code == 422
        assert excinfo.value.code is None


class TestTheSweep:
    async def test_a_clean_sweep_reports_what_it_did(self, mock_http):
        mock_http(_answer(200, SWEPT))

        result = await _client().reconcile("greenland")

        assert result.members == 45
        assert result.created == 2
        assert result.divergences == []

    async def test_a_diverging_sweep_raises_with_the_list_intact(self, mock_http):
        """The service answers 500 deliberately. Everything it checked is
        something the same call claimed to have done, so a finding is a
        provisioning call that reported success and had not succeeded."""
        mock_http(
            _answer(
                500,
                {
                    "detail": {
                        "code": "reconcile_diverged",
                        "message": "reconcile of greenland left 1 member(s) outside",
                        **SWEPT,
                        "divergences": [
                            {
                                "key": "gl-00001",
                                "username": "gl-00001",
                                "kind": "not in the REC organization",
                                "detail": "no `organization` claim",
                            }
                        ],
                    }
                },
            )
        )

        with pytest.raises(ReconcileDivergence) as excinfo:
            await _client().reconcile("greenland")

        error = excinfo.value
        assert error.community == "greenland"
        assert [d["key"] for d in error.divergences] == ["gl-00001"]
        assert "1 member(s)" in str(error)
        assert error.code == "reconcile_diverged"
        # and it is still a ProvisioningApiError, so a caller that only knows
        # about the base class still catches it
        assert isinstance(error, ProvisioningApiError)

    async def test_a_500_that_is_not_a_divergence_stays_an_ordinary_failure(
        self, mock_http
    ):
        """Only a body shaped like the report is read as one. Anything else is
        the service falling over, and pretending otherwise would invent an empty
        list of divergences out of an outage."""
        mock_http(_answer(500, {"detail": "Internal Server Error"}))

        with pytest.raises(ProvisioningApiError) as excinfo:
            await _client().reconcile("greenland")

        assert not isinstance(excinfo.value, ReconcileDivergence)
        assert excinfo.value.status_code == 500
