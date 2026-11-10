# Adding papers to a collection

There are two routes. A contributor can propose one paper without running the
generation pipeline. A maintainer can build papers independently, then periodically
make a new collection cut from all retained builds. A proposal is reviewed and held
for that next cut. It is not inserted directly into a released collection.

Released collections are listed in `collections.yaml`. Each lives in a private
domain repository `asb-skills-<domain>`; for example, metabolomics v3 is in
`asb-skills-metabolomics`. Each domain's content, proposals, candidates and
landing belong in its `asb-skills-<domain>` checkout. This repository holds the
tooling, governance and release registry. Run the `scripts/` commands below
from this tooling checkout; `<domain checkout>` marks the root of the domain
checkout in every content path.

## The two rails

| Rail | Use it for | Result |
|---|---|---|
| Proposal | One paper, tool or resource from a contributor | A reviewed entry under `<domain checkout>/collections/<domain>/proposals/` with `status: hold` |
| Build and cut | A maintainer's batch of new and retained papers | A new candidate branch, version directory, receipts and lineage |

### Contributor rail: propose one paper

Open a **Propose a paper, tool, or resource** issue, or use `/propose-skill` in
a checkout that provides that command. Give a DOI or public link, the target
collection and one or two sentences on why it matters. A curator resolves the
metadata and stages the paper in a `wave-*.yaml` file under
`<domain checkout>/collections/<domain>/proposals/` with `status: hold`.

The shared offline intake command is `python scripts/intake_issue.py --kind
paper`; its full path arguments, receipt, exit codes and trust boundary are in
[`intake-issue.md`](intake-issue.md). It stages `hold` only for a resolved,
open-access paper with full text-reuse rights; unclear or closed submissions
remain `candidate` for curator review. The command never closes the issue,
builds the paper, merges a change or marks a row `included`. Its GitHub comment
and label fields are consumed by a separate domain adapter.

After review, a maintainer builds the held paper. It enters the collection in
the next combined view and cut, not by editing the released version.

Validate paper and resource queues with `python scripts/proposal_corpus.py
validate <domain checkout>/collections/<domain>/proposals/wave-*.yaml`. Their
status vocabulary is `candidate` for machine-discovered proposals awaiting
review, `hold` for curator-queued work, `included` after confirmed landing, and
`rejected` or `duplicate` for explicit dispositions. See
[`proposal-corpus-schema.md`](proposal-corpus-schema.md) for field and
transition rules.

`/propose-skill` is the sibling rail for a complete skill rather than a paper.
It stages under the current version's `proposals/skills/` directory. Maintainers
check those skill proposals, preview promotion and promote a reviewed one with:

```bash
python scripts/check_proposals.py <domain checkout>/collections/<domain>/<current-version>
python scripts/promote_proposals.py --collection <domain checkout>/collections/<domain>/<version> \
  --slug <proposal-slug> --date <YYYY-MM-DD> --dry-run
python scripts/promote_proposals.py --collection <domain checkout>/collections/<domain>/<version> \
  --slug <proposal-slug> --date <YYYY-MM-DD>
```

`promote_proposals.py` moves a reviewed complete skill into the collection and
updates its indexes. It does not turn a paper into skills, run consolidation or
create a release.

### Maintainer rail: build, view, cut and candidate

Each paper is one independent AgenticScienceBuilder build. The input package contains
the article and its metadata; the output directory is unique to that paper.

```bash
asb build <paper-package> --output <increment-root>/<paper-id> --llm \
  --enrich-skills --claim-ledger --skill-bundle --classify \
  --domain-plugin <domain>
```

The November 2026 metabolomics wave averaged about 1.6 hours and USD 0.35 per
paper. That is an observation from that wave, not a budget guarantee. New builds can
therefore be added to an increment root as papers arrive without rebuilding the
released wave.

When a batch is ready, create a fresh per-paper view containing the retained old
builds plus the new builds, one build directory or symlink per paper. Filter that view
under the triage policy used by the current pipeline:

```bash
python <asb-checkout>/scripts/make_filtered_view.py \
  --view <combined-view> --out <filtered-view> \
  --keep promoted,critique --min-yes-rate 0.40
```

Run a new offline consolidation cut. `ASB_EMBED_MODEL` names the locally available
embedding model; this command does not need a hosted embedding service.

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
ASB_EMBED_MODEL=bge-small-en-v1.5 asb consolidate-skills \
  <filtered-view>/<domain> \
  --auto-merge-threshold 0.95 --suggest-threshold 0.90 \
  --cross-run-only --embed-view name_tools
```

Assemble the candidate from that cut and the unfiltered per-paper builds. The tiered
inventory is the paper-access input; the three commits and the filter receipt are
lineage inputs recorded in `source.json`. Assemble into
`<domain checkout>/candidates/<cut-id>/`; its accompanying receipts go into
`<domain checkout>/receipts/<cut-id>/` at landing.

```bash
python scripts/assemble_candidate.py \
  --cut <filtered-view>/<domain>/corpus \
  --builds <combined-view>/<domain> \
  --tiered <tiered-corpus.json> \
  --domain <domain> --version <vN> \
  --out <domain checkout>/candidates/<cut-id> \
  --receipts <domain checkout>/receipts/<cut-id> \
  --asb-commit <asb-commit> --tooling-commit <tooling-commit> \
  --corpus-commit <corpus-commit> --verified-on <YYYY-MM-DD> \
  --view-source <filtered-view>/filter_receipt.json \
  --model bge-small-en-v1.5 --thresholds 0.95,0.90
```

Review the assembled candidate and its gate report, then preview and perform the local
landing from a clean `asb-skills-<domain>` collection repository on `main`:

```bash
python scripts/land_candidate.py \
  --candidate <domain checkout>/candidates/<cut-id> \
  --receipts <domain checkout>/receipts/<cut-id> \
  --repo <domain checkout> --domain <domain> --version <vN> \
  --title "<Collection title>" --author-name "<name>" \
  --author-email "<email>" --dry-run
python scripts/land_candidate.py \
  --candidate <domain checkout>/candidates/<cut-id> \
  --receipts <domain checkout>/receipts/<cut-id> \
  --repo <domain checkout> --domain <domain> --version <vN> \
  --title "<Collection title>" --author-name "<name>" \
  --author-email "<email>"
```

Landing creates a local `candidate/<cut-id>` branch and commits
`<domain checkout>/collections/<domain>/<vN>/`, `<domain checkout>/receipts/<cut-id>/`
and the marketplace update in that checkout. It does not push, merge or release
the candidate.

## What is incremental and what is batch

Builds are incremental because one paper's output does not depend on another paper's
build. Consolidation is deliberately batch-scoped: similarity groups and canonical
skills depend on the complete set of papers in the view. Adding one paper can change
clusters formed from earlier papers.

The cut writer therefore leaves an identical existing `corpus/skills/` tree untouched
and refuses a differing cut before writing. To add papers, make a new combined view
and a new cut rather than modifying the old cut in place. Candidate assembly derives
the 12-character `cut_id` from the cut's `coverage_summary.json`, writes a complete
receipt set, and records the view, source commits, thresholds and candidate-tree
digest in `source.json`. Landing uses that identity for both the candidate branch and
the receipt directory. Waiting for a command or receiving its output is not review:
the candidate still needs human review before the normal release procedure.

## Recommended cadence

Build papers as they arrive, including every few days if useful. Rebuild the combined
view and make a fresh cut every few weeks, or when a coherent review batch has
accumulated. This keeps paid, independent builds moving while reserving the offline
clustering, candidate review and release work for a batch.

## Version limitation

The current assembly and landing scripts accept only `v<N>`, where `N` is a positive
integer such as `v3` or `v4`. They reject a minor directory such as `v3.1`. A re-cut
must therefore land in a new integer version directory today. Minor collection
versions require a future tooling change; do not encode one by hand.

## Automated staging

A `propose` issue labelled `paper-intake` is processed by the domain repository's
intake Action, which parses the issue, resolves the DOI and access route, checks
duplicates against the collection corpus and the open wave and watch files, and
stages one row with `status: hold` and `triage.decision: pending` on
`bot/intake-paper-<issue>`. It opens one pull request, comments its findings on
the issue and labels it `intake-staged` or `intake-blocked`; a definite duplicate
is commented and labelled `duplicate` without a branch. The bot never closes the
issue, merges, builds or marks a row `included`. Curator review, `accept`, the
build and the release stay manual, and the issue stays open until its build lands.
