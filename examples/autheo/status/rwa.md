# Autheo RWA stack (TaaS + DEX) — STATUS

- Repo: public: ThothDivision/autheo-taas-plan, private: ThothDivision/autheo-real-dex (public)
- North star: Pick an asset and a chain, Autheo handles the rest: issuance rules, compliance, DvP settlement and routing, non-custodial; every step an MCP tool.
- State / RAG: doing / green — Plan site rebuilt and deployed (taas-plan, DEX plan merged into dex/); build progress tracked privately.
- Milestone: M0-V Discovery (business, beside M0)
- Exit test: Signed LOIs from one cash-leg bank, one issuer and one market maker/buy-side (R-01, R-05); 5-person console usability test logged; D-02, D-03, D-09 decided.
- Evidence (claimed): {'public': {'head': '7503f6b', 'links': ['https://thothdivision.github.io/autheo-taas-plan/', 'https://thothdivision.github.io/autheo-taas-plan/dex/'], 'ci': 'success'}}
- Live: {'public': {'visibility': 'public', 'head': '7503f6bb2fce', 'head_date': '2026-10-13T22:43:34Z', 'head_subject': 'DEX plan now lives in dex/; private dev repo referenced by a one-liner only', 'ci': 'success', 'ci_url': 'https://github.com/ThothDivision/autheo-taas-plan/actions/runs/38479721308', 'checked': '2026-10-13T22:55:23+00:00'}}
- Owner: SolutionsAsService · last verified 2026-10-13
- Depends on: -

## Next actions
1. Record agent trading under mandates (DEX phase 3) as an explicit dependency on agent-env Phase C in DEX-INTEGRATION.md (todo)
2. Turn phase gates into exit tests (threshold + who runs it) (todo)

## Blockers
- none

## RAID log
- **R** M0-V discovery (LOIs, usability) is business work with no owner date; M1 is gated on it. (owner Head of BD)

## Decisions
- D-04 licensing map (proposed)
- D-11 freeze override and appeal authority (proposed)
- 2026-10-13 one project, one repo pair: autheo-dex-plan merged into autheo-taas-plan/dex (archived); TAAS-DEX merged into the private build repo (archived)
