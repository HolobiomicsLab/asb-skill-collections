# Paper issue intake

`scripts/intake_issue.py` turns a GitHub issue exported by `gh issue view` into
one proposal row and one machine-readable receipt. It is the local, deterministic
core used by a separate domain Action. It does not call GitHub's issue, label,
comment, pull-request, or merge APIs.

## Command

```bash
python <tooling>/scripts/intake_issue.py --kind paper --issue-json issue.json \
  --domain <slug> \
  --wave-file <domain-checkout>/collections/<slug>/proposals/wave-<YYYY-MM>-community.yaml \
  --covered <corpus>/covered_dois.json \
  --collection-corpus <domain-checkout>/collections/<slug>/v<N>/corpus.yaml \
  --proposal-glob '<domain-checkout>/collections/<slug>/proposals/wave-*.yaml' \
  --proposal-glob '<domain-checkout>/collections/<slug>/proposals/watch-*.yaml' \
  --date YYYY-MM-DD --out receipt.json [--email-env ASB_WATCH_EMAIL] [--dry-run]
```

The issue JSON has the shape returned by `gh issue view --json
number,title,body,author,labels,url,createdAt,updatedAt`. The explicit `--date`
is also the access verification date and monthly wave identifier. `--dry-run`
writes only the receipt. `--kind workflow` is reserved for later implementation
and currently returns a blocked receipt.

Exit code 0 means staged, 1 means blocked, and 2 means duplicate. Only staged
runs add or idempotently update a row. Blocked and duplicate runs never modify
the wave file. The receipt at `--out` is written for every outcome.

## Receipt and issue adapter contract

Every receipt has this shape. Values not established by the resolver are null;
`access` is null only when no identity was staged or deduplicated.

```json
{
  "schema": "asb-intake-receipt/1",
  "outcome": "staged|blocked|duplicate",
  "kind": "paper",
  "issue": 123,
  "domain": "metabolomics",
  "date": "YYYY-MM-DD",
  "doi": "10.... or null",
  "title": "resolved title or null",
  "repository": "public repository URL or null",
  "access": {},
  "code_license": "SPDX identifier or null",
  "warnings": [],
  "duplicate_of": {"where": "covered|corpus|proposal", "path": "file name", "doi": "10...."},
  "row": {},
  "wave_file": "explicit destination path or null",
  "inputs_sha256": {"issue_json": "sha256", "wave_file_before": "sha256 or null"},
  "comment_markdown": "complete issue comment",
  "labels_add": [],
  "labels_remove": []
}
```

For a staged proposal, `labels_add` is `intake-staged` and the removals are
`intake-blocked` and `needs-triage`. A blocked proposal adds `intake-blocked`;
a duplicate adds `duplicate`. The comment includes identity, article access,
article reuse and code licence, and warnings where available. Duplicate comments
use only an existing stage and file name, never a local absolute path or a
private repository URL. Staged comments include: "This is queued for curator
review, not built. The issue remains open until its build lands."

The separate adapter consumes these fields verbatim. No GitHub side effect is
part of this command.

## Trust boundary and decisions

HTML comments are removed and the bold template fields are read as strings.
Bodies and fields have size limits. Links are bare DOIs or HTTPS URLs on a fixed
set of registry and public repository hosts. Shell text is never executed.
Network calls go only to fixed Crossref, DataCite, OpenAlex, Unpaywall, and
GitHub API URLs through an injectable fetcher. Tests use no network.

Crossref resolves ordinary paper DOIs, DataCite resolves software and Zenodo
DOIs, and OpenAlex is metadata fallback. Title search requires a high title
similarity and honors the publisher's expected DOI prefix. Registry-declared
published versions replace preprint DOIs. No missing title or year is invented.

Deduplication checks covered DOIs, the released corpus, and proposal/watch files
in that order. Repository identity alone is not proof of a paper duplicate.
Repository verification happens after duplicate elimination. Article reuse and
code licence remain independent. An unresolved lookup is not called closed.

Only an identified open-access paper with full text reuse rights is staged as
`hold`. Other useful resources remain `candidate` with `triage.decision:
pending` and a reason. A human curator still decides whether to build.

This command never closes an issue, merges or pushes a branch, builds a paper,
changes `included`, executes a proposed repository, or relaxes a licence.
