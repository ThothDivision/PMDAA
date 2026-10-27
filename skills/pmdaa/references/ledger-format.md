# Ledger format

One YAML file per portfolio, `PORTFOLIO.yaml`. `scripts/portfolio.py check` enforces the rules marked **(checked)**.

```yaml
portfolio: autheo                  # (checked) name
north_star: "One sentence: the outcome all projects serve"   # (checked) OKR objective / north star
wip_limit: 3                       # (checked) max projects in state 'doing'; over the limit is a warning
public: false                      # true = public-safe ledger; same as --public
updated: 2026-10-13
agents:                            # optional roster; a project's `agent` must name one of these ids
  - {id: challe, role: orchestrator, mode: general, note: "what this agent is for"}
projects:
  - id: dex                        # (checked) unique; used by depends_on
    name: Autheo DEX
    repo: owner/name               # optional; enables refresh. Or a pair (not both):
    # repos: {public: owner/plan, private: owner/build}   # (checked) see Pairs
    local: /path/to/clone          # optional; for git status
    visibility: public             # (checked) public | private; must match GitHub after refresh
    one_line: "Short status a stranger may read"
    north_star: "What this project is for"
    state: doing                   # (checked) backlog | doing | blocked | done  (kanban column)
    rag: amber                     # (checked) green | amber | red
    rag_evidence: "The CI run, exit-test result or link that justifies the colour"   # (checked) non-empty
    milestone:
      id: M0
      name: Walking skeleton
      exit_test: "A test a stranger could run, with a threshold"   # (checked) non-empty
      decide_by: 2026-11-01        # optional
    evidence:                      # what the last session verified (claimed)
      head: eecb377                # STALE CLAIM if live.head has moved past it
      ci: success
      links: [https://example.org/run/1]
    live: {}                       # written by refresh: visibility, head, head_date, head_subject, ci, ci_url, checked
    blockers: []                   # (checked) required when state is blocked
    next_actions:                  # (checked) 1..3 when open
      - {action: "The concrete next thing", owner: agent, status: todo}   # status: todo | doing | done
    owner: SolutionsAsService      # single-threaded owner
    agent: challe                  # optional; which agent/role is on it now (warned if absent from the roster)
    last_verified: 2026-10-13      # (checked) STALE after --stale-days
    depends_on: [other-id]         # (checked) ids exist, no cycles; drives the critical path
    raid:                          # risks, assumptions, issues, dependencies
      - {type: R, text: "...", owner: someone, trigger: "..."}
    decisions: ["ADR link, or a one-line decision with its date"]
```

## Rules

- **Claimed vs. live.** `evidence` is what the last session verified; `live` is what GitHub says now. They are never merged
  automatically: an agent looks at what changed and decides.
- **CI on HEAD** = the runs for the HEAD commit: all success = `success`, any still running = `pending`, any other conclusion =
  `failure`, no runs = `none` (a repo with no CI cannot be green on CI alone; cite another check).
- **Critical path** = the longest `depends_on` chain of open projects (one unit per project; no durations are claimed).
- **Public-safe.** In a public ledger (`public: true` or `--public`) a private project may carry only `id`, `name`,
  `visibility`, `one_line`, `rag`, `state` and `depends_on`. Keep the full ledger private and derive the public one from it.
- **Pairs.** A project has at most two repos: one public (docs, specs, public-safe code) and one private (internals):
  `repos: {public: owner/name, private: owner/name}`. `refresh` checks both and writes `live: {public: {...}, private: {...}}`;
  `evidence` is per side too (`evidence: {public: {head: ...}}`). Each side must match its GitHub visibility. The project is
  `public` when it has a public repo. In a public ledger the private repo is a **name only**: `refresh` skips it, `check
  --public` prints just its name, and `live.private` / `evidence.private` are errors. The old single `repo` keeps working.
- **Agents.** `agents:` is an optional roster of `{id, role, mode, note}`; a project's `agent:` must name one of
  its ids, or `-` for unassigned. `owner` is the human who answers for the project and stays single-threaded;
  `agent` is who is on it now and may change between sessions. An unknown id is a warning, not an error, so
  adding an agent to a project before adding it to the roster does not break the ledger.
- **Comments.** `refresh` rewrites the file, which drops YAML comments; keep notes in fields.

## Board

`portfolio.py board PORTFOLIO.yaml [--out DIR]` writes `BOARD.md`, `board.html` (static, no scripts) and
`status/<id>.md` per project, with the checker's flags at the bottom of the board.

`board --terminal` prints the board to the terminal instead of writing files — the local "where is every
project" view, with an Agent column and RAG in colour (plain text when piped or under `NO_COLOR`).
`check --json` or `board --json` emit the same status as JSON, for a TUI or dashboard to consume.
