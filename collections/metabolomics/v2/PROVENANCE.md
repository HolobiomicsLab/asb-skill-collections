# Generation provenance — ASB Metabolomics v2

How this collection was generated, for traceability. Values are taken verbatim
from the per-build `build_manifest.json` (`cli_invocation` + `agents.*.model`)
emitted by the AgenticScienceBuilder (ASB) pipeline.

## Exact build command (per source paper / repo)

Each tool was built independently with the **same** invocation (only the build
spec, output dir, and per-paper KB differ):

```bash
python -m agentic_science_builder build <OWNER/REPO | git-URL> \
  --source-kind github \
  --github-repo <OWNER/REPO> \            # omitted for non-GitHub git hosts; full URL passed as the build spec instead
  --output outputs/asbb_pilot/coll_<slug>_cq \
  --llm --entity-spine --claim-ledger --classify --rich-cards \
  --emit-executable --skill-bundle --emit-challenge --emit-indicium \
  --enrich --no-pin \
  --ground-synthesis \
  --perspicacite-rag-mcp-url http://127.0.0.1:8000/mcp \
  --perspicacite-kb asb-paper-<doi> --perspicacite-kb-mode paper \
  --max-cards 5 --seed 1
```

- **Grounding:** `--ground-synthesis` against a per-paper Perspicacité KB
  (`asb-paper-<doi>`, mode `paper` = paper full text **+ supplementary
  information**, auto-ingested). KB autogen was on.
- **Determinism:** `--seed 1`, `--max-cards 5` per build.
- Non-GitHub tools (Bitbucket / GitLab / institutional) used the full clone URL
  as the build spec with `--github-repo` omitted.

## Models used — a **mixed-model** pipeline

ASB routes different pipeline stages to different models (recorded as
`anthropic/*` and `openai/*` slugs; at generation time these were served via
**OpenRouter**). The split for this collection:

| Stage (agent) | Model |
|---|---|
| Decomposition / outline (Agent 2a) | `anthropic/claude-opus-4-8` |
| Card revision (Agent 2c) | `anthropic/claude-opus-4-8` |
| Entity extraction (Agent 1) | `anthropic/claude-haiku-4-5` |
| Card drafting (Agent 2b) | `anthropic/claude-haiku-4-5` |
| Critique (Agent 3) | `anthropic/claude-haiku-4-5` |
| Claim extraction (Agent 1.5) | `anthropic/claude-haiku-4-5` |
| Classification | `anthropic/claude-haiku-4-5` |
| Executable emission | `anthropic/claude-haiku-4-5` |
| **Skill synthesis (Agent 5)** | default tier → `anthropic/claude-haiku-4-5` |
| Retrieval embeddings | `openai/text-embedding-3-large` |
| Script embeddings | `openai/text-embedding-3-small` |

> In short: **Opus 4.8** for the two reasoning-heaviest stages (outline +
> card-revise), **Haiku 4.5** for everything else (including skill synthesis),
> with OpenAI embeddings for retrieval. A high-value subset is earmarked for a
> later re-run of skill synthesis on a stronger model.

The exact slug per stage for any given build is in that build's
`build_manifest.json` (`cli_invocation.flags_resolved.*_model` and
`agents.<agent>.model`). The models are **not prescribed for *use*** — see
`USAGE.md`: grounding only requires a running Perspicacité, with any provider.

## Full traceability (coming later)

This release ships the **distilled** artifacts (skills, tool records, indexes,
collection metadata). The **raw per-paper ASB capsules and the benchmark layer**
— entity spine, claim ledger, rich cards, challenges, indicium records, and each
`build_manifest.json` — are **not yet included**. They will be released
subsequently, at which point every skill is **fully traceable** end-to-end:
source paper + repo → capsule → claims/evidence → distilled skill.
