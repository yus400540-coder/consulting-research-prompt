# Scenario router

Assign one primary scenario that owns the decision; add zero or more supporting
scenarios only when they answer a distinct dependent decision. Classify from the
question, not from unverified company facts. If unclear, use `custom-decision` and
make ambiguity an `[A]` review question.

| Scenario ID | Trigger | Decision form | Priority branches | Appropriate methods | Required deliverables | Common client data |
| --- | --- | --- | --- | --- | --- | --- |
| `market-entry` | Enter a country, segment, or category | Whether/where/how to enter | attractiveness; right to win; entry economics; mode | segmentation, demand sizing, entry-mode screen | entry thesis, country/segment priority, entry economics | target revenue, capability, constraints |
| `growth-strategy` | Accelerate revenue/share | Which growth bets to fund | growth pools; customer; offer; capability | growth decomposition, segmentation, initiatives | growth portfolio, roadmap, KPIs | sales, pipeline, budgets |
| `business-model` | Redesign how value/revenue is created | Which model is viable | value proposition; monetization; unit economics; operating model | business-model canvas, unit economics, experiments | target model, economics, pilot plan | pricing, costs, funnel data |
| `portfolio-strategy` | Allocate across businesses/products | Hold, build, harvest, or exit | attractiveness; position; synergies; capital | portfolio matrix when data supports it, capital allocation | portfolio actions, capital plan | BU financials, investment plans |
| `pricing` | Change price/packaging/discounts | What price architecture maximizes value | willingness to pay; waterfall; elasticity; governance | price waterfall, conjoint where appropriate, elasticity | price architecture, guardrails, impact case | transactions, discounts, costs |
| `channel-strategy` | Select or redesign routes to market | Which channels and roles to use | customer journey; coverage; channel economics; conflict | channel economics, coverage mapping, partner screen | channel design, partner plan, incentives | channel sales, partner terms |
| `customer-growth-retention` | Acquire, retain, or reactivate customers | Which levers improve profitable lifecycle value | segments; funnel; cohorts; experience; offers | cohort/funnel analysis, journey mapping, churn models | growth/retention plan, KPI tree | CRM, cohorts, campaign results |
| `cost-reduction` | Reduce cost or improve productivity | Which cost actions meet a target safely | spend; process; make/buy; overhead; implementation | spend cube, zero-based challenge, benchmarking | savings bridge, initiative plan, risk controls | GL, procurement, headcount |
| `turnaround` | Distress, liquidity pressure, severe underperformance | How to stabilize then restore value | cash; profitability; customers; operations; governance | 13-week cash flow, rapid diagnostic, restructuring | stabilization plan, turnaround roadmap | cash, debt, covenant, daily operations |
| `supply-chain-operations` | Improve service, inventory, network, or throughput | Which operating changes optimize cost/service | demand; supply; inventory; network; execution | S&OP diagnostic, network optimization, value-stream map | operating blueprint, service/cost case | inventory, OTIF, capacity, suppliers |
| `digital-ai-transformation` | Deploy digital, data, automation, or AI | Which use cases create governed value | use cases; data; process economics; architecture; adoption | use-case prioritization, process mining, value cases | use-case portfolio, target architecture, adoption plan | process times, data inventory, IT spend |
| `organization-design` | Redesign structure, roles, governance, talent | Which organization enables strategy | accountabilities; spans/layers; decision rights; skills | operating model, RACI, 7S when alignment is central | target org, governance, transition plan | org chart, roles, workforce data |
| `commercial-due-diligence` | Assess target market/commercial case for a transaction | Whether commercial thesis supports the deal | market; customers; competition; plan credibility | market/customer interviews where approved, triangulation | commercial diligence report, risk/opportunity case | IM, target sales, customer data |
| `financial-due-diligence` | Assess earnings, cash, and financial quality | Whether financial performance is sustainable | QoE; revenue; margin; cash; working capital | QoE bridge, trend/variance analysis | financial-health report, QoE findings, red flags | management accounts, ledgers, debt |
| `valuation` | Price a business, asset, or deal | What value/range is defensible | financial health; forecast; WACC; comparables; synergies | DCF conditional on prerequisites, trading/transaction comps | valuation range, assumptions, sensitivity | audited financials, forecasts, cap table |
| `post-merger-integration` | Integrate an acquisition or merger | Which integration choices realize value | synergies; operating model; people; systems; Day 1 | synergy tracking, clean teams, integration planning | Day 1 plan, IMO plan, synergy roadmap | deal thesis, org/system maps |
| `competitive-intelligence` | Understand competitor moves or position | How to respond to competitors | competitors; capabilities; offers; likely moves | competitor profiling, war gaming, sourced synthesis | competitor map, response options | win/loss, competitor observations |
| `location-selection` | Select site, plant, office, or facility location | Which location best meets constraints | demand; labor; cost; logistics; incentives; risk | weighted location screen, network model | ranked locations, sensitivity, recommendation | footprint, volume, labor needs |
| `government-industrial-planning` | Plan public-sector industrial or regional development | Which policy/investment portfolio advances goals | baseline; sectors; ecosystem; finance; implementation | economic baseline, cluster analysis, stakeholder design | industrial plan, project portfolio, governance | policy goals, fiscal data, land/infrastructure |
| `executive-partner-diligence` | Evaluate executive, partner, or sponsor fit | Whether to appoint/partner and under what controls | track record; capability; incentives; integrity; conflicts | structured reference plan, governance assessment | diligence memo, conditions, risk register | CV, references, agreements |
| `regulatory-esg-response` | Address regulatory, compliance, ESG, or stakeholder requirement | How to comply while protecting value | requirements; exposure; controls; cost; stakeholders | obligations map, materiality, control gap assessment | response roadmap, compliance/ESG case | permits, policies, emissions, incidents |
| `custom-decision` | Unknown, mixed, or nonstandard problem | What decision and evidence are required | decision owner; alternatives; criteria; unknowns | problem framing, MECE issue tree, hypothesis design | decision charter, tailored plan | client context needed to frame |

## Composition rules

- **acquisition + price:** primary `commercial-due-diligence` (or `financial-due-diligence` when earnings quality is the decision); supporting `valuation`, then `post-merger-integration`. Do not price before financial-health and commercial thesis gates are explicit.
- **distress + cost:** primary `turnaround`; support with `cost-reduction` after the cash stabilization branch. Preserve customer, safety, and control constraints.
- **new geography:** primary `market-entry`; add `location-selection`, `channel-strategy`, or `regulatory-esg-response` only if material to the entry choice.
- **AI + process economics:** primary `digital-ai-transformation`; support with `supply-chain-operations` or `cost-reduction` where quantified process economics determine value. Never assume AI value without an adoption and unit-economics test.
- **unknown problems:** use `custom-decision`, define the decision owner and alternatives, and ask human review to choose a scenario before later research.

## Method guardrails

SWOT is a sourced synthesis, not a fact-generation method. Five Forces, 7S, portfolio matrices, and DCF are conditional: use them only when their required evidence, scope, and decision purpose are stated; otherwise list the missing prerequisites and select a simpler method.
