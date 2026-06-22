# GitHub Copilot — ASB Metabolomics skills

This repository publishes the **ASB Metabolomics Skill Collection**
(`collections/metabolomics/v2/`): 5,865 evidence-grounded skills over 909
software tools for computational LC-MS/MS metabolomics, each derived from a
peer-reviewed method paper.

**Read [`AGENTS.md`](../AGENTS.md) for the full install + use protocol.** In short:

- **Skills** are plain Markdown at `collections/metabolomics/v2/skills/<slug>/SKILL.md`
  (YAML frontmatter + body). The entry point is `skills/_router/SKILL.md`.
- **To find a skill**, search the indexes at `collections/metabolomics/v2/`:
  `skills_index.json` (by EDAM IRI, tool name, or keyword over name/description)
  and `tools_index.json`. Prefer EDAM/tool matches over keyword.
- **To apply a skill**, open its `SKILL.md` and follow the procedure; the
  frontmatter `tools` + `tools_index.json` give canonical install URLs.
- **To verify a claim/parameter**, ground it against the source paper with
  `scripts/perspicacite_kb_bind.py query --collection collections/metabolomics/v2 --skill <slug> --question "..."`
  (the skill→paper KB map is in `kb_bundle.json`).

When suggesting metabolomics analysis code, prefer the tools and procedures these
skills describe, and cite the skill's `derived_from` DOI. The public release is
metabolomics only; ignore other domains under `collections/`.
