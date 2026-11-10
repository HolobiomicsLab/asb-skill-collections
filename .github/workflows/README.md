# Workflows

- `validate.yml` runs the Python suite, registry/catalogue consistency, search-index manifest freshness, root CITATION.cff and marketplace validation.
- `pages.yml` deploys `docs-site/` to GitHub Pages after relevant changes on `main` or manual dispatch.
- `publish-pypi.yml` builds and publishes the tooling package for package releases or a manual TestPyPI dry run.
- `verify-supplements.yml` validates community supplement manifests, files, hashes and licence rules.
- `vet-curator.yml` checks new curator candidacies and posts a report on their pull requests.
- `domain-gates.yml` is the reusable content pipeline called by domain repositories at a full tooling commit SHA.

Released-content workflows moved to each domain repository's pipeline.
Their scripts remain in `scripts/` and are path-invocable against a domain checkout.

## CI of a domain repository

Each `asb-skills-<domain>` repository owns its content checks. Install
`scripts/templates/domain-ci.yml` as `.github/workflows/gates.yml`,
`scripts/templates/domain-plugin-validate.yml` as
`.github/workflows/plugin-validate.yml` and
`scripts/templates/domain-intake.yml` as `.github/workflows/intake.yml`, and
`scripts/templates/domain-retraction-watch.yml` as
`.github/workflows/retraction-watch.yml`, or render all four from the registry:

```bash
python scripts/render_domain_ci.py --manifest collections.yaml \
  --domain <domain> --tooling-sha <full-tooling-commit-sha> --out <domain checkout>/.github/workflows
```

The generator emits one matrix row per non-legacy release and also renders
the paper intake and retraction-watch callers for the named domain. For a domain
without a registry release, pass `--stage candidate --collection-path
collections/<domain>/v1`; this renders one row with no receipt and a comment
requiring a released-stage rerender after registration. An optional JSON
file passed through `--receipts` maps `collection_path` to `receipts_path`; an
empty receipt path skips receipt re-verification. The registry does not yet
record receipt directories or the tooling commit per release, so the lead must
select and review these pins before rendering.

The caller references `domain-gates.yml@<full-tooling-commit-sha>`. Bump that
SHA deliberately after reviewing the new tooling, then update the release's
recorded tooling commit in `collections.yaml` when that record is added. The
reusable workflow uses `github.job_workflow_sha` to check out exactly the same
tooling revision as the called workflow. It supplies the caller's read-only
`GITHUB_TOKEN` to that checkout.

The content job checks index coverage, description discipline, EDAM IRI form,
advertised counts, licence and provenance tiers, the tool catalogue, related
skill references, proposals and the release surface. It then runs the release
gate and, when configured, re-verifies `<receipts_path>/gate_report.json`
without writing it. Strict mode is the default. DOI sampling is nonblocking
because publisher and network failures are inconclusive. The release gate uses
standard-library similarity checks, so the S6 embedding cache is unnecessary.

The plugin job runs `claude plugin validate --strict` on
`.claude-plugin/marketplace.json` and every local plugin source it lists.

Before installing a caller, rehearse locally:

```bash
scripts/run_domain_gates.sh <tooling-root> <content-root> <collection_path> [receipts_path] [--strict]
```

The default rehearsal is advisory for the release gate and skips DOI network
resolution. `PYTHON` selects the interpreter. DOI resolution, live plugin
validation, hosted Actions permissions and human review remain CI or maintainer
checks. LinkML, RO-Crate and Indicium validation are not included in this
reusable workflow; their legacy jobs need separately maintained package and
source prerequisites.

## Retraction watch

Each domain repository runs `domain-retraction-watch.yml` monthly against its
released and staged `corpus.yaml` files, using the tooling repository at a
reviewed pinned commit. Copy `scripts/templates/domain-retraction-watch.yml` to
`.github/workflows/retraction-watch.yml` in the domain checkout and replace
`<TOOLING_SHA>` with that full commit. Set the `CROSSREF_MAILTO` repository
variable to the maintainer contact for Crossref requests. The monitor does not
modify corpus rows or skills.

The normal generator renders this file with the other three callers. A hit opens
or comments on a labelled issue;
it requires a reviewed release action, never a silent removal. Registry errors
make the run incomplete and fail the job rather than reporting a clean sweep.


## Issue intake

The intake workflow runs only in the private domain repository. A reader
without access to it files a proposal as an issue on this public repository,
and a maintainer stages it in the domain repository. The workflow acts only
on issues of the domain repository that carry both `propose` and `paper-intake`.

`scripts/templates/domain-intake.yml` runs in each `asb-skills-<domain>`
repository on issue `opened`, `edited`, `reopened` and `labeled` events. Its
job runs only when the issue carries both `propose` and `paper-intake`, so the
shared propose form does not feed every resource or workflow suggestion into
the paper parser. The tooling commit is pinned in the rendered caller and
checked out separately from the domain content, which is checked out at `main`.

The job reads the issue with `gh issue view` into `issue.json`, so the body is
data and never a shell string. It then runs `scripts/intake_issue.py`, which is
the only step allowed research network egress (`api.crossref.org`,
`api.datacite.org`, `api.openalex.org`, `api.unpaywall.org` and
`api.github.com`), and applies the receipt with `scripts/intake_github.py`.

On `staged` the adapter resets or creates `bot/intake-paper-<issue>` from
`main`, commits only the wave file and, when the receipt names one, the copy
under `collections/<domain>/proposals/receipts/intake-<issue>.json`, pushes the
branch and opens or updates one pull request. It comments the core's text on
the issue once per receipt digest, using an `<!-- asb-intake ... -->` marker,
then applies the receipt's label additions and removals. On `blocked` and
`duplicate` it comments and labels only, with `duplicate` added for the latter.
The attached workflow does not pass `--dry-run`: it is the write path.

The intake core exits 0 for staged, 1 for blocked and 2 for duplicate, and 64
for a usage error; the workflow applies the receipt for 0, 1 and 2 and fails the
job for any exit code above 2.

The Action never closes the issue, merges a pull request, pushes `main`, builds
a paper or marks a row `included`. Those remain curator actions. The bot commit
identity comes from the `ASB_INTAKE_BOT_NAME` and `ASB_INTAKE_BOT_EMAIL`
repository variables; a missing pair makes the adapter refuse.

Covered DOIs are optional. `covered_dois.json` lives in the private corpus
registry, which a domain Action cannot check out without a second token. When
maintainers mirror it at `collections/<domain>/proposals/covered_dois.json`
the core uses it; otherwise it deduplicates against the collection corpus and
the open `wave-*.yaml` and `watch-*.yaml` files. Mirroring is an owner
decision, not a requirement.

Install the rendered caller in a domain repository:

```bash
python scripts/render_domain_ci.py --manifest collections.yaml \
  --domain <domain> --tooling-sha <full-tooling-commit-sha> \
  --out <domain checkout>/.github/workflows
```

That writes `gates.yml`, `plugin-validate.yml`, `intake.yml` and
`retraction-watch.yml` (the candidate stage writes no `plugin-validate.yml`).
Create the `propose`, `paper-intake`, `needs-triage`, `intake-staged`,
`intake-blocked`, `duplicate` and `retraction-watch` labels in the domain
repository before enabling the jobs, set the
`CROSSREF_MAILTO`, `ASB_WATCH_EMAIL`, `ASB_INTAKE_BOT_NAME` and
`ASB_INTAKE_BOT_EMAIL` repository variables, and confirm that Actions may
create pull requests. Run one owner-approved live dry run first: disable the
push by committing the caller with the adapter step replaced by
`python tooling/scripts/intake_github.py --receipt receipt.json --repo content
--domain "$DOMAIN" --dry-run`, read the printed commands, then restore the
write step. A dry run that opens no pull request is the expected result.
