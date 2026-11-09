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
`scripts/templates/domain-ci.yml` as `.github/workflows/gates.yml` and
`scripts/templates/domain-plugin-validate.yml` as
`.github/workflows/plugin-validate.yml`, or render both from the registry:

```bash
python scripts/render_domain_ci.py --manifest collections.yaml \
  --domain <domain> --tooling-sha <full-tooling-commit-sha> --out <domain checkout>/.github/workflows
```

The generator emits one matrix row per non-legacy release. An optional JSON
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

To render by hand, no generator is required: the template contains no other
placeholders. If `scripts/render_domain_ci.py` is present, use its normal
template rendering route instead. A hit opens or comments on a labelled issue;
it requires a reviewed release action, never a silent removal. Registry errors
make the run incomplete and fail the job rather than reporting a clean sweep.
