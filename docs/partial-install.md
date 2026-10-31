# Installing part of a collection

The metabolomics collection (`collections/metabolomics/v2`) holds 5,859 skills.
Installed whole, it is a 61 MB snapshot of 6,870 files. Most tasks need a
handful of those skills. This page describes the three ways to take less.

| Way | Command | Needs a checkout | What you get |
|---|---|---|---|
| Technique pack | `asbb install <pack>` | yes | every skill tagged with one technique, for example the 2,617 LC-MS skills |
| Selection | `asbb install --skills ...`, `--skills-file ...` or `--query ...` | yes | exactly the skills you name or the top hits of a search, installed as a pack |
| Fetch | `asbb fetch <slugs> --collection <slug>/vN --dest <dir>` | no | the chosen `SKILL.md` files and a provenance record, nothing else |

A pack and a selection are the same thing built from a different membership
rule: a pack takes every skill whose `techniques` carry its tag, a selection
takes a list of slugs. Both are derived by `scripts/build_packs.py`, so both
install as one advertised router over `leaves/`, with `skills_index.json` and
`kb_bundle.json` filtered to their members, the offline search script and the
grounding helper. Fetch skips all of that and downloads leaf files only.

Selections and fetch need a router-shaped collection with a root
`skills_index.json` and `leaves/`; today that is `metabolomics/v2` only.

All figures on this page were measured on 2026-10-30 from a checkout of `main`
at `e80767838` plus this change, with `HOME` pointed at a temporary directory.
Outputs below show that directory as `$HOME`.
Byte totals include the install receipt `.asbb-unit.json`, which records the
destination path, so they vary by a few tens of bytes with the length of
`$HOME`.

## Sizes

Installed into the `agents` runtime (`$HOME/.agents/skills`):

| Install | Leaves | Files written | Bytes written | On disk (`du -sk`) |
|---|---:|---:|---:|---:|
| Full collection, `metabolomics` | 5,859 | 6,870 | 61,255,784 | 73,476 KiB |
| Technique pack, `metabolomics-lc-ms` | 2,617 | 2,627 | 25,568,608 | 29,752 KiB |
| Selection of 10 skills | 10 | 20 | 145,501 | 188 KiB |
| Fetch of the same 10 skills | 10 | 11 | 90,271 | 112 KiB |

In the 10-skill selection, the leaves are 85,937 bytes. The two helper scripts
(`bin/search_skills.py`, `bin/perspicacite_kb_bind.py`) add 35,751 bytes and
the filtered indexes 14,797 bytes.

## Before you start

The installer reads a local checkout. Use Python 3.12 or later with PyYAML in a
virtual environment, and run the commands from the repository root:

```bash
git clone https://github.com/HolobiomicsLab/asb-skill-collections
cd asb-skill-collections
uv venv -p 3.12 && source .venv/bin/activate && uv pip install pyyaml
```

Without uv, `python3.12 -m venv .venv && . .venv/bin/activate && python -m pip install pyyaml`
prepares the same environment.

`fetch` is the exception. It downloads from GitHub and needs only the `asbb`
package; see [Fetch](#fetch-without-a-checkout).

## Technique packs

Eight packs are declared in `packs/metabolomics/packs.yaml`:

| Pack | Skills |
|---|---:|
| `metabolomics-ce-ms` | 113 |
| `metabolomics-direct-infusion` | 97 |
| `metabolomics-gc-ms` | 367 |
| `metabolomics-ion-mobility` | 385 |
| `metabolomics-lc-ms` | 2,617 |
| `metabolomics-ms-generic` | 804 |
| `metabolomics-ms-imaging` | 291 |
| `metabolomics-nmr` | 276 |

A skill tagged with several techniques is in several packs.

```bash
python3 -m asb_skill_collections.asbb_cli install metabolomics-lc-ms --runtime agents
```

```text
installed 1 skill(s) from metabolomics-lc-ms -> $HOME/.agents/skills
```

The count is of advertised entries: the pack's router. The 2,617 leaves sit in
the managed snapshot under `$HOME/.agents/skills/.asbb-units/<content-id>`.

## A selection of skills

`asbb install` takes a selection in place of a pack name. Name the collection
with `--collection` (`metabolomics` for its latest version, or
`metabolomics/v2`), then choose the skills in any combination of:

| Option | Selects |
|---|---|
| `--skills a,b,c` | these slugs; repeatable |
| `--skills-file FILE` | one slug per line; `#` starts a comment |
| `--query "TEXT" --top N` | the first N hits of `asbb search` for TEXT (default N is 10) |

`--name` sets the name the selection is installed and uninstalled under. The
default is `<collection>-subset-<8 hex digits>`, a digest of the sorted slug
list: the same set of skills always gets the same name, so installing it again
refreshes it in place.

### Preview, then dry run

`--query` uses the same index, selector and filters as `asbb search`, so the
search shows what the selection will hold:

```bash
python3 -m asb_skill_collections.asbb_cli search "untargeted LC-MS/MS annotation" --collection metabolomics/v2 --k 10
```

`--dry-run` resolves the selection, derives it and prints every write without
making one:

```bash
python3 -m asb_skill_collections.asbb_cli install --query "untargeted LC-MS/MS annotation" --top 10 --collection metabolomics/v2 --runtime agents --dry-run
```

```text
selection metabolomics-subset-349bfa1b: 10 skill(s) from metabolomics/v2
  untargeted-lc-ms-data-preprocessing          restricted
  untargeted-metabolomics-annotation           open
  untargeted-lcms-peak-annotation              open
  lc-ms-mass-matching-reference-building       open
  ranked-annotation-prioritization             open
  annotation-benchmark-performance-evaluation  open
  ms1-spectral-annotation-chemical-space       open
  lcms-feature-probability-scoring             open
  metabolite-mass-lookup-preparation           open
  ms2-spectrum-consolidation                   open
licence tiers (open, noncommercial, restricted, unknown): https://github.com/HolobiomicsLab/asb-skill-collections/blob/main/governance/LICENSE_TIERS.md
would copy complete unit to $HOME/.agents/skills/.asbb-units/e50488b958510ec68ffe32a6c9f14e90fe5dad33f13e80f3d86e3410aa695a54
would write $HOME/.agents/skills/_router
would install metabolomics-subset-349bfa1b (10 skill(s), 1 advertised entry(ies)) -> $HOME/.agents/skills
remove with: asbb uninstall metabolomics-subset-349bfa1b --runtime agents
```

Drop `--dry-run` to install. The installed unit holds the 10 leaves, the
filtered `skills_index.json` and `kb_bundle.json`, `bin/search_skills.py`,
`bin/perspicacite_kb_bind.py`, `commands/ground.md`, `GROUNDING.md` and the
router, whose description reads "search this unit's 10 evidence-grounded
skills". Run from the unit, `bin/search_skills.py` searches those 10 only.

### From a file, under your own name

```text
# annotation set
untargeted-metabolomics-annotation
ms2-spectrum-consolidation  # consolidate before matching
```

In a fresh destination (two selections cannot share one, see
[One router per destination](#one-router-per-destination) below), or after
`asbb uninstall metabolomics-subset-349bfa1b --runtime agents`:

```bash
python3 -m asb_skill_collections.asbb_cli install --skills-file my-skills.txt --collection metabolomics/v2 --name my-annotation-set --runtime agents
```

```text
selection my-annotation-set: 2 skill(s) from metabolomics/v2
  untargeted-metabolomics-annotation  open
  ms2-spectrum-consolidation          open
licence tiers (open, noncommercial, restricted, unknown): https://github.com/HolobiomicsLab/asb-skill-collections/blob/main/governance/LICENSE_TIERS.md
installed my-annotation-set (2 skill(s), 1 advertised entry(ies)) -> $HOME/.agents/skills
remove with: asbb uninstall my-annotation-set --runtime agents
```

### Uninstall

```bash
python3 -m asb_skill_collections.asbb_cli uninstall my-annotation-set --runtime agents
```

```text
removed 1 entry(ies) for my-annotation-set
```

The router and the snapshot are removed, and the record leaves
`$HOME/.asbb/installed.json`.

### What is refused

Nothing is written when a selection is refused, and the command exits 1.

| Case | Message |
|---|---|
| a slug not in the index | `error: 1 slug(s) not in the collection index: no-such-skill` |
| nothing selected | `error: the selection is empty: --skills, --skills-file and --query named no skill` |
| a pack name and a selection together | `error: name a pack, or select skills with --skills, --skills-file or --query, not both` |
| `--name` taken by a marketplace pack | `error: selection name 'metabolomics-lc-ms' is a marketplace pack; choose another` |

A selection of every skill in the collection (5,859) installs as one
advertised router over 5,859 leaves; only the router is advertised to the host,
whatever the selection holds.

### One router per destination

Every pack and every selection advertises its router as `_router`. Two of them
cannot share one destination: with `metabolomics-lc-ms` already installed in
`$HOME/.agents/skills`, installing a selection there is refused with

```text
error: $HOME/.agents/skills/_router exists and is not owned by this pack; use --force to overwrite
```

The same refusal applies between two packs. Install the second one elsewhere
with `--dest DIR`, or uninstall the first.

## Fetch without a checkout

`asbb fetch` downloads chosen leaves straight from GitHub. It reads the
collection's `skills_index.json` at the requested ref to check the slugs and
read their licence tiers, then fetches each
`collections/<slug>/vN/leaves/<skill>/SKILL.md` from
`raw.githubusercontent.com`.

```bash
asbb fetch untargeted-metabolomics-annotation,ms2-spectrum-consolidation --collection metabolomics/v2 --dest asb-skills
```

```text
fetched 2 skill(s) from metabolomics/v2 at main -> asb-skills
  untargeted-metabolomics-annotation  open
  ms2-spectrum-consolidation          open
licence tiers (open, noncommercial, restricted, unknown): https://github.com/HolobiomicsLab/asb-skill-collections/blob/main/governance/LICENSE_TIERS.md
provenance: asb-skills/PROVENANCE.json
```

```text
asb-skills/PROVENANCE.json
asb-skills/ms2-spectrum-consolidation/SKILL.md
asb-skills/untargeted-metabolomics-annotation/SKILL.md
```

`--ref` takes a branch, tag or commit (default `main`). `PROVENANCE.json`
records the repository, the ref, the collection, the date, the slugs, each
skill's licence tier, and the URL and SHA-256 of every file written. The leaves
are byte-identical to the checkout: all 10 leaves of the selection above,
fetched from `main`, matched `collections/metabolomics/v2/leaves/` exactly.

What fetch does not give you: no router, no index, no search or grounding
helper, and no install record. The files are the collection's own `SKILL.md`
bytes; no agent host was run against them for this page.

Every fetch reads the whole `skills_index.json` (5,430,046 bytes on `main`
today), so the download is about 5.5 MB whether you ask for one skill or ten.

Fetch refuses, before writing anything, a slug the remote index does not list,
a collection not written as `<slug>/vN`, a ref that is not a plain branch, tag
or commit name (such as `x/../main`), and a destination that already holds
`PROVENANCE.json` or a directory of the same name as a requested skill. Running
the fetch command above a second time gives:

```text
error: asb-skills already holds PROVENANCE.json, untargeted-metabolomics-annotation, ms2-spectrum-consolidation; fetch into a new or empty directory
```

### Getting the `asbb` command

The package is not published to a package index (see the README). Install it
from a clone, without the editable flag:

```bash
git clone https://github.com/HolobiomicsLab/asb-skill-collections
uv venv -p 3.12 && source .venv/bin/activate
uv pip install ./asb-skill-collections
```

Without uv, `python3.12 -m venv .venv && . .venv/bin/activate && python -m pip install ./asb-skill-collections`
does the same.

The fetch output above came from such an install in a fresh virtual
environment, run from a directory that is not a checkout. There the package
resolved to the environment's `site-packages`, and the wheel held the
`asb_skill_collections` package only, not the corpus and not `scripts/`.
`install` with a selection still needs a checkout: from a package install, pass
it with `--repo`.

## Licence tiers

Every skill carries a `license_tier` about the tool it describes, not about the
skill text, which is CC-BY-4.0. `open` permits commercial use. `noncommercial`
means academic or noncommercial use only: confirm the purpose before applying
the skill. `restricted` means an established licence that constrains reuse, and
`unknown` means no tool-level licence evidence was found. Both `install` and
`fetch` print the tier of every skill they handle. Definitions and policy:
[`governance/LICENSE_TIERS.md`](../governance/LICENSE_TIERS.md).
