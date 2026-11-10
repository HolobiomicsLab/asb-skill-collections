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
access to them. The nine domains released on 2026-11-09 were installed this way
on 2026-11-10; the `metabolomics` entry was last installed before its source
moved. Routes and dates: [`docs/STATUS.md`](docs/STATUS.md).

One skill is advertised, the router `metabolomics-router` at
`skills/_router/SKILL.md`. The corpus ships beside it as data (`leaves/`,
indexes, `tools/`, `workflows/`) and is read on demand.

## Use

Search, apply, ground. Full protocol in [`AGENTS.md`](AGENTS.md) and
`<domain checkout>/collections/metabolomics/v3/USAGE.md`.

- Obtain leaves through `asbb fetch --collection metabolomics/v3`, a domain
  checkout or the [Zenodo archive](https://doi.org/10.5281/zenodo.24093587).
- Search with the shipped script, from any directory:
  `python3 "<collection root>/bin/search_skills.py" --query "<task>" -k 10`
  (add `--target workflows` or `--target tools`). `<collection root>` is the
  directory with `skills_index.json`, two directories above the router's
  `SKILL.md`. The routers released on 2026-11-09 print
  `python bin/search_skills.py`, which works only from the collection root
  with a `python` executable.
- Ground a skill against its source with this repository's binder:
  `python3 scripts/perspicacite_kb_bind.py query --collection "<collection root>" --skill <slug> --question "..."`.
  The map is `kb_bundle.json`; tiers are `paper`, `si` and `repo`. No released
  collection ships the binder; selections built with `asbb install` carry a copy.

[`collections.yaml`](collections.yaml) is the release registry. It pins each
domain repository, commit and tree digest, and the Zenodo DOIs of every
release. The domain repositories are private.
