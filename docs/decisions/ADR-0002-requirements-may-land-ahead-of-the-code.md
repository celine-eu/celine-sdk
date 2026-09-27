# ADR-0002 — A requirement may land ahead of the code, marked planned

**Date:** 2026-09-27
**Status:** accepted

## Context

The specifications were **extracted from the implementation** on 2026-08-15, and their index
says so: each requirement states what the code already does and what consumers therefore
depend on. That was the right rule for an extraction, and it made every requirement a
promise the suite could check on the day it was written.

It has no answer for a change that crosses a seam. The next platform change needs the
registry wrapper to attach and detach a meter, to write a member's role and area through a
dedicated registry route, and to surface the registry's machine-readable refusal codes; the
onboarding wrapper needs a way to ask for a community's areas to be synced to the registry.
The consumers — the community dashboard's backend and onboarding — are specified and built
in the same delivery, against these helpers. If the requirement may only be written once the
code exists, the consumers are designed against nothing, and the SDK's half of the contract
is whatever the first implementation happened to do.

`rec-registry` meets the same question for its own requirements and answers it the same way
(its decision on planned requirements). Two repositories on either side of one seam with two
rules would leave the seam half-specified.

## Decision

A requirement may be written before the code that satisfies it, provided it is **marked
planned**:

- A line `**Status:** planned` directly under its heading. A requirement with no status line
  is implemented, which is every requirement written before this decision.
- A planned requirement states the behaviour the change will deliver, in the same terms as an
  implemented one — something a test can name.
- No test carries `@verifies` for it yet. The change that makes it true lands its tests with
  their tags and **removes the status line in the same change**, which is the moment it
  becomes a promise to consumers.
- An implemented requirement is never rewritten to describe behaviour the code lacks. When
  planned work changes it, the planned behaviour is a new planned requirement, or a paragraph
  inside the old one headed **Planned**, and the current text stays true until the change
  lands.

## Consequences

- The specifications now hold two kinds of sentence, and a reader must check the status line
  before relying on one. A planned requirement is a design commitment, not something a
  consumer may call.
- The harness reports a planned requirement as uncovered until its tests land. That is the
  honest reading: nothing verifies it. It is also why a planned requirement should not sit in
  the specifications long — one that outlives the delivery it was written for is an
  aspiration, and is either landed or deleted.
- The generated tree is still not specified (the index says why). A planned requirement on a
  wrapper method may depend on a route the generated client does not have yet; regenerating
  from the service's published spec is part of the change that lands it, not of writing the
  requirement.
- Someone will be tempted to write a planned requirement for a wish with no delivery behind
  it. The rule above — landed or deleted — is the answer.
