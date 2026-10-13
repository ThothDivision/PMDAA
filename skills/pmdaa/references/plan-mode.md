# Plan mode: the P-DADA contract

Verbatim from skills/p-dada/SKILL.md (P-DADA, PrometheusIntelligence/p-dada); only link paths changed. Run it unchanged.


Fork of [DADA](https://github.com/AnEntrypoint/dada) for plans instead of graphic design. The traversal mechanics (living
Frontier, branches, reopening, WHOLE rounds, stop conditions, one subagent per literary reference) are DADA's; the graph,
the critics, the measurements and the artifact are planning ones.

## Contract (read first)

Loading this skill means performing the workflow, not borrowing its vocabulary. A run is complete only when these five
artifacts exist in `PLANNING-LOG.md` beside the plan (create it and append as you go; if you cannot write files, put them in the reply):

1. **Traversal Plan**, including the living **Frontier**
2. **Decision Records**, one per move (a move is a change to the plan: a section added, a decision taken, a claim cut)
3. **Panel Reports**, one per round
4. **Anchor Ledger**
5. **Compliance Check**

There is no move quota. The run ends when the stop conditions hold. If an external limit stops you first, write the Open
frontier, say the run is incomplete and give the resume point. In the final reply state the mode, the tools used, the stop
conditions met or not met, and every step skipped. Never describe the process as followed if it was not.

## Mode (choose once, state it in the Traversal Plan)

| | Vision | Execution |
|---|---|---|
| Use when | The plan is read by people who decide whether to back, join or partner (public site, investor or partner brief) | The plan is read by people who build it (repo plan, milestones, specs) |
| Governing criterion | **Kernel of good strategy** (Rumelt): diagnosis, guiding policy, coherent actions — and every claim a reader could check is true or labelled | **Buildable and testable**: every milestone has an exit test a stranger could run, every decision has options, a recommendation, an owner and a "decide by" |
| Required critics (one subagent per reference) | Rumelt (*Good Strategy Bad Strategy*), Minto (*The Pyramid Principle*), Klein (premortem, *Sources of Power*), Krug (*Don't Make Me Think*), plus at least 2 more | Brooks (*The Mythical Man-Month*), Nygard (ADRs, *Documenting Architecture Decisions*), Shostack (*Threat Modeling*), Flyvbjerg (*How Big Things Get Done*), plus at least 2 more |
| Extra record field | Reader and decision the section serves | Exit test and owner |

Both modes need a seat that argues about who the plan leaves out (users without a voice in the room, regulators, the
counterparty that carries the risk), and at least one pair of critics joined by a dotted edge in the graph.

## The plan must be measured

A plan's "measurements" are checks a machine or a reader can repeat. Run them before every panel round and at the final state:

- **Claim audit**: every number, date, standard, regulation or market fact is (a) sourced with a link, (b) computed in the
  plan from stated inputs, or (c) labelled *assumption* / *indicative*. Count each class and print the counts.
- **Decision audit**: every open question is either a Decision Record (options, recommendation, decide-by, owner) or
  listed as deliberately deferred with a reason. Count open vs decided.
- **Exit-test audit** (Execution): every milestone has at least one test a stranger could run and a measurable threshold.
- **Consistency**: phase names, component names and numbers agree across every document (one glossary, one roadmap of record).
- **Recompute**: every derived number (totals, windows, scenario results) is recomputed from its source table before each WHOLE round; a total that is not the sum of its printed rows is a defect.
- **Build**: links resolve, diagrams parse, the site builds.

## How the traversal works

Keep a **Frontier** of candidate moves reachable from visited anchors along outgoing, incoming and dotted edges. Choose
in this order: open Andon objections, REOPENED moves, dotted counterpoints of BREAK moves not yet applied or declined, the
sharpest critic disagreement in the last panel, incoming anchors that would ground what exists, outgoing edges. Among equals
take the move that changes the most (a removed false claim outranks an added section). Branch rival structures, compare
them in a Pugh matrix and scrap the losers. When a decision changes, reopen every section that depends on it.

```
## Frontier
| Candidate | Reached via (edge, direction) | From anchor | Status OPEN / DEFERRED (reason) / TAKEN (Mn) |
```

## Workflow

### Step 0. Tooling and inputs
Inventory graph, diagram, task and search tools and use them. Read everything that exists: the current plan, the code or
sandbox it describes, linked repos, prior logs and the carry-forward file. A premortem round **R0** on the inherited plan is
mandatory: the panel lists how it will fail; every objection becomes a Frontier item.

### Step 1. Traversal Plan
State the mode with its reason, the readers and the decision each reader must make, the governing criterion, hard limits
(what the plan must not claim, e.g. "not an offer of securities"), the seed (3–5 anchors with exact labels from
[references/planning-graph.md](planning-graph.md), including one dotted counterpoint) and the initial Frontier.

### Step 2. The loop: one Frontier candidate per pass
Write the Decision Record **before** changing the plan:

```
## Move Mn: <name>  (KEEP-THE-RULE | BREAK)
- Anchor(s) and edge followed:
- Depends on (moves / decisions):
- Hypothesis: what this change lets a reader do or decide
- Options considered (at least two for any decision) and the recommendation:
- Measurement before → after (claim / decision / exit-test counts, or the specific check):
- Result: KEEP | ADAPT | SCRAP | REOPEN (who)
```

Then run the panel on the changed section and record:

```
### Panel, Move Mn or WHOLE, round R  (sections examined)
| Critic (work) | Observed in the plan (quote or count) | Verdict PASS / OBJECT / ANDON | Requested change |
```

An OBJECT is resolved as ADAPT, SCRAP or OVERRULE; an overrule names the trade in the plan's own units (what the refused
change would cost the reader). An authority sits only when it argues from its own work on the page.

### Step 3. WHOLE rounds
Run a WHOLE round on the full plan whenever a cluster of moves settles and always before the stop test.

### Step 4. Stop test
- **S1** No OPEN Frontier items.
- **S2** A WHOLE round with PASS from every required critic and no Andon.
- **S3** Two consecutive WHOLE rounds with no ADAPT, SCRAP, REOPEN or new OPEN item.
- **S4** Falsification push: the boldest claim or bet in the plan was attacked (premortem, reference-class check, or a
  recomputation) and the result logged with what changed in the plan.
- **S5** Every dotted edge leaving a used anchor applied or declined with a reason.

Then: a double-loop paragraph (did the criterion, panel or graph fail the plan; one graph amendment), a **Carry-Forward
Ledger** of durable facts about the domain, and the **Compliance Check**:

- [ ] Inputs read, tools inventoried, R0 premortem run
- [ ] Mode, readers and criterion stated
- [ ] Seed with exact labels and a dotted counterpoint; living Frontier
- [ ] At least one BREAK move; no quota used as a stopping rule
- [ ] A Decision Record before each move, with options and measurements
- [ ] A Panel Report per round meeting the mode's composition rule, one subagent per reference
- [ ] Claim, decision, exit-test and consistency audits printed at the final state
- [ ] S1–S5 shown as met, with where
- [ ] Anchor Ledger complete; final reply states mode, tools, stop conditions and everything skipped

## Anti-skip rules
- A plan that reads well but cannot be checked has not passed; uncounted claims are a skip.
- An open question without options, a recommendation and a decide-by is not a decision.
- A milestone without an exit test is a wish.
- A single model writing every critic in turn is not a panel; record it as non-compliant if no subagents exist.
- Short on effort is not an exemption; write the Open frontier.

## Graphs
- Planning: [references/planning-graph.md](planning-graph.md) — seed, panel and moves come from here.
- Presentation of a plan site (layout, type, readability): DADA's design graph in [references/design-graph.md](design-graph.md).
