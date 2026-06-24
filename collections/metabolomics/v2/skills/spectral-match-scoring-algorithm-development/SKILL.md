---
name: spectral-match-scoring-algorithm-development
description: Use when when building or extending MS/MS library search tools that must
  re-rank top candidate spectra (e.g., top 2000 from MS2Deepscore) to identify the
  analogue or exact match.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - GitHub
  - MS2Deepscore
  - RDKit
  - scikit-learn
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- you want to make some kind of change to the code base
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
- fork the repository to your own Github profile and create your own feature branch
  off of the latest master commit
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-match-scoring-algorithm-development

## Summary

Design and integrate scoring functions that rank MS/MS spectral library matches by combining structural similarity metrics (InChIKey-based and neighborhood scores) with spectral similarity features. This skill enables MS2Query's random forest re-ranking pipeline to distinguish reliable analogue and exact matches from false positives in full-library searches.

## When to use

When building or extending MS/MS library search tools that must re-rank top candidate spectra (e.g., top 2000 from MS2Deepscore) to identify the best analogue or exact match. Specifically, when you have pre-computed spectral similarity scores and structural metadata (InChIKey, SMILES) for candidates but need a composite scoring scheme to optimize which library match ranks first.

## When NOT to use

- Input library spectra lack structural metadata (InChIKey, SMILES, or INCHI); the neighbourhood and InChIKey scoring components cannot be computed.
- Pre-filtering on precursor m/z has already eliminated candidates; MS2Query's score combination is designed to work on unfiltered top-k sets to discover cross-precursor-mass analogues.
- Query spectra are unannotated or from non-standard formats; MS2Query requires standardized MS2 input (mzML, MGF, MSP, etc.) with valid precursor m/z and peak lists.

## Inputs

- MS2Deepscore similarity scores for top 2000 candidate library spectra (numeric vectors, range 0–1)
- Candidate library spectra with annotated InChIKey or SMILES metadata
- Query spectrum mass-to-charge ratio and precursor m/z
- Structural fingerprints or SMILES strings for all candidates

## Outputs

- Average InChIKey score per candidate (0–1)
- Neighbourhood score per candidate (0–1)
- Combined MS2Query model prediction score (0–1) ranking all candidates
- Top-ranked library match with prediction confidence

## How to apply

Begin by reviewing the scoring algorithm specification (e.g., PR #78) to understand how average InChIKey score and neighbourhood score are defined. Implement two scoring component functions in Python: one computing average InChIKey score across structural analogues in the candidate set, and another estimating neighbourhood score based on Tanimoto or structural similarity thresholds. Integrate both scores as features into a random forest that also includes MS2Deepscore and other spectral metrics. Validate each component against known candidate sets using unit tests, ensuring the combined model's prediction scores range [0, 1] with higher scores indicating reliable matches. Run the full regression test suite (`python setup.py test`) to confirm no existing functionality is broken, then document the new metrics in CHANGELOG.md.

## Related tools

- **MS2Query** (Framework in which scoring components are integrated; orchestrates full-library search, candidate ranking, and result output.) — https://github.com/iomega/ms2query
- **MS2Deepscore** (Provides pre-computed spectral similarity embeddings for the top 2000 candidates that serve as input features to the re-ranking random forest.)
- **RDKit** (Computes structural fingerprints, Tanimoto similarity, and SMILES/InChIKey conversions for neighbourhood score calculation.)
- **scikit-learn** (Implements the random forest model that combines average InChIKey score, neighbourhood score, and spectral metrics.)

## Examples

```
from ms2query.scoring import compute_average_inchikey_score, compute_neighbourhood_score; avg_score = compute_average_inchikey_score(candidate_inchikeys); nb_score = compute_neighbourhood_score(query_fingerprint, candidate_fingerprints, threshold=0.85)
```

## Evaluation signals

- Unit test suite validates that average InChIKey score is correctly computed as the mean structural similarity (via InChIKey matching or Tanimoto distance) over all structural analogues in the candidate set, with output in range [0, 1].
- Neighbourhood score unit tests verify that candidates within a defined structural similarity threshold (e.g., Tanimoto > 0.85) are correctly identified and scored proportionally to their proximity in chemical space.
- Combined MS2Query prediction scores for a held-out test set of query spectra show that the top-ranked match has higher agreement with ground-truth (exact matches or curated analogues) than MS2Deepscore alone, measured by precision or ROC-AUC.
- Regression test suite passes without errors (`python setup.py test`), confirming no existing scoring or matching functionality was broken.
- For dummy test data (dummy_spectra.mgf), output CSV matches the expected_results_dummy_data.csv exactly or within expected variance, validating reproducibility.

## Limitations

- Scoring components require complete structural metadata (InChIKey or SMILES); library spectra lacking this information are excluded from analogue scoring and may not rank correctly.
- MS2Query performs no peak-picking or MS2 spectrum clustering; if input files contain many redundant MS2 spectra per feature, preprocessing with MZMine or similar is advised to avoid inflating candidate ranks with duplicates.
- Random forest re-ranking is trained on the GNPS library (2021-12-15 snapshot for positive mode); scoring performance may degrade for chemically novel compounds or spectra from ions not well-represented in training data.
- No strict minimum prediction score threshold is enforced; the score ranges 0–1 but users must manually select a threshold (suggested > 0.7 for high reliability, 0.6–0.7 with caution, < 0.6 often discarded) based on their precision/recall trade-off.
- InChIKey and neighbourhood scores assume structural similarity is predictive of spectral similarity; compounds with unusual fragmentation patterns may score low despite true structural relationship.

## Evidence

- [other] MS2Query implements scoring mechanisms for MS/MS spectral-based analogue search to enable reliable candidate matching.: "MS2Query implements scoring mechanisms for MS/MS spectral-based analogue search to enable reliable candidate matching."
- [other] Review PR #78 specification and scoring algorithm definitions for average inchikey score and neighbourhood score metrics.: "Review PR #78 specification and scoring algorithm definitions for average inchikey score and neighbourhood score metrics."
- [other] Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity.: "Implement scoring component functions in Python that compute average inchikey score across candidate matches and neighbourhood score based on structural similarity."
- [readme] The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected.: "The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected."
- [readme] a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "a score > 0.7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be"
- [other] make sure the existing tests still work by running ``python setup.py test``: "make sure the existing tests still work by running ``python setup.py test``"
- [other] update the `CHANGELOG.md` file with change: "update the `CHANGELOG.md` file with change"
- [readme] It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library.: "It is important that the library spectra are annotated with smiles, inchi's or inchikeys in the metadata otherwise they are not included in the library."
