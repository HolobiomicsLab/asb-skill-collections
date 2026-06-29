# Next ASB generation wave (post-v0.2.0)

Tracks content and tasks deliberately deferred out of the **metabolomics-v0.2.0**
release so it ships clean. Nothing here blocks v0.2.0; each item needs an **ASB
generation run** (paper/repo → skills) or a small new mechanism, not a corpus
status flip.

## Why these are deferred, not blocked

The released collection (`collections/metabolomics/v2/`) already admits tools on
the openness of their **code repository** (the `repo-oa` tier family — see
[OPEN_ACCESS_POLICY.md → *Software tools — repository-OA tier*](../governance/OPEN_ACCESS_POLICY.md)).
`patRoon`, `OpenTIMS`, and `Galaxy-M` are therefore **already included** in v2.
The items below are tools that are **not yet in v2**: including them means running
the distillation pipeline to produce skills, which is out of scope for a v0.2.0
that is otherwise ready.

## Deferred tools

| Tool | Repo | Code license | License status | Needs |
|---|---|---|---|---|
| **CCSfind** | `sangeeta97/ccs_find` | MIT | ✅ resolved (clean) | distillation run → leaf skills |
| **Galaxy W4M** | `workflow4metabolomics/tools-metabolomics` | GPL-3.0 | ✅ resolved (clean, [#16](https://github.com/HolobiomicsLab/asb-skill-collections/issues/16)) | distillation run; decide vs. existing Galaxy-M |
| **Masster** | `zamboni-lab/masster-dist` | source-available, **non-commercial** (non-OSI) | ⚠️ author-approved (N. Zamboni, [#12](https://github.com/HolobiomicsLab/asb-skill-collections/issues/12)) but **not** `repo-oa` | the *restricted-use tier* (below) **and** a distillation run |

## Tasks for the wave

1. **Build the restricted-use tier.** Masster is source-available + non-commercial,
   so it does **not** qualify for `repo-oa`. Implement the tier flagged in
   OPEN_ACCESS_POLICY.md: a machine-readable usage-restriction field + a
   user-facing non-commercial notice, with the author's permission recorded.
   Gate support in `scripts/release_gate.py` alongside `_REPO_OA_TIERS`.
2. **Distill the deferred tools** (CCSfind, W4M, then Masster once the tier exists).
   See the recipe below.
3. **Backfill `code_license` SPDX** for the ~568 existing `repo-oa` tools in v2 and
   promote them to the precise `repo-permissive` / `repo-copyleft` tier (read each
   repo's `LICENSE`; automatable). Forward-standard from the repo-OA policy; does
   not change what the gate already admits.
4. **(Optional) Make distillation agentic.** Today it is a scripted Python CLI
   (`asb build`) in the AgenticScienceBuilder repo — *not* a Claude Code skill.
   A `/add-asb-skill <doi> <repo>` wrapper skill that orchestrates verify → build
   → collect → reindex would turn "add a tool" into a single prompt.

## Distillation recipe (per tool)

Distillation is **scripted**, in the `AgenticScienceBuilder` repo (it *uses* LLM
APIs internally; it is not driven by a Claude Code skill).

**Prerequisites:** `ANTHROPIC_API_KEY` (distillation agents); the paper PDF +
optional SI (ASB does not auto-fetch); conda env `agentic-science-builder`.
Optional: `OPENAI_API_KEY` (only if also composing a superskill) and a running
Perspicacité server (grounding falls back to git-clone + local read otherwise).

```bash
# 1. Package the paper: a dir with article.pdf [+ supplementary.pdf] and a
#    README.md carrying  doi: / repo_url: / title:
# 2. Distill (AgenticScienceBuilder repo, conda env active):
PYTHONPATH=src python3 -m agentic_science_builder build <pkg_dir> \
    --output outputs/<run> --llm --enrich-skills --claim-ledger --no-pin --metabolomics
# 3. Promote into the registry + reindex (this repo):
cp -r <AgenticScienceBuilder>/outputs/<run>/skills/<slug> collections/metabolomics/v2/skills/
python3 scripts/regen_catalogue.py collections/metabolomics/v2 --update-indexes
# 4. Add the corpus.yaml entry (repo-permissive / repo-copyleft + code_license),
#    then gate:
python3 scripts/release_gate.py collections/metabolomics/v2 --strict
```
