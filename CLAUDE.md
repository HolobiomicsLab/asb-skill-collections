# CLAUDE.md — ASB Metabolomics skills

This repo publishes the **ASB Metabolomics Skill Collection**
(`collections/metabolomics/v2/`): 5,865 evidence-grounded skills + 909 tools for
computational LC-MS/MS metabolomics.

## Install (Claude Code plugin)

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

Skills auto-load from `collections/metabolomics/v2/skills/<slug>/SKILL.md`; the
default entry is `skills/_router/SKILL.md`.

## Use

Search → apply → ground. Full protocol in [`AGENTS.md`](AGENTS.md) and
[`collections/metabolomics/v2/USAGE.md`](collections/metabolomics/v2/USAGE.md).

- Find a skill via `collections/metabolomics/v2/skills_index.json` (EDAM IRI /
  tool name / keyword) or `tools_index.json`.
- Ground a skill against its source paper with the Perspicacité binder:
  `python scripts/perspicacite_kb_bind.py query --collection collections/metabolomics/v2 --skill <slug> --question "..."`
  (skill→KB map in `kb_bundle.json`; tiers `paper`/`si`/`repo`).

The public release is **metabolomics only**; other `collections/` domains are
staged/internal.
