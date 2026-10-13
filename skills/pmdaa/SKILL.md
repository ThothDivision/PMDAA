---
name: pmdaa
description: "PMDAA (Planning + Management Directed Ambition Agent). Use when asked to plan a project AND/OR keep a portfolio of projects on track across sessions: where is each project, what is blocked, what is next, is the status still true. Plan mode is P-DADA unchanged (planning anchor graph, living Frontier, critic panel, PLANNING-LOG.md). Manage mode keeps a machine-readable PORTFOLIO.yaml ledger (north star, milestone with exit test, RAG with evidence, RAID log, next 3 actions, owner, last-verified, dependencies), live-checks git HEAD, CI and visibility via gh, marks stale claims, picks the next action by critical path and WIP limit, and renders a status board. Every session starts with the resume protocol and ends by updating the ledger."
---

# PMDAA: Planning + Management Directed Ambition Agent

P-DADA plans one thing well and then forgets it. PMDAA keeps the plan **and** the portfolio: what each project is for, where
it actually is (checked live, not remembered), what blocks it, and the next action. The ledger is the agent's memory across
sessions; the repo and CI are the truth the ledger is checked against.

## Contract (read first)

| Mode | Use when | Output (required) |
|---|---|---|
| **Plan** | Create, flesh out or review a plan, roadmap or planning site | The full P-DADA contract in [references/plan-mode.md](references/plan-mode.md): five artifacts in `PLANNING-LOG.md` |
| **Manage** | "Where are we", "what's next", "keep X on track", any session that touches a project in a ledger | Refreshed `PORTFOLIO.yaml`, rendered board, one entry in `SESSION-LOG.md` beside the ledger |

A session can do both: Manage picks the next action; if that action is "plan M2", run Plan mode for it, then return and record
the outcome in the ledger. Never report a project's status from memory or from the ledger alone; report what the live check showed.

The checker and board renderer is `scripts/portfolio.py` in this skill folder (Python 3 + PyYAML; `refresh` needs `gh` or `$GH`).

## Resume protocol (every session that touches a portfolio)

1. **Read the ledger.** Find `PORTFOLIO.yaml` (path given by the user, a memory note, or `portfolio/<name>/` in the workspace).
   Read north star, WIP limit, every project's milestone, blockers and next actions, and the last `SESSION-LOG.md` entry.
2. **Live-check.** `python3 scripts/portfolio.py refresh PORTFOLIO.yaml` writes `live:` per project: visibility, HEAD, HEAD
   date, CI result on HEAD. Local clones: also `git -C <local> status --short` (uncommitted work is a claim nobody can see).
3. **Mark stale claims.** `python3 scripts/portfolio.py check PORTFOLIO.yaml`. Treat every warning as a question:
   - `STALE CLAIM` (repo moved since `evidence.head`): read the commits since, re-run the exit test if cheap, then update `evidence` and RAG, or set RAG amber with "unverified since <sha>".
   - `UNVERIFIED` (green with failing CI): pull the Andon cord: RAG red until CI is green again or the failure is explained.
   - `STALE` (not verified in N days): verify, or say so on the board.
   - A visibility mismatch is an **error**: stop and fix it before anything is published.
4. **Pick the next action**, in this order: Andon (red CI on the critical path) → blocked project on the critical path →
   stale claim on the critical path → first open next action of a `doing` project on the critical path → other `doing` projects
   by cost of delay. Do not move a backlog project to `doing` while `doing` ≥ `wip_limit`; finish or pause one first.
5. **Do the work** (Plan mode if it is planning). Work owned by another agent or person stays theirs: record it as
   `status: doing` with its owner rather than taking it over.
6. **Close the session.** Update the ledger: `evidence.head` = the HEAD you verified, `last_verified` = today, RAG + evidence,
   next actions (max 3, done ones removed), blockers, RAID, decisions. Run `check` (0 errors) and `board`. Append to
   `SESSION-LOG.md`: date, what was verified (SHAs, CI links), flags found, action taken, what changed in the ledger, and the
   first action for the next session. Commit the ledger if it lives in a repo.

## Ledger (`PORTFOLIO.yaml`)

Format, field rules and the public-safety rule: [references/ledger-format.md](references/ledger-format.md). A worked public
example lives in the PMDAA repo's `examples/` folder. Per-project `status/<id>.md` files are rendered from the ledger, never
edited by hand: one source of truth.

## Management graph

Anchors, edges and counterpoints for Manage mode: [references/management-graph.md](references/management-graph.md). Each ledger
field exists because an anchor demands it; when a project resists the ledger (research, a partnership, hardware), consult the
dotted counterpoints before forcing it into a milestone.

## Manage-mode measurements (print the counts in the session log)

- **Evidence audit**: projects whose RAG cites a commit, CI run, exit-test result or document vs. projects whose RAG is opinion.
- **Freshness**: projects verified this session / within `--stale-days` / stale; stale claims found and resolved.
- **Flow**: projects `doing` vs. WIP limit; blocked count; next actions closed since the last session.
- **Exit-test audit**: every current milestone has an exit test a stranger could run (the checker enforces presence; you judge quality).

## Anti-skip rules

- A status that was not live-checked this session is labelled with its last-verified date, never presented as current.
- Green needs evidence; evidence older than HEAD is a stale claim, not evidence.
- More than three next actions is a backlog, not a plan; move the rest to the milestone or the RAID log.
- A project is at most a pair: one public repo and one private repo (`repos: {public, private}`); in a public file the private repo is a name only.
- A private project in a public file gets its name and one line, nothing else (`check --public` enforces the fields; you check the words).
- If the ledger was not updated at the end of the session, the session did not happen as far as the next one is concerned.

## Graphs

- Planning: [references/planning-graph.md](references/planning-graph.md) (P-DADA, verbatim).
- Management: [references/management-graph.md](references/management-graph.md).
- Plan-site presentation: [references/design-graph.md](references/design-graph.md) (DADA, verbatim).
