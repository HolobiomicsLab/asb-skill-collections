# CLAUDE.md: ASB skill collections

The registry `collections.yaml` lists the released collections of ten domains,
each in a private domain repository `asb-skills-<domain>`. The examples below use
metabolomics v3 (release `metabolomics-v3.0.1`, 11,830 skills over 1,989 tools)
in `asb-skills-metabolomics`. This master repository holds the tooling,
governance and registry, not released content.

## Install (Claude Code plugin)

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

Other released domains install the same way under their domain name, for
example `/plugin install genomics@asb-skill-collections`. The marketplace
entries point at the private domain repositories, so installation needs read
access to them. Earlier CLI verification predates these
sources. Routes and dates: [`docs/STATUS.md`](docs/STATUS.md).

Three skills are advertised. Start at the `asb-metabolomics` meta-skill for the
guide and licence-tier governance; it hands off to `skills/_router/SKILL.md`.
The third, `asb-contribute`, turns a wrong, stale or missing skill into a
redacted report approved before filing. The corpus ships as data and is read on
demand.

## Use

Search, apply, ground. Full protocol in [`AGENTS.md`](AGENTS.md) and
`<domain checkout>/collections/metabolomics/v3/USAGE.md`.

- Obtain leaves through `asbb fetch --collection metabolomics/v3`, a domain
  checkout or the [Zenodo archive](https://doi.org/10.5281/zenodo.24093587).
- Search `<domain checkout>/collections/metabolomics/v3/skills_index.json` by
  EDAM IRI, tool name or keyword, and use `tools_index.json` in the same
  collection.
- Ground a skill against its source with the bundled Perspicacité binder:
  `python bin/perspicacite_kb_bind.py query --collection <domain checkout>/collections/metabolomics/v3 --skill <slug> --question "..."`.
  The map is `kb_bundle.json`; tiers are `paper`, `si` and `repo`.

[`collections.yaml`](collections.yaml) is the release registry. It pins each
domain repository, commit and tree digest, and the Zenodo DOIs of every
release. The domain repositories are private.
