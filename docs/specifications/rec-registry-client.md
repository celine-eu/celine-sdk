# REC registry client

`celine.sdk.rec_registry`. Six repositories import it. It wraps the generated registry
client so callers see short method names and Pydantic schemas instead of `Response`
objects — the general shape of every wrapper in this SDK.

What is stated here is only the part of that wrapper where a wrong answer is
indistinguishable from a right one: the two **batch asset lookups**, whose empty list is a
real answer the service gives on purpose. The rest of the wrapper — every single-id
lookup, the writes, the user-scoped client — is not specified yet.

The service's own behaviour belongs to `rec-registry`, not here; where a requirement below
mirrors one of its, the identifier is named so the two can be kept honest.

---

## Batch asset lookups

`lookup_assets_by_sensor_ids` and `lookup_assets_by_user_ids` are mirrors: one starts from
a device and finds its owner, the other starts from owners and finds their devices.

Both sit in front of routes where **an empty list means something**. A sensor id that
matches nothing contributes no row (`rec-registry` REQ-0043); a user id belonging to nobody
and a member who owns nothing are *deliberately* indistinguishable, so that the route
cannot be used to discover who is registered (`rec-registry` REQ-0045). Everything below
follows from that: the wrapper must never add a third meaning to a sentence that already
has two.

### REQ-0120 — a refused batch lookup raises, and never answers an empty list

A response the generated client does not parse into a list of assets — a `422` parsed as
`HTTPValidationError`, or any status parsed as `None` — raises `RecRegistryApiError`
carrying the status code and the response body.

Returning `[]` there is the failure this requirement exists to prevent: it fails in the
direction that loses data quietly, because the caller is told, in the only language the
method has, that **nothing matched**. A consumer resolving six hundred sensor ids for a
dataspace query would conclude that none of them are registered.

The exception is the wrapper's own, not the generated layer's, and mirrors
`celine.sdk.dt.util.DTApiError`.

### REQ-0121 — a batch larger than the bound is split, not refused

Both routes accept at most `MAX_BATCH_LOOKUP_IDS` ids — 500, mirrored from `rec-registry`,
where REQ-0043 and REQ-0045 read one shared constant of that name and 501 is a `422`.

The wrapper splits a longer input into consecutive requests of at most that many ids and
concatenates the rows in request order. Chunking is invisible to the caller: the bound is a
property of the route, not a mistake the caller made.

The number is named once. It has been written twice before, in the service, and the two
copies disagreed for months (`rec-registry#37`).

### REQ-0122 — an empty batch asks nothing

No ids means no request and an empty list, matching the service, which answers an empty
list without querying.

### REQ-0123 — the older singular name still works

`lookup_asset_by_sensor_ids` — singular `asset` — remains as a deprecated alias
delegating to `lookup_assets_by_sensor_ids`. It is the name `digital-twin` calls, and this
SDK reaches its consumers through a version bump with no file in those repositories
changing, so a removed method fails at runtime rather than at build.
