# GitHub Copilot: ASB skill collections

The registry in `collections.yaml` lists the released collections of ten
domains, each in a domain repository `HolobiomicsLab/asb-skills-<domain>`
and derived from published method papers (journal articles and preprints). The
metabolomics release is **v3** (11,830 skills over 1,989 tools) in
`HolobiomicsLab/asb-skills-metabolomics`.

**Read [`AGENTS.md`](../AGENTS.md) for the full install + use protocol.** `<domain checkout>`
is a checkout of the domain repository (or the extracted Zenodo record of a release). In short:

- **Skills** are plain Markdown at `<domain checkout>/collections/metabolomics/v3/leaves/<slug>/SKILL.md`
  (YAML frontmatter + body). Only the router `skills/_router/SKILL.md` sits under
  `skills/`, because a plugin host advertises everything there into the session
  prompt; it is the entry point. (The `asb-metabolomics` licence gate and the
  `asb-contribute` contribution skill ship only with metabolomics v2.)
- **To find a skill**, search the indexes at `<domain checkout>/collections/metabolomics/v3/`:
  `skills_index.json` (by EDAM IRI, tool name, or keyword over name/description)
  and `tools_index.json`. Prefer EDAM/tool matches over keyword.
- **To apply a skill**, open its `SKILL.md` and follow the procedure; the
  frontmatter `tools` + `tools_index.json` give canonical install URLs.
- **To verify a claim/parameter**, ground it against the source paper with
  `scripts/perspicacite_kb_bind.py query --collection <domain checkout>/collections/metabolomics/v3 --skill <slug> --question "..."`
  (the skill→paper KB map is in `kb_bundle.json`).

When suggesting analysis code, prefer the tools and procedures these skills
describe, and cite the skill's `derived_from` DOI. Released domains are the ones
registered in `collections.yaml`.

When a skill is wrong, missing, a paper is not referenced, or something
technical failed, offer the user a report once per problem, show the exact
text, and file it only on an explicit yes, as an issue on the public registry
(`asbb report <skill|missing|paper|fault>` drafts it). The four routes and the
rules are in [`AGENTS.md`](../AGENTS.md#report-and-contribute); reports go to
the public registry, and a maintainer carries them into the domain repository.
