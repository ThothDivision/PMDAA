# P-DADA project

Planning fork of DADA (AnEntrypoint/dada). The distributable skill lives in `skills/p-dada/`; `.agents/skills/p-dada` links to it.
`references/planning-graph.md` is the planning anchor graph; `references/design-graph.md` is DADA's design graph, kept verbatim for
presenting plan sites. Keep the frontmatter name, folder name and `agents/openai.yaml` consistent with `p-dada`.

Keep DADA's traversal contract (living Frontier, no move quota, WHOLE rounds, S1–S5, one subagent per literary reference, overrules
named in the object's own units). Planning measurements are claim, decision, exit-test and consistency audits plus a site build.
Validate with `python3 scripts/validate_skills.py`. Do not publish credentials or machine configuration. Planning logs live with the
plan they describe, not in this repo.
