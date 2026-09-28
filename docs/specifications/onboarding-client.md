# Onboarding client

`celine.sdk.onboarding`. It wraps the generated onboarding client in two classes: the
member's own surface (`OnboardingClient`) and the admin surface (`OnboardingAdminClient`):
the delegated member emails and the registry sync. Only the registry sync is specified
here; the rest of onboarding's admin surface is in the generated client.

The registry sync was specified before the code
([ADR-0002](../decisions/ADR-0002-requirements-may-land-ahead-of-the-code.md)) because it
writes the registry, and a wrapper that chose a default for the caller there would decide
whether the registry is written.

The service's own behaviour belongs to `onboarding`: the template as the source of truth for
a community's areas, what the sync creates, changes, leaves alone and refuses, the "set up
community" step that precedes it, and the `recs.write` capability, held by realm admins only,
that authorises it. It is named here only so the two can be kept honest.

---

## Registry sync

### REQ-0140 — the registry sync sends dry run and prune as the caller chose them

`OnboardingAdminClient.registry_sync(rec_slug, *, dry_run, prune=False, token=None)` sends
`POST /api/admin/recs/{rec_slug}/registry-sync` with the query parameters `dry_run` and `prune` **always present**. `dry_run` has no default in the wrapper:
the caller states it on every call, so whether the registry is written is never decided by a
default on either side of the seam. `prune` is `false` unless the caller sets it, matching the
service, whose sync is additive unless asked to remove. A value that is not a `bool` for
either is refused with `TypeError` before any request, because the generated client drops a
`None` from the query and the service's default would then decide. The call carries the
caller's token (a realm admin's, since onboarding grants `recs.write` to no service) and no
acting-user header.

It answers onboarding's report — what would be, or was, created, changed, left alone and
refused, and (from onboarding 0.4.0) renamed, with the key a renamed area came from in
`renamed_from` — as a schema, without interpreting it. Which outcomes onboarding reports as rows
and which it answers as a refusal is onboarding's to decide; the wrapper passes both through
as they came.

A status other than success raises `OnboardingApiError` carrying the status code, the
service's message and its `code`, the way the wrapper already reads the admin member routes'
`{"detail": {"code", "message"}}` refusals. That is onboarding's own error shape, which the
sync route shares; it is not the registry's flat `{"detail", "code"}` (REQ-0127), and the
wrapper does not reshape one into the other. The code is compared as a string. The status
is read before the body is parsed, so onboarding's own `422` (`template_invalid`,
`template_not_syncable`) is raised with its code rather than failing in the generated
validation-error parser.
