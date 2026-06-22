---
name: candidate-neighbourhood-analysis-for-spectral-matching
description: Use when you have a query MS/MS spectrum matched against a library and need to re-rank the top 2000 candidate spectra by combining spectral similarity (MS2Deepscore) with structural neighbourhood information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - MS2Query
  - GitHub
  - MS2Deepscore
  - RDKit
  - matchms
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- fork the repository to your own Github profile and create your own feature branch off of the latest master commit
- use the search functionality [here](https://github.com/iomega/ms2query/issues)
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

# candidate-neighbourhood-analysis-for-spectral-matching

## Summary

Compute neighbourhood score metrics across MS/MS spectral candidate matches to re-rank library hits based on structural similarity clustering. This skill applies scoring components that quantify how similar top-ranked candidates are to each other, enabling MS2Query's random forest re-ranker to distinguish reliable exact matches and analogues from spurious hits.

## When to use

Apply this skill when you have a query MS/MS spectrum matched against a library and need to re-rank the top 2000 candidate spectra by combining spectral similarity (MS2Deepscore) with structural neighbourhood information. Use it specifically when you want to improve hit confidence by identifying whether candidate matches cluster together in chemical space (indicating a reliable match family) or are isolated.

## When NOT to use

- Query spectra without assigned precursor m/z or ionization mode — MS2Query requires ion mode to select the correct pre-trained model.
- Library spectra that lack structural annotation (SMILES, InChI, or InChIKey) — neighbourhood scoring depends on chemical structure metadata.
- High-throughput screening where no precursor m/z prefiltering is acceptable — MS2Query's full-library comparison approach may be slow on very large libraries without library-level optimization.

## Inputs

- Top 2000 ranked candidate library spectra (ranked by MS2Deepscore score)
- Query MS/MS spectrum
- Library spectra with annotated chemical structures (SMILES, InChI, or InChIKey)
- MS2Deepscore embeddings (pre-computed for library spectra)

## Outputs

- Neighbourhood score per candidate (scalar, 0–1 range)
- Average InChIKey score per candidate (scalar, 0–1 range)
- MS2Query model prediction score per candidate (scalar, 0–1 range)
- Ranked and filtered match results (CSV with columns: query_id, library_match, precursor_mz_difference, ms2query_model_prediction, neighbourhood_score, inchikey_score, molecular_class)

## How to apply

After MS2Deepscore ranks the top 2000 candidate library spectra for a query spectrum, compute the neighbourhood score by calculating average structural similarity (via InChIKey or SMILES-derived metrics) between each candidate and its k-nearest neighbours in the ranked list. Combine this neighbourhood score with the average InChIKey score (proportion of top candidates sharing the same InChI layer) as input features into MS2Query's random forest model. The model outputs a final prediction score between 0 and 1; use a threshold (commonly > 0.7 for high-confidence matches, 0.6–0.7 for caution, < 0.6 for discard) to filter reliable hits. This re-ranking step does not require precursor m/z filtering, allowing both exact matches and analogues to be identified in one pass.

## Related tools

- **MS2Query** (Orchestrates the full scoring pipeline, including neighbourhood analysis, within the random forest re-ranking stage for MS/MS library matching.) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Produces initial spectral similarity embeddings and rankings (top 2000) that feed into neighbourhood analysis.)
- **RDKit** (Computes molecular structure similarity and InChI-based metrics (InChIKey layers) for neighbourhood scoring.)
- **matchms** (Provides data structures for MS/MS spectrum representation and metadata (SMILES, InChI, precursor m/z) used in neighbourhood analysis.)

## Examples

```
from ms2query.run_ms2query import run_complete_folder; from ms2query.ms2library import create_library_object_from_one_dir; ms2library = create_library_object_from_one_dir('./ms2query_library_files'); run_complete_folder(ms2library, './ms2_spectra_directory')
```

## Evaluation signals

- Neighbourhood score values fall within [0, 1] range and correlate with structural coherence of top candidates (clusters of similar structures should yield high scores).
- Average InChIKey score matches expected proportions: for exact matches, high agreement on InChIKey layers; for analogues, variable agreement reflecting chemical space divergence.
- Final MS2Query model prediction scores increase monotonically (or nearly so) with combined neighbourhood and inchikey scores, demonstrating that the random forest learned meaningful feature interactions.
- Filtering by prediction score threshold (e.g., > 0.7) produces manually verified high-precision match sets; inspect a sample of filtered matches to confirm they are chemically plausible (exact matches have near-zero precursor m/z difference; analogues show expected structural variations).
- Regression test: re-running neighbourhood analysis on dummy data or a held-out validation set reproduces the expected results CSV (compare to expected_results_dummy_data.csv provided in repository).

## Limitations

- Neighbourhood scoring assumes that structurally similar compounds cluster together in the top 2000 candidates; if library is sparse or query structure is novel, neighbourhood signal may be weak or uninformative.
- InChIKey-based scoring relies on exact structural annotation in the library; missing, malformed, or non-standardized SMILES/InChI fields will cause scoring failures or suboptimal re-ranking.
- No precursor m/z filtering is applied during candidate selection, so neighbourhood analysis must operate on a large candidate set (top 2000); for very large libraries, this can be computationally expensive.
- The random forest model is pre-trained on GNPS 2021-12-15 library; neighbourhood scoring may not generalize well to libraries with very different chemical composition or MS/MS ionization modes not represented in training data.
- Threshold interpretation (e.g., 0.7 for high confidence) is data-dependent and research-goal-dependent; no single universal threshold exists — users must validate thresholds on their own reference matches.

## Evidence

- [readme] By using a minimum threshold for this score, unreliable matches are filtered out.: "By using a minimum threshold for this score, unreliable matches are filtered out."
- [readme] The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "The top 2000 spectra with the highest MS2Deepscore are selected. In contrast to other analogue search methods, no preselection on precursor m/z is performed."
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features."
- [readme] score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be"
- [other] MS2Query implements scoring mechanisms for MS/MS spectral-based analogue search to enable reliable candidate matching.: "MS2Query implements scoring mechanisms for MS/MS spectral-based analogue search to enable reliable candidate matching."
- [other] Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity.: "Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity."
- [other] Integrate both scoring components into the MS2Query match ranking pipeline to combine with existing similarity metrics.: "Integrate both scoring components into the MS2Query match ranking pipeline to combine with existing similarity metrics."
