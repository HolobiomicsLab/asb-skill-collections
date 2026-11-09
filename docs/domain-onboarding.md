# Domain onboarding and release

This guide takes one scientific domain from a prepared corpus to a released and maintained
domain repository. Commands run from the public tooling checkout unless they name another root.
Replace angle-bracket fields with reviewed values. The pipeline's builder instructions are in its
`docs/adding-a-domain.md` file.

## 1. Prerequisites

Prepare an ASB domain profile, run a corpus wave, resolve and tier its papers, then create a cut.
The cut must have a collection tree, a cut identifier and complete receipts. Confirm the intended
domain slug and title before creating repository files.

```bash
python scripts/collect_from_cut.py --help
```

Use the cut's actual collection and receipt paths below. Its `source.json` must be complete and
name full ASB, tooling and corpus commits; a directory name alone is not proof of a complete cut.

## 2. Scaffold the domain repository

For a domain with no registry release, render candidate-stage CI from the explicit collection path.
The directory must be empty unless `--force` is intended. Use `--dry-run` first to review the files.

```bash
python scripts/scaffold_domain_repo.py --domain <domain> --title "<Domain title>" \
  --stage candidate --collection-path collections/<domain>/v1 \
  --tooling-sha <full-reviewed-tooling-commit> \
  --publication-drafts <publication-drafts-directory> \
  --out <domain-checkout> --dry-run
python scripts/scaffold_domain_repo.py --domain <domain> --title "<Domain title>" \
  --stage candidate --collection-path collections/<domain>/v1 \
  --tooling-sha <full-reviewed-tooling-commit> \
  --publication-drafts <publication-drafts-directory> \
  --out <domain-checkout>
```

After registration, rerender with `--stage released` and without `--collection-path`. The scaffold
copies publication drafts when present, rejects disallowed repository links and calls the workflow
renderer in-process. Review metadata before using it in a deposit.

The candidate marketplace intentionally has an empty `plugins` list. Validate its syntax with
`claude plugin validate .claude-plugin/marketplace.json`; strict mode treats that required empty
list as a warning and fails. Candidate rendering therefore omits the plugin workflow until
registration. This is a plugin-workflow limitation, not a missing content-gate row. Released
marketplaces use `claude plugin validate --strict` normally.

## 3. Land the candidate branch

Check the landing plan, then run it without `--dry-run`. Landing creates and commits the local
`candidate/<cut-id>` branch and installs collection and receipt files; it does not push or merge.

```bash
python scripts/land_candidate.py --candidate <candidate-directory> \
  --receipts <candidate-receipts> --repo <domain-checkout> \
  --domain <domain> --version v1 --title "ASB <Domain> Skill Collection v1" --dry-run
python scripts/land_candidate.py --candidate <candidate-directory> \
  --receipts <candidate-receipts> --repo <domain-checkout> \
  --domain <domain> --version v1 --title "ASB <Domain> Skill Collection v1"
```

The title must equal `collection.yaml:title`. Inspect the branch and receipts before opening a
candidate pull request.

## 4. Run gates locally and in CI

Run the complete local rehearsal with strict content checks, strict EDAM vocabulary resolution and
an advisory diagnostic release-gate run. Keep the reports as candidate evidence.

```bash
scripts/run_domain_gates.sh <tooling-root> <domain-checkout> \
  collections/<domain>/v1 receipts/<cut-id> --strict
python scripts/domain_content_gates.py --tooling <tooling-root> \
  --content <domain-checkout> --collection collections/<domain>/v1 \
  --receipts receipts/<cut-id> --strict --edam-strict
python scripts/release_gate.py <domain-checkout>/collections/<domain>/v1 \
  --advisory --report <diagnostic-report.json>
```

The scaffolded `gates.yml`, `intake.yml` and `retraction-watch.yml` are the candidate CI callers;
rerendering at the released stage adds `plugin-validate.yml`, and `gates.yml` has one candidate
matrix row that must be rerendered after registration.
Local success does not establish hosted Actions permissions or human approval.

## 5. Resolve the PII gate

`release_gate.py` hard-fails high-confidence clinical or personal identifiers and non-author emails
in verbatim evidence spans. Ambiguous PII or dual-use findings require human review. A strict hard-gate
failure stops the candidate: do not merge, deposit, tag or register it, and do not override or redact
the finding silently. The product owner and designated human curators decide the disposition; an agent
only reports the evidence and applies an explicit decision.

```bash
python scripts/release_gate.py <domain-checkout>/collections/<domain>/v1 \
  --strict --report <domain-checkout>/receipts/<cut-id>/gate_report.json
```

## 6. Confirm the corpus pin

The full `corpus_commit` in `receipts/<cut-id>/source.json` must be reachable on the corpus repository's
`main`. Reconcile without rewriting history, then obtain the owner's authorisation for any push.

```bash
git -C <corpus-checkout> status --short
git -C <corpus-checkout> merge-base --is-ancestor <full-corpus-commit> origin/main
```

A successful exit from the second command is the reachability test. Keep this private repository name
out of public files and URLs.

## 7. Register the release

Use the release orchestrator's `manifest` stage after the DOI and tag facts exist. At the first release,
pass the newly created domain concept DOI explicitly. The stage computes and validates the release row
and tree digest; review the tooling pull request before merge.

```bash
python scripts/release_domain.py manifest --domain <domain> --version v1 \
  --repo-root <domain-checkout> --tooling-root <tooling-root> \
  --state <release-state.json> --concept-doi 10.5281/zenodo.<concept-id> \
  --commit <full-domain-release-commit> --tag-name <domain>-v1.0.0 \
  --released <YYYY-MM-DD>
python scripts/check_collections_manifest.py --checkout <domain>=<domain-checkout>
```

Rerender released-stage CI and the released marketplace after this row lands in `collections.yaml`.

## 8. Run the release stages

The `asb-domain-release` skill owns the detailed release protocol and its human stops. The orchestrator
stages are `gate`, `land`, `deposit-plan`, `deposit-draft`, `record-doi`, `receipt`, `manifest` and `tag`.
Inspect each stage's inputs with `--help`; `--execute` is deliberate, and status is read with `status`.

```bash
python scripts/release_domain.py gate --domain <domain> --version v1 \
  --repo-root <domain-checkout> --state <release-state.json> --candidate <candidate-directory>
python scripts/release_domain.py deposit-plan --domain <domain> --version v1 \
  --repo-root <domain-checkout> --state <release-state.json> \
  --record-id <record-id> --publication-date <YYYY-MM-DD>
python scripts/release_domain.py deposit-draft --domain <domain> --version v1 \
  --repo-root <domain-checkout> --state <release-state.json> \
  --record-id <record-id> --publication-date <YYYY-MM-DD>
python scripts/release_domain.py record-doi --domain <domain> --version v1 \
  --repo-root <domain-checkout> --state <release-state.json> \
  --doi 10.5281/zenodo.<version-id> --released <YYYY-MM-DD>
python scripts/release_domain.py receipt --domain <domain> --version v1 \
  --repo-root <domain-checkout> --state <release-state.json>
python scripts/release_domain.py tag --domain <domain> --version v1 \
  --repo-root <domain-checkout> --state <release-state.json> \
  --commit <full-doi-merge-commit> --tag-name <domain>-v1.0.0
python scripts/release_domain.py status --domain <domain> --version v1 \
  --repo-root <domain-checkout> --state <release-state.json>
```

The first release of a domain creates its concept DOI. The create-record path is not yet implemented
in the orchestrator; this first-record step is planned. Existing `deposit-plan` and `deposit-draft`
operate on an existing record lineage, so stop and use the owner-approved first-record procedure rather
than inventing a record id.

## 9. Maintain the domain

Set the repository variables documented in `docs/intake-issue.md` and the retraction-watch section of
`docs/REGISTRY.md`. The monthly watch opens or comments on a labelled issue; it never removes content.
Paper intake stages a branch and pull request for curator review; it never merges or marks a row included.

Apply reviewed EDAM vocabulary remaps, rebuild facets, and pack local record capsules when the corresponding
source data changes. These commands do not publish a release.

```bash
python scripts/check_retractions.py --collections <domain-checkout>/collections \
  --staged <domain-checkout>/staged-collections --report <retraction-report.json>
python scripts/remap_edam.py --help
python scripts/build_facets.py build --collection <domain-checkout>/collections/<domain>/v1 \
  --out <facet-output.json> --dry-run
python scripts/pack_capsules.py --view <capsule-view.yaml> \
  --collection <domain-checkout>/collections/<domain>/v1 \
  --out <capsule-output-directory> --date <YYYY-MM-DD> --strict
```

## 10. Owner gates

The owner decides the candidate merge, Zenodo publication, tag creation and push, and repository visibility.
Before opening a domain repository, scan its remote references and review every finding. Visibility is never
an automatic consequence of a release or a clean gate report.

```bash
python scripts/scan_remote_refs.py --repo <domain-checkout> --remote origin \
  --out <remote-reference-scan.json>
```

Stop for the owner at each gate. A draft, local tag, candidate pull request or scan report is not approval.
