# Zenodo deposit for a collection release

Maintainer procedure. It prepares a new version of an existing record or a new
first-release record up to a draft. Publishing is a manual step in the Zenodo
web interface.

Tool: `scripts/zenodo_deposit.py` (standard library and PyYAML, a dependency
of the package). Tests: `tests/test_zenodo_deposit.py`,
`tests/test_zenodo_deposit_bundle.py`, `tests/test_zenodo_deposit_creators.py`
and `tests/test_zenodo_deposit_domain.py`. The tool never calls the publish
action of the API, and has no flag that does.

## Orchestrated release

`scripts/release_domain.py` coordinates the release across the domain checkout,
this tooling checkout and, when supplied, the hub. The common invocation is:

```bash
python scripts/release_domain.py <stage> --domain <slug> --version v<N> \
  --repo-root <domain checkout> --tooling-root <this checkout> \
  --state <path to release_state.json> [stage options]
```

| Stage | Action and durable result |
|---|---|
| `gate` | Runs the strict release gate and surface check; records the verdict and receipt digest. `--candidate` selects a pre-landing tree. |
| `land` | Dry-runs `land_candidate.py`, then lands only with `--execute`; requires `--candidate`, `--receipts` and `--title`. Records the branch and commit. |
| `deposit-plan` | Prepares the archive and metadata offline with `--record-id` and repeatable `--extra-file`; records their digests. `--first-release` instead prepares a new record with no record id and refuses an existing domain lineage. |
| `deposit-draft` | Reuses a pending next-version draft or creates the first one, replaces every file and applies the inherited metadata fix. With `--first-release`, it finds a matching unpublished draft by title and version or creates a new record. Refuses an archive digest different from the plan. `--sandbox` selects the sandbox. |
| `record-doi` | Requires `--doi`; updates collection and root CITATION.cff, the README release row and, when present, the USAGE citation, the collection `.claude-plugin/plugin.json` `version` and the `version` of the root `.claude-plugin/marketplace.json` entry whose `source` is `./<release path>` (both set to the release label without `v`). All contents are computed before any write, so a refusal (for example a README without the release row) changes nothing. `.zenodo.json` is unchanged. `--hub-root` also invokes the hub's release-manifest emitter. |
| `receipt` | Regenerates the strict receipt, verifies it and repeats the surface check. The report is `receipts/<cut-id>/gate_report.json` when that directory exists, otherwise `gate_report.json` in the collection. Refuses untracked files in the release path, which would enter the payload binding. |
| `manifest` | Requires the merged DOI commit in `--commit`; reads the tree digest from git objects at that commit and refuses when the release path in the checkout differs from it or holds untracked files. Upserts `collections.yaml` in its existing layout, regenerates the catalogue and validates the checkout. Repeatable `--checkout <domain>=<path>` adds other domain checkouts to the catalogue, index and check. `--regen` also rebuilds the search index and refuses unless every registry domain has a checkout. A new domain requires `--concept-doi`. |
| `tag` | Prints the exact tag and push commands for the DOI merge commit. `--verify` checks the remote tag after the owner pushes it. |
| `status` | Prints each recorded stage, its inputs, outputs and digests, and the next unfinished stage. |

The state file uses schema `asb-release-state/1` and records UTC timestamps,
the domain HEAD at each stage, commands with exit codes, digests and owner
prompts. A completed stage with identical inputs prints `unchanged; no-op`;
`--force` repeats it. `--resume` continues through prepared stages and stops at
the next owner dependency. The Markdown stage log is
`receipts/<cut-id>/release_log.md` when those receipts exist, otherwise beside
the state file. An explicit `--receipts` also selects the log location for a
read-only domain checkout.

Exit status 0 means the requested stage is done, 1 means refusal with a reason,
and 2 means an owner's act is next. Merges, the Zenodo publish click, tag
creation and push, and repository visibility remain the owner's. They appear as
`OWNER:` commands or prompts and are never executed by the orchestrator.

### Release label and patch releases

The release label is the collection's `.zenodo.json` `version`, written
`v<major>.<minor>.<patch>` with the major of `--version` (`v<N>.0.0` when the
field is absent). The default tag is `<domain>-<label>`; `--tag-name` overrides
it. A `.0.0` label names its DOI by the major (`Zenodo version DOI of v3`). A
later label, for example `v3.0.1`, is a new Zenodo version of the same
collection path:

- both CITATION files gain an identifier `Zenodo version DOI of v3.0.1` and keep
  the earlier DOIs of the major; the collection `doi` field moves to the new DOI;
- the USAGE paragraph changes only its version DOI and keeps its other clauses;
- the README row's Released and DOI cells move to the patch;
- the plugin version becomes the label without its `v` (`3.0.1`) in the
  collection `plugin.json` and in the marketplace entry of the collection path;
  other marketplace entries keep their bytes;
- the registry row of the major takes the new tag, commit, digest, DOI, date and
  counts, and lists the values it replaces under `superseded`.

The earlier tag stays where it is; tags never move.

Every release sets the plugin version the same way: `1.0.0` for a `v1.0.0`
label, `2.0.0` for `v2.0.0`, `3.0.1` for `v3.0.1`. Candidates keep `0.1.0` until
`record-doi`. The edit replaces only the version value, and the stage refuses
when the text cannot be edited that way.

## Order of a release

1. The Zenodo version is made with this tool and published by hand (procedure
   below).
2. Its version DOI is recorded in a pull request.
3. The release tag `<domain>-v<release version>` is pushed after that pull
   request is merged.

The tag runs `.github/workflows/release.yml`. Its Zenodo step runs only when
the repository variable `ZENODO_UPLOAD` is `true`, and the variable is unset by
default, so the tag run makes no Zenodo request. Zenodo keeps one unpublished
new version per record: a draft made by the workflow would collide with the
draft made here. Use one deposit path per release.

## Prerequisites

| Item | Value |
|---|---|
| Production token | environment variable `ZENODO_TOKEN` |
| Sandbox token | environment variable `ZENODO_SANDBOX_TOKEN` |
| Token scopes | `deposit:write` and `deposit:actions` (newversion needs `deposit:actions`; file and metadata calls need `deposit:write`) |
| Record to version from | the latest published version record id, not the concept id |
| Metadata template | `<domain checkout>/collections/<domain>/<vN>/.zenodo.json` |

The tokens are read from the environment only and are never printed. Create them
in the Zenodo account settings (Applications, Personal access tokens). The
sandbox is a separate service with separate accounts and records.

For `metabolomics`, the template names record `20794027` (version
`metabolomics-v0.1.0`) in an `isVersionOf` relation. The tool reads the record id
from that relation. `--record-id` overrides it.

## Procedure

Run from the repository root, on the commit that carries the release.

1. Build the archive and note the sha256.

   ```bash
   python scripts/zenodo_deposit.py archive metabolomics v2
   ```

   Output: path (`dist/zenodo/metabolomics-v2.zip`), sha256, size, entry count.

2. Print the plan. No network.

   ```bash
   python scripts/zenodo_deposit.py plan metabolomics v2
   ```

   Check the target host, the record id, the metadata and the file list. The
   command exits 1 and prints `rejected by the API:` for each problem, and
   `refused:` when the template's creators do not start with
   `scripts/release_creators.yaml` (see Metadata handling). `draft` stops on the same conditions
   before any request.

3. Make a sandbox draft first. The sandbox has no copy of the production record.
   Create and publish a small test record in the sandbox by hand, then pass its
   id.

   ```bash
   export ZENODO_SANDBOX_TOKEN=...
   python scripts/zenodo_deposit.py draft metabolomics v2 --sandbox --record-id <sandbox record id>
   ```

   Open the printed URL and check the title, creators, description, license,
   version, related identifiers, communities, language and the uploaded files.

4. Make the real draft.

   ```bash
   export ZENODO_TOKEN=...
   python scripts/zenodo_deposit.py draft metabolomics v2
   ```

The output gives the draft URL and the sha256 of each uploaded file. The archive
sha256 must equal the sha256 from step 1.

5. Publish by hand. In the Zenodo web interface, open the draft, check every
   field, and click Publish. This mints the version DOI and cannot be undone.
   The concept DOI stays the same.

6. Record the new version DOI in the `doi:` field of
   `<domain checkout>/collections/<domain>/<vN>/CITATION.cff` and in the collection entry of
   `catalogue.jsonld`, in a pull request. `CITATION.cff` is bound by the
   collection's gate receipt, so regenerate the receipt in the same pull
   request with `python scripts/release_gate.py <domain checkout>/collections/<domain>/<vN> --strict`,
   in an environment where the AgenticScienceBuilder package is not importable
   (see the receipt job of `validate.yml`); otherwise that job fails.

7. Once that pull request is merged, push the release tag on the merged
   commit. With `ZENODO_UPLOAD` unset, `release.yml` runs the tests and the
   strict release gate and makes no Zenodo request.

### First release of a domain

A first release creates the domain's Zenodo lineage. There is no previous
record, so do not pass `--record-id`. Use the same staged release procedure
with `--first-release` on the two deposit stages:

```bash
python scripts/release_domain.py deposit-plan --domain <domain> --version v1 \
  --repo-root <domain checkout> --tooling-root <this checkout> \
  --state <path to release_state.json> --first-release
python scripts/release_domain.py deposit-draft --domain <domain> --version v1 \
  --repo-root <domain checkout> --tooling-root <this checkout> \
  --state <path to release_state.json> --first-release
```

The plan refuses a registry entry that already has a concept DOI. The draft
stage reuses an unpublished deposition whose title and version match the
template, or creates a new deposition. The template receives the
`asb_skill_collections` community when it has none; an existing communities
value is preserved. An `isNewVersionOf` relation is refused.

The direct equivalent of the second command is:

```bash
python scripts/zenodo_deposit.py create <domain> v1 --repo-root <domain checkout> \
  --tooling-root <this checkout>
```

`create` uploads the archive and extras, then sends only the template metadata,
without inherited values. It prints the draft URL and `conceptrecid`. Neither
command publishes.

The owner reviews and publishes the draft in Zenodo. Publishing mints both the
version DOI and the domain's concept DOI. Read them from the published record,
then record the version DOI and, after the usual receipt and DOI pull request
merge, the concept DOI:

For a first release, `record-doi` reads the published record without a token,
prints the concept DOI and stores it in the stage log. `manifest` then defaults
`--concept-doi` to that value when the flag is absent and the registry entry has
no concept DOI yet.

```bash
python scripts/release_domain.py record-doi ... --doi <version DOI>
python scripts/release_domain.py receipt ...
python scripts/release_domain.py manifest ... --commit <merged DOI commit> \
  --concept-doi <concept DOI>
```

Finish with the usual receipt, merged DOI change, tag and repository visibility
gates. Later versions use the normal `draft` path and keep the same concept DOI.

## What `draft` sends

| Step | Request |
|---|---|
| 1 | `POST /api/deposit/depositions/{record}/actions/newversion` |
| 2 | `GET` the `latest_draft` link from step 1 |
| 3 | `DELETE /api/deposit/depositions/{draft}/files/{file}` for each inherited file |
| 4 | `PUT {bucket}/{domain}-{vN}.zip` with the archive |
| 5 | `PUT {bucket}/{file name}` for each `--extra-file`, in the order given |
| 6 | `PUT /api/deposit/depositions/{draft}` with `{"metadata": {...}}`: the template over the metadata the draft inherited |

Any non-2xx answer stops the run and names the step. A failed run leaves a draft
on Zenodo. Zenodo allows one unpublished new version per record; running `draft`
again reuses it and replaces its files. Discard a draft in the web interface.

## Archive contents

The archive holds the domain repository's collection directory under the prefix `<domain>/<vN>/`,
plus three files bundled so the deposit runs grounding on its own:
`scripts/perspicacite_kb_bind.py`, `scripts/requirements.txt` and `AGENTS.md`,
and the license texts at their repository paths: `LICENSING.md` (which license
covers which layer), `LICENSE` (the Apache-2.0 text) and
`governance/LICENSE_TIERS.md` (the per-skill license tiers). A missing license
text stops the build. These are the files `release.yml` bundles.

Extra files passed with repeatable `--extra-file` options on `plan` and `draft`
are listed beside the archive with their size and sha256, then uploaded after
the archive. They are not added to the zip. `archive` does not accept this
option, and a missing extra file stops `draft` before its first request.

- Entries are sorted by name. Timestamps are fixed to 1980-01-01. File modes are
  `0755` for files with the user execute bit and `0644` otherwise.
- Paths with a `__pycache__` component are left out. So is any path with a
  component starting with `.`, except `.zenodo.json`. This leaves out the
  collection's `.claude-plugin/` directory and any `.cache/` directory.
- Two builds of the same tree give the same sha256 on one machine. DEFLATE output
  is not specified bit for bit, so a different zlib build can give a different
  sha256 for the same tree. Compare hashes from one machine.

When its Zenodo step is on (`ZENODO_UPLOAD` is `true`), `release.yml` differs:
it keeps dotfiles (so its archive carries `.claude-plugin/plugin.json`), uploads
`.cache/leafemb_v<N>.npz` as a second file `<domain>-v<N>-leafemb.npz` when
present, and publishes when the repository variable `ZENODO_PUBLISH` is `true`.
This tool still keeps neither collection dotfiles nor collection caches in the
zip and never publishes; an external cache can be uploaded with `--extra-file`.

## Domain repositories

A release repository may hold only its collection and release content, without
the master's tooling and governance directories. Pass the master checkout as
`--tooling-root` to `archive`, `plan` or `draft`. Every bundled, licence and
creators file resolves from `--repo-root` first, then from the tooling root;
archive paths stay under `<domain>/<vN>/` and do not change. Without the option,
the repository holding the running script is the tooling root. Existing master
checkouts retain their repository files, and an archive built from one is
unchanged by an explicit empty tooling root.

`plan` prints both roots and the root that supplied each resolved file.
`LICENSING.md` and `LICENSE` are release content: the tooling root is only a
fallback, and a tooling-supplied `LICENSING.md` adds a notice that its text may
differ from the domain repository's. A file absent from both roots stops the
command with both roots named.

For the `asb-skills-metabolomics` v3 deposit, the command sequence is:

```bash
python <path to asb-skill-collections>/scripts/zenodo_deposit.py archive metabolomics v3 \
  --repo-root <path to asb-skills-metabolomics> \
  --tooling-root <path to asb-skill-collections>
python <path to asb-skill-collections>/scripts/zenodo_deposit.py plan metabolomics v3 \
  --repo-root <path to asb-skills-metabolomics> \
  --tooling-root <path to asb-skill-collections> \
  --record-id 20794027 --publication-date 2026-11-09 \
  --extra-file <path to leafemb_metabolomics.npz>
python <path to asb-skill-collections>/scripts/zenodo_deposit.py draft metabolomics v3 \
  --repo-root <path to asb-skills-metabolomics> \
  --tooling-root <path to asb-skill-collections> \
  --record-id 20794027 --publication-date 2026-11-09 \
  --extra-file <path to leafemb_metabolomics.npz>
```

The extra file is uploaded as `leafemb_metabolomics.npz`, after the archive.
The draft remains unpublished for manual review.

## Metadata handling

The template keeps the metadata at the top level of the file. The API wants it
under `metadata`; the tool wraps it.

| Item | Handling |
|---|---|
| Keys | checked against the deposit metadata list at https://developers.zenodo.org (read 2026-10-30); an unknown key stops `draft` |
| `upload_type`, `access_right` | checked against the controlled vocabulary |
| `license` | required when `access_right` is `open` or `embargoed` |
| `related_identifiers[].relation` | checked against the API vocabulary |
| `isVersionOf` | not in the API vocabulary. The tool reads the record id from it and does not send it. Zenodo links the versions of a record itself |
| Inherited metadata | the draft starts from the previous record. Keys it carries that the template lacks, such as `communities` and `language`, are kept and listed in the output. The template wins on every key it has. `doi` and `prereserve_doi` are never sent; an inherited `dates` entry without `start` or `end` (the web interface can store one) is dropped and counted in the output, since the API rejects it with 400 "Invalid date provided". `plan` makes no request and cannot show inherited keys |
| `publication_date` | set to today (`--publication-date` overrides) when the template has none, so the draft does not keep the previous version's date |
| First-release community | `create` and `deposit-draft --first-release` add `asb_skill_collections` only when the template has no communities value. No metadata is inherited, and an `isNewVersionOf` relation stops the command |
| `creators[].name` | the API documents the form `Family name, Given names`. Entity names such as a community or a lab are sent as written, not in that form |
| `creators` | must start with `scripts/release_creators.yaml`, unchanged and in order: a person entry as `Family, Given` with its bare ORCID iD and affiliation when listed, an entity entry by its name. Entries after the list are accepted only as persons with a bare ORCID iD, each iD once: the co-authors that `scripts/select_release_coauthors.py --apply` appends (see `docs/CURATION_CALL.md`). Any other difference is refused by `plan` and `draft` |

## Alternative: GitHub-Zenodo integration

Zenodo can archive a GitHub release when the repository is enabled in the Zenodo
GitHub settings. It reads `.zenodo.json` or `CITATION.cff` from the repository
root and archives the repository snapshot. This is described in the Zenodo
documentation and was not run for this repository. It does not fit a
per-collection release: the metadata template and the files live under
`<domain checkout>/collections/<domain>/<vN>/`, and the snapshot is the whole repository.

The release workflow (`.github/workflows/release.yml`) makes the same kind of
draft from CI only when the repository variable `ZENODO_UPLOAD` is `true` and
`ZENODO_TOKEN` is set, and publishes it when `ZENODO_PUBLISH` is `true`.
`ZENODO_UPLOAD` is unset by default. Before its first request the step stops
when a license text is missing or when the creators of a checked-in
`.zenodo.json` do not start with `scripts/release_creators.yaml`, by the rule
of `plan` and `draft`. It then sends the template unchanged,
including the `isVersionOf` relation
that the API vocabulary does not list. That was not exercised against a live
deposit here. Use the sandbox draft in step 3 to check it before relying on that
path.
