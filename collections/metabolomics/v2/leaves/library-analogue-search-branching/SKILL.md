---
name: library-analogue-search-branching
description: Use when when you need to reconstruct or validate the control-flow architecture
  of a spectral search system that must handle both exact-match library lookups and
  analogue discovery in a single pass, particularly when the system uses pre-computed
  embeddings for efficiency and machine learning for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2Query
  - MS2Deepscore
  - Spec2Vec
  - GitHub
  - Python
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# Library-analogue search branching

## Summary

MS2Query implements a unified workflow that internally branches between reliable true library matching and fast analogue search within a single run, using MS2Deepscore embeddings and random forest re-ranking to automatically select the most likely match type. This skill involves understanding and documenting the architectural split that enables MS2Query to search for both exact matches and analogues without requiring separate workflows.

## When to use

When you need to reconstruct or validate the control-flow architecture of a spectral search system that must handle both exact-match library lookups and analogue discovery in a single pass, particularly when the system uses pre-computed embeddings for efficiency and machine learning for re-ranking. This is appropriate when analyzing or extending a codebase like MS2Query where the routing logic between match types is implicit or poorly documented.

## When NOT to use

- When you are running MS2Query as a black-box tool and do not need to understand or modify its internal branching logic.
- When your query spectra are not annotated or pre-processed (MS2Query requires peak-picked or clustered spectra and does not perform its own peak picking; preprocessing with MZMine is recommended).
- When you need to train new MS2Deepscore or Spec2Vec models; this skill concerns the search-time branching logic, not model training.

## Inputs

- MS2Query repository source code (GitHub iomega/ms2query)
- Pull request history and commit logs (esp. PR #72)
- Query MS/MS spectra in supported formats (mzML, json, mgf, msp, mzxml, usi, or pickled matchms object)
- Pre-computed MS2Deepscore embeddings for library spectra
- Trained random forest model combining 5 features for re-ranking

## Outputs

- Documented control-flow diagram or pseudo-code showing branch routing logic
- Decision criteria and threshold documentation (MS2Query model prediction score ranges)
- Data dependency map showing parameter flow between orchestrator and branch components
- Entry/exit point specification for true-match and analogue-search branches
- CSV results table with columns including ms2query_model_prediction score and precursor m/z difference

## How to apply

Begin by reviewing the MS2Query repository history (especially PR #72 mentioned in the task card) to identify architectural commits introducing the two-branch split. Extract the control-flow logic that routes query spectra: first, all query spectra are compared against the library using pre-computed MS2Deepscore embeddings to rapidly select the top 2000 spectra (no precursor m/z prefiltering). Then, a random forest model combining 5 features re-ranks these candidates to predict a score between 0 and 1, with the highest-scoring library match selected as either an analogue or exact match depending on precursor m/z difference. Document decision criteria (e.g., the score threshold; the README notes that score > 0.7 indicates many good matches, 0.6–0.7 requires caution, < 0.6 can be discarded), entry/exit points for each logical branch (feature selection from top 2000 vs. final ranking), and parameter passing between the orchestrator and each branch component. Validate that the documented split matches the iomega/ms2query codebase implementation and that all decision nodes and routing paths are accounted for.

## Related tools

- **MS2Query** (The spectral search tool implementing the unified analogue/exact-match workflow with internal branching via MS2Deepscore embeddings and random forest re-ranking) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Pre-computes spectral similarity embeddings used by MS2Query to rapidly select top 2000 candidate library spectra before random forest re-ranking)
- **Spec2Vec** (One of the models trained for the library; used in MS2Query's feature set for re-ranking)
- **GitHub** (Source for repository history, PR tracking, and issue search to identify architectural changes and branching logic) — https://github.com/iomega/ms2query
- **Python** (Language for inspecting and documenting the control-flow logic in the MS2Query codebase and writing validation tests)

## Examples

```
from ms2query.run_ms2query import download_zenodo_files, run_complete_folder
from ms2query.ms2library import create_library_object_from_one_dir
download_zenodo_files('positive', './ms2query_library_files')
ms2library = create_library_object_from_one_dir('./ms2query_library_files')
run_complete_folder(ms2library, './ms2_spectra_directory')
```

## Evaluation signals

- Confirmed identification of PR #72 or equivalent commit introducing the two-branch architectural split in the iomega/ms2query repository
- Extracted control-flow routing logic matches actual implementation: verify that query spectra are routed through MS2Deepscore embedding comparison → top-2000 selection (no m/z prefilter) → random forest re-ranking with 5-feature model → score-based threshold filtering
- Score threshold documentation aligns with README guidance: score > 0.7 = high-confidence match/analogue, 0.6–0.7 = use with caution, < 0.6 = discard
- Data dependency map shows precursor m/z difference is available at exit for distinguishing exact matches (no m/z difference) from analogues (m/z difference > 0)
- All decision nodes accounted for and no routing paths are missing; entry/exit points for each branch are clearly specified and can be traced through a representative query spectrum end-to-end

## Limitations

- MS2Query does not perform its own peak picking or clustering; input spectra must be preprocessed separately (e.g., using MZMine) to reduce redundant MS/MS spectra per feature.
- The branching and re-ranking logic relies on pre-computed MS2Deepscore embeddings for speed; recomputing embeddings or training new models requires separate workflows and is beyond the scope of the search-time branching.
- The random forest model uses 5 unspecified features; the exact feature list and their relative importance are not fully documented in the README, limiting interpretability of the branching decision.
- No preselection on precursor m/z is performed, which may increase false positives in low-resolution or contaminated spectra; reliability depends on applying the MS2Query prediction score threshold post-hoc.

## Evidence

- [readme] MS2Query uses MS2 mass spectral data to find the best match in a library and is able to search for both analogues and exact matches.: "MS2Query uses MS2 mass spectral data to find the best match in a library and is able to search for both analogues and exact matches."
- [readme] The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly. The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "The workflow for running MS2Query first uses MS2Deepscore to calculate spectral similarity scores between all library spectra and a query spectrum. By using pre-computed MS2Deepscore embeddings for"
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library"
- [readme] This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue. To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue. To give a general indication, a score > 0,7 has many good analogues and exact"
- [readme] MS2Query does not need two different workflows for searching for analogues and searching for exact matches, it automatically selects the most likely library spectra. If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference.: "MS2Query does not need two different workflows for searching for analogues and searching for exact matches, it automatically selects the most likely library spectra. If it is important to separate"
