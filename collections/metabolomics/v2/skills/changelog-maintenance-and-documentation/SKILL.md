---
name: changelog-maintenance-and-documentation
description: Use when you have added or modified user-facing parameters to a model class (such as L1/L2 regularization in SiameseModel), written unit tests to verify the new functionality, and need to communicate these changes to users and maintain a historical record.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3365
  tools:
  - ms2deepscore
  - GitHub
  - bump2version
  - Python
derived_from:
- doi: 10.1101/2024.03.25.586580v5
  title: MS2DeepScore 2.0
evidence_spans:
- '`ms2deepscore` provides a Siamese neural network that is trained to predict molecular structural similarities'
- use the search functionality [here](https://github.com/matchms/ms2deepscore/issues)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_2_0_cq
    doi: 10.1101/2024.03.25.586580v5
    title: MS2DeepScore 2.0
  dedup_kept_from: coll_ms2deepscore_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.03.25.586580v5
  all_source_dois:
  - 10.1101/2024.03.25.586580v5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# changelog-maintenance-and-documentation

## Summary

Maintain a project changelog and update docstrings to document new features, parameter additions, and API changes in machine learning libraries. This skill ensures reproducibility and user awareness of model capability extensions (e.g., regularization parameters) by systematically recording changes and integrating them into model documentation.

## When to use

You have added or modified user-facing parameters to a model class (such as L1/L2 regularization in SiameseModel), written unit tests to verify the new functionality, and need to communicate these changes to users and maintain a historical record. Apply this skill after feature completion but before release to coordinate version bumping, changelog entries, and docstring updates.

## When NOT to use

- Internal refactoring or code cleanup that does not alter user-facing API — changelog entries are for user-relevant changes only.
- Experimental or unstable features not yet ready for release — defer changelog entry until feature is merged to stable branch.
- Bug fixes in unreleased versions — record in changelog only if the bug affects users of the current release.

## Inputs

- SiameseModel class definition with new parameters (e.g., l1_regularization, l2_regularization)
- Unit test suite validating parameter acceptance and application
- Issue tracker reference (e.g., GitHub issue #67)
- Current CHANGELOG.md file
- Model docstring (existing)

## Outputs

- Updated model docstring with parameter documentation
- Updated CHANGELOG.md with issue reference and change summary
- Incremented version number in version control (via bump2version)
- Test suite execution report confirming no regressions

## How to apply

After implementing new model parameters or capabilities: (1) Write or update the model's docstring to describe the new parameters, their types, defaults, and effects (e.g., L1 and L2 regularization with sensible defaults like 0.0 for no regularization). (2) Create a changelog entry referencing the issue number (e.g., issue #67) and briefly describing the feature (e.g., 'Add configurable L1/L2 regularization to SiameseModel'). (3) Use bump2version to increment the version number (major, minor, or patch) reflecting the scope of the change. (4) Run the full test suite via `python setup.py test` to confirm no regressions before committing. (5) Include a reference to the issue in both the CHANGELOG.md and the docstring to create a bidirectional link between implementation, testing, and user-facing documentation.

## Related tools

- **bump2version** (Automate version number incrementing (major|minor|patch) in project files during release)
- **Python** (Run test suite via `python setup.py test` to validate that new parameters do not introduce regressions)
- **GitHub** (Host issue tracker, version control, and changelog repository; reference issue numbers in documentation) — https://github.com/matchms/ms2deepscore
- **ms2deepscore** (The library whose SiameseModel class and docstrings are being documented with new parameter information) — https://github.com/matchms/ms2deepscore

## Examples

```
python -c "from ms2deepscore.models import SiameseModel; model = SiameseModel(l1_regularization=0.01, l2_regularization=0.01); print('L1:', model.l1_regularization, 'L2:', model.l2_regularization)" && bump2version minor && grep -i 'issue #67' CHANGELOG.md && python setup.py test
```

## Evaluation signals

- Model docstring includes parameter name, type, default value, and description for each new argument (e.g., 'l1_regularization: float, default=0.0, L1 penalty coefficient applied to model weights').
- CHANGELOG.md entry exists with the issue reference (e.g., 'Fixes #67') and summarizes the feature in one sentence.
- Version number is incremented consistently (e.g., from 1.0.0 to 1.1.0 for minor feature) using bump2version.
- Full test suite passes without error: `python setup.py test` returns exit code 0 and all tests pass.
- Parameter is accessible and functional in a quick integration test: `model = SiameseModel(l1_regularization=0.01, l2_regularization=0.01)` creates an instance without error and the regularization is applied to model weights during training.

## Limitations

- Changelog entries require manual coordination; automated changelog generation from commit messages is not described in the article, so entries must be written by hand.
- Version bumping via bump2version affects multiple files; coordination errors can cause version skew across setup.py, __init__.py, or other manifests if not carefully configured.
- Documentation updates (docstrings and CHANGELOG) are not automatically validated; review by maintainers or CI linting is needed to ensure consistency and completeness.
- The skill does not cover release tagging or publication to PyPI; those are separate post-documentation steps.

## Evidence

- [other] Document the new parameters in the model docstring and update CHANGELOG.md to reference issue #67.: "Document the new parameters in the model docstring and update CHANGELOG.md to reference issue #67."
- [methods] Bump the version using `bump2version <major|minor|patch>`: "Bump the version using `bump2version <major|minor|patch>`"
- [methods] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [other] Add L1 and L2 regularization parameters to the SiameseModel constructor with sensible defaults (e.g., 0.0 for no regularization).: "Add L1 and L2 regularization parameters to the SiameseModel constructor with sensible defaults (e.g., 0.0 for no regularization)."
