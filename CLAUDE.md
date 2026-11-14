# CLAUDE.md: ASB skill collections

The registry `collections.yaml` lists the released collections of ten domains,
each in a domain repository `asb-skills-<domain>`. The examples below use
metabolomics v3 (release `metabolomics-v3.0.2`, 11,830 skills over 1,989 tools)
in `asb-skills-metabolomics`. This master repository holds the tooling,
governance and registry, not released content.

## Install (Claude Code plugin)

```bash
/plugin marketplace add HolobiomicsLab/asb-skill-collections
/plugin install metabolomics@asb-skill-collections
```

Other released domains install the same way under their domain name, for
example `/plugin install genomics@asb-skill-collections`. The marketplace
entries point at the domain repositories, which are public, so installation
needs no read access. The nine domains released on 2026-11-09 were installed this way
on 2026-11-10; the `metabolomics` entry was last installed before its source
moved. Routes and dates: [`docs/STATUS.md`](docs/STATUS.md).

One skill is advertised, the router `metabolomics-router` at
`skills/_router/SKILL.md`. The corpus ships beside it as data (`leaves/`,
indexes, `tools/`, `workflows/`) and is read on demand.

## Use

Search, apply, ground. Full protocol in [`AGENTS.md`](AGENTS.md) and
`<domain checkout>/collections/metabolomics/v3/USAGE.md`.

- Obtain leaves through `asbb fetch --collection metabolomics/v3`, a domain
  checkout or the [Zenodo archive](https://doi.org/10.5281/zenodo.24122117).
- Search with the shipped script, from any directory:
  `python3 "<collection root>/bin/search_skills.py" --query "<task>" -k 10`
  (add `--target workflows` or `--target tools`). `<collection root>` is the
  directory with `skills_index.json`, two directories above the router's
  `SKILL.md`. The routers of the patch releases of 2026-11-10 print this
  command with the collection path filled in; those released on 2026-11-09
  printed `python bin/search_skills.py`, which works only from the collection
  root with a `python` executable.
- Ground a skill against its source with this repository's binder:
  `python3 scripts/perspicacite_kb_bind.py query --collection "<collection root>" --skill <slug> --question "..."`.
  The map is `kb_bundle.json`; tiers are `paper`, `si` and `repo`. No released
  collection ships the binder; selections built with `asbb install` carry a copy.

[`collections.yaml`](collections.yaml) is the release registry. It pins each
domain repository, commit and tree digest, and the Zenodo DOIs of every
release. The domain repositories are public.

## Report and contribute

At each distinct problem, offer the user a report without being asked, once:
a procedure failed or no longer matches the tool, the search found nothing
usable, a method paper is missing from the search, the leaves had to be composed
by hand, or a command of the collection failed. The four routes:

1. this skill is wrong or could be better;
2. a skill is missing: request it, or propose yours;
3. a paper is not referenced: propose it;
4. something technical failed: report it.

Draft with `asbb report <skill|missing|paper|fault>` (or `bin/report_issue.py`
where a collection ships it), show the exact title, labels and body, and post
only on an explicit yes, with `gh issue create --repo HolobiomicsLab/asb-skill-collections`
or the printed address. Never paste paths, credentials or sample names. Reports
go to this public registry, and a maintainer carries reports into the
domain repository. Detail in [`AGENTS.md`](AGENTS.md).
