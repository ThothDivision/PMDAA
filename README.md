# P-DADA — Planning DADA

An agent skill for plans: strategy, product vision, architecture and build plans, roadmaps, business models and public planning
sites. Fork of [DADA](https://github.com/AnEntrypoint/dada): same non-linear traversal (living Frontier, branches, reopening,
WHOLE rounds, five stop conditions, one subagent per literary reference), with a planning anchor graph and planning critics.

## Install

```sh
npx skills add PrometheusIntelligence/p-dada -s p-dada
```

## Use

Invoke `$p-dada` with the plan or idea. Two modes:
- **Vision** — public-facing plan; criterion: Rumelt's kernel (diagnosis, guiding policy, coherent action) and every checkable claim true or labelled.
- **Execution** — build plan; criterion: every milestone has an exit test, every decision has options, a recommendation, an owner and a decide-by.

Each run writes `PLANNING-LOG.md` beside the plan: Traversal Plan with Frontier, Decision Records, Panel Reports, Anchor Ledger
and Compliance Check, plus printed claim / decision / exit-test audits. Read `skills/p-dada/SKILL.md` for the contract and
`skills/p-dada/references/planning-graph.md` for the graph.

## Validation
`python3 scripts/validate_skills.py` (PyYAML). CI runs the same check.

Credit: DADA by AnEntrypoint · P-DADA fork by PrometheusIntelligence · Pimp My Skill · SolutionsAsService
