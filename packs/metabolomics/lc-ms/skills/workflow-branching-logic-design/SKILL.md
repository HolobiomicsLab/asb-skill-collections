---
name: workflow-branching-logic-design
description: Use when when a spectral matching tool produces mixed output containing both exact library matches and analog search results, and your analysis or publication requires separate handling, interpretation, or reporting of these two match classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - GitHub
  - Git
  - MS2Query
  - MS2Deepscore
  - Python
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-branching-logic-design

## Summary

Design and implement conditional routing logic in MS/MS spectral matching pipelines to separate true library matches from analog search results based on match type classification. This skill ensures downstream workflows operate on homogeneous result sets with appropriate interpretation thresholds and confidence metrics.

## When to use

When a spectral matching tool produces mixed output containing both exact library matches and analog search results, and your analysis or publication requires separate handling, interpretation, or reporting of these two match classes. Specifically when MS2Query or similar re-ranking pipelines need to distinguish between zero-difference precursor m/z matches (exact) versus non-zero-difference analogs for quality control, threshold tuning, or result stratification.

## When NOT to use

- Input spectra lack reliable precursor m/z annotations or have missing metadata—branching cannot proceed without this discriminator.
- Your analysis goal requires a single unified confidence ranking across match types—forced branching will fragment what should remain a continuous score distribution.
- Downstream tools or databases already enforce strict exact-match-only or analog-only filtering—redundant branching adds complexity without gain.

## Inputs

- MS2Query result CSV with columns: precursor_mz, library_precursor_mz, ms2query_model_prediction
- Spectral matching pipeline output (MGF, JSON, or pickled matchms objects)
- Match classification rule specification (precursor m/z tolerance, similarity score thresholds)

## Outputs

- Branched result set: true library matches (exact match subset)
- Branched result set: analog search results (analog match subset)
- Workflow metadata documenting branch routing logic and thresholds applied

## How to apply

Examine the output predictions and precursor m/z differences from your spectral matching pipeline. Implement conditional branching that routes results into at least two pathways: (1) exact matches (precursor m/z difference ≈ 0) and (2) analog matches (precursor m/z difference > threshold). Apply match-type-specific interpretation thresholds—for example, MS2Query recommends ms2query_model_prediction > 0.7 for high reliability, but this may be tuned differently for exact vs. analog classes. Store or process each branch separately to prevent threshold bleed between classes. Document the branching criteria (precursor m/z tolerance, score thresholds) in your workflow and update CHANGELOG to record the implementation.

## Related tools

- **MS2Query** (Spectral matching engine that produces mixed library/analog results requiring branching for separate interpretation and confidence thresholding) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Upstream similarity scoring component integrated in MS2Query pipeline; outputs fed into re-ranking random forest that informs match classification) — https://github.com/iomega/ms2query
- **Git** (Version control for feature branch implementation and PR tracking of branching logic changes)
- **Python** (Language for implementing conditional routing logic and unit test suite validating both branching pathways)

## Examples

```
# In Python, after running MS2Query and loading results:
import pandas as pd
results = pd.read_csv('results/query_spectra_ms2query_results.csv')
exact_matches = results[abs(results['precursor_mz_difference']) <= 0.1]
analog_matches = results[abs(results['precursor_mz_difference']) > 0.1]
exact_matches.to_csv('results/exact_matches.csv', index=False)
analog_matches.to_csv('results/analog_matches.csv', index=False)
```

## Evaluation signals

- Unit tests pass for both true library match and analog search branching pathways with no test regression (run `python setup.py test`).
- Exact-match branch contains only results with precursor m/z difference ≤ defined tolerance (typically ≤ 0.1 Da); analog branch contains only results with larger differences.
- Branched result CSVs are non-overlapping (no spectrum routed to both branches) and collectively exhaustive (all input spectra assigned).
- ms2query_model_prediction score distributions differ between branches (exact matches typically cluster at higher confidence than analogs), validating that branching captures semantically distinct populations.
- Documentation and CHANGELOG.md accurately describe branching criteria and match-type-specific thresholds; PR code review confirms conditional logic correctness.

## Limitations

- Branching relies on precursor m/z difference as the primary discriminator; spectral preprocessing or calibration errors that corrupt m/z values will cause misclassification. MS2Query does not perform peak picking or clustering—input spectra must be pre-processed to avoid multiple spectra per feature.
- The ms2query_model_prediction threshold (e.g., > 0.7 for high recall) is dataset- and use-case-dependent; no single threshold optimizes both exact and analog branches across all research goals. Threshold tuning requires empirical validation on your data.
- Branching does not inherently improve the quality of MS2Deepscore embeddings or the random forest model; poor upstream predictions will propagate to both branches regardless of routing logic.

## Evidence

- [other] MS2Query implements workflow branching to separate true library matches from analog search results, as introduced in PR #72.: "MS2Query implements workflow branching to separate true library matches from analog search results, as introduced in PR #72."
- [readme] If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference.: "If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since"
- [readme] This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1...a score > 0,7 has many good analogues and exact matches.: "This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good"
- [other] Implement conditional logic in the MS2Query codebase that routes spectral results into separate workflow paths based on match type.: "Implement conditional logic in the MS2Query codebase that routes spectral results into separate workflow paths based on match type."
- [other] Add unit tests covering both library-match and analog-search branching pathways.: "Add unit tests covering both library-match and analog-search branching pathways."
