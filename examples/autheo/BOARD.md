# autheo portfolio board

**North star:** Pick an asset and a chain, and Autheo handles the rest: real-world assets issued, traded and settled non-custodially, with agents that can act only inside signed mandates and leave verifiable receipts.

Rendered 2026-10-13 · WIP limit 4 · critical path: taas-plan → dex-plan → real-dex

| Project | State | RAG | Milestone | Exit test | Live HEAD / CI | Next action | Verified |
|---|---|---|---|---|---|---|---|
| Autheo RWA stack build (real-dex) | doing | green | Non-custodial RWA stack build (tokenization + DEX + interop); M0 walking skeleton in progress. |  |  |  |  |
| Autheo Agent Environment | doing | green | Phase A | Responsible platform owners approve versioned contracts (identity/credential, Dev Portal, Marketplace, L1); unknowns explicit, no guessed endpoints or DID semantics. | 2adb938 success | DEX interop: agent-env side landed in 0.6.0 (dex.* scopes); DEX side in progress (sibling subagent). Verify end to end: mandate -> unsigned order -> human signature -> receipt hash in audit chain | 2026-10-13 |
| Autheo Stack (ecosystem map and plan of record) | doing | amber | S1 | Page renders at 390px and 1440px with no horizontal overflow; every roadmap stage has an exit test and a stop-if; PLANNING-LOG.md has the five P-DADA artifacts; no private-repo internals; all outbound links 200. | 7cb7e63 none | Add a CI job: link check + HTML parse on push (so the page can go green on evidence) | 2026-10-13 |
| Autheo TaaS plan | doing | green | M0-V | Signed LOIs from one cash-leg bank, one issuer and one market maker/buy-side (R-01, R-05); 5-person console usability test logged; D-02, D-03, D-09 decided. | c5e3a0b success | Commit or discard the uncommitted local index.html edit (3 lines) after checking who owns it | 2026-10-13 |
| Autheo DEX plan | doing | amber | Phase 0 | Market-structure spec, policy-hook interface shared with TaaS, settlement contract design and intent format reviewed with counsel and a venue partner (review notes linked). | 1e0fffa success | Sync with taas-plan c5e3a0b: Autheo DEX is one venue; router interoperates with external DEXs and aggregators | 2026-10-13 |
| TAAS-DEX (dev repo placeholder) | blocked | amber | README-only development repo; the build is happening in autheo-real-dex. |  |  |  |  |
| Autheo AssetTrack (+ ATN-01 node) | doing | amber | Custody-aware asset tracking concept (reefer pilot) with the ATN-01 v1.2 truck RF node concept CAD. |  |  |  |  |
| Autheo NFC Wallet | doing | amber | Hardware wallet (NFC/RFID) docs + firmware; v1.1 original-vision enclosure. |  |  |  |  |
| military-display (3D design-review viewer) | doing | green | Private design-review viewer hosting the Wallet and ATN-01 3D studies. |  |  |  |  |

## Flags
- portfolio: WIP 8 > limit 4; finish or pause before starting more
