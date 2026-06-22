---
name: git-feature-branch-management
description: Use when when contributing a new feature, bug fix, or documentation update to a shared repository (like iomega/ms2query), and you need to isolate your changes from the main development branch to allow for testing, review, and conditional integration without disrupting the primary codebase.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - GitHub
  - Git
  - MS2Query
  - Python
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- fork the repository to your own Github profile and create your own feature branch off of the latest master commit
- use the search functionality [here](https://github.com/iomega/ms2query/issues)
- push your feature branch to (your fork of) the ms2query repository on GitHub
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query_cq
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query_cq
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

# git-feature-branch-management

## Summary

Create, manage, and integrate feature branches in a Git repository to isolate development work before merging into the main codebase. This skill ensures that new features or bug fixes are developed independently and tested before integration, maintaining code stability and enabling collaborative development.

## When to use

When contributing a new feature, bug fix, or documentation update to a shared repository (like iomega/ms2query), and you need to isolate your changes from the main development branch to allow for testing, review, and conditional integration without disrupting the primary codebase.

## When NOT to use

- When making only trivial documentation fixes that do not require testing or code review — direct commits to master may be acceptable for minor updates.
- When you lack write permissions to the upstream repository and cannot fork — use a different collaboration strategy.
- When the repository does not use Git or GitHub — this skill is specific to Git-based workflows.

## Inputs

- Upstream Git repository URL (e.g., https://github.com/iomega/ms2query)
- Latest master commit reference
- Feature specification or issue description
- Modified or new source code files
- Existing test suite

## Outputs

- New feature branch (local and remote)
- Updated source code in feature branch
- New or modified unit tests
- Updated CHANGELOG.md
- Updated code documentation
- Pull request against upstream repository

## How to apply

Fork the upstream repository to your own GitHub profile, then create a new feature branch from the latest master commit using `git checkout -b <branch-name>`. Work on your changes in isolation within this branch. Before pushing, run existing tests with `python setup.py test` to ensure no regression. Add new unit tests covering your changes, update code documentation and CHANGELOG.md to describe your work, then push the feature branch to your fork on GitHub and create a pull request against the upstream repository. This workflow ensures that changes are vetted before merging and that the master branch remains stable.

## Related tools

- **Git** (Version control system for creating and managing feature branches, committing changes, and pushing to remote repository) — https://github.com/iomega/ms2query
- **GitHub** (Hosting platform for forking repositories, managing pull requests, and facilitating code review before merge) — https://github.com/iomega/ms2query
- **Python** (Test execution environment for running `python setup.py test` to verify no regression in codebase) — https://github.com/iomega/ms2query

## Examples

```
git clone https://github.com/your-username/ms2query.git && cd ms2query && git checkout -b feature/workflow-branching && git push -u origin feature/workflow-branching
```

## Evaluation signals

- Feature branch is cleanly forked from the latest master commit with no extraneous commits.
- Existing test suite passes with `python setup.py test` with zero regression errors.
- New unit tests cover the modified or new code paths and pass successfully.
- CHANGELOG.md is updated with a clear description of the feature or fix.
- Pull request is created against the upstream repository with a descriptive title and body, and passes all continuous integration checks.

## Limitations

- This workflow assumes the upstream repository maintainers will review and merge the pull request; there is no guarantee of acceptance or timeline for integration.
- Merge conflicts may arise if the master branch has advanced significantly while the feature branch was under development, requiring manual conflict resolution.
- If the feature branch is not kept up-to-date with upstream master, the pull request may become stale and lose relevance.
- Requires Git and GitHub familiarity; practitioners unfamiliar with these tools may struggle with branch creation, commit history, or pull request mechanics.

## Evidence

- [other] fork the repository to your own Github profile and create your own feature branch off of the latest master commit: "fork the repository to your own Github profile and create your own feature branch off of the latest master commit"
- [other] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [other] add your own tests (if necessary): "add your own tests (if necessary)"
- [other] update or expand the documentation: "update or expand the documentation"
- [other] update the `CHANGELOG.md` file with change: "update the `CHANGELOG.md` file with change"
- [other] push your feature branch to (your fork of) the ms2query repository on GitHub: "push your feature branch to (your fork of) the ms2query repository on GitHub"
- [other] create the pull request, e.g. following the instructions [here](https://help.github.com/articles/creating-a-pull-request/): "create the pull request, e.g. following the instructions here"
