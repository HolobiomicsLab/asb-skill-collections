---
name: analog-search-result-routing
description: Use when after MS2Query has ranked and scored library matches against query spectra, when you need to apply different confidence thresholds, interpretation strategies, or downstream workflows depending on whether the result is an exact match (precursor m/z difference ≈ 0) or a chemical analog.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - GitHub
  - Git
  - MS2Query
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Analog-Search-Result-Routing

## Summary

Separate MS2Query spectral search results into distinct workflow branches for true library matches versus analog search results, enabling downstream analysis tailored to match type. This skill ensures that exact matches and chemical analogs are handled with appropriate thresholds and interpretation strategies.

## When to use

After MS2Query has ranked and scored library matches against query spectra, when you need to apply different confidence thresholds, interpretation strategies, or downstream workflows depending on whether the result is an exact match (precursor m/z difference ≈ 0) or a chemical analog (precursor m/z difference significant). Use this skill if your research question requires distinguishing between confirmed identifications and structural homologs.

## When NOT to use

- Input is a single query spectrum without prior MS2Query execution — this skill assumes results already exist and only filters/routes them.
- Your research question requires only a single ranked list of all matches regardless of type — branching adds unnecessary complexity if no downstream workflow differs by match type.
- Library spectra lack sufficient metadata or annotation to disambiguate exact matches from analogs in the output.

## Inputs

- MS2Query output CSV file with ms2query_model_prediction scores
- Precursor m/z difference column from results
- Query spectra file (MGF, mzML, or msp format)
- MS2Query library match results with molecular class annotations

## Outputs

- Filtered CSV of true library matches (exact or near-exact m/z, high confidence)
- Filtered CSV of analog search results (significant m/z difference, lower confidence)
- Branched workflow artifacts or separate result directories per match type
- Interpretation report with match-type-specific summary statistics

## How to apply

Inspect the ms2query_model_prediction score and precursor m/z difference columns in the MS2Query output CSV. For true library matches, apply stricter thresholds (score > 0.7 recommended) since exact m/z alignment is confirmed. For analog results, use more lenient thresholds (0.6–0.7 range acceptable with caution; < 0.6 generally discarded) because structural similarity without m/z confirmation carries more uncertainty. Route matches with precursor m/z difference ≈ 0 and high prediction scores to a 'confirmed identification' workflow; route those with significant m/z differences to an 'analog discovery' workflow. The branching logic should account for mass spectrometer tolerance (typically 5 ppm or instrument-specific specification) when determining m/z alignment. Implement conditional branching in MS2Query post-processing code (e.g., Python logic in run_ms2query module) that examines both columns and assigns results to separate result files or data structures for independent analysis.

## Related tools

- **MS2Query** (Performs initial MS/MS library matching and analog search, producing scored results that are then routed by this skill) — https://github.com/iomega/ms2query
- **Python** (Language for implementing conditional branching logic and CSV filtering in post-processing scripts)
- **GitHub** (Version control platform for collaborative development and testing of branching logic (PR #72 reference)) — https://github.com/iomega/ms2query

## Examples

```
import pandas as pd
results_df = pd.read_csv('ms2query_results.csv')
ms_tolerance_ppm = 5
exact_matches = results_df[(results_df['precursor_mz_difference'].abs() < (ms_tolerance_ppm / 1e6)) & (results_df['ms2query_model_prediction'] > 0.7)]
analogs = results_df[(results_df['precursor_mz_difference'].abs() >= (ms_tolerance_ppm / 1e6))]
exact_matches.to_csv('results_true_library_matches.csv', index=False)
analogs.to_csv('results_analog_search.csv', index=False)
```

## Evaluation signals

- Exact matches (precursor m/z difference < mass spectrometer tolerance, typically ≤ 5 ppm) are routed to the true library match branch with high prediction scores (> 0.7).
- Analog results (precursor m/z difference exceeding tolerance threshold) are routed to the analog branch with appropriate lower thresholds (0.6–0.7 range or user-specified).
- No results appear in both branches simultaneously — routing is mutually exclusive and exhaustive.
- Downstream workflows applied to each branch produce qualitatively different summaries (e.g., true matches emphasize molecular confirmation; analogs emphasize structural similarity and uncertainty).
- Unit tests confirm both pathways execute without error and produce expected output schemas (columns, row counts, value ranges).

## Limitations

- Branching decision depends critically on precursor m/z difference accuracy; errors in m/z calibration or library metadata can misclassify results. True matches with poor annotation or non-standard adducts may be misrouted.
- No universal optimal threshold for the ms2query_model_prediction score exists — the skill requires domain-specific tuning (0.6–0.7 range is guidance, not a strict rule; different compound classes and library sources may need adjustment).
- MS2Query does not perform peak picking or clustering of redundant spectra beforehand, so high-abundance compounds with many query spectra may dominate one branch, skewing interpretation.
- Analog routing assumes precursor m/z difference is a reliable distinguishing feature, but complex samples, isotopologues, or multiply charged ions may introduce ambiguity.

## Evidence

- [other] MS2Query implements workflow branching to separate true library matches from analog search results: "MS2Query implements workflow branching to separate true library matches from analog search results, as introduced in PR #72."
- [other] Branching logic routes spectral results by match type: "Implement conditional logic in the MS2Query codebase that routes spectral results into separate workflow paths based on match type."
- [other] Column for precursor m/z difference can separate exact matches from analogs: "If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since"
- [other] Threshold guidance for interpreting prediction scores by match type: "To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results"
- [other] MS2Query combines multiple features to rank matches: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
