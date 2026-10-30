# Flexibility client

`celine.sdk.flexibility`. It wraps the generated Flexibility API client in two classes: the
member's surface (`FlexibilityClient`: suggestions and their own commitments) and the
service surface (`FlexibilityAdminClient`: the commitments export, pending commitments,
settlement).

Only the **commitments export** is specified here, because it is the one call whose empty
answer is a real answer: a mirror flow asks for every commitment since a date, and `[]`
means "there were none". The rest of the wrapper is not specified yet.

The service's own behaviour — who may export, which statuses the export returns, how
`created_after` filters — belongs to `flexibility-api`.

---

## Commitments export

### REQ-0210 — a refused or unreadable export raises, and never answers an empty list

`FlexibilityAdminClient.export_commitments(*, created_after=None, token=None)` sends
`GET /api/commitments/export`, with `created_after` as an ISO datetime when given.

- A `200` whose body is a JSON list answers that list as `CommitmentOutSchema` items, in the
  order the service sent them. An empty list answers `[]`.
- Any other status — `401`, `403`, `404`, `422`, any `5xx`, a proxy's HTML page — raises
  `FlexibilityApiError` with `status_code` set to the status the service answered.
- A `200` whose body is not a list of commitments — not JSON, `null`, an object, an item
  missing a field — raises `FlexibilityApiError` with `status_code` `200`.

The message names the call and the status code only. The response body is kept on
`FlexibilityApiError.body` and never written into the message, and no decode or validation
error is chained underneath it, so a caller that logs the exception writes neither the
token nor anything the service echoed back.

The status is read before the body is parsed, so a non-JSON refusal raises this error
rather than a decode error from the generated parser.

Returning `[]` for a refusal is the failure this requirement exists to prevent: a mirror
flow receiving it completes, writes nothing, and reports success.
