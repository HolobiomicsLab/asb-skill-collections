# Release Rollback Runbook

This document is the runbook for withdrawing a tagged ASB-Skill collection
release after it has shipped. It applies when a published `<slug>-v<N>`
release must be retracted post-publication.

## When to invoke

Rollback is appropriate when one or more of the following becomes true
**after** a release has been tagged, deposited to Zenodo, and mirrored to
HuggingFace:

- A source paper in the corpus has been **retracted** by its publisher.
- An **author opt-out** request (see `AUTHOR_OPT_OUT.md`) covers content
  in the tagged release.
- A **plagiarism or fraud** finding affects derived skills / tools / claims.
- A **court order** or formal legal notice requires removal.
- A **critical correctness bug** in derived content is discovered (e.g.
  systematically wrong claim extraction, license-handling error,
  cross-contaminated provenance).

Routine corrections — typos, minor description fixes, single-skill bugs that
do not affect the integrity of the release as a whole — should ship as a
normal `<slug>-v<N+1>` minor release, not a rollback.

## Approval

- **Non-emergency rollback:** requires Lead Curator (of the affected
  collection) **plus** one maintainer.
- **Emergency rollback** (retraction, fraud, court order, GDPR Art. 17,
  active reputational harm): the **lead maintainer can act unilaterally**,
  with post-hoc notification of the Lead Curator.

## Procedure (7 steps)

### 1. Open a rollback issue

File a GitHub Issue titled `[ROLLBACK] <slug>-v<N>: <one-line reason>`.
The body documents:

- Affected release tag(s) (e.g. `metabolomics-v1.0.0`)
- Affected papers / DOIs
- Affected derived artifacts (skill / tool / benchmark IDs)
- Reason and supporting links (retraction notice, opt-out issue, etc.)
- Approver signatures (Lead Curator + maintainer GitHub handles)

### 2. Identify affected releases

Enumerate every Zenodo deposition DOI and every HuggingFace dataset card
that contains the affected content. Releases prior to ingestion of the
affected paper are **not** withdrawn.

### 3. Update Zenodo depositions

For each affected Zenodo DOI:

- Mark the deposition as **withdrawn** via the Zenodo REST API
  (`POST /api/deposit/depositions/<id>/actions/edit` -> update
  `metadata.notes` and `access_right` -> `publish`). Add a note linking
  the rollback issue.
- **Note:** Zenodo records cannot be deleted; "withdrawn" is the strongest
  available state and is permanent.

### 4. Push a patched release

Cut a new patch release that contains the rollback fix:
e.g. `metabolomics-v1.0.0` -> `metabolomics-v1.0.1`. The patch release:

- Removes the affected content (per `AUTHOR_OPT_OUT.md` rules, or per
  the rollback's specific scope)
- Adds an entry to `CHANGELOG.md` under a `### Withdrawn` heading citing
  the rollback issue
- Bumps the collection's `version` field in `corpus.yaml`

### 5. Update the HuggingFace mirror

- Delete the affected dataset card via the HF API
  (`DELETE /api/datasets/<owner>/<dataset>`), or — if the dataset
  contains other valid releases — push a new revision that omits the
  withdrawn content and update the dataset README to link the rollback
  issue.
- Trigger `mirror-to-hf.yml` against the patched release tag.

### 6. Mark the original tag as withdrawn

In the repo:

```bash
git tag <slug>-v<N>-withdrawn <slug>-v<N>
git push origin <slug>-v<N>-withdrawn
```

The original `<slug>-v<N>` tag itself is **retained** in git history (so
external references resolve), and a sibling `-withdrawn` tag flags its
status. Force-pushing the original tag commit is **prohibited** — use
`--force-with-lease` only on the `-withdrawn` sibling tag if it must be
re-pointed (e.g. moved to a clearer commit), never on the original.

### 7. Public notice

- Add a `### Withdrawn` section to `CHANGELOG.md` for the affected
  release line, citing the rollback issue and the patched release.
- Open a **GitHub Discussion** in the repo's "Announcements" category
  with a short summary and a link to the rollback issue. Pin it for one
  release cycle.

## Time SLA

From **approval** (issue marked `approved` by Lead Curator + maintainer, or
by lead maintainer in an emergency) to **fully-propagated rollback**
(Zenodo + HF + repo + public notice): **48 hours**.

Emergency rollbacks aim for **24 hours** end-to-end.

## What we explicitly do not do

- **Delete Zenodo records.** Not possible by design. We mark them
  `withdrawn` instead.
- **Pretend the version never existed.** Git history retains the original
  tag; CHANGELOG documents the withdrawal.
- **Force-push the original release tag commit.** Doing so would break
  external citations and is prohibited by this runbook.
- **Skip the public notice.** Silent rollback undermines the trust model
  of the collection.

## Backout (un-rollback)

If a rollback was issued in error (e.g. a retraction notice was itself
withdrawn, an opt-out was rescinded, a bug report turned out to be invalid):

1. Open a new issue titled `[UN-ROLLBACK] <slug>-v<N>: <reason>` with the
   same approval requirements as the original rollback.
2. Ship a further patch release (e.g. `v1.0.2`) restoring the removed
   content, citing the un-rollback issue in `CHANGELOG.md`.
3. **Do not** delete the `<slug>-v<N>-withdrawn` tag — leave it as the
   audit trail of what happened.
4. On Zenodo, the withdrawn deposition stays withdrawn; the restored
   content lives in the new patch release's deposition.
5. Update the original rollback issue with a closing comment linking the
   un-rollback PR and the new patch release.

The un-rollback is itself a documented event, not a coverup.
