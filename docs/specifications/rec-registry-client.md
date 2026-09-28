# REC registry client

`celine.sdk.rec_registry`. Six repositories import it. It wraps the generated registry
client so callers see short method names and Pydantic schemas instead of `Response`
objects — the general shape of every wrapper in this SDK.

What is stated here is only the part of that wrapper where a wrong answer is
indistinguishable from a right one: the three **batch lookups**, whose empty list is a real
answer the service gives on purpose. The rest of the wrapper — every single-id lookup, the
writes, the user-scoped client — is not specified yet, except the **meter and profile
writes** (REQ-0125–REQ-0128), the **area and topology writes** of onboarding's template sync
(REQ-0129–REQ-0131, REQ-0133), and how the **self-service reads** raise a registry refusal
(REQ-0132), all at the end of this page.

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

The same exception also carries the registry's machine-readable refusal `code` and its
`detail` (REQ-0127). The batch lookups set neither — their refusals are validation errors,
which name no code — so both are `None` there.

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

---

## The DID batch

### REQ-0124 — the DID batch answers members, and shares the bound and the refusal rule

`lookup_members_by_dids` resolves a set of dataspace DIDs to the members holding them,
across communities. It is the join between the connector's answer to *who consented* —
stated in DIDs — and the registry's answer to *what they hold* (`rec-registry` REQ-0061).

**It answers members, not assets**, and that is the requirement rather than an
implementation detail. Onboarding writes a participant's declared supply point onto the
member and registers **no asset**, because a meter's `sensor_id` is assigned at physical
installation — so an asset-shaped answer is empty for every participant whose meter is not
yet commissioned, which is most of the population a consent-gated export covers. Every row
therefore carries `delivery_points`, and its `did`, which is what lets the caller attribute
a row back to the DID it asked about.

It shares the batch helper with the two asset lookups and therefore shares REQ-0120 (a
refusal raises rather than answering an empty list), REQ-0121 (a batch over
`MAX_BATCH_LOOKUP_IDS` is split and concatenated in request order) and REQ-0122 (an empty
batch asks nothing). Sharing is the point: three routes with the same empty-list hazard and
one implementation of it is why a fourth cannot quietly get it wrong.

A DID belonging to nobody and a member holding no supply points are deliberately
indistinguishable at the service (`rec-registry` REQ-0061), and the wrapper adds no third
meaning.

---

## Meter and profile writes

A community manager attaches a member's meter, detaches it, and corrects the member's role
and area, from the community dashboard. Its backend calls the registry through this wrapper
with a token carrying only the scope that one write needs — `rec-registry.assets.write` for a
meter, `rec-registry.members.profile.write` for a profile — so the helpers below take the
token per call, as every other method does.

These helpers differ from the existing writes on purpose. `create_member`, `patch_member`,
`upsert_asset` and their siblings return the undecoded response, because for their callers a
`409` is an ordinary outcome to branch on (a retried registration finds the member already
there). They keep that contract; onboarding depends on it. For the dashboard a refusal is an
answer to show the manager, and the registry names it with a code — so the helpers below
parse success into a schema and raise on everything else, and the code is the part of the
refusal the caller acts on.

The rules they rely on belong to `rec-registry`: the meter asset key `meter-<sensor_id>`
with the sensor id trimmed, one active holder per sensor id across communities, detaching as
a hard delete of the asset, and the dedicated profile route and its action. They are named
here only so the two can be kept honest.

### REQ-0125 — attaching a meter writes one asset through the per-asset route

The meter write (`RecRegistryAdminClient.put_asset`) sends one asset to `PUT /admin/communities/{community_key}/members/{member_key}/assets/{asset_key}`,
with the asset key and body the caller gives and nothing added, and answers the stored asset
as the generated `AssetDetailSchema` — the shape the asset `GET` answers, which the registry
declares on the `PUT` too since 1.6.0 (the wrapper declares no schema of its own; a key the
registry adds later is ignored, not refused). It does not compose the key and does not trim the sensor id: the key convention
and the comparison are the registry's, and a second copy of either here would be the one
that drifts.

Writing an asset the member already holds with the same body answers the stored asset, as
the registry does; the wrapper does not turn a no-op into an error.

This is what fills the gap REQ-0124 describes: onboarding registers no asset, and a meter
reaches a member only when a manager attaches it.

### REQ-0126 — detaching a meter deletes that one asset

The meter delete (`RecRegistryAdminClient.delete_asset`) sends `DELETE` for one asset key of one member and answers nothing on
`204`. The member's other assets are not touched. Any other status raises under REQ-0127 —
including a `404` for a key the member does not hold, which the wrapper does not read as
"already detached": whether that is success is the caller's decision, not a translation the
wrapper makes silently.

### REQ-0127 — a refused write raises with the registry's code

Extends REQ-0120 to the helpers of this section. A status the helper does not treat as
success — declared in the registry's spec or not — raises `RecRegistryApiError` carrying the
status code, the body and, when the registry's refusal names one, its machine-readable
`code` as a string (`sensor_held`, `asset_key_too_long`, `invalid_area_boundary`, and the
rest of the registry's error-code vocabulary). A refusal that names no code has `code` of
`None`.

The registry declares its coded `422` beside FastAPI's validation `422` as one `oneOf`
body (`ErrorResponse` / `HTTPValidationError`). The generated parse tries `ErrorResponse`
first and accepts a validation body as one too, with no `code`, so the model it returns
does not tell the two apart: the code is always read from the raw body, as below.

The registry's refusal body is flat: `{"detail": "<sentence>", "code": "<code>"}`, where
`detail` is always a string and `code` sits beside it at the top level. The helper reads
`code` from there and never parses the sentence; `detail` is kept for people. This is the
registry's shape, not onboarding's — onboarding nests its code inside `detail` — and the two
wrappers each read the shape their own service emits. The generated
layer's own "unexpected status" error never reaches the caller, and neither does its
parse of `code` into the generated `ErrorCode` enum: the helpers read the response
themselves. A body that is not JSON (a proxy's page) raises the same exception with
`code` and `detail` of `None`; an unreadable `200` raises rather than answering nothing.

The code is compared as a string and never mapped to an enum here: the vocabulary is the
registry's, a new code must not fail a caller built against the old list, and a generated
enum never compares equal to its string. `sensor_held` in particular is a normal answer —
another active member, in this community or another, holds the sensor — and the dashboard
shows it to the manager; the wrapper adds nothing to it, and it carries no member or
community the registry did not name.

The exception gains `code` and `detail`, keyword-only and defaulting to `None`, without
losing `status_code` or `body`, so a caller of the batch lookups that catches it is
unchanged.

### REQ-0128 — the profile write sends only role and area, to the profile route

The profile write (`RecRegistryAdminClient.patch_member_profile`) sends `PATCH /admin/communities/{community_key}/members/{member_key}/profile`
with a body of **only** the keys the caller set, out of `role` and `area`. It has no parameter
for any other member field, so it cannot send one, and an omitted key is omitted rather than
sent as `null` (the same rule as REQ-0111). It answers the updated member as a schema, and a
refusal raises under REQ-0127 (`invalid_role` and `unknown_area` are `422`; a missing
member or community is `404`). Called with neither key, it raises `ValueError` and sends
nothing: the registry refuses an empty body with a validation `422` that carries no code, so
there would be nothing to show. It passes the values as given — which roles a caller may set
is that caller's rule (the dashboard's backend allows only `consumer` and `prosumer`), and the
role and area sets are the registry's (`rec-registry` REQ-0066, REQ-0070).

It never falls back to the general member `PATCH`: that route needs
`rec-registry.members.write`, which the dashboard's backend is deliberately not granted,
because it would let it rewrite a member's `user_id`, `did` and status.

---

## Areas and topology: the onboarding template sync

Onboarding's templates are the source of truth for a community's areas, and onboarding
writes them to the registry: each primary substation as one topology node, then the area
that references it (`rec-registry` REQ-0067, REQ-0072). The sync and its drift check read
the community first to know what is there. For them a refusal is a row in a report to an
admin — an area that breaks the one-substation rule, an area members still use, a node an
area still lists — so these helpers follow the raising helpers above rather than the
undecoded writes: success is a schema, anything else raises `RecRegistryApiError` under
REQ-0127, with the registry's `code` read from the raw body.

The token is passed per call, as everywhere in this wrapper: onboarding requests its
optional write scope (`rec-registry.community.write`) only for the writes, and its read with
the default one. What is compared, created, pruned or refused is onboarding's to decide; the
wrapper adds no step, retries nothing and deletes nothing it was not asked to.

### REQ-0129 — the community read answers areas and topology, or raises

The community read (`RecRegistryAdminClient.read_community`) sends
`GET /admin/communities/{community_key}` and answers the generated `CommunityDetailSchema`:
each area with its `boundary` (`source`, `id`) and `topology`, and each topology node with
`id`, `type`, `name`, `operator_id` and `parent` — the names the registry reads and writes
since 1.6.0. Anything but `200` raises `RecRegistryApiError`, including a missing community
(`404`, which this route answers without a `code` and does not declare) and a missing grant
(`403`), so a community that could not be read is never taken for one with no areas. An
unreadable `200` raises too.

`get_community`, which answers the undecoded response, is unchanged; its callers depend on
that.

### REQ-0130 — an area write sends one area and answers the community

The area write (`RecRegistryAdminClient.put_area`) sends
`PUT /admin/communities/{community_key}/areas/{area_key}` with the body the caller gives —
`{name, boundary: {source, id}, topology: [id]}` — and nothing added. The area delete
(`RecRegistryAdminClient.delete_area`) sends `DELETE` for one area key. Both answer the whole
community as `CommunityDetailSchema`, as the registry does, so the caller sees the areas it
did not touch.

A refusal raises under REQ-0127: `invalid_area_boundary` (`422`) on the write,
`area_in_use` (`409`) on the delete — whose sentence names the member count, which the
wrapper keeps in `detail` and does not parse — and `community_not_found` (`404`). A `404`
with no code for an area the community does not have is raised, not read as "already
deleted": whether that is success is the caller's decision. The one-substation rule, and
that the area's node must exist before the area, are the registry's; the wrapper checks
neither.

### REQ-0131 — a topology node write sends one node and answers the community

The node write (`RecRegistryAdminClient.put_topology_node`) sends
`PUT /admin/communities/{community_key}/topology/{node_id}` with the body the caller gives —
`{id, type, name?, operator_id?, parent?}`. It does not fill the body's `id` from the path or
the other way round: the registry refuses a mismatch with a validation `422`, and the wrapper
lets that refusal through rather than hiding it. The node delete
(`RecRegistryAdminClient.delete_topology_node`) sends `DELETE` for one node id. Both answer
the whole community as `CommunityDetailSchema`.

A refusal raises under REQ-0127: `invalid_area_boundary` (`422`, the write would change the
`type` of a node an area relies on), `topology_node_in_use` (`409`, an area lists the node;
the sentence names the areas), `community_not_found` (`404`), and a `404` with no code for a
node the community does not have, which is not read as "already deleted".

### REQ-0133 — an area rename sends only the new key and answers what moved

The area rename (`RecRegistryAdminClient.rename_area`) sends
`POST /admin/communities/{community_key}/areas/{area_key}/rename` with a body of **only**
`{"new_key": <new key>}`, and answers the generated `AreaRenamedSchema`: `old_key`,
`new_key`, `members_moved` and the whole community after the rename, as the registry answers
it (`rec-registry` REQ-0079). It is one request: the wrapper does not follow it with an area
`PUT` or `DELETE` of its own, and it does not check the key's pattern — both are the
registry's. The registry moves the area as stored and every member of the community whose
`area` is the old key, of any status, in one transaction; that is why a template sync uses
it for an area whose substation the registry holds under another key, where a `PUT` under
the new key is refused (one area per boundary) and the old key's `DELETE` is refused while
members hold it.

Anything but `200` raises under REQ-0127: `invalid_area_key` (`422`, the new key is not an
area key), `area_not_found` (`404`), `area_key_taken` (`409`, the new key exists, the old key
included), `community_not_found` (`404`); `code` is `None` for a validation `422`, a missing
grant (`403`) or a body that is not JSON. An unreadable `200` raises too. It needs
`rec-registry.community.write`.

---

## Self-service reads

### REQ-0132 — a refused self-service read raises `RecRegistryApiError` with the code

Since 1.6.0 the registry declares the `403` its self-service routes answer a caller who is
no member — `{"detail": "You are not a member of any community", "code": "not_a_member"}`
on `/user/community`, `/user/member`, `/user/assets`, `/user/assets/{asset_key}` and
`/user/delivery-points` (`rec-registry` REQ-0073).

Each of `RecRegistryUserClient.get_my_community`, `get_my_member`, `get_my_assets`,
`get_my_asset` and `get_my_delivery_points` answers its schema on `200` and on anything else
raises `RecRegistryApiError` under REQ-0127: `status_code`, the raw `body`, and the
registry's `code` and `detail` read from the top level of the body — so a caller that tells
"no member" apart does it with `exc.status_code == 403 and exc.code == "not_a_member"`, and
a member owning nothing stays a `200` with no items. The response is read by the wrapper,
never by the generated parse: that parse calls `response.json()` on every status the route
declares, so a body that is not JSON on such a status (a proxy's page on the `403`, or on
`/user/assets/{asset_key}`'s `422`) would fail there with a decode error. It raises
`RecRegistryApiError` with `code` and `detail` of `None` instead. An undeclared status raises
the same exception, never the generated `UnexpectedStatus`, and an unreadable `200` raises
rather than answering `None`.

This replaces the earlier contract, under which these reads raised the generated
`UnexpectedStatus`. The consumers in the workspace other than dataset-api catch any
exception around these reads. dataset-api's row filter, which denies rows on `not_a_member`
and nothing else, calls the route itself today and is to move to `get_my_assets` and this
exception's `code`.
`get_me` is unaffected: the registry answers it `200` with no membership.
