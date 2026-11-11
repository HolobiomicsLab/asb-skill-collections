# Local build-capsule records

`scripts/pack_capsules.py` turns a released paper view or a plain builds root
into a deterministic, local archive set. It performs no network operation,
deposit, upload, or collection-record change.

First run an advisory pass so failures remain available for diagnosis:

```sh
python scripts/pack_capsules.py \
  --view <paper-view-or-builds-root> \
  --collection <released-collection-root> \
  --out <advisory-output-directory> \
  --date YYYY-MM-DD \
  --access-records <same-doi-access.json>
```

Review its receipts, resolve every failure, then make the release candidate with
a strict pass into a fresh output directory:

```sh
python scripts/pack_capsules.py \
  --view <paper-view-or-builds-root> \
  --collection <released-collection-root> \
  --out <strict-output-directory> \
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
  `build_count` is every considered build; `builds_packed` and
  `builds_left_out` partition it. `capsule_count` is the capsules in packed
  builds and therefore in the record; `capsules_left_out` is the capsules of
  builds the screen left out. `not_released_count` is separate because those
  builds were excluded before screening.
- `capsules.jsonl`: one row per capsule in a packed build. Its `license` is the
  source paper's licence. A Parquet copy with the same rows is optional only
  when `pyarrow` is already installed.
- `SCREEN.json`: `asb-capsules-screen/1`, with totals and per-build failures.
- `benchmark-manifest.json`: capsules whose evaluation definition is
  structurally complete, without a second payload copy. It does not promise
  that they are runnable, their inputs are retrievable, or their checks are
  machine-scorable; its rows and totals expose those readiness measures.
- `zenodo/metadata.json` and `hf/README.md`: local record descriptions.

The generated README field dictionary defines every capsule and benchmark row
field, validation state, evaluation state and screen counter. Validation counts
derived from `claims_checked` are kept separate from counts declared by the
validation summary; disagreement is visible and lowers the state. Generated
record metadata is CC-BY-4.0, paper quotations retain that paper's terms, and
tools retain their own licences.

## Screen order

Every staged JSON, JSONL, JSON-LD, Markdown, YAML and plain-text member is
screened before zipping. Quoted text follows one of three regimes, recorded
per build as `quote_retention` in `MANIFEST.json` and `SCREEN.json`. Open
sources under a Creative Commons licence of any version (BY, BY-SA, BY-NC,
BY-ND and their combinations), CC0, public domain, or an explicit reuse grant
keep their attributed text in full (`full`): each of these licences allows
sharing the text verbatim with attribution. The text stays under the paper's
licence, NonCommercial and NoDerivatives terms included, which the record
README states; the `license` field of each row lets a reader select by licence.
The named function `capsule_screen.allows_verbatim_sharing` holds this rule
(owner's decision of 11 November 2026; the release gate of the skill
collections is stricter and caps NC and ND text). Open sources under any other
licence string keep recognised source fields under 300 characters
per field and 1,500 retained
characters per DOI (`capped`). Restricted, unresolved, licence-less, and
ungranted-preprint sources drop quote text and retain a DOI, location,
offsets, original length, digest and reason (`dropped`).

`capsule_screen.source_text_kind` is the recognition rule used by both the
screen and its output check. Structured properties resolve to their local
name without case distinctions, so `asbval:evidence_quote` and an expanded JSON-LD property name follow
the same rule as `evidence_quote`. The quote properties are `source_excerpt`,
`evidence_quote`, `quote`, `quoted_text`, `verbatim` and `snippet`, including
lists and JSON-LD `@value` objects. Retrieved source passages are the `text`
fields of `passages_used[]` and `substring_hits[]`. A bare `text` or `value`
elsewhere is not enough: generated claims, validator notes, summaries,
prompts and evaluation strategies keep their text. A claim's
`substring_in_paper` flag validates its source excerpt, not the generated
claim text, so it does not widen this rule.

In `evidence/source_snippets.md`, each `## ev_<number>` entry's plain body is
a source field. Its heading and `Source`/`Reason` metadata stay present. An
unstructured source-snippet member is treated as one field. Other evidence
and ledger Markdown uses blockquotes. In `inputs/dataset_preview.md`, the
fenced payloads labelled `paper.md` or `article_fulltext.md` are source fields;
internal Markdown fences do not end a preview wrapper. Other dataset and
repository previews remain. Designated evidence fields
follow the policy even when a trace flag does not establish an exact match.
Removed structured fields remain empty; removed Markdown bodies keep a
`[redacted-quote]` marker. Each shortened or removed field has an anchor in
`_screen_redactions`, or an `asb-redaction` Markdown comment, with the original
length and SHA-256 digest. Metadata and document structure remain available.

One budget is shared by all recognised fields and members of the build's
DOI, in sorted member and mapping-key order and list order. Full retention
still applies the privacy rewrites below. For capped fields, replacements
cannot extend the retained string beyond its allowance, and only the final
retained characters consume the budget. The packer independently reads the
serialized output and records `quotes_after_screen` per build and capsule.
`count` counts non-empty source fields; `characters` and `longest` measure
their final text. Empty fields, markers and anchors contribute no source
characters; `truncated` and `dropped` count transformations. Non-empty source
text in a dropped build, a field over 300 characters in a capped build, or a
capped build over 1,500 characters fails the build and prevents its archive.

A GitHub URL of a
private repository (web, raw or SSH form, with or without `.git` and a trailing
path) then becomes the bare `owner/name`, counted as `private_urls_rewritten`;
other fields, such as a commit hash, are untouched. The private repositories
are the pipeline and every `repository` of `collections.yaml`, read by
`pack_capsules.private_repositories`, which the plan also uses. Emails then
use the release-gate rules. A phone-shaped number is redacted only with a
cue: an international prefix (`+`), an area code of three to five digits in
parentheses that is not a year, or a telephone or fax label (tel, tél,
telephone, phone, fax) at most thirty characters before it on the same line;
right after such a label any grouping of seven to fifteen digits counts.
Digit groups without a cue are the numeric data of a paper (masses, axis
ticks, page ranges, identifiers) and are kept. Build-machine paths
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

A build-machine path is a root marker followed by path characters (anything
but whitespace, quotes, `<>()[]{}` and a comma). `/Users/`, `/Volumes/`,
`/var/folders/` and the macOS `/private/tmp/`, `/private/var/`, `/private/etc/`
are distinctive and count anywhere, so `/System/Volumes/Data/...` is rewritten.
`/home/`, `/root/` and `/tmp/` are ordinary directory names and count only
where an absolute path starts: not after a word character, `.`, `-`, `~` or
`}`, so `test/tmp/` or `${HOME}/tmp/` is left alone, but after a one-letter
option, so `-I/home/...` is rewritten. A drive letter counts only before a
home directory (`C:\Users\<name>\...`, `C:/Users/...`, or
`C:\Documents and Settings\<name>\...`), outside a longer word or URI scheme.
Other drive-shaped text, including LaTeX such as `X:\mathbb` and `x:\quad`,
is kept. Rewrite and residual checks share `MACHINE_ROOT`. A `file:` URI with one or three slashes is
rewritten with its path. A home directory quoted from a paper
(`/home/<name>/...`) is rewritten like a build-machine path: the screen cannot
tell an author's account from the build machine's.

The residual path check is wider than the rewrite, so what the rewrite cannot
handle leaves the build out instead of passing. Any root marker counts, unless
the mention ends there (`in the /tmp/ directory`) or a placeholder
follows (`/tmp/<name>`); a `file:` URI counts when something follows it. A
root marker followed by a quote, a bracket or a comma, or an email redacted
inside a path, is therefore a failure. The release gate of a capsule's RO-Crate
(`crate_problems`) stays a separate check after the screen.

YAML sets and ordered pairs are screened like lists and written as lists; a
binary value is checked, not rewritten. Two mapping keys that become the same
key once screened fail the document rather than lose a value.

Known limits: UNC paths (`\\server\share`), percent-encoded roots and the
absolute paths of other systems (`/opt/`, `/mnt/`, `/data/`, `/scratch/`,
`/srv/`) are not rewritten; the build machine has none of them. A path with a
space is rewritten up to the space.

Residual sensitive content or a deny hit is a build failure. In advisory mode
the failing build is omitted while receipts remain. `--strict` returns
non-zero and removes all generated build archives on any failure, while
retaining the receipts for diagnosis.

The generated metadata relates the collection's Zenodo DOI with
`isSupplementTo` and this public tooling repository with `references`; both
are objects in `related_identifiers`. The pipeline repository,
AgenticScienceBuilder, is private: it is
named in the description and not linked, and the screen rewrites its URLs.
`--pipeline-public`, once that repository is public, adds the `isCompiledBy`
link and the URL in `hf/README.md`, keeps its URLs in the builds, and is
recorded as `inclusion_policy.pipeline_public` in `MANIFEST.json`. The dataset card names the capsules DOI only when it is given (`--capsules-doi`); without it the card points to the collection's registry row.
No existing collection record is modified.

Only builds of papers that the released `corpus.yaml` lists as `included` are
packed. Any other build in the view is not staged, zipped or described; its
slug is listed under `not_released` in `MANIFEST.json`, with
`not_released_count`, and the pack `README.md` states the number.

## From a pack to a published record

`scripts/capsules_deposit.py` takes a pack to a Zenodo record. Every step but
`create` is offline.

At full-pack time, the public projection removes `branch` and `is_dirty` from
every Git entry of `build_manifest.json`, including nested entries, while
keeping commits and all other fields. Each capsule's
`artifact_provenance.json` retains every full-build artifact entry and marks
whether its path is present in the shipped capsule. These projections do not
rewrite the private source build.

1. Pack with the advisory pass and then the strict pass above. Only a successful
   strict output proceeds to deposit planning. A full pack of a large domain
   takes hours.
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
   recorded `pipeline_public` is kept. Refresh refuses legacy capsule rows that
   lack the validation-consistency and evaluation-readiness fields, because it
   does not reopen the copied zips; run a full pack first. Pass
   `--capsules-doi <DOI>` after publication to place the capsules DOI in the
   regenerated HuggingFace card. Without it, the card directs readers to the
   collection registry row and contains no placeholder.
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
   so they can be read on the record page. The pack's `README.md` remains a
   local guide. The uploaded `README.md` is generated by `plan` from the same
   manifest, screen and benchmark counts: it names the record archive and its
   nested layout, explains exclusions and screening, states quotation rights
   and generated-metadata licensing, gives the public takedown route and tells
   readers to cite the record by its DOI. The plan exits non-zero and lists
   each refusal when:
   - a build with a zip shows a screen failure or a deny hit in `SCREEN.json`;
   - a zip is absent from `MANIFEST.json`, or its size or sha256 differs;
   - a zip or a capsule row belongs to a build that is not an included paper
     of the collection, a row names a build the manifest does not list, or
     `capsules.jsonl` or the benchmark listing names a build without a zip;
   - the metadata would be rejected by the deposit API, or its creators differ
     from `scripts/release_creators.yaml`;
   - `isSupplementTo`, or the manifest, does not name the collection's current
     version DOI (run refresh);
   - a URL of a private repository (the pipeline or a domain repository) is in
     a descriptive file or in a text member of a build zip;
   - a local absolute path (`/Users/`, `/Volumes/`, `/private/`) is in a
     descriptive file.

   Its counts are the record holdings: builds packed, builds left out by the
   screen, builds not released, capsules, benchmark capsules and
   `capsules_left_out`. The last field remains a plan and receipt diagnostic;
   `record-doi` writes the established registry block whose `capsules` count is
   the capsules actually held.
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
