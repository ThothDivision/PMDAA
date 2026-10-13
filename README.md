# PMDAA — Planning + Management Directed Ambition Agent

An agent skill that **plans** projects and then **keeps a portfolio of them on track** across sessions: where each project
is (checked live against git and CI, not remembered), what blocks it, and the next action.

- **Plan mode** is [P-DADA](https://github.com/PrometheusIntelligence/p-dada) unchanged: planning anchor graph, living Frontier,
  independent critic panel, five artifacts in `PLANNING-LOG.md`.
- **Manage mode** keeps a machine-readable `PORTFOLIO.yaml` ledger (north star, milestone + exit test, RAG with evidence, RAID
  log, next 3 actions, owner, last-verified, dependencies) and runs a **resume protocol** every session:
  read ledger → live-check git/CI → mark stale claims → pick the next action (critical path, WIP limit) → update the ledger.

Lineage: [DADA](https://github.com/AnEntrypoint/dada) (design) → P-DADA (planning) → PMDAA (planning + management).

## Install

```sh
npx skills add ThothDivision/PMDAA -s pmdaa
```

Or symlink `skills/pmdaa` into your agent's skills folder. `skills/p-dada` is kept as the upstream planning skill so this fork
can keep pulling from P-DADA; `pmdaa` carries verbatim copies of its graphs (CI fails if they drift).

## Use

```text
$pmdaa resume the autheo portfolio: live-check every project, flag stale status, pick the next action
$pmdaa plan M2 for project X (Plan mode = P-DADA)
```

The ledger tool (Python 3 + PyYAML; `refresh` needs the GitHub CLI):

```sh
P=skills/pmdaa/scripts/portfolio.py
python3 $P refresh PORTFOLIO.yaml   # live: visibility, HEAD, CI on HEAD per project (gh, or $GH)
python3 $P check   PORTFOLIO.yaml   # errors (broken ledger) + warnings (STALE, STALE CLAIM, UNVERIFIED, WIP)
python3 $P check   PORTFOLIO.yaml --public   # a private project may carry name + one line only
python3 $P board   PORTFOLIO.yaml   # BOARD.md, board.html, status/<id>.md
```

Worked example (public-safe): [examples/autheo](examples/autheo/BOARD.md). Format: [ledger-format.md](skills/pmdaa/references/ledger-format.md).
Contract: [skills/pmdaa/SKILL.md](skills/pmdaa/SKILL.md). Graphs: [management](skills/pmdaa/references/management-graph.md),
[planning](skills/pmdaa/references/planning-graph.md).

## Validation

`python3 scripts/validate_skills.py && python3 -m unittest discover -s tests` (PyYAML). CI runs both plus the example ledger check.

The site in `web/` is DADA's original design page, kept as the design reference for plan sites.

Credit: DADA by AnEntrypoint · P-DADA by PrometheusIntelligence · PMDAA by ThothDivision / SolutionsAsService · Pimp My Skill
