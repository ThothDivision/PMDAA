# Autheo Agent Environment — STATUS

- Repo: SolutionsAsService/autheo-agent-environment (public)
- North star: Anyone can give an agent bounded authority and anyone can verify what it did, offline, without a registry.
- State / RAG: doing / green — 'Reference environment checks' success on 2adb938 (0.6.0: dex.* scopes, budget assets, venue decision vectors, @autheo/did JS package).
- Milestone: Phase A Contracts and product decisions (docs/ROADMAP.md)
- Exit test: Responsible platform owners approve versioned contracts (identity/credential, Dev Portal, Marketplace, L1); unknowns explicit, no guessed endpoints or DID semantics.
- Evidence (claimed): {'head': '2adb938', 'ci': 'success', 'links': ['https://github.com/SolutionsAsService/autheo-agent-environment/actions/runs/38476638470', 'https://solutionsasservice.github.io/autheo-agent-environment-site/']}
- Live: {'visibility': 'public', 'head': '2adb938ba310', 'head_date': '2026-10-13T22:16:15Z', 'head_subject': 'feat(venue): 0.6.0 dex.* scopes, budget assets, venue decision vectors, @autheo/did JS package', 'ci': 'success', 'ci_url': 'https://github.com/SolutionsAsService/autheo-agent-environment/actions/runs/38476638470', 'checked': '2026-10-13T22:26:39+00:00'}
- Owner: SolutionsAsService · last verified 2026-10-13
- Depends on: -

## Next actions
1. DEX interop: agent-env side landed in 0.6.0 (dex.* scopes); DEX side in progress (sibling subagent). Verify end to end: mandate -> unsigned order -> human signature -> receipt hash in audit chain (doing)
2. Approval object bound to one request digest so 'escalate' resolves to a human signature (Phase 0.2 next increment, Phase C prerequisite) (todo)
3. Phase A: write the contract list and owner questions for Autheo identity/L1 and get one owner sign-off (todo)

## Blockers
- none

## RAID log
- **R** Revocation freshness not guaranteed; mandates must stay short-lived until an anchored revocation list exists. (owner SolutionsAsService)
- **A** Autheo identity will accept did:key / VC 2.0 chains; not confirmed by platform owners (Phase A). (owner SolutionsAsService)
- **R** 0.6.0 defines a dex.order.sign scope; the public plan says the agent never signs. Confirm the scope cannot let an agent key sign an order (or rename it). (owner SolutionsAsService)

## Decisions
- docs/EXISTING-SOLUTIONS.md: W3C VC 2.0 + Data Integrity eddsa-jcs-2022, did:key
- Agents never hold signing authority over funds (environment simulates; nothing executes)
