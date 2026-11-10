# Release status

What has been verified for each distribution surface of `asb-skill-collections`,
when, and what was measured on 2026-10-30.

Step 2 of the per-domain split was completed on 2026-11-08: this master is the
registry and tooling repository; released content is in the domain repositories.
The measurements below predate the new marketplace sources and do not verify an
install through them. `collections.yaml` pins repository, commit and tree digest
for each release.

Two kinds of entry appear below.

- **README (e80767838)** quotes, verbatim, the statement the README carried on
  `main` at `e80767838` before its restructure on 2026-10-30. Nothing here is
  promoted beyond what that README claimed. Quotations keep the original
  punctuation, including dashes.
- **Measured 2026-10-30** records a check run on that date against `main` at
  `e80767838`, with the command used. A measurement of reachability or of a
  dry run is not an end-to-end verification and is not presented as one.

## Summary

| Surface | State | Last verified (as the README at `e80767838` states it, or measured 2026-10-30) |
|---|---|---|
| Managed install of the full `metabolomics` domain (`--runtime agents`) | verified | 2026-09-13, `int/collections-release-2026-09-13` at `777671bc3` |
| Claude Code, local-checkout marketplace | verified | Claude Code 2.1.241; no date stated |
| Checkout CLI (`asbb search`, `get`, `--list-collections`) | verified | 2026-09-13, shared-selector behaviour at `777671bc3` |
| Claude Code, public GitHub marketplace transport | verified at CLI level, in-session load not exercised | measured 2026-10-30, Claude Code 2.1.304, `main` at `e80767838`; 358 MB on disk |
| Per-technique packs | `metabolomics-lc-ms` verified at CLI level, in-session load not exercised; the other seven experimental, not installed | measured 2026-10-30, Claude Code 2.1.304 and `--runtime agents`; 29 MB |
| Marketplace install of the nine domains released on 2026-11-09 (sources in the private domain repositories) | verified at CLI level with repository access; in a session the router was exercised on collections loaded with `--plugin-dir`, not on a marketplace install | measured 2026-11-10: Claude Code 2.1.319 (`claude plugin install <domain>@asb-skill-collections`, nine exit 0, installed commit equal to the registry commit) and Codex CLI 0.154.0 (`codex plugin add <domain>@asb-skill-collections`, nine exit 0); the `metabolomics` entry at `metabolomics-v3.0.1` was not re-installed |
| Web UI uploads | experimental, not verified end to end | not exercised |
| Runtime adapters other than `agents` | experimental | not launched |
| MCP server | pending current verification | pinned release audit; no date stated |
| PyPI | not published, by design in v0 | n/a |
| Documentation site (GitHub Pages) | live: HTTP 200 for the site root and `search.html` on 2026-11-10; not enabled at the 2026-10-30 measurement | 2026-11-10 |
| HuggingFace mirror and leaderboard | planned, not yet live | n/a |
| Benchmark and capsules | to be released later | n/a |
| `w3id.org/holobiomicslab/` IRIs | resolve | since 2026-09-14 |
| `w3id.org/asb` and `w3id.org/asb/validation` | resolve | since 2026-10-29 |
| Zenodo DOI | metabolomics concept DOI 10.5281/zenodo.20794026 with versions `metabolomics-v0.1.0` (2026-06-22, v2), `metabolomics-v3.0.0` (superseded) and `metabolomics-v3.0.1`; nine further domain records, each with its concept and version DOI in `collections.yaml` | 2026-06-22 deposit measured 2026-10-30; later records are registry rows of 2026-11-09 |
| Metabolomics v3.0.0 Zenodo deposit | version DOI `10.5281/zenodo.24054446`; publication date 2026-11-09 | record supplied for the 2026-11-09 release |
| Metabolomics v3.0.0 deposit files | `metabolomics-v3.zip`, 37,974,225 bytes, md5 `9fd503cd2361e924c29cf2ba4eedcf04`; `metabolomics-v3-leafemb.npz`, 148,632,620 bytes, md5 `0bc4a202fbe1fe92d8bfd4058a0d2baa` | release record |
| Metabolomics v3.0.0 domain tag | `metabolomics-v3.0.0` at `788df247c887bea90670a4252ab94da36088d2be` in `HolobiomicsLab/asb-skills-metabolomics` | tagged domain checkout |
| Metabolomics v3.0.1 | version DOI `10.5281/zenodo.24093587`; tag `metabolomics-v3.0.1` in `HolobiomicsLab/asb-skills-metabolomics`; replaces v3.0.0 as the v3 row of `collections.yaml`, which lists v3.0.0 as superseded | registry row, 2026-11-09 |
| Nine domain releases | agentic-ai, astronomy, genomics, metabarcoding, metagenomics, multi-omics and proteomics (v1); epigenomics and transcriptomics (v2); tags `<domain>-v<N>.0.0`; concept and version DOIs, commits and tree digests in `collections.yaml` | registry rows, 2026-11-09 |
| Marketplace entries of the nine new domains | not exercised through Claude Code; the transport measurement of 2026-10-30 predates these sources | n/a |

## Verified release perimeter

README (e80767838):

> The release-verified perimeter is the complete `metabolomics` domain installed
> as a managed snapshot, Claude Code from a local-checkout marketplace, and the
> checkout CLI. Exact lifecycle output, uninstall residue and pending surfaces
> are recorded in `<domain checkout>/collections/metabolomics/v2/USAGE.md`, section 1.
> The complete-snapshot and shared-selector behaviour was verified on
> `int/collections-release-2026-09-13` at `777671bc3`; this source revision
> predates those fixes.

Measured 2026-10-30:

- `git merge-base --is-ancestor 777671bc3 e80767838` succeeds, and so does the
  same check for `600f4a5dc`, the source revision that USAGE.md §1 says predates
  the installer fixes. `main` at `e80767838` therefore contains the commit on which
  the fixes were verified. `777671bc3` is dated 2026-09-13 04:06 +0200 (`git log -1`).
- `python3 -m asb_skill_collections.asbb_cli install metabolomics --runtime agents --dry-run`
  with `HOME` set to an empty scratch directory exited 0 and printed
  `would install 3 skill(s) from metabolomics`; nothing was written. The full
  install was not re-run.
- The three checkout CLI commands of USAGE.md §1 (`python3 -m asb_skill_collections.asbb_cli`
  `search ... --k 1`, `get ...`, `search --list-collections`) exited 0. The search returned
  `metabolomics/v2/workflows/untargeted-lcmsms-annotation`, score 4.0, selector
  `asb-keyword` 1.0.0 rule `router`; `--list-collections` printed
  `metabolomics/v2  5859 skills  +workflows`. The interpreter was Python 3.11.15,
  below the `requires-python = ">=3.12"` of `pyproject.toml`.
- `python -m scripts.unit_closure`: `PASS: 0 violation(s) across 9 indexed unit(s).`
- `python scripts/check_advertised_counts.py`: PASS (count claims in README.md,
  AGENTS.md, CLAUDE.md and the unit's Markdown match the on-disk census:
  5,859 leaves, 909 tool records, 566 papers in `corpus.yaml`, 21 `workflow.yaml`).

Current package selector note: `asb_skill_collections/asb_skill_index.py`
1.1.0 weights description 3, name 2 and tool metadata 1, with a query-sensitive
plumbing de-boost that retains matched rows. The released v2 and pack scripts
remain at 1.0.0 until the domain repository regenerates them under a release
decision. Their output and options are unchanged here.

## Claude Code public marketplace

README (e80767838), section labelled "pending verification":

> The equivalent local-checkout marketplace route was exercised with Claude Code
> 2.1.241. The public GitHub transport remains pending because this rehearsal had
> no usable DNS; it is not inferred from the local result. Claude's component
> inventory saw `_router`, `asb-contribute`, `asb-metabolomics` and `ground`.

Measured 2026-10-30, reachability:

- The repository is public (`gh api repos/HolobiomicsLab/asb-skill-collections`:
  `"visibility":"public"`).
- `curl` of `raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main/.claude-plugin/marketplace.json`
  returned 200; `git ls-remote` of the public URL returned `e807678383b5…` for `HEAD`.
- `marketplace.json` lists 9 plugins (`metabolomics` and 8 packs), all at version 0.1.0.

Measured 2026-10-30, install at CLI level: verified at CLI level with Claude Code
2.1.304, in-session load not exercised. Each run set `HOME` and
`CLAUDE_CONFIG_DIR` to scratch directories; no model session was run.

- `claude plugin marketplace add HolobiomicsLab/asb-skill-collections` exited 0
  in two runs, in 19.5 s and in 20.8 s; the 20.8 s run recorded that the clone
  went over SSH. In a further run with SSH given no identity, as for a user
  without a key, Claude Code printed `SSH clone failed, retrying with HTTPS` and
  succeeded in 26.2 s.
- `claude plugin install metabolomics@asb-skill-collections` exited 0 in 2.5 s
  and in 3.9 s, at `e80767838`. The plugin cache held 6,866 files.
- Disk cost: the marketplace keeps a shallow clone of this repository, 286 MB
  (of which `.git` is 43 MB), beside the 72 MB plugin cache: 358 MB in all.
- `claude plugin details metabolomics@asb-skill-collections` listed 7 components:
  the skills `_router`, `asb-contribute` and `asb-metabolomics`, and the commands
  `claim-skill`, `ground`, `propose-skill` and `synthesize-meta-skill`, with an
  estimated always-on cost of about 626 tokens.
- `claude plugin validate .` passed with 2 warnings, for the fields
  `schema_version` and `publisher` of `marketplace.json`, which the host does
  not know; both fields were removed on 2026-10-31 and `--strict` passes.
- The cached plugin holds the 5,859 leaves, and its `bin/search_skills.py --query`
  ran from the cache.
- Not exercised: loading the skills in a live Claude Code session, which needs a
  model call.

For comparison, the local-checkout route (`claude plugin marketplace add "$PWD"`,
then the same install) took 1.4 s and 3.8 s and wrote the 72 MB plugin cache
without a clone.

## Per-technique packs

README (e80767838), section labelled "experimental, not verified end to end":

> Packs **overlap** (a multi-technique skill appears in several): install **one** full plugin **or** a few packs, not both. See `<domain checkout>/packs/metabolomics/README.md`.

Measured 2026-10-30: the 8 pack sources exist on disk and `unit_closure` reports
no violation across the 9 indexed units. One pack, `metabolomics-lc-ms`, was
installed at CLI level, in-session load not exercised:

- `claude plugin install metabolomics-lc-ms@asb-skill-collections` exited 0
  (Claude Code 2.1.304, public marketplace). The plugin cache was 29 MB, with
  the components `_router` and `ground` and an estimated always-on cost of about
  141 tokens.
- `asbb install metabolomics-lc-ms --runtime agents` wrote 2,627 files, 29,752 KiB
  on disk ([partial-install.md](partial-install.md#sizes)).

The other seven packs were not installed.

## Web UI

README (e80767838), section labelled "experimental, not verified end to end":

> This route was not exercised for the release and no end-to-end instructions are
> asserted here.

Measured 2026-10-30: nothing. AGENTS.md describes the upload steps; they remain
unverified.

## Runtime adapters

README (e80767838), section labelled "experimental, not verified end to end":

> This behaviour was verified for `--runtime agents`; Codex, Copilot CLI, Gemini
> CLI, Cursor, Cline and VS Code were not launched, so their adapters remain
> experimental.

Measured 2026-10-30: `asbb_cli install --list-runtimes` lists `agents`, `codex`,
`copilot`, `gemini`, `claude`, `cursor`, `cline`, `vscode-copilot` and `--dest DIR`.
No host was launched.

The adapter commands and install behaviour that the README at `e80767838`
documented are kept here verbatim, because the restructured README shows only
the `agents` route. Apart from `--runtime agents`, they are not verified end to end.

**Skill-native runtimes** (read `SKILL.md` directly):

```bash
# Codex + Copilot CLI + Gemini CLI all share ~/.agents/skills — one install:
python3 -m asb_skill_collections.asbb_cli install metabolomics-lc-ms --runtime agents

# Or a specific home: --runtime codex | copilot | gemini
# Vendor into a project for Claude Code: --runtime claude  (add --user for ~/.claude)
```

**Rules/instruction IDEs** (rendered instructions backed by a complete unit — run
from the target project, making the checkout importable and naming it explicitly):

```bash
ASB_COLLECTIONS_REPO=/path/to/asb-skill-collections
export PYTHONPATH="$ASB_COLLECTIONS_REPO${PYTHONPATH:+:$PYTHONPATH}"
python3 -m asb_skill_collections.asbb_cli install metabolomics-lc-ms --repo "$ASB_COLLECTIONS_REPO" --runtime cursor          # .cursor/rules/*.mdc
python3 -m asb_skill_collections.asbb_cli install metabolomics-lc-ms --repo "$ASB_COLLECTIONS_REPO" --runtime cline           # .clinerules/*.md
python3 -m asb_skill_collections.asbb_cli install metabolomics-lc-ms --repo "$ASB_COLLECTIONS_REPO" --runtime vscode-copilot  # .github/instructions/*.instructions.md
```

**Anything else** (pi, Antigravity, or a runtime without a preset):

```bash
python3 -m asb_skill_collections.asbb_cli install metabolomics-lc-ms --dest ~/some/skills/dir
```

Every install copies the pack's shipped files into a managed snapshot under
`<destination>/.asbb-units/`, including its leaves, indexes, helpers and workflows.
Local caches, virtual environments and Git metadata are excluded. The advertised
entries identify this installed root for relative paths and commands, naming it
both absolutely and relative to the entry's own directory, so an installation
that is later moved on disk stays usable — and `uninstall`/`install` accept a
`--dest` naming where it was moved to. Skill-native
entries **symlink** to adapters in the snapshot by default; `--copy` (also used by
`--dest`) creates real adapter directories. Rules targets receive rendered files
with the same root instructions. All modes retain their shipped assets after the
checkout is moved or removed; rerun `install` to refresh the snapshot.

`--dry-run` previews without writing. A conflicting entry requires `--force`,
which records its transfer to the new pack. `asbb uninstall <pack> --runtime <id>`
(or `--dest DIR`) removes only unchanged entries still owned by that pack and its
unchanged managed snapshot. Replaced entries and unsafe paths are preserved and
reported. Versions, content identities and ownership are tracked in
`~/.asbb/installed.json`. Skipped entries retain their assets and receipts for
later cleanup; legacy receipts without ownership evidence require manual review.

## MCP server

README (e80767838), section labelled "pending current verification":

> The pinned release audit records a successful checkout stdio trial. This
> rehearsal could not install the optional `mcp` dependency because PyPI DNS
> resolution failed, so no current handshake or host integration is claimed.

Measured 2026-10-30: the `mcp` package (1.27.2) is installed in the maintainer's
local environment, so a stdio handshake can be re-run; it was not run.

## PyPI

README (e80767838), with the link to the private pipeline repository removed:

> **Not on PyPI in v0.** `asb-skill-collections` is unpublished by
> design decision 5 —
> a `pip install asb-skill-collections` from an index would fetch the CLI without
> the corpus it reads, which is not a working install. Publication is deferred to
> v1, once the corpus ships as package data. Maintainers: the (currently dormant)
> release flow is in [`docs/RELEASING_PYPI.md`](RELEASING_PYPI.md).

Measured 2026-10-30: `https://pypi.org/pypi/asb-skill-collections/json` returned 404.

## Documentation site (GitHub Pages)

README (e80767838) linked a Contribute page at
`https://holobiomicslab.github.io/asb-skill-collections/contribute.html`.

Measured 2026-10-30: Pages is not enabled on the repository
(`gh api repos/HolobiomicsLab/asb-skill-collections/pages`: 404; `has_pages: false`).
The Contribute page URL and the site root both returned 404. The site sources
(`docs-site/`) and `.github/workflows/pages.yml` are in the repository. On 2026-11-10 an anonymous request to the site root and to `search.html` returned HTTP 200.
The working
route for an improvement report is `scripts/make_improvement_report.py` or the
`asb-contribute` skill.

## HuggingFace mirror and leaderboard

README (e80767838):

> **HuggingFace mirror & leaderboard** — planned, not yet live.

Measured 2026-10-30: `https://huggingface.co/api/datasets?author=HolobiomicsLab`
returned an empty list; `https://huggingface.co/api/datasets/HolobiomicsLab/asb-metabolomics-v2`
(the name `mirror-to-hf.yml` would use) returned 401, which HuggingFace returns for a
missing or private repository.

## Benchmark and capsules

README (e80767838):

> Only **ASB-Skills** and **ASB-Tools** are published now; the benchmark and capsule
> layers follow (see `<domain checkout>/collections/metabolomics/v2/PROVENANCE.md`).

> **Benchmark / capsules** — to be released later.

Measured 2026-10-30: nothing.

## w3id identifiers

README (e80767838):

> **`w3id.org/holobiomicslab/…` IRIs** — resolve since 2026-09-14
> ([perma-id/w3id.org#6690](https://github.com/perma-id/w3id.org/pull/6690)). The registry, contributors and leaderboard
> IRIs content-negotiate: `Accept: application/ld+json` gets the raw JSON-LD (303),
> a browser gets the GitHub view (302). A collection IRI redirects to its directory.
> All targets follow `main`, not a release tag.

The `w3id.org/asb` vocabularies were registered by
[perma-id/w3id.org#7017](https://github.com/perma-id/w3id.org/pull/7017), merged
2026-10-29 17:31 UTC (#6690 was merged 2026-09-14 09:22 UTC; `gh pr view`).

Measured 2026-10-30 (`curl -sI -m 20`, first hop unless stated):

| IRI | Request | Result |
|---|---|---|
| `https://w3id.org/holobiomicslab/asb-skill/registry` | browser | 302 to `github.com/.../blob/main/catalogue.jsonld` |
| `https://w3id.org/holobiomicslab/asb-skill/registry` | `Accept: application/ld+json` | 303 to `raw.githubusercontent.com/.../main/catalogue.jsonld` |
| `https://w3id.org/holobiomicslab/asb-skill/contributors` | browser / JSON-LD | 302 / 303, as above, to `contributors.jsonld` |
| `https://w3id.org/holobiomicslab/asb-skill/leaderboard/career` | browser / JSON-LD | 302 / 303, as above, to `leaderboard/career.jsonld` |
| `https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2` | browser | 302 to `github.com/.../tree/main/collections/metabolomics/v2` |
| `https://w3id.org/asb` | `Accept: text/turtle`, following redirects | 301 to `/asb/`, 303 to `holobiomicslab.eu/ns/asb`, 303 to `asb.ttl`, 200 `text/turtle` |
| `https://w3id.org/asb/validation` | `Accept: text/turtle`, following redirects | 303 to `holobiomicslab.eu/ns/asbval`, 303 to `asbval.ttl`, 200 `text/turtle` |

## Zenodo DOI and release tag

README (e80767838) used `10.5281/zenodo.20794026` in the badge and
`10.5281/zenodo.20794027` in the text, and announced `metabolomics-v0.2.0`.

Measured 2026-10-30 (`curl` and the Zenodo REST API, `/api/records/20794027` and
`/api/records/20794027/versions`):

- `10.5281/zenodo.20794026` is the **concept DOI** (`conceptdoi` of record
  20794027). `https://doi.org/10.5281/zenodo.20794026` resolves through
  `zenodo.org/doi/...` to `zenodo.org/records/20794027` (200).
- `10.5281/zenodo.20794027` is the **version DOI** of the only version under that
  concept (`hits.total: 1`): title "ASB Metabolomics Skill Collection v2
  (metabolomics-v0.1.0)", version `metabolomics-v0.1.0`, publication date
  2026-06-22, one file `metabolomics-v2.zip` (19,474,788 bytes). Its description
  gives 5,865 skills, 909 tools and 568 papers.
- At that measurement, the repository held 5,859 skills, 909 tools, 566 papers and 21 workflows
  in `<domain checkout>/collections/metabolomics/v2`. `<domain checkout>/collections/metabolomics/v2/.zenodo.json`
  prepares version `metabolomics-v0.2.0`; no such deposit exists yet.
- `git ls-remote --tags origin` shows one release tag, `metabolomics-v0.1.0`;
  `gh release list` shows one pre-release, "ASB Metabolomics Skill Collection
  v0.1.0", of 2026-06-22. There is no `metabolomics-v0.2.0` tag or release.

## Staged collections

README (e80767838):

> The legacy v1 trees for epigenomics, transcriptomics and metabolomics were
> staged/internal and not part of the public plugin release.

Measured 2026-10-30: marketplace sources were
`<domain checkout>/collections/metabolomics/v2` and
`<domain checkout>/packs/metabolomics/*` only. Private domain repositories
(`asb-skills-<domain>`) exist for metabolomics and nine further domains and are
not public. After step 2, the entries use domain-repository `git-subdir`
sources; the full plugin serves v3 and the packs remain v2-derived.
