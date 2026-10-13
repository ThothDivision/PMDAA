#!/usr/bin/env python3
"""PMDAA portfolio ledger: check, live-refresh (gh) and render a status board.

  python3 portfolio.py check   PORTFOLIO.yaml [--public] [--stale-days 7]
  python3 portfolio.py refresh PORTFOLIO.yaml           # writes live: {visibility, head, ci, ...} per project via gh
  python3 portfolio.py board   PORTFOLIO.yaml [--out DIR] # BOARD.md, board.html, status/<id>.md

Needs PyYAML. 'refresh' needs the GitHub CLI ('gh', or the path in $GH). Exit code 1 on ledger errors.
"""
import argparse, datetime as dt, html, json, os, subprocess, sys
from pathlib import Path
import yaml

RAG = {"green", "amber", "red"}
STATES = {"backlog", "doing", "blocked", "done"}  # kanban columns
REQUIRED = ["id", "name", "visibility", "north_star", "state", "rag", "rag_evidence", "milestone", "next_actions", "owner", "last_verified"]
PUBLIC_PRIVATE_KEYS = {"id", "name", "visibility", "one_line", "rag", "state", "depends_on"}  # all a public ledger may say about a private project
CHIP = {"green": "#1f7a45", "amber": "#9a6700", "red": "#b42318"}


def as_date(v):
    return v if isinstance(v, dt.date) else dt.date.fromisoformat(str(v)[:10])


def critical_path(projects):
    """Longest chain of open projects along depends_on (one unit per project; no durations are claimed)."""
    by_id = {p["id"]: p for p in projects}
    memo = {}

    def chain(pid, seen=()):
        if pid in seen:
            raise ValueError(f"dependency cycle through {pid}")
        if pid not in memo:
            deps = [d for d in by_id[pid].get("depends_on", []) if d in by_id and by_id[d].get("state") != "done"]
            memo[pid] = max((chain(d, seen + (pid,)) for d in deps), key=len, default=[]) + [pid]
        return memo[pid]

    return max((chain(p["id"]) for p in projects if p.get("state") != "done"), key=len, default=[])


def check(ledger, public=False, stale_days=7, now=None):
    """Return (errors, warnings). Errors break the ledger; warnings are stale or unverified claims."""
    now = now or dt.date.today()
    errors, warnings = [], []
    projects = ledger.get("projects") or []
    for key in ("portfolio", "north_star", "wip_limit", "projects"):
        if key not in ledger:
            errors.append(f"portfolio: missing '{key}'")
    ids = [p.get("id") for p in projects]
    if len(ids) != len(set(ids)):
        errors.append("portfolio: duplicate project ids")
    for p in projects:
        pid = p.get("id", "?")
        if p.get("visibility") not in ("public", "private"):
            errors.append(f"{pid}: visibility must be public or private")
        for d in p.get("depends_on", []):
            if d not in ids:
                errors.append(f"{pid}: depends_on unknown project '{d}'")
        if public and p.get("visibility") == "private":
            extra = set(p) - PUBLIC_PRIVATE_KEYS
            if extra:
                errors.append(f"{pid}: private project in a public ledger may only carry {sorted(PUBLIC_PRIVATE_KEYS)}; remove {sorted(extra)}")
            continue
        missing = [k for k in REQUIRED if k not in p]
        if missing:
            errors.append(f"{pid}: missing {missing}")
            continue
        if p["rag"] not in RAG:
            errors.append(f"{pid}: rag must be one of {sorted(RAG)}")
        if p["state"] not in STATES:
            errors.append(f"{pid}: state must be one of {sorted(STATES)}")
        if not p["rag_evidence"]:
            errors.append(f"{pid}: a RAG status needs evidence")
        if not (p["milestone"] or {}).get("exit_test"):
            errors.append(f"{pid}: current milestone needs an exit test (a milestone without one is a wish)")
        actions = p["next_actions"] or []
        if p["state"] != "done" and not actions:
            errors.append(f"{pid}: an open project needs a next action")
        if len(actions) > 3:
            errors.append(f"{pid}: at most 3 next actions ({len(actions)})")
        if p["state"] == "blocked" and not p.get("blockers"):
            errors.append(f"{pid}: state blocked but no blockers listed")
        age = (now - as_date(p["last_verified"])).days
        if age > stale_days:
            warnings.append(f"{pid}: STALE, last verified {age} days ago")
        live, claimed = p.get("live") or {}, p.get("evidence") or {}
        if live.get("error"):
            warnings.append(f"{pid}: live check failed: {live['error']}")
        if live.get("visibility") and live["visibility"] != p["visibility"]:
            errors.append(f"{pid}: ledger says {p['visibility']} but GitHub says {live['visibility']}")
        if live.get("head") and claimed.get("head") and not live["head"].startswith(str(claimed["head"])):
            warnings.append(f"{pid}: STALE CLAIM, repo moved {claimed['head']} -> {live['head'][:7]} since the status was verified")
        if p["rag"] == "green" and live.get("ci") == "failure":
            warnings.append(f"{pid}: UNVERIFIED, RAG green but CI on HEAD failed")
    doing = sum(1 for p in projects if p.get("state") == "doing")
    if isinstance(ledger.get("wip_limit"), int) and doing > ledger["wip_limit"]:
        warnings.append(f"portfolio: WIP {doing} > limit {ledger['wip_limit']}; finish or pause before starting more")
    if not errors:
        try:
            critical_path(projects)
        except ValueError as e:
            errors.append(f"portfolio: {e}")
    return errors, warnings


def gh(*args):
    out = subprocess.run([os.environ.get("GH", "gh"), *args], capture_output=True, text=True, timeout=60)
    if out.returncode:
        raise RuntimeError(out.stderr.strip() or f"gh {args[0]} failed")
    return json.loads(out.stdout)


def ci_summary(runs):
    if not runs:
        return "none"
    if any(r["status"] != "completed" for r in runs):
        return "pending"
    return "failure" if any(r["conclusion"] not in ("success", "skipped", "neutral") for r in runs) else "success"


def refresh(ledger, now=None):
    now = (now or dt.datetime.now(dt.timezone.utc)).isoformat(timespec="seconds")
    for p in ledger.get("projects", []):
        if not p.get("repo"):
            continue
        try:
            meta = gh("repo", "view", p["repo"], "--json", "visibility,defaultBranchRef")
            commit = gh("api", f"repos/{p['repo']}/commits/{meta['defaultBranchRef']['name']}")
            runs = gh("run", "list", "-R", p["repo"], "--commit", commit["sha"], "-L", "20", "--json", "status,conclusion,url,workflowName")
            p["live"] = {"visibility": meta["visibility"].lower(), "head": commit["sha"][:12],
                         "head_date": commit["commit"]["committer"]["date"],
                         "head_subject": commit["commit"]["message"].splitlines()[0][:100],
                         "ci": ci_summary(runs), "ci_url": runs[0]["url"] if runs else None, "checked": now}
        except Exception as e:  # keep going: an unreachable repo is itself a status
            p["live"] = {"error": str(e)[:200], "checked": now}
    return ledger


def status_md(p):
    ms, live, ev = p.get("milestone") or {}, p.get("live") or {}, p.get("evidence") or {}
    lines = [f"# {p['name']} — STATUS", "", f"- Repo: {p.get('repo', '-')} ({p['visibility']})", f"- North star: {p['north_star']}",
             f"- State / RAG: {p['state']} / {p['rag']} — {p['rag_evidence']}",
             f"- Milestone: {ms.get('id', '')} {ms.get('name', '')}", f"- Exit test: {ms.get('exit_test', '')}",
             f"- Evidence (claimed): {ev or '-'}", f"- Live: {live or '-'}", f"- Owner: {p['owner']} · last verified {p['last_verified']}",
             f"- Depends on: {', '.join(p.get('depends_on', [])) or '-'}", "", "## Next actions"]
    lines += [f"{i}. {a['action']} ({a.get('status', 'todo')})" if isinstance(a, dict) else f"{i}. {a}" for i, a in enumerate(p["next_actions"], 1)]
    lines += ["", "## Blockers", *([f"- {b}" for b in p.get("blockers", [])] or ["- none"]), "", "## RAID log"]
    lines += [f"- **{r.get('type', '?')}** {r.get('text', '')} (owner {r.get('owner', '-')})" for r in p.get("raid", [])] or ["- none"]
    lines += ["", "## Decisions", *([f"- {d}" for d in p.get("decisions", [])] or ["- none"])]
    return "\n".join(lines) + "\n"


def render(ledger, out):
    out = Path(out)
    (out / "status").mkdir(parents=True, exist_ok=True)
    projects = ledger.get("projects", [])
    errors, warnings = check(ledger, public=ledger.get("public", False))
    path = " → ".join(critical_path(projects)) if not errors else "n/a (fix errors)"
    head = ["Project", "State", "RAG", "Milestone", "Exit test", "Live HEAD / CI", "Next action", "Verified"]
    rows = []
    for p in projects:
        live, ms = p.get("live") or {}, p.get("milestone") or {}
        nxt = (p.get("next_actions") or [""])[0]
        rows.append([p.get("name", p["id"]), p.get("state", ""), p.get("rag", ""), ms.get("id", "") or p.get("one_line", ""),
                     ms.get("exit_test", ""), f"{str(live.get('head', ''))[:7]} {live.get('ci', '')}".strip(),
                     nxt.get("action", "") if isinstance(nxt, dict) else nxt, str(p.get("last_verified", ""))])
        if "milestone" in p:
            (out / "status" / f"{p['id']}.md").write_text(status_md(p), encoding="utf-8")
    flags = errors + warnings or ["none"]
    meta = f"Rendered {dt.date.today()} · WIP limit {ledger.get('wip_limit')} · critical path: {path}"
    md = [f"# {ledger.get('portfolio')} portfolio board", "", f"**North star:** {ledger.get('north_star')}", "", meta, "",
          "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    md += ["| " + " | ".join(str(c).replace("|", "/") for c in r) + " |" for r in rows]
    md += ["", "## Flags", *[f"- {f}" for f in flags]]
    (out / "BOARD.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    e = html.escape
    cell = lambda i, c: f"<td><b style='background:{CHIP.get(c, '#555')}'>{e(c)}</b></td>" if i == 2 else f"<td>{e(str(c))}</td>"
    trs = "".join("<tr>" + "".join(cell(i, c) for i, c in enumerate(r)) + "</tr>" for r in rows)
    (out / "board.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(str(ledger.get('portfolio')))} portfolio board</title><style>body{{font:15px/1.45 system-ui,sans-serif;margin:2rem;color:#16181d}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ddd;padding:.45rem;text-align:left;vertical-align:top}}th{{background:#f3f1ea}}
b{{color:#fff;padding:.1rem .5rem;border-radius:1rem}}.wrap{{overflow-x:auto}}</style></head><body>
<h1>{e(str(ledger.get('portfolio')))} portfolio board</h1><p><strong>North star:</strong> {e(str(ledger.get('north_star')))}</p><p>{e(meta)}</p>
<div class="wrap"><table><tr>{''.join(f'<th>{h}</th>' for h in head)}</tr>{trs}</table></div>
<h2>Flags</h2><ul>{''.join(f'<li>{e(f)}</li>' for f in flags)}</ul></body></html>
""", encoding="utf-8")
    return errors, warnings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["check", "refresh", "board"])
    ap.add_argument("ledger")
    ap.add_argument("--public", action="store_true", help="enforce public-safe content for private projects")
    ap.add_argument("--stale-days", type=int, default=7)
    ap.add_argument("--out", help="board output dir (default: the ledger's dir)")
    a = ap.parse_args(argv)
    path = Path(a.ledger)
    ledger = yaml.safe_load(path.read_text(encoding="utf-8"))
    public = a.public or ledger.get("public", False)
    if a.command == "refresh":
        # shortcut: rewriting drops YAML comments; keep notes in fields, not comments.
        path.write_text(yaml.safe_dump(refresh(ledger), sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
    if a.command == "board":
        errors, warnings = render(ledger, a.out or path.parent)
    else:
        errors, warnings = check(ledger, public, a.stale_days)
    for f in errors:
        print("ERROR", f)
    for f in warnings:
        print("WARN ", f)
    print(f"{len(ledger.get('projects', []))} projects, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
