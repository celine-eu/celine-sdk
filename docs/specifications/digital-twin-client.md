# Digital Twin client

`celine.sdk.dt`. `DTClient` wraps the generated Digital Twin client in one curated class per
domain (`communities`, `participants`, `grid`). None of it is specified yet, except the part
below: what every method writes to a log when the Digital Twin refuses a request, that no
method keeps state between calls through its arguments, and that `GridClient` no longer offers
the legacy wind and heat calls. A request carries the caller's
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

---

## The grid client

### REQ-0161 — `GridClient` has no wind or heat methods

`GridClient` has no public attribute `wind_map`, `wind_bosco`, `wind_alert_distribution`,
`wind_trend`, `heat_map`, `heat_alert_distribution` or `heat_trend`, and `celine.sdk.dt.grid`
imports none of the generated `it_grid_wind_*` / `it_grid_heat_*` operations or response
models. The Digital Twin no longer serves the routes they called.

Wind and heat risk data is read through `GridClient.fetch_values` with the `risks`,
`risks_now`, `risks_8h`, `risk_km` and `trendline` fetchers, or the named methods that wrap
them (`risks`, `risks_now`, `trendline`).

*Verified by: unit — `hasattr(GridClient, name)` is false for each of the seven names, and the module source of `celine.sdk.dt.grid` names none of the generated wind/heat modules*
