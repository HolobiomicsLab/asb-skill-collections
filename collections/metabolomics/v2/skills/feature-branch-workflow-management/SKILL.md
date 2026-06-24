---
name: feature-branch-workflow-management
description: Use when when implementing a new feature or bug fix in a shared repository
  (such as Maven GUI metabolomics analysis software) where multiple contributors work
  in parallel and code quality is enforced via CI/CD pipelines (Travis, Appveyor).
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - git
  - qmake
  - make
  - Maven GUI
  - Qt5
  - Travis
  - Appveyor
  license_tier: open
derived_from:
- doi: 10.3390/metabo12080684
  title: MAVEN2
evidence_spans:
- git clone --recursive [redacted-email]:eugenemel/maven.git maven
- qmake -r build.pro
- make -j4
- 'Maven GUI: Metabolomics Analysis and Visualization Engine'
- Install the qt5 package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maven2_cq
    doi: 10.3390/metabo12080684
    title: MAVEN2
  dedup_kept_from: coll_maven2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12080684
  all_source_dois:
  - 10.3390/metabo12080684
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-branch-workflow-management

## Summary

A Git-based workflow for isolating feature development, code review, and integration in collaborative projects using named feature branches and pull requests. This skill ensures that experimental code remains separate from the main branch until it passes review and continuous integration gates.

## When to use

When implementing a new feature or bug fix in a shared repository (such as Maven GUI metabolomics analysis software) where multiple contributors work in parallel and code quality is enforced via CI/CD pipelines (Travis, Appveyor). Use this skill whenever a change requires peer review before merging into the main release branch, or when a release cycle requires staged updates to changelog and version metadata.

## When NOT to use

- When contributing to a project that uses trunk-based development or rebase-only workflows without pull request review.
- When the change is a trivial documentation fix or local-only development that will never be merged upstream.
- When working on a repository with no configured CI/CD integration (Travis, Appveyor, GitHub Actions) — feature branches provide no enforcement value.

## Inputs

- Git repository (eugenemel/maven or similar with CI/CD configured)
- Feature specification or bug report describing the change
- Existing master branch state

## Outputs

- Named feature branch (e.g., prepare_release_<version>)
- Pull request with review comments and CI/CD status
- Merged commit into master with retained history
- Git tag with version identifier
- Distributable package (via make_dist_[platform].sh)

## How to apply

Create a named feature branch (e.g., `prepare_release_<version>`) from the current master branch using `git checkout -b`. Make incremental commits on the feature branch with clear messages. Push the branch to the remote repository and open a pull request for code review. Once reviewers approve and both Travis (Mac/Linux) and Appveyor (Windows) continuous integration builds pass, merge the PR back into master. Update your local repository with `git fetch upstream master` and `git merge upstream master` to sync with the merged state. Tag the release with `git tag -a <version>` and push tags to trigger downstream distribution builds. The rationale is to prevent incomplete or breaking changes from reaching users by enforcing review and automated testing before mainline integration.

## Related tools

- **git** (Version control: create, push, and merge feature branches; tag releases; manage local and upstream repository state) — https://github.com/eugenemel/maven
- **Travis** (Continuous integration for Mac and Linux builds triggered on pull request and tag creation)
- **Appveyor** (Continuous integration for Windows builds (and as of 20241105, also Mac) triggered on pull request and tag creation)
- **qmake** (Build system invocation to verify compilation on feature branch before PR submission) — https://github.com/eugenemel/maven
- **make** (Compilation and packaging tool to produce distributable artifacts after merge) — https://github.com/eugenemel/maven

## Examples

```
git checkout -b prepare_release_v20250115; git add CHANGELOG.md; git commit -m 'Update CHANGELOG to v20250115'; git push origin prepare_release_v20250115; # then open PR on GitHub, wait for Travis/Appveyor to pass, merge; git fetch upstream master; git merge upstream master; git tag -a v20250115; git push --tags
```

## Evaluation signals

- Feature branch exists in remote repository and is tracking upstream master as its base.
- Pull request is open and all CI/CD checks (Travis and Appveyor) report passing status.
- At least one peer review approval is recorded in the pull request comments.
- After merge, `git log master` shows the feature commit(s) with a merge commit message linking to the PR number.
- Version tag exists and matches the CHANGELOG.md entry; distributable packages are generated and available in GitHub Releases.

## Limitations

- Requires discipline: developers must not commit directly to master or bypass CI/CD checks.
- CI/CD pipelines must be properly configured and maintained; outdated or flaky tests reduce the value of the workflow.
- Pull request review is only effective if reviewers have sufficient context and expertise; isolated or under-reviewed PRs may introduce latent defects.
- The workflow introduces latency between code completion and deployment, unsuitable for projects requiring continuous or real-time updates.
- As of 20241105, Linux builds have been retired from the Maven project, so CI/CD coverage is now Mac and Windows only — features targeting Linux will not be validated.

## Evidence

- [other] Create branch `prepare_release_<version>`: "Create branch `prepare_release_<version>`"
- [other] Submit Pull Request for the `prepare_release_<version>` branch: "Submit Pull Request for the `prepare_release_<version>` branch"
- [other] Once other members agree to release, merge the PR and ensure Travis and Appveyor pass: "Once other members agree to release, merge the PR and ensure Travis and Appveyor pass"
- [other] Update local repo with merge commit; git checkout master; git fetch upstream master; git merge upstream master: "Update local repo with merge commit
 git checkout master
 git fetch upstream master
 git merge upstream master"
- [intro] As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor: "As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor"
