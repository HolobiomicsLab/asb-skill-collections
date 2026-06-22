---
name: version-control-feature-branch-management
description: Use when when you have modifications to propose for a shared codebase (e.g., bug fixes, new features, or documentation updates) and need to integrate them without disrupting the main development branch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0080
  tools:
  - MS2Query
  - Git
  - GitHub
  - Python
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# version-control-feature-branch-management

## Summary

A structured workflow for managing feature development in Git using branching, testing, and documentation to ensure code quality and traceability in collaborative scientific software projects. This skill is essential when contributing changes to an active open-source repository where multiple developers coordinate through pull requests and unified version control.

## When to use

When you have modifications to propose for a shared codebase (e.g., bug fixes, new features, or documentation updates) and need to integrate them without disrupting the main development branch. Apply this skill when the project maintains a master branch as the stable reference and requires peer review before merging.

## When NOT to use

- You are modifying a personal, non-collaborative repository where a feature branch workflow adds unnecessary overhead.
- The project uses a different branching strategy (e.g., git-flow with develop branch, or trunk-based development) and you have not confirmed the contribution guidelines.
- You do not have write access to the repository or cannot create a fork (work around this by requesting contributor status or opening an issue first).

## Inputs

- Git repository (cloned locally)
- Latest master commit reference
- Modified source code files
- Test suite (e.g., pytest, unittest)
- Documentation files (e.g., .md, .rst)
- CHANGELOG.md file

## Outputs

- Feature branch (local and remote)
- Test execution report (pass/fail)
- Updated documentation
- Updated CHANGELOG.md entry
- Pull request on GitHub (for review)

## How to apply

Create a feature branch from the latest master commit to isolate your work from concurrent development. After making changes, run the existing test suite (e.g., `python setup.py test`) to verify you have not broken functionality. Add new unit tests if your changes introduce new behavior. Update relevant documentation and the CHANGELOG.md file to describe your modifications. Stay synchronized with upstream master by pulling in remote changes to avoid merge conflicts. Once your feature is complete and tested, push the branch to your fork on GitHub and create a pull request for review by project maintainers.

## Related tools

- **Git** (Version control system for creating and managing feature branches, committing changes, and pushing to remote repositories)
- **GitHub** (Remote hosting platform for repository forks, branch tracking, pull request management, and issue search) — https://github.com/iomega/ms2query
- **Python** (Language for running test suite validation (e.g., `python setup.py test`))

## Examples

```
git checkout -b feature/spectrum-normalization master && python setup.py test && git add . && git commit -m 'Add spectrum normalization module' && git push origin feature/spectrum-normalization
```

## Evaluation signals

- Feature branch name correctly reflects the feature scope and is traceable to an issue or discussion
- All existing tests pass without modification after your changes (`python setup.py test` completes with zero failures)
- New unit tests are included for new functionality and all new tests pass
- CHANGELOG.md entry is present, dated, and describes the change clearly
- Documentation files (README, docstrings, etc.) have been updated to reflect the new or modified behavior
- Pull request is created against the master branch, contains a clear description, and references relevant issue(s)

## Limitations

- Requires familiarity with Git commands and GitHub workflows; users unfamiliar with branching may create branches from incorrect parent commits or have difficulty resolving merge conflicts.
- The test suite must exist and be maintained; if tests are missing or outdated, this workflow cannot fully validate code correctness before merging.
- Synchronizing with upstream master by pulling changes increases the risk of merge conflicts, especially in active projects with frequent commits; conflict resolution skills are required.
- Streamlit web app and future development modules (e.g., web interfaces) may have uncertain maintenance status, which can complicate feature requests and testing for experimental functionality.

## Evidence

- [methods] fork the repository to your own Github profile and create your own feature branch off of the latest master commit: "fork the repository to your own Github profile and create your own feature branch off of the latest master commit"
- [methods] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [methods] add your own tests (if necessary): "add your own tests (if necessary)"
- [methods] update or expand the documentation: "update or expand the documentation"
- [methods] update the `CHANGELOG.md` file with change: "update the `CHANGELOG.md` file with change"
- [methods] stay up to date with the master branch by pulling in changes, possibly from the 'upstream' repository: "stay up to date with the master branch by pulling in changes, possibly from the 'upstream' repository"
- [readme] MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10: "MS2Query is tested by continous integration on MacOS, Windows and Ubuntu for python version 3.9 and 3.10"
