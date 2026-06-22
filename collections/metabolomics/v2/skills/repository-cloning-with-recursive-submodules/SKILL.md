---
name: repository-cloning-with-recursive-submodules
description: Use when you need to set up a development environment for a project that declares Git submodules (typically listed in .gitmodules), particularly when the build system (qmake, make, Maven, etc.) expects all dependencies to be present in the working tree.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Maven GUI
  - git
  - qmake
  - make
  - Qt5
  - MSYS2
  - Homebrew
  - pacman
derived_from:
- doi: 10.3390/metabo12080684
  title: MAVEN2
evidence_spans:
- 'Maven GUI: Metabolomics Analysis and Visualization Engine'
- git clone --recursive [redacted-email]:eugenemel/maven.git maven
- qmake -r build.pro
- make -j4
- Install the qt5 package
- Install the MSYS2 platform for Windows
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repository-cloning-with-recursive-submodules

## Summary

Clone a Git repository and all of its nested submodules in a single operation, ensuring that all interdependent source trees (e.g., Maven GUI and Maven Core libraries) are available locally for compilation. This skill is essential when a project's build depends on multiple versioned library repositories managed as Git submodules.

## When to use

Use this skill when you need to set up a development environment for a project that declares Git submodules (typically listed in .gitmodules), particularly when the build system (qmake, make, Maven, etc.) expects all dependencies to be present in the working tree. The Maven GUI project uses this pattern: the main repository declares maven_core as a submodule, so a shallow clone would fail at the configuration or compilation step.

## When NOT to use

- The project has no declared submodules (use `git clone` without `--recursive` for simpler, faster clones).
- You only need to inspect or modify the main repository and do not need the submodule source code for your analysis.
- Submodule repositories are unavailable or access-restricted; in this case, a recursive clone will hang or fail.

## Inputs

- Git repository URL (SSH or HTTPS) pointing to a project with declared submodules
- .gitmodules configuration file (implicitly read by git)
- Target directory path for the local clone

## Outputs

- Local working directory containing the main repository and all initialized submodule trees
- Hidden .git directory with full commit history and submodule metadata
- Source files ready for downstream build steps (qmake configuration, make compilation)

## How to apply

Run `git clone --recursive` with the target repository URL to initialize and populate all declared submodules in a single pass, avoiding the two-step process of cloning then running `git submodule update --init --recursive`. The `--recursive` flag automatically fetches submodule metadata from .gitmodules and checks out the pinned commit for each submodule. For Maven GUI, this ensures that both the main application source tree and the maven_core library tree are present before invoking qmake and make. Verify success by confirming that subdirectories listed in .gitmodules (e.g., maven_core) contain populated source trees, not empty directories.

## Related tools

- **git** (Version control and repository cloning with submodule resolution) — https://github.com/eugenemel/maven
- **qmake** (Qt build system that expects all source dependencies (including submodule libraries) to be present in the working tree) — https://github.com/eugenemel/maven
- **make** (Compilation driver that depends on successful qmake configuration, which in turn requires submodules to be available) — https://github.com/eugenemel/maven

## Examples

```
git clone --recursive [redacted-email]:eugenemel/maven.git maven
```

## Evaluation signals

- The cloned directory structure includes both the main repository and populated submodule directories (e.g., maven_core with source files, not empty).
- Running `git submodule status` within the cloned directory shows all submodules at their pinned commits with no '-' (uninitialized) prefix.
- Subsequent build steps (e.g., `qmake -r build.pro` and `make -j4`) execute without 'file not found' or 'missing dependency' errors related to submodule code.
- The .git/config file contains [submodule] sections with correct paths and URLs for all declared submodules.
- No need to run `git submodule update --init --recursive` after cloning; all submodules are immediately usable.

## Limitations

- Network bandwidth and time scale with repository size; recursive cloning of large projects with many submodules may take several minutes.
- SSH authentication: SSH-based URLs require configured SSH keys; HTTPS URLs may be more reliable if SSH access is restricted.
- Submodule pinning: the clone checks out the exact commit recorded in the main repository's .gitmodules and index, not the latest main branch of each submodule; this is intentional but may result in outdated submodule code if dependencies have been updated.
- No offline fallback: recursive cloning requires network connectivity to all submodule repositories; intermittent connection loss may require re-running the full clone.

## Evidence

- [other] Clone the maven repository recursively from github.com/eugenemel/maven using git.: "Clone the maven repository recursively from github.com/eugenemel/maven using git"
- [readme] Cloning behavior and submodule reference in the maven_core README.: "git clone  [redacted-email]:eugenemel/maven_core.git maven_core"
- [readme] Submodule warning message during clone operation.: "Cloning into 'maven_core'...
warning: redirecting to https://github.com/eugenemel/maven_core/"
- [other] Workflow dependency on successful clone prior to build configuration.: "Set up the build environment by installing Qt5, qmake, and make on the target platform"
