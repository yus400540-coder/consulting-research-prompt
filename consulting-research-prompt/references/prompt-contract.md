# Prompt contract

The generated Markdown prompt is a review-gated specification for a later executor.
It must state that `research-to-obsidian` is required for later execution, that no
auto execution is authorized, and that the current package remains `draft` or
`needs-review` until human review.

## Required order

Use these headings in this exact order. Populate only from the company name,
consulting question, and clearly labeled assumptions or client requests.

1. **Review warning** — human review, no auto execution, and required downstream `research-to-obsidian` dependency.
2. **Client and decision** — client/company, decision owner if known, consulting question, alternatives, and success criteria.
3. **Verified identity plus assumptions** — legal/common name, official identity source, jurisdiction, public/private/ticker, industry, main business, same-name ambiguity; distinguish `[F]`, `[I]`, `[A]`, and `[E]`.
4. **Scope/exclusions** — geography, products, period, stakeholders, exclusions, and unresolved scope gates.
5. **MECE issue tree** — decision branches, subquestions, and dependencies.
6. **Hypotheses/kill tests** — prioritized hypotheses, falsifiers, required evidence, and decision impact.
7. **Public source plan** — planned source channels, route, original source, permitted substitutes, and risk if missing; no private-derived sensitive search terms may be sent to public services.
8. **Client request list** — item, period, granularity, priority, sensitivity, reason, substitute, and consequence if missing.
9. **Analysis sequence** — evidence acquisition, evidence ledger, synthesis, financial health, scenario/valuation only after gates, and review checkpoints.
10. **Deliverables** — decision memo, evidence ledger, financial-health report, scenario outputs, and only applicable specialist outputs.
11. **Full `research-to-obsidian` Vault rules** — the later executor must apply the rules below only after human approval.
12. **Scope/evidence/publication gates** — explicit approval gates before expansion, decision claims, and publication.
13. **Retrieval and audit acceptance** — acceptance checks for traceability, retrieval, completeness, and audit trail.

## Evidence and financial gates

Every claim, assumption, request, and model output must be tagged consistently: `[F]` cited fact, `[I]` inference, `[A]` assumption, or `[E]` estimate/model output. For each quantitative item, specify units, periods, sources, and confidence. Complete a company financial-health report before strategy-to-model conclusions or valuation. The valuation prerequisites are a scoped decision purpose, financial-health report, normalized historical financials, forecast assumptions, capital structure, discount-rate logic, and relevant comparable evidence; otherwise valuation remains out of scope or `[A]`.

## Full `research-to-obsidian` Vault rules for later execution

After human approval, perform original source capture before analysis; preserve URL or file identity, publisher, publication date, access date, extract location, and claim-level citation. Perform full extraction of relevant evidence rather than summary-only collection. Write incrementally after each source batch and analysis stage, use wikilinks between entity, source, hypothesis, and deliverable notes, keep an `index.md`, and append every action/evidence decision to append-only `log.md`. Record contrary evidence alongside supporting evidence, resolve or preserve the conflict, and never overwrite the audit history.

## Acceptance

Before a reviewer approves later execution, confirm scope and permissions, every decision-critical assertion has an original-source route or disclosed gap, all client-required data is requested rather than fabricated, and the Vault can retrieve each conclusion through its wikilinks and audit log. The prompt author must not start research, create a Vault, publish a conclusion, or trigger downstream execution.
