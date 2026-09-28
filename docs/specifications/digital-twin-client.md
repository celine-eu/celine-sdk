# Digital Twin client

`celine.sdk.dt`. `DTClient` wraps the generated Digital Twin client in one curated class per
domain (`communities`, `participants`, `grid`). None of it is specified yet, except the part
below: what every method writes to a log when the Digital Twin refuses a request, and that no
method keeps state between calls through its arguments. A request carries the caller's
values — a participant id, a date, for the boundary fetchers a point's coordinates — and a
refusal repeats them.

The fetchers themselves, and what they answer, belong to `digital-twin`.

---

## Refusals and payloads

### REQ-0160 — no DT client method logs a refusal's detail, and the payload is the caller's

**Every public method** of `CommunityClient`, `ParticipantClient` and `GridClient` that logs
a refusal logs only which call was refused (the method, or the fetcher or ontology spec id),
the status and the error `type` codes (`missing`, `float_parsing`, ...) — **never the
refusal's `msg`, `input` or `loc` values, and never the community, participant or network id
the caller sent**. FastAPI's validation body repeats the submitted input; the platform does
not log coordinates or identifiers taken from it. A method that raises without logging
satisfies this too. The raised `DTApiError` carries no refusal detail either.

`CommunityClient.fetch_values` posts the caller's `payload` to
`POST /communities/it/{community_id}/values/{fetcher_id}`, with `limit` and `offset` added
when given. It, `ParticipantClient.fetch_values`, `GridClient.fetch_values` and both
`fetch_ontology` methods work on a **copy**: the caller's dict is never modified, and a call
that passes no payload starts from a new empty one, so nothing one call adds reaches the
caller or the next call. **No public method has a mutable default argument** (a `dict`,
`list` or `set`); an absent payload is `None`. `ParticipantClient.fetch_values` still sends
`offset` `0` when the caller gives none, as it always has.
