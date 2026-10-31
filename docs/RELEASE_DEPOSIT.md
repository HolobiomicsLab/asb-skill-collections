# Zenodo deposit for a collection release

Maintainer procedure. It prepares a new version of an existing Zenodo record up
to a draft. Publishing is a manual step in the Zenodo web interface.

Tool: `scripts/zenodo_deposit.py` (standard library only). Tests:
`tests/test_zenodo_deposit.py`. The tool never calls the publish action of the
API, and has no flag that does.

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
| Metadata template | `collections/<domain>/<vN>/.zenodo.json` |

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
   command exits 1 and prints `rejected by the API:` for each problem.

3. Make a sandbox draft first. The sandbox has no copy of the production record.
   Create and publish a small test record in the sandbox by hand, then pass its
   id.

   ```bash
   export ZENODO_SANDBOX_TOKEN=...
   python scripts/zenodo_deposit.py draft metabolomics v2 --sandbox --record-id <sandbox record id>
   ```

   Open the printed URL and check the title, creators, description, license,
   version, related identifiers, communities, language and the single uploaded
   file.

4. Make the real draft.

   ```bash
   export ZENODO_TOKEN=...
   python scripts/zenodo_deposit.py draft metabolomics v2
   ```

   The output gives the draft URL and the sha256 of the uploaded file. It must
   equal the sha256 from step 1.

5. Publish by hand. In the Zenodo web interface, open the draft, check every
   field, and click Publish. This mints the version DOI and cannot be undone.
   The concept DOI stays the same.

6. Record the new version DOI in the `doi:` field of
   `collections/<domain>/<vN>/CITATION.cff` and in the collection entry of
   `catalogue.jsonld`, in a pull request.

7. Once that pull request is merged, push the release tag on the merged
   commit. With `ZENODO_UPLOAD` unset, `release.yml` runs the tests and the
   strict release gate and makes no Zenodo request.

## What `draft` sends

| Step | Request |
|---|---|
| 1 | `POST /api/deposit/depositions/{record}/actions/newversion` |
| 2 | `GET` the `latest_draft` link from step 1 |
| 3 | `DELETE /api/deposit/depositions/{draft}/files/{file}` for each inherited file |
| 4 | `PUT {bucket}/{domain}-{vN}.zip` with the archive |
| 5 | `PUT /api/deposit/depositions/{draft}` with `{"metadata": {...}}`: the template over the metadata the draft inherited |

Any non-2xx answer stops the run and names the step. A failed run leaves a draft
on Zenodo. Zenodo allows one unpublished new version per record; running `draft`
again reuses it and replaces its files. Discard a draft in the web interface.

## Archive contents

The archive holds `collections/<domain>/<vN>/` under the prefix `<domain>/<vN>/`,
plus three files bundled so the deposit runs grounding on its own:
`scripts/perspicacite_kb_bind.py`, `scripts/requirements.txt` and `AGENTS.md`.
These are the files `release.yml` bundles.

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
This tool does none of these.

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
| Inherited metadata | the draft starts from the previous record. Keys it carries that the template lacks, such as `communities` and `language`, are kept and listed in the output. The template wins on every key it has. `doi` and `prereserve_doi` are never sent. `plan` makes no request and cannot show inherited keys |
| `publication_date` | set to today (`--publication-date` overrides) when the template has none, so the draft does not keep the previous version's date |
| `creators[].name` | the API documents the form `Family name, Given names`. Entity names such as a community or a lab are sent as written, not in that form |

## Alternative: GitHub-Zenodo integration

Zenodo can archive a GitHub release when the repository is enabled in the Zenodo
GitHub settings. It reads `.zenodo.json` or `CITATION.cff` from the repository
root and archives the repository snapshot. This is described in the Zenodo
documentation and was not run for this repository. It does not fit a
per-collection release: the metadata template and the files live under
`collections/<domain>/<vN>/`, and the snapshot is the whole repository.

The release workflow (`.github/workflows/release.yml`) makes the same kind of
draft from CI only when the repository variable `ZENODO_UPLOAD` is `true` and
`ZENODO_TOKEN` is set, and publishes it when `ZENODO_PUBLISH` is `true`.
`ZENODO_UPLOAD` is unset by default. The step sends the template unchanged,
including the `isVersionOf` relation
that the API vocabulary does not list. That was not exercised against a live
deposit here. Use the sandbox draft in step 3 to check it before relying on that
path.
