# Modes

*Status: v0. The roster and the `--terminal` / `--json` flags are implemented in `scripts/portfolio.py`; the
mode definitions below are the design a session follows. They are presets, not a new contract — a mode changes
which anchors a session leans on, who sits on the critic panel, and what artifact it must leave behind. It does
not replace Plan mode or Manage mode.*

## Why modes exist

One portfolio has several kinds of session in it: decide where the whole thing goes, learn how a domain does
something before committing, explain a decision to a human, grind out a milestone. All four read the same ledger
but none should behave the same way. Naming the mode up front stops a session from drifting — doing research
while pretending to plan, or teaching while pretending to decide.

## Selecting a mode

Say it in the invocation, or set it on the agent in the ledger:

```text
$pmdaa --mode=researcher how do Cosmos chains normally close an IBC mint path?
$pmdaa --mode=general where should autheo go next quarter?
$pmdaa --mode=teaching explain why the inherited voucher denom mattered
```

```yaml
agents:
  - {id: secbot, role: researcher, mode: researcher}
```

A session that does not name a mode is **manage** (the resume protocol, unchanged).

## The modes

| Mode | Use when | Governing criterion | Required artifact | Panel |
|---|---|---|---|---|
| **manage** (default) | "Where are we", "what's next", any session that touches a project | Status is true: every claim live-checked this session | Refreshed `PORTFOLIO.yaml` + `SESSION-LOG.md` entry | none (the checker is the critic) |
| **general** | Deciding where the portfolio or a project goes: sequencing, cut/keep, make-vs-buy, what stops now | Rumelt's kernel of good strategy: a diagnosis, a guiding policy, and coherent actions that follow from both | Decision records with options, a recommendation, an owner and a decide-by; the ledger updated to match | Rumelt (*Good Strategy/Bad Strategy*), Klein (premortem, *Sources of Power*), plus one seat for whoever the plan leaves out |
| **researcher** | Learning best practice or prior art before committing: how others solved X, what the incidents say, what the standard is | Sourced: every claim carries a primary source that was actually fetched and read, or is marked UNVERIFIED | A findings note with a source per claim and an explicit excluded/UNVERIFIED list | One adversarial reader whose only job is to find unsourced claims |
| **teaching** | Explaining a domain or a decision to a human | The human can act on it without asking a follow-up | Nothing durable — the explanation is the deliverable; do not "leave a record" by inventing one | none |
| **vision** | A plan read by people deciding whether to back, join or partner | Kernel of good strategy, and every checkable claim is true or labelled | P-DADA's five artifacts in `PLANNING-LOG.md` | P-DADA Vision composition |
| **execution** | A plan read by people who build it | Buildable and testable: every milestone has an exit test a stranger could run | P-DADA's five artifacts in `PLANNING-LOG.md` | P-DADA Execution composition |

`vision` and `execution` are the two presets Plan mode already had; they are listed here so one table holds
every mode. See [plan-mode.md](plan-mode.md) for their full contract.

## What a mode must not do

- **teaching must not plan.** It explains; it does not commit a decision or edit the ledger. If an explanation
  surfaces a decision, name it and switch modes.
- **researcher must not decide.** It returns findings with sources and an explicit UNVERIFIED list. Turning
  findings into a decision is a **general** or Plan-mode move, with a decision record.
- **general must not hide behind research.** A strategy session that ends with "we need to look into it" has not
  produced a guiding policy. Either decide, or set a decide-by and an owner.
- **Any mode may read the ledger; only manage, general and the planning modes may write it.** A researcher or a
  teacher that changes RAG has overstepped.

## Measurements (print them in the session log)

- **general**: decisions with options + recommendation + owner + decide-by, vs open questions; projects moved
  between states and why.
- **researcher**: claims sourced to a primary source actually read, vs marked UNVERIFIED or excluded.
- **teaching**: no artifact is required; if one was produced anyway, say so and why.

## Open (v0)

- Modes are a convention the session follows, not yet enforced by the tool. `portfolio.py` does not read
  `mode:`; it is documentation for the agent and a label on the roster.
- No `watch` mode yet: re-refresh and reprint the terminal board on an interval.
- The eventual orchestrator MCP should read the roster and dispatch work per mode; until then `agent:` is a
  label, not a dispatch.
