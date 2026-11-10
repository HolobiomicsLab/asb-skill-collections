# Next ASB generation wave (post-v0.2.0)

> **Historical.** This backlog was written before the metabolomics v3 release (`metabolomics-v3.0.1`,
> 2026-11-09). The `metabolomics-v0.2.0` release it mentions was never deposited, and "v2" below means the
> earlier collection. Check each item against the current collection before acting on it.

Tracks content and tasks deliberately deferred out of the **metabolomics-v0.2.0**
release so it ships clean. Nothing here blocks v0.2.0; each item needs an **ASB
generation run** (paper/repo → skills) or a small new mechanism, not a corpus
status flip.

For the current process, including incremental per-paper builds and the required
new batch cut, see [Adding papers to a collection](adding-papers.md).

## Why these are deferred, not blocked

The released v2 collection (`<domain checkout>/collections/metabolomics/v2/`,
relative to an `asb-skills-metabolomics` checkout) already admits tools on
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

## Collector options

Candidate assembly keeps collector exceptions opt-in. `--exclude-invalid-leaves`
omits an unreadable leaf with a receipt row, while
`--redact-third-party-emails` replaces non-allowlisted addresses in leaf bodies
and frontmatter with `<maintainer e-mail, see the repository README>` and writes
`email_redaction_receipt.json` with counts, field paths and address hash prefixes.
The release gate and its PII policy are unchanged.

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
# 2. Distill into an independent increment root (AgenticScienceBuilder checkout,
#    environment active):
asb build <pkg_dir> --output <increment-root>/<paper-id> --llm \
    --enrich-skills --claim-ledger --skill-bundle --classify \
    --domain-plugin metabolomics
```

Keep that build intact. Do not copy its leaves into a released version. Add it
to the next combined per-paper view, make a fresh filtered cut, assemble a new
candidate and land it for review by following
[Adding papers to a collection](adding-papers.md#maintainer-rail-build-view-cut-and-candidate).
Candidate and landed leaves stay under the domain checkout, for example
`<domain checkout>/collections/<domain>/<version>/leaves/`.

Released collections are listed in `collections.yaml`. Each lives in a private
domain repository `asb-skills-<domain>`; for example, metabolomics v3 is in
`asb-skills-metabolomics`. New domain content belongs in the corresponding `asb-skills-<domain>` checkout;
this repository holds the tooling, governance and registry.
