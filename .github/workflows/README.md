# Workflows

- `validate.yml` runs the Python suite, registry/catalogue consistency, search-index manifest freshness, root CITATION.cff and marketplace validation.
- `pages.yml` deploys `docs-site/` to GitHub Pages after relevant changes on `main` or manual dispatch.
- `publish-pypi.yml` builds and publishes the tooling package for package releases or a manual TestPyPI dry run.
- `verify-supplements.yml` validates community supplement manifests, files, hashes and licence rules.
- `vet-curator.yml` checks new curator candidacies and posts a report on their pull requests.

Released-content workflows moved to each domain repository's pipeline.
Their scripts remain in `scripts/` and are path-invocable against a domain checkout.
