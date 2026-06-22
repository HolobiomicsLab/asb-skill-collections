---
name: spectral-search-logic-control-flow
description: Use when when you need to understand or modify how MS2Query routes query spectra through its dual-pathway architecture, or when integrating MS2Query into another tool and need to trace how spectral similarity scores (MS2Deepscore) feed into library-match versus analogue-search branches with.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - MS2Deepscore
  - Random Forest Re-ranker
  - GNPS Library
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
---

# spectral-search-logic-control-flow

## Summary

Decompose and document the architectural split in MS2Query between true library-match and analogue-search branches, including routing logic, decision criteria, data flow, and control points. This skill is essential for understanding how MS2Query orchestrates two parallel search pathways from a single query spectrum through unified spectral similarity scoring.

## When to use

When you need to understand or modify how MS2Query routes query spectra through its dual-pathway architecture, or when integrating MS2Query into another tool and need to trace how spectral similarity scores (MS2Deepscore) feed into library-match versus analogue-search branches with different re-ranking strategies.

## When NOT to use

- Input is already a pre-ranked library match list with no need to understand branching logic or modify routing behavior.
- Query spectra require custom peak-picking or clustering preprocessing; this skill addresses search workflow architecture, not upstream MS2 preprocessing.
- Goal is only to run MS2Query end-to-end without inspecting or modifying internal control flow—use command-line interface instead.

## Inputs

- MS2Query repository source code (Python, iomega/ms2query)
- Pull request history and commit log for architectural changes
- Query MS2 spectra (mgf, mzML, json, msp, mzxml formats)
- Pre-computed MS2Deepscore embeddings for library spectra
- Library spectra in sqlite format with precursor m/z and metadata

## Outputs

- Control-flow diagram or pseudocode documenting decision nodes and routing paths
- Parameter documentation: decision thresholds, top-K selection (e.g., top 2000), score ranges (0–1)
- Data dependency map showing MS2Deepscore → re-ranker → final match output
- Validation report confirming codebase implementation matches documented flow
- CSV results with ms2query_model_prediction column (0–1 scores) and precursor m/z difference for match classification

## How to apply

Begin by reviewing the MS2Query repository history and pull requests (particularly PR #72) to identify the commits that introduced the two-branch workflow split. Extract the orchestrator/router logic that decides whether a query spectrum proceeds to library matching or analogue search, documenting the decision criteria and any precursor m/z-based filtering rules. Map data dependencies by tracing how MS2Deepscore embeddings and scores flow from the library into each branch, and document how the random forest re-ranker uses its 5 features to combine results. Validate the documented control flow against the Python codebase in iomega/ms2query by confirming all entry/exit points, parameter passing, and threshold checks match the implementation.

## Related tools

- **MS2Query** (Main tool whose spectral search workflow architecture (library-match and analogue-search branches) is decomposed and documented) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Provides pre-computed embeddings and spectral similarity scores that feed into both search branches as input features)
- **Random Forest Re-ranker** (Component within MS2Query that combines 5 features to re-rank and optimize final match selection across both branches) — https://github.com/iomega/ms2query
- **GNPS Library** (Pre-trained library spectral database (sqlite) used for benchmarking and as default library source for MS2Query)

## Examples

```
from ms2query.run_ms2query import download_zenodo_files, run_complete_folder
from ms2query.ms2library import create_library_object_from_one_dir
ms2library = create_library_object_from_one_dir('./ms2query_library_files')
run_complete_folder(ms2library, './ms2_spectra_directory')
```

## Evaluation signals

- Documented control-flow logic accounts for all decision nodes and routing paths in the repository implementation without gaps or contradictions.
- Data dependency map can be validated by tracing a test query spectrum through the codebase: verify MS2Deepscore input → top-2000 selection → random forest feature input → final score output (0–1) and match classification.
- Parameter thresholds (e.g., top 2000 spectra selected, score ranges 0–1, recommended confidence threshold > 0.7) are confirmed to match the source code and README guidance.
- Validation report confirms no preselection on precursor m/z is performed in the initial scoring phase but precursor m/z difference is used post-hoc to separate analogues from exact matches in output.
- Control-flow diagram is walkable by an agent unfamiliar with MS2Query; following the documented routes and decision criteria should enable prediction of which branch a given spectrum will follow and why.

## Limitations

- MS2Query does not perform peak picking or clustering of similar MS2 spectra; preprocessing with tools like MZMine may be required beforehand if input files contain many redundant spectra per feature.
- The skill documents the current architecture as it exists in the iomega/ms2query repository; future PRs or refactoring may alter branch structure, decision logic, or parameter passing without prior notice.
- Streamlit web app component has been deprecated and removed from future development, so GUI-based workflow visualization may not be available; control-flow documentation must rely on code inspection and CLI/Python API.
- Random forest re-ranker combining 5 features is treated as a black box within this skill; internal feature importance and threshold tuning are not decomposed.

## Evidence

- [other] MS2Query provides functionality for both reliable true library matching and fast analogue search within its MS/MS spectral-based search workflow.: "MS2Query provides functionality for both reliable true library matching and fast analogue search within its MS/MS spectral-based search workflow."
- [readme] The workflow uses MS2Deepscore to calculate spectral similarity scores, selects the top 2000 spectra, and uses a random forest to re-rank and select the best match.: "The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for"
- [readme] MS2Query predicts a score between 0 and 1 using a random forest, and unreliable matches are filtered by setting a minimum threshold on this score.: "The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected. By using a minimum threshold for this score, unreliable"
- [readme] Guidance on interpreting ms2query_model_prediction scores: > 0.7 indicates many good analogues and exact matches; 0.6–0.7 can be useful but requires caution; < 0.6 should often be discarded.: "To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results"
- [readme] MS2Query does not need separate workflows for analogues and exact matches; precursor m/z difference in the output can be used post-hoc to distinguish them.: "MS2Query does not need two different workflows for searching for analogues and searching for exact matches, it automatically selects the most likely library spectra. If it is important to separate"
