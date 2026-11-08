# CLAUDE.md — ASB Metabolomics skills

The public release is **metabolomics v3** (11,830 skills + 1,989 tools) in
`HolobiomicsLab/asb-skills-metabolomics`; this repo's marketplace and the local
paths below still serve v2 (5,859 skills + 909 tools).

## Install (Claude Code plugin)

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

Verified at CLI level on 2026-10-30 with Claude Code 2.1.304; loading the skills
in a live session was not exercised. The marketplace keeps a 286 MB clone of this
repository beside the 72 MB plugin cache. From a local checkout,
`claude plugin marketplace add "$PWD"` then
`claude plugin install metabolomics@asb-skill-collections` installs the same
plugin without the clone. Routes and dates: [`docs/STATUS.md`](docs/STATUS.md).

Three skills are advertised; the corpus ships as data at
`collections/metabolomics/v2/leaves/<slug>/SKILL.md` and is read on demand. Start at
the `asb-metabolomics` meta-skill (guide + license-tier governance), which hands off
to `skills/_router/SKILL.md` for routing. The third, `asb-contribute`, is the
contribution route: it turns a skill that proved wrong, stale or missing into a
redacted report you approve before anything is filed.

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
