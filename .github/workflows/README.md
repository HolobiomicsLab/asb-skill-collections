# Workflows

- `validate.yml` runs the Python suite, registry/catalogue consistency, search-index manifest freshness, root CITATION.cff and marketplace validation.
- `pages.yml` deploys `docs-site/` to GitHub Pages after relevant changes on `main` or manual dispatch.
- `publish-pypi.yml` builds and publishes the tooling package for package releases or a manual TestPyPI dry run.
- `verify-supplements.yml` validates community supplement manifests, files, hashes and licence rules.
- `vet-curator.yml` checks new curator candidacies and posts a report on their pull requests.

Released-content workflows moved to each domain repository's pipeline.
Their scripts remain in `scripts/` and are path-invocable against a domain checkout.

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
