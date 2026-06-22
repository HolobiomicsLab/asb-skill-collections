---
name: spectral-library-match-classification
description: 'Use when when you have run MS2Query on query MS/MS spectra and obtained results with library matches that need to be disambiguated into two categories: (1) exact matches (precursor m/z difference near zero) versus (2) analog matches (chemically related but different precursor m/z).'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - GitHub
  - Git
  - MS2Query
  - MS2Deepscore
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
---

# spectral-library-match-classification

## Summary

Classify MS/MS spectral search results into true library matches versus analog search hits by implementing workflow branching logic that routes results based on precursor m/z difference and MS2Query model prediction scores. This skill enables researchers to separately interpret exact matches from chemically related analogs in a single unified search run.

## When to use

When you have run MS2Query on query MS/MS spectra and obtained results with library matches that need to be disambiguated into two categories: (1) exact matches (precursor m/z difference near zero) versus (2) analog matches (chemically related but different precursor m/z). Use this skill when your downstream analysis or reporting requires separate workflows or confidence thresholds for these two result types.

## When NOT to use

- Input is a single merged result table with no precursor m/z information or ms2query_model_prediction scores—classification cannot proceed without these columns.
- Your analysis goal is purely to identify the single best-scoring match per spectrum without regard to match type; branching adds unnecessary complexity.
- Query spectra have not been preprocessed or clustered, and you have many redundant MS/MS measurements per feature—MS2Query does not handle clustering internally, so branching will not resolve this upstream problem.

## Inputs

- MS2Query results CSV file (output from run_complete_folder or ms2query CLI)
- MS/MS query spectra (mzML, mgf, msp, mzxml, json, usi, or pickled matchms object)

## Outputs

- Classified results table or separate CSV files partitioned by match type (exact vs. analog)
- Annotated results with match_type column ('exact_match' or 'analog_search')
- Branched result sets suitable for downstream confidence-filtered analysis

## How to apply

MS2Query generates a single ranked result per query spectrum but does not inherently separate true library matches from analog search results. Implement conditional branching logic that uses two criteria: (1) check the precursor m/z difference column—values near zero (typically <5 ppm tolerance) indicate exact matches; (2) apply the ms2query_model_prediction score threshold to both branches, but adjust expectations per branch (e.g., >0.7 for high confidence exact matches, >0.6 for analogs). Route results into separate result tables or annotate rows with a match_type field ('exact' or 'analog'). This branching preserves the full ranking while enabling branch-specific interpretation: exact matches have higher reliability for compound identification, while analogs indicate structurally related compounds and support chemodiversity discovery.

## Related tools

- **MS2Query** (Spectral similarity search engine that performs both library and analog matching; generates ranked results and model prediction scores that form the basis for classification) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Deep learning model used internally by MS2Query to compute spectral similarity embeddings; underpins the ranking that precedes classification) — https://github.com/iomega/ms2query
- **Python** (Programming language for implementing conditional branching logic and result partitioning; supports pandas for CSV manipulation)
- **GitHub** (Version control and issue tracking for managing branching implementation (PR #72) and test coverage) — https://github.com/iomega/ms2query

## Examples

```
# Partition MS2Query results into exact vs. analog matches using precursor m/z and model score
import pandas as pd
results_df = pd.read_csv('results/query_spectra_ms2query_results.csv')
exact_matches = results_df[results_df['precursor_mz_difference_ppm'].abs() < 5]
analogs = results_df[results_df['precursor_mz_difference_ppm'].abs() >= 5]
high_confidence_exact = exact_matches[exact_matches['ms2query_model_prediction'] > 0.7]
to_review_analogs = analogs[(analogs['ms2query_model_prediction'] >= 0.6) & (analogs['ms2query_model_prediction'] <= 0.7)]
print(f'Exact matches (high conf): {len(high_confidence_exact)}, Analogs to review: {len(to_review_analogs)}')
```

## Evaluation signals

- Exact-match branch contains only results with precursor m/z difference < 5 ppm (or your specified tolerance); analog branch contains all others.
- No result rows are lost or duplicated during branching; sum of row counts in both branches equals input row count.
- Results with ms2query_model_prediction < 0.6 are present in both branches but flagged or separated for review; scores > 0.7 are predominantly retained.
- Spot-check: manually verify 5–10 results in each branch confirm expected precursor m/z distances and compound structure similarity (exact matches have identical or nearly identical molecular formulas; analogs differ).
- Branch-specific statistics (mean prediction score, count by match type) are reproducible across re-runs with identical input.

## Limitations

- Precursor m/z difference alone does not guarantee true identity; isotopologue patterns, in-source fragmentation, and adduct misassignment can produce false exact-match candidates. Always cross-validate with retention time, MS1 isotope pattern, or independent confirmation.
- MS2Query model prediction scores are calibrated on the GNPS library (2021-12-15 for default model); accuracy may degrade if your spectra derive from underrepresented compound classes or ionization conditions not in the training set.
- No strict minimum threshold for ms2query_model_prediction is provided; the recommended range (0.6–0.7 for marginal, >0.7 for high confidence) depends on your research goal (recall vs. precision trade-off). Thresholds must be validated empirically per project.
- Branching does not resolve upstream preprocessing issues (e.g., redundant MS/MS spectra per feature); MZmine or equivalent clustering must be applied before MS2Query.
- Analog search results can include both chemically related true analogs and spurious matches; the branching step alone does not validate analog correctness—interpretation requires domain knowledge and additional evidence (e.g., MS/MS fragmentation pattern coherence).

## Evidence

- [readme] MS2Query does not need two different workflows for searching for analogues and searching for exact matches, it automatically selects the most likely library spectra. If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference.: "If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since"
- [other] MS2Query implements workflow branching to separate true library matches from analog search results, as introduced in PR #72.: "MS2Query implements workflow branching to separate true library matches from analog search results, as introduced in PR #72."
- [readme] This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue.: "This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue."
- [readme] To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution"
- [other] Implement conditional logic in the MS2Query codebase that routes spectral results into separate workflow paths based on match type.: "Implement conditional logic in the MS2Query codebase that routes spectral results into separate workflow paths based on match type."
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
