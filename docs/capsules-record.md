# Local build-capsule records

`scripts/pack_capsules.py` turns a released paper view or a plain builds root
into a deterministic, local archive set. It performs no network operation,
deposit, upload, or collection-record change.

```sh
python scripts/pack_capsules.py \
  --view <paper-view-or-builds-root> \
  --collection <released-collection-root> \
  --out <local-output-directory> \
  --date YYYY-MM-DD \
  --access-records <same-doi-access.json> \
  --strict
```

Use `--limit N` for the first N builds in sorted order, `--with-indicium` to
add build knowledge graphs, and `--deny-patterns-file` for runtime-only
literal, case-insensitive strings. Deny strings are never printed or written
to receipts. The release date and tooling commit are explicit receipt values;
importable code never reads the clock.

## Archive layout

- `builds/<build-slug>.zip`: one sorted, fixed-timestamp archive per passing
  build. It contains the slim-plus capsule set, build ledger and manifests.
- `MANIFEST.json`: `asb-capsules-manifest/1`, including source digests, archive
  sizes and hashes, access, validation, evaluation and per-build screen data.
- `capsules.jsonl`: one row per capsule. A Parquet copy is optional only when
  `pyarrow` is already installed.
- `SCREEN.json`: `asb-capsules-screen/1`, with totals and per-build failures.
- `benchmark-manifest.json`: the complete operational-evaluation subset,
  without a second payload copy.
- `zenodo/metadata.json` and `hf/README.md`: local record descriptions.

## Screen order

Every staged JSON, JSONL, JSON-LD, Markdown, YAML and plain-text member is
screened before zipping. Quoted text follows one of three regimes, recorded
per build as `quote_retention` in `MANIFEST.json` and `SCREEN.json`. Open
sources under a permissive licence (the CC-BY family, CC0, public domain, or
an explicit reuse grant) keep their attributed text in full (`full`). Open
sources under any other licence string keep structured quote fields and
evidence blockquotes under 300 characters per field and 1,500 retained
characters per DOI (`capped`). Restricted, unresolved, licence-less, and
ungranted-preprint sources drop quote text and retain a DOI, location,
offsets, original length, digest and reason (`dropped`). A GitHub URL of a
private repository (web, raw or SSH form, with or without `.git` and a trailing
path) then becomes the bare `owner/name`, counted as `private_urls_rewritten`;
other fields, such as a commit hash, are untouched. The private repositories
are the pipeline and every `repository` of `collections.yaml`, read by
`pack_capsules.private_repositories`, which the plan also uses. Emails and
phone-shaped values then use the release-gate rules. Build-machine paths
become build locators and RO-Crates use the canonical release pruning rule.
The optional deny list runs last.

In a JSON, JSONL, JSON-LD or YAML document these rewrites, and the residual
check below, apply to the decoded strings (values and mapping keys), and the
document is then serialized again, so a rewrite never runs through an escape
or a line break of the serialization. A YAML document that nothing changed
keeps its source text unless that text holds something to screen outside its
values, a comment for example. Markdown, plain text, CSV and TSV members, and a
document that does not parse (already a failure), are rewritten and checked as
text. Deny-list patterns are counted on the final text of every member.

A build-machine path is a root marker followed by at least one path character
(anything but whitespace, quotes, `<>()[]{}` and a comma). `/Users/`,
`/Volumes/` and `/var/folders/` count anywhere, so `/System/Volumes/Data/...`
is rewritten. `/home/`, `/tmp/` and `/private/` are ordinary directory names and count
only where an absolute path starts: not after a word character, `.`, `-`,
`~`, `}`, `)`, `>` or `*`, so `test/tmp/` or `${HOME}/tmp/` is left alone. A
drive letter counts when it is not part of a longer word or URI scheme and its
separator is followed by a path character, so `C:\Users\...` is rewritten
and a bare `D:/ ` is not. A `file://` URI is rewritten with its path; one that
is followed by anything else is a residual. The rewrite and the residual check
share this rule, so the check verifies that the rewrite was complete. The
release gate of a capsule's RO-Crate (`crate_problems`) is wider: it also
counts a root marker with nothing after it and any `file://`, and stays a
separate check after the screen. A home directory quoted from a paper
(`/home/<name>/...`) is rewritten like a build-machine path: the screen cannot
tell an author's account from the build machine's.

Residual sensitive content or a deny hit is a build failure. In advisory mode
the failing build is omitted while receipts remain. `--strict` returns
non-zero and removes all generated build archives on any failure, while
retaining the receipts for diagnosis.

The generated metadata links the collection's Zenodo DOI and this tooling
repository. The pipeline repository, AgenticScienceBuilder, is private: it is
named in the description and not linked, and the screen rewrites its URLs.
`--pipeline-public`, once that repository is public, adds the `isCompiledBy`
link and the URL in `hf/README.md`, keeps its URLs in the builds, and is
recorded as `inclusion_policy.pipeline_public` in `MANIFEST.json`. A capsules DOI placeholder remains until the owner publishes the record.
No existing collection record is modified.

Only builds of papers that the released `corpus.yaml` lists as `included` are
packed. Any other build in the view is not staged, zipped or described; its
slug is listed under `not_released` in `MANIFEST.json`, with
`not_released_count`, and the pack `README.md` states the number.

## From a pack to a published record

`scripts/capsules_deposit.py` takes a pack to a Zenodo record. Every step but
`create` is offline.

1. Pack, as above. A full pack of a large domain takes hours.
2. Refresh, when the collection has moved since the pack (a patch release
   changes the version DOI and label):

   ```sh
   python scripts/capsules_deposit.py refresh --pack <pack> \
     --collection <released-collection-root> --out <new-pack> --date YYYY-MM-DD
   ```

   The descriptive files are rewritten by the code the packer uses, so they
   are what a full pack with the same inputs would write. Each build zip is
   copied unchanged after its size and sha256 are checked against
   `MANIFEST.json`. Builds whose paper is no longer an included paper of the
   corpus are dropped and listed under `not_released`. The source pack is never
   written. The screen is not rerun: a change of the collection's roles,
   access records or private repositories needs a full pack, and the pack's
   recorded `pipeline_public` is kept.
3. Plan:

   ```sh
   python scripts/capsules_deposit.py plan --pack <new-pack> \
     --collection <released-collection-root> --out <plan-dir> --date YYYY-MM-DD
   ```

   It writes `<plan-dir>/upload/asb-<domain>-v<N>-build-capsules.zip` and
   `<plan-dir>/deposit-plan.json`, and prints the metadata, the files with
   size, sha256 and md5, and the refusals. Zenodo accepts at most 100 files
   per record by default, so the build zips travel inside one archive: stored
   without recompression, sorted, with fixed timestamps and modes, beside the
   descriptive files. `README.md`, `MANIFEST.json`, `capsules.jsonl`,
   `SCREEN.json` and `benchmark-manifest.json` are also uploaded on their own
   so they can be read on the record page. The plan exits non-zero and lists
   each refusal when:
   - a build with a zip shows a screen failure or a deny hit in `SCREEN.json`;
   - a zip is absent from `MANIFEST.json`, or its size or sha256 differs;
   - a zip or a capsule row belongs to a build that is not an included paper
     of the collection, or a row names a build the manifest does not list;
   - the metadata would be rejected by the deposit API, or its creators differ
     from `scripts/release_creators.yaml`;
   - `isSupplementTo`, or the manifest, does not name the collection's current
     version DOI (run refresh);
   - a URL of a private repository (the pipeline or a domain repository) is in
     a descriptive file or in a text member of a build zip;
   - a local absolute path (`/Users/`, `/Volumes/`, `/private/`) is in a
     descriptive file.
4. Draft, from the owner's terminal, with `ZENODO_TOKEN` (or
   `ZENODO_SANDBOX_TOKEN` and `--sandbox`) in the environment:

   ```sh
   python scripts/capsules_deposit.py create --plan <plan-dir>/deposit-plan.json
   ```

   It refuses a plan with refusals and a stale plan (a file whose size, sha256
   or md5 no longer matches). It creates a new record, uploads the six files,
   checks the size and md5 Zenodo stores for each, sets the metadata, and
   prints the draft address. It never publishes. As soon as the draft exists
   it writes `draft.json` (`draft-sandbox.json` with `--sandbox`) beside the
   plan with the draft id, concept record id, address, host and whether the
   setup finished. A second run with that file present refuses, so a script
   rerun after a failure halfway does not create a second draft; `--again`
   creates another one.
5. Publish: the owner checks the draft in the Zenodo web interface and clicks
   Publish. Publishing mints the DOI and cannot be undone.
6. Record:

   ```sh
   python scripts/capsules_deposit.py record-doi --plan <plan-dir>/deposit-plan.json \
     --doi <version DOI> --concept-doi <concept DOI> --record-id <id> \
     --manifest collections.yaml [--published YYYY-MM-DD]
   ```

   It writes a `capsules` block on the released version's row of
   `collections.yaml` (version and concept DOI, record id, the version DOI the
   record supplements, builds packed, left out and not released, capsules,
   benchmark capsules, archive size and sha256, and the publication date:
   `--published`, by default the plan's date), adds the
   capsules DOI to that domain's version DOI cell in the `README.md`
   collections table, regenerates `catalogue.jsonld` (the documentation site
   shows `capsules_doi` beside the version DOI), and runs
   `scripts/check_collections_manifest.py`. When that check fails, the three
   files are restored. A row without the block stays valid and shows nothing.
   A later patch release of the same version keeps the block.
