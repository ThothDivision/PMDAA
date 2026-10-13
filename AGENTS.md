# PMDAA project

Planning + Management Directed Ambition Agent. Two distributable skills live in `skills/`, each linked from `.agents/skills/`:

- `skills/pmdaa/` — the skill this repo ships: Plan mode (P-DADA contract in `references/plan-mode.md`) + Manage mode (portfolio
  ledger, resume protocol, `scripts/portfolio.py`, `references/management-graph.md`).
- `skills/p-dada/` — upstream P-DADA (PrometheusIntelligence/p-dada), kept unchanged so upstream changes merge cleanly. When it
  changes, copy its `references/planning-graph.md` and `design-graph.md` into `skills/pmdaa/references/` and refresh
  `plan-mode.md`; the validator fails on graph drift.

Keep frontmatter name, folder name and `agents/openai.yaml` consistent per skill. Keep DADA's traversal contract (living Frontier,
no move quota, WHOLE rounds, S1–S5, one subagent per literary reference). Validate with `python3 scripts/validate_skills.py` and
`python3 -m unittest discover -s tests`. Do not publish credentials, machine configuration or private-repo internals: `examples/`
holds only public-safe ledgers (`portfolio.py check --public`). Planning logs and real portfolios live with what they describe,
not in this repo.
