---
name: consulting-research-prompt
description: Use when a user wants a company name and consulting question converted into a human-reviewable consulting research prompt.
---

# Consulting Research Prompt

Generate a decision-focused research package for review, not research results.
The required input is exactly a company name plus a consulting question. Treat every
other detail as an assumption or client request, labeling assumptions `[A]`; do not
silently accept it as fact.

## Boundaries

This Skill must not execute `research-to-obsidian`.
Do not conduct substantive research, create a Vault, run a model, or invoke a
downstream Skill. The only generated statuses are `draft` and `needs-review`.
Do not emit an initial `approved` or `rejected` status. The package can be generated
when research-to-obsidian is not installed, but its execution prompt must disclose
that later execution requires `research-to-obsidian`.

## Parallel prompt construction

Before constructing the package, confirm the work has at least two independent
lanes and parallel dispatch is likely to reduce elapsed time. Otherwise stop and
report that parallel acceleration is unavailable; do not silently fall back to a
serial run.

Use native collaboration to dispatch at most three worker agents in one wave. Do
not spawn nested agents or invent work merely to fill a slot. Give each worker one
exclusive lane:

1. identity, industry, and source routes;
2. decision framing, scenario routing, and issue tree;
3. financial due diligence, client data requests, and valuation gates.

Use two workers when two lanes cover the request. The main agent coordinates and
merges results instead of creating a fourth research lane. Workers return structured
fragments and must not write the final package. Workers must not invoke downstream
Skills, conduct the later research, or create an Obsidian Vault. If collaboration is
unavailable or a clean file/output partition is impossible, stop and explain why.

## Generate the review package

1. Make a minimal, permission-bound identity check: legal/common name, official
   identity source, jurisdiction, public/private/ticker, industry, main business, and
   same-name ambiguity. Record unavailable fields as `[A]` or review questions; do
   not expand this into company research.
2. Choose exactly one primary scenario and zero or more supporting scenarios with
   the [scenario router](references/scenario-router.md). Frame the decision,
   exclusions, issue tree, hypotheses, kill tests, public-source plan, and client
   requests.
3. Draft a structured `brief.json` matching the [brief schema](references/brief-schema.md),
   validate it, and render the human-review package. Keep the generated state `draft`
   or `needs-review`.
4. Produce the Markdown prompt in the exact order required by the
   [prompt contract](references/prompt-contract.md), using the
   [source-channel matrix](references/source-channel-matrix.md) for planned evidence
   routes. Then ask for human review. Do not auto-execute the prompt.

## Human review

The reviewer confirms identity, scope, scenario selection, data permissions,
assumptions, and any proposed client requests before any later research or
client-facing use. The reviewer alone may approve, reject, revise, or route the work.

## Package references

- [Brief schema](references/brief-schema.md)
- [Scenario router](references/scenario-router.md)
- [Source-channel matrix](references/source-channel-matrix.md)
- [Prompt contract](references/prompt-contract.md)
- [Review template](assets/review-template.html)
