---
name: pull-request-change-tracking
description: 'Use when investigating how a specific pull request (e.g., PR #72 introducing MS2Query''s two-branch workflow split) modified the codebase architecture, control flow, or data routing.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MS2Query
  - GitHub
  - Python
  techniques:
  - mass-spectrometry
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

# pull-request-change-tracking

## Summary

Track and document architectural and functional changes introduced by pull requests in a scientific software repository, mapping modifications to control flow, data dependencies, and component behavior. This skill is essential for understanding how feature branches integrate into a codebase and for validating that modifications match their intended design.

## When to use

Apply this skill when investigating how a specific pull request (e.g., PR #72 introducing MS2Query's two-branch workflow split) modified the codebase architecture, control flow, or data routing. Use it to reconstruct the rationale for changes, trace how new branches or decision nodes were introduced, and validate that feature implementation matches design intent.

## When NOT to use

- The PR makes only cosmetic or documentation-only changes with no control-flow or architectural modifications.
- You are tracking changes across multiple unrelated PRs in a single pass; process each PR separately.
- The repository has no public GitHub PR history or the PR has been deleted or force-pushed, making diff reconstruction impossible.

## Inputs

- GitHub pull request URL or PR number
- Repository source code (Python modules from iomega/ms2query)
- Repository commit history or PR diff
- Current codebase for cross-validation

## Outputs

- Documented workflow split with control-flow diagrams or pseudocode
- Decision criteria and routing logic for each branch
- Data dependency map showing parameter passing and intermediate outputs
- Validation report confirming PR changes match current implementation

## How to apply

Begin by reviewing the pull request on GitHub to identify what architectural or functional change it introduced (e.g., splitting a monolithic search workflow into separate library-match and analogue-search branches). Extract the control-flow logic that routes inputs to different code paths, documenting decision criteria, entry points, and exit points for each branch. Map data dependencies and parameter passing between the orchestrator and each component, including what spectral similarity scores or metadata flow through each branch. Cross-reference the PR's changes against the current codebase in the repository to confirm the documented split matches actual implementation. Finally, verify that all routing decisions, conditional logic, and data transformations are accounted for by comparing the PR diff with the code in context (e.g., confirming that MS2Deepscore embeddings feed into the top-2000 preselection logic before random-forest re-ranking).

## Related tools

- **GitHub** (Source repository for PR history, diff review, and commit-level tracing of architectural changes) — https://github.com/iomega/ms2query
- **Python** (Language for reading and parsing source code modules to extract control-flow logic and data dependencies)
- **MS2Query** (Target codebase under analysis; provides concrete workflows (library matching, analogue search) whose branching logic is traced) — https://github.com/iomega/ms2query

## Evaluation signals

- The documented control-flow logic matches line-for-line with Python source code in the current repository (e.g., conditional statements routing spectra to library-match vs. analogue-search branches).
- All decision nodes are accounted for: confirm that the routing criteria (e.g., MS2Deepscore threshold, top-2000 preselection) are present in both the PR diff and the current codebase.
- Data dependencies are bidirectional: validate that outputs from one branch (e.g., re-ranked scores from the random forest) flow correctly into downstream consumers and that parameter passing matches the declared API.
- PR timestamps and commit SHAs are traceable to repository history; the documented changes correspond to actual commits in the target branch.
- No orphaned or unreachable code: confirm that all branches introduced in the PR remain reachable in the current codebase (i.e., the PR was not later reverted or substantially refactored without update).

## Limitations

- GitHub PR diffs may not show the full behavioral context if conditional logic relies on external configuration, environment variables, or dynamic library loading; code review alone may not capture all control paths.
- Large PRs (>500 lines changed) can be difficult to fully map in a single pass; breaking them into logical sub-components (e.g., one component per data-processing stage) is recommended.
- If the PR was merged and later code refactored the affected modules without preserving the original structure, the documented split may become misaligned with current implementation; periodic re-validation is necessary.
- Private or internal repositories not accessible via public GitHub will prevent full tracing; this skill assumes public or internal-access codebase availability.

## Evidence

- [other] Review the MS2Query repository history and PR #72 to identify the architectural changes that introduced the two-branch workflow split.: "Review the MS2Query repository history and PR #72 to identify the architectural changes that introduced the two-branch workflow split"
- [other] Extract the control-flow logic that routes query spectra to either the library-match branch or the analogue-search branch, documenting decision criteria and entry/exit points for each branch.: "Extract the control-flow logic that routes query spectra to either the library-match branch or the analogue-search branch, documenting decision criteria and entry/exit points for each branch"
- [other] Map the data dependencies and parameter passing between the orchestrator and each branch component.: "Map the data dependencies and parameter passing between the orchestrator and each branch component"
- [readme] The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly. The top 2000 spectra with the highest MS2Deepscore are selected.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed. MS2Query optimizes re-ranking the best"
- [other] Validate: confirm the documented split matches the codebase implementation in the iomega/ms2query repository and that all decision nodes and routing paths are accounted for.: "confirm the documented split matches the codebase implementation in the iomega/ms2query repository and that all decision nodes and routing paths are accounted for"
