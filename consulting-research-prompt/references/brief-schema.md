# Brief schema v1

This schema defines a review-only structured task brief. It frames proposed work
for human review; it is not research output, approval to research, or a request
to obtain client data.

## Required top-level fields

Every brief must contain these fields:

- `schema_version`: non-Boolean integer `1`.
- `status`: generated status, either `draft` or `needs-review`. Do not generate
  `approved` or `rejected`.
- `generated_at`: generation timestamp.
- `input`: object with non-empty `company` and `question` strings.
- `identity`: company/entity identification, including its verification state.
- `classification`: a primary scenario and optional supporting scenarios.
- `decision`: the decision the brief is intended to inform.
- `scope`: proposed geography, product, period, and/or other scope boundaries.
- `issue_tree`: branches and questions that organize the decision analysis.
- `hypotheses`: testable statements, described below.
- `source_plan`: planned evidence routes, described below.
- `client_requests`: client-data requests, described below.
- `deliverables`: planned review outputs.
- `risks`: known evidence, scope, or decision risks.
- `open_questions`: unresolved questions for human review.
- `execution_prompt`: review-gated prompt text.
- `review`: review metadata, whose `status` exactly matches top-level `status`.

## Hypotheses and evidence

`hypotheses` is a list. Each entry contains non-empty `id`, `statement`,
`priority`, `kill_test`, and `required_evidence`. Use `priority` to make the
decision importance explicit. `kill_test` states what evidence would falsify the
hypothesis. `required_evidence` is a non-empty list of evidence needed to test
it. If included, `confidence` is a number from `0.0` to `1.0` inclusive.

Use evidence-state tags consistently in statements, source plans, and review
notes:

- `[F]` fact supported by cited evidence.
- `[I]` inference drawn from facts.
- `[A]` assumption pending validation.
- `[E]` estimate or model output.

## Source plan and client data

`source_plan` is a list. Every source record has a `route` selected from:

- `public-available`
- `public-partial`
- `client-required`
- `proxy-available`
- `unknown`

`client_requests` is a list. Each request must have non-empty `priority`,
`item`, `period`, `granularity`, `reason`, `decision_affected`, `sensitivity`,
`substitute`, and `consequence_if_missing`.

When client data is missing, do not fabricate it or silently substitute public
data. Mark the missing item, identify any proxy as `[A]` or `[E]`, state the
decision consequence, and retain the request for human review. A
`client-required` route means the relevant conclusion remains unverified until
the client supplies the specified data.

## Review gate

`execution_prompt` must explicitly require `人工审核` or `human review`, and
must also include `范围确认` or `scope gate`. The brief remains in `draft` or
`needs-review` until a human changes its status outside this generated schema.
