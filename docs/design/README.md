# Design documents

Forward-looking specs for features that ship in v1.1+. The API contract is committed now so consumers can prepare; implementation lands in the version listed in each doc.

| Doc | Topic | First-ship version |
|---|---|---|
| [`skill-load-telemetry.md`](./skill-load-telemetry.md) | Opt-in HTTP beacon when a Claude Code agent loads a skill. Privacy-preserving by design. | v1.1 (endpoint), v2.0 (router ranking) |
| [`cross-collection-global-tools.md`](./cross-collection-global-tools.md) | Repo-root `tools/` ledger replacing the per-collection layout. One canonical IRI per tool across all collections. | v1.1 (transition), v2.0 (legacy removed) |
| [`cross-paper-citation-graph.md`](./cross-paper-citation-graph.md) | `cite_graph.json` per collection; references / cited-by surface in `paper.html`. Populated by Perspicacité MCP. | v1.1 (data), v1.2 (UI), v2.0 (graph view) |

All three are tracked as P1 (deferred to v1.1+); none block the v1 release. They were brainstormed during the 2026-05-25 hardening sprint.

## See also

- `governance/OPEN_ACCESS_POLICY.md` — content policy for source papers.
- `.github/CONTRIBUTING.md` — pipeline + budget-tier model.
- `governance/RELEASE_ROLLBACK.md` — what happens when a release needs to be withdrawn.
