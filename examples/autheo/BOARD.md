# autheo portfolio board

**North star:** Pick an asset and a chain, and Autheo handles the rest: real-world assets issued, traded and settled non-custodially, with agents that can act only inside signed mandates and leave verifiable receipts.

Rendered 2026-10-13 · WIP limit 4 · critical path: agent-env → asset-track → viewer

| Project | State | RAG | Milestone | Exit test | Live HEAD / CI | Next action | Verified |
|---|---|---|---|---|---|---|---|
| Autheo RWA stack (TaaS + DEX) | doing | green | M0-V | Signed LOIs from one cash-leg bank, one issuer and one market maker/buy-side (R-01, R-05); 5-person console usability test logged; D-02, D-03, D-09 decided. | public 7503f6b success | Record agent trading under mandates (DEX phase 3) as an explicit dependency on agent-env Phase C in DEX-INTEGRATION.md | 2026-10-13 |
| Autheo Agent Environment | doing | green | Phase A | Responsible platform owners approve versioned contracts (identity/credential, Dev Portal, Marketplace, L1); unknowns explicit, no guessed endpoints or DID semantics. | 7f3d981 success | DEX interop end to end: mandate -> unsigned order -> human signature -> receipt hash in audit chain (DEX side landed in the private build at 53caf04; pin 0.7.0 at 27c34c9) | 2026-10-13 |
| Autheo Stack (ecosystem map and plan of record) | doing | amber | S1 | Page renders at 390px and 1440px with no horizontal overflow; every roadmap stage has an exit test and a stop-if; PLANNING-LOG.md has the five P-DADA artifacts; no private-repo internals; all outbound links 200. | 7cb7e63 none | Add a CI job: link check + HTML parse on push (so the page can go green on evidence) | 2026-10-13 |
| Autheo AssetTrack (+ ATN-01 node) | doing | amber | Custody-aware asset tracking (reefer pilot): concept, ATN-01 v1.2 truck RF node CAD and a custody web app. |  |  |  |  |
| Autheo NFC Wallet | doing | amber | Hardware wallet (NFC/RFID) docs + firmware; v1.1 original-vision enclosure. |  |  |  |  |
| military-display (3D design-review viewer) | doing | green | Private design-review viewer hosting the Wallet and ATN-01 3D studies. |  |  |  |  |

## Flags
- portfolio: WIP 6 > limit 4; finish or pause before starting more
