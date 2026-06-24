# License Clarification Issues

This directory holds the tooling for the ASB Metabolomics license-clarification
issue-wave: a safe-by-default script that opens GitHub issues on upstream tool
repositories asking authors to add an explicit open-source license.

## Purpose

Many computational metabolomics tools in the corpus are hosted on GitHub without
an explicit license. Without a license, "all rights reserved" applies by default,
leaving users uncertain whether (and how) they may use, modify, or redistribute
the tool. The wave sends a single friendly, templated issue to each affected
upstream repository asking the authors to clarify their intent.

## Safety model

The script is conservative by design:

| Property | Detail |
|---|---|
| **Dry-run by default** | Running without `--create` only prints a plan — no issue is ever filed. |
| **`--create` opt-in** | Issues are only filed when `--create` is explicitly passed. |
| **`--limit N` throttle** | Caps the total number of issues to file in a single invocation. |
| **`(owner, repo)` dedup** | Multiple corpus entries pointing to the same GitHub repo yield exactly one issue request. |
| **`already_filed` dedup** | Before creating an issue, the script checks whether a prior "License clarification" issue already exists on the target repo. If one is found, the entry is marked `skipped-exists` and skipped. |
| **GitHub-only** | Only `github.com` URLs (or bare `owner/repo` shorthands) are processed. GitLab, Bitbucket, Codeberg, SourceForge, sr.ht, and any other host are excluded. |
| **Injection guard** | Owner and repo identifiers are validated against `^[A-Za-z0-9][A-Za-z0-9_.-]*$` before any subprocess call. Unsafe values (e.g. `--label`) raise a `ValueError` and are excluded from candidates. |
| **`gh` failure safe** | If `gh issue list` fails (non-zero exit), the entry is marked `skipped-error` rather than silently proceeding to create. |
| **Rate limit** | A 2-second sleep is inserted between consecutive creates (not before the first one). |
| **`wave.yaml` is a runtime artifact** | The output file is `.gitignore`-d — it is generated fresh each run and must not be committed. |

## Run commands

### Step 1 — dry-run (safe, no network writes)

```bash
python3 -m scripts.license_clarification_issues \
    --corpus collections/metabolomics/v2/corpus.yaml
```

Prints a summary and writes the plan to `governance/license_clarification/wave.yaml`
(git-ignored). Inspect it before proceeding.

### Step 2 — file issues (requires `--create`)

File a small batch first to verify the template looks right:

```bash
python3 -m scripts.license_clarification_issues \
    --corpus collections/metabolomics/v2/corpus.yaml \
    --create --limit 5
```

Once satisfied, remove `--limit` or increase it to file the full wave:

```bash
python3 -m scripts.license_clarification_issues \
    --corpus collections/metabolomics/v2/corpus.yaml \
    --create --limit 50
```

Requires `gh` (GitHub CLI) to be authenticated (`gh auth login`).

## Deployment ledger

`governance/license_clarification/deployments.yaml` is a **committed, append-only
record** of every issue we have filed. It uses the schema
`license-clarification-deployments/1`.

### Schema

```yaml
schema: license-clarification-deployments/1
deployments:
- repo: owner/name           # GitHub owner/repo slug
  tool_names: [..]           # corpus tool names linked to this repo
  doi: 10.x/y                # DOI from corpus, or null
  issue_url: https://github.com/owner/name/issues/N
  filed_on: '2026-06-24'     # ISO date the issue was filed
  wave: trial-2026-06-24     # wave identifier
  status: open               # open | responded | license-added | closed | wontfix
  license_after: null        # SPDX id if the repo later adds a license
  last_checked: null         # ISO date of last verify run
```

### Append-on-create

When `--create` is used, the script automatically appends one record per newly
created issue (deduplicated by `repo`). Dry-run mode never touches the ledger.

### Verify workflow

Run `verify` to check the live state of all filed issues and update `status` /
`license_after` in the ledger:

```bash
python3 -m scripts.license_clarification_issues verify
```

This calls `gh` read-only to check:
1. Whether the upstream repo now has an SPDX license → `status: license-added`.
2. Whether the issue was closed → `status: closed`.
3. Whether there are comments → `status: responded`.

After running `verify`, review the output and **commit the updated ledger**:

```bash
git add governance/license_clarification/deployments.yaml
git commit -m "chore(license): verify update <date>"
```

`wave.yaml` remains git-ignored (runtime artifact). `deployments.yaml` is committed.
