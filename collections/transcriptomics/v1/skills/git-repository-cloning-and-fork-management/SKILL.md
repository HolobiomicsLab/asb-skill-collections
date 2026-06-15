---
name: git-repository-cloning-and-fork-management
description: Use when you need to set up a local copy of a scientific software project (e.g., Scanpy) to run its test suite, modify source code, or prepare a feature or bugfix contribution. The canonical repository is hosted on GitHub and you do not have direct push access.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2422
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3173
  tools:
  - git
  - GitHub
  - Hatch
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- This section of the docs covers our practices for working with git on our codebase
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# git-repository-cloning-and-fork-management

## Summary

Fork and clone a remote Git repository to establish a local development environment for contributing code changes. This skill enables reproducible access to a canonical codebase (e.g., scverse/scanpy) while preserving the ability to propose upstream contributions via pull requests.

## When to use

You need to set up a local copy of a scientific software project (e.g., Scanpy) to run its test suite, modify source code, or prepare a feature or bugfix contribution. The canonical repository is hosted on GitHub and you do not have direct push access.

## When NOT to use

- You only need to run or install a released version of the software; use `pip install scanpy` or `conda install scanpy` instead of cloning.
- You are contributing a single documentation fix or issue report that does not require local code changes or test execution.
- The repository is private and you have not been granted access; cloning will fail with authentication errors.

## Inputs

- GitHub repository URL (canonical upstream, e.g., https://github.com/scverse/scanpy)
- GitHub user account with authentication (HTTPS token or SSH key)
- Local filesystem path for the clone

## Outputs

- Local Git repository directory with full commit history
- Working directory with source code, configuration files (e.g., hatch.toml, pyproject.toml), and test suite
- Git remote tracking branches: 'origin' (your fork) and optionally 'upstream' (canonical repository)

## How to apply

First, fork the remote repository (e.g., scverse/scanpy) to your own GitHub account using the GitHub web interface. Then, clone your fork to a local machine using `git clone <your-fork-url>`. This establishes a local repository linked to your fork as 'origin' and preserves the upstream repository reference. The fork allows you to push changes to your own remote copy without requiring upstream write access, enabling you to create and iterate on branches before submitting a pull request. For Scanpy specifically, after cloning, you can immediately invoke `hatch test` from the repository root to verify the clone is functional and the test suite executes with exit code 0.

## Related tools

- **git** (Version control system used to fork and clone the repository; enables branching, committing, and push/pull workflows for contribution.) — https://github.com/scverse/scanpy
- **GitHub** (Web hosting platform providing fork and clone infrastructure via the GitHub API and web interface.) — https://github.com/scverse/scanpy
- **Hatch** (After cloning, used to set up the development environment and execute the full test suite via `hatch test` to verify the clone is functional.) — https://github.com/scverse/scanpy

## Examples

```
git clone https://github.com/your-username/scanpy.git && cd scanpy && hatch test
```

## Evaluation signals

- The cloned directory contains the complete source tree, including scanpy/ subdirectory, hatch.toml, pyproject.toml, and tests/ directory.
- Running `git remote -v` shows 'origin' pointing to your fork and (optionally) 'upstream' pointing to the canonical scverse/scanpy repository.
- Running `hatch test` from the repository root completes successfully with exit code 0 and reports zero non-skipped test failures, confirming the clone is functional and all development dependencies are correctly resolved.
- Committing a test change and pushing to your fork succeeds without authentication errors, confirming write access to the remote origin.
- A new branch created locally (e.g., `git checkout -b my-feature`) can be pushed to the fork and a pull request can be opened against the upstream repository.

## Limitations

- Forking requires a GitHub account; forks are public by default and visible in your GitHub profile.
- Clone size can be large for mature projects with long commit histories; use `--depth` for shallow clones if bandwidth is constrained (though this may limit local history).
- The local clone reflects the state of the fork at clone time; you must run `git pull` or `git fetch` to sync with upstream changes later.
- If upstream pushes force-rewrites (e.g., history rebase), your fork may diverge; synchronizing requires explicit `git fetch upstream` followed by a rebase or merge strategy.

## Evidence

- [other] Fork the Scanpy repository to your own GitHub account: "Fork the Scanpy repository to your own GitHub account"
- [other] Clone via git after forking: "Fork and clone the scverse/scanpy repository to a local machine using git."
- [other] Test suite execution via Hatch verifies functional clone: "Create a development environment using Hatch by running `hatch test` from the repository root, which automatically creates the predefined Hatch environment specified in hatch.toml."
- [other] Git is the version control system used by Scanpy: "This section of the docs covers our practices for working with git on our codebase"
