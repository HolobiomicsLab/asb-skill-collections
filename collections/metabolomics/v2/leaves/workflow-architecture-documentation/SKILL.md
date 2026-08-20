---
name: workflow-architecture-documentation
description: Use when you need to understand how a complex MS/MS spectral search system
  routes query spectra through multiple parallel processing pipelines with different
  objectives (e.g., reliable exact matching vs. fast approximate matching).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3361
  tools:
  - MS2Query
  - MS2Deepscore
  - Python
  - GitHub
  techniques:
  - LC-MS
  license_tier: open
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

# Reconstruct and Document MS/MS Search Workflow Architecture with Branch Split

## Summary

Systematically extract, map, and validate the architectural split of a spectral search workflow into discrete processing branches (library matching vs. analogue search) by tracing control flow, data dependencies, and routing logic through repository history and codebase. This skill ensures comprehensive documentation of branch-specific decision criteria, parameter passing, and entry/exit points.

## When to use

Apply this skill when you need to understand how a complex MS/MS spectral search system routes query spectra through multiple parallel processing pipelines with different objectives (e.g., reliable exact matching vs. fast approximate matching). Use it specifically when the workflow split is not explicitly documented in a single place, requires tracing through version control history (e.g., pull requests), or when you must validate that all routing paths and decision nodes are accounted for in the codebase.

## When NOT to use

- The workflow architecture is already fully documented in a single, authoritative source (e.g., a published design document or architecture RFC).
- You only need to run MS2Query end-to-end without understanding internal branch behavior or modifying routing logic.
- The repository is inactive or the branch split is deprecated (check CHANGELOG.md and recent releases before starting).

## Inputs

- MS2Query repository (GitHub: iomega/ms2query)
- Pull request history and release notes
- Python source code implementing the orchestrator and branch logic
- MS/MS query spectra in supported formats (mzML, MGF, MSP, JSON, USI)
- Pre-trained library files and model embeddings (MS2Deepscore, random forest)

## Outputs

- Control-flow diagram or textual specification of branch routing logic
- Data dependency matrix mapping parameter flow between orchestrator and branches
- Decision node documentation (criteria, thresholds, entry/exit conditions)
- Validated architecture map cross-referenced to codebase implementation
- Branch-specific processing pipeline descriptions (inputs, models, outputs per branch)

## How to apply

Begin by reviewing the repository's pull request history and commit logs (e.g., PR #72) to identify when the two-branch architectural split was introduced and what motivated it. Extract the orchestrator or main entry point logic that determines which branch a query spectrum is routed to—identify decision criteria (e.g., precursor m/z thresholds, library metadata checks, user-specified parameters). Trace data flow through each branch: the library-match branch and the analogue-search branch, documenting how spectra are processed, which models or scoring functions are applied (e.g., MS2Deepscore embeddings, random forest re-ranking), and how results are unified or filtered. Map parameter passing between the orchestrator and each branch, including thresholds (e.g., the MS2Query model prediction score range 0.6–0.7 or >0.7 for confidence filtering). Validate the documented split by cross-referencing the control-flow logic against the iomega/ms2query codebase, confirming that all decision nodes, routing paths, and dependencies match the implementation.

## Related tools

- **MS2Query** (Core spectral search tool whose workflow architecture is being documented; implements both library matching and analogue search branches) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Pre-trained deep learning model used in the top-2000 candidate selection phase across both branches)
- **Python** (Language for extracting, analyzing, and validating the control-flow logic and data dependencies in the codebase)
- **GitHub** (Repository hosting and version control; used to trace PR history, commits, and releases documenting architectural changes) — https://github.com/iomega/ms2query

## Evaluation signals

- All decision nodes in the orchestrator are identified and their routing criteria are documented (e.g., how spectrum is assigned to library-match vs. analogue-search branch).
- Data dependency mapping is complete: all parameters passed from orchestrator to each branch are listed with their types, ranges, and usage rationale.
- Cross-reference validation: extracted control-flow logic matches at least two independent code sections in the iomega/ms2query repository (e.g., main entry point and branch implementation).
- Thresholds and filtering logic are explicitly documented (e.g., MS2Query model prediction score >0.7 for high-confidence matches, pre-selection of top 2000 spectra by MS2Deepscore).
- Entry/exit points for each branch are clearly specified, including expected input format, intermediate checkpoints, and output structure.

## Limitations

- Repository structure or API may change between versions; always cross-check against the latest master branch in iomega/ms2query.
- PR #72 or other historical commits may have been rebased or force-pushed; verify commit availability before relying on specific SHAs.
- The Streamlit web app was removed (PR #83) and future development is uncertain; some integration or visualization logic may not reflect current codebase.
- Branch-specific behavior depends on pre-trained model files and library embeddings that must be downloaded separately (>2 GB); offline analysis of logic alone does not validate end-to-end performance.
- Documentation extraction from Python source code requires familiarity with the matchms API, NumPy/Pandas data structures, and scikit-learn random forest interfaces used in MS2Query.

## Evidence

- [other] MS2Query provides functionality for both reliable true library matching and fast analogue search within its MS/MS spectral-based search workflow.: "MS2Query provides functionality for both reliable true library matching and fast analogue search within its MS/MS spectral-based search workflow."
- [other] Extract the control-flow logic that routes query spectra to either the library-match branch or the analogue-search branch, documenting decision criteria and entry/exit points for each branch.: "Extract the control-flow logic that routes query spectra to either the library-match branch or the analogue-search branch, documenting decision criteria and entry/exit points for each branch."
- [readme] The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly. The top 2000 spectra with the highest MS2Deepscore are selected.: "The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. The top 2000 spectra with the highest MS2Deepscore"
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected. By using a minimum threshold for this score, unreliable matches are filtered out.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library"
- [readme] a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "a score > 0.7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be"
- [other] Map the data dependencies and parameter passing between the orchestrator and each branch component.: "Map the data dependencies and parameter passing between the orchestrator and each branch component."
