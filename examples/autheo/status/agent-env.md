# Autheo Agent Environment — STATUS

- Repo: SolutionsAsService/autheo-agent-environment (public)
- North star: Anyone can give an agent bounded authority and anyone can verify what it did, offline, without a registry.
- State / RAG: doing / green — 'Reference environment checks' success on 7f3d981 (0.7.0: dex.order.request_signature, dex.order.sign a deprecated alias; 265 pytest + JS vector checks).
- Milestone: Phase A Contracts and product decisions (docs/ROADMAP.md)
- Exit test: Responsible platform owners approve versioned contracts (identity/credential, Dev Portal, Marketplace, L1); unknowns explicit, no guessed endpoints or DID semantics.
- Evidence (claimed): {'head': '7f3d981', 'ci': 'success', 'links': ['https://github.com/SolutionsAsService/autheo-agent-environment/actions/runs/38480499870', 'https://solutionsasservice.github.io/autheo-agent-environment-site/']}
- Live: {'visibility': 'public', 'head': '7f3d981a6ae5', 'head_date': '2026-10-13T22:50:53Z', 'head_subject': 'feat(venue): 0.7.0 rename dex.order.sign -> dex.order.request_signature', 'ci': 'success', 'ci_url': 'https://github.com/SolutionsAsService/autheo-agent-environment/actions/runs/38480499870', 'checked': '2026-10-13T22:55:23+00:00'}
- Owner: SolutionsAsService · last verified 2026-10-13
- Depends on: -

## Next actions
1. DEX interop end to end: mandate -> unsigned order -> human signature -> receipt hash in audit chain (DEX side landed in the private build at 53caf04; pin 0.7.0 at 27c34c9) (todo)
2. Approval object bound to one request digest so 'escalate' resolves to a human signature (Phase 0.2 next increment, Phase C prerequisite) (todo)
3. Phase A: write the contract list and owner questions for Autheo identity/L1 and get one owner sign-off (todo)

## Blockers
- none

## RAID log
- **R** Revocation freshness not guaranteed; mandates must stay short-lived until an anchored revocation list exists. (owner SolutionsAsService)
- **A** Autheo identity will accept did:key / VC 2.0 chains; not confirmed by platform owners (Phase A). (owner SolutionsAsService)

## Decisions
- docs/EXISTING-SOLUTIONS.md: W3C VC 2.0 + Data Integrity eddsa-jcs-2022, did:key
- Agents never hold signing authority over funds (environment simulates; nothing executes)
- 2026-10-13 0.7.0: dex.order.sign -> dex.order.request_signature (alias accepted in 0.7, removed in 0.8); the agent never signs
