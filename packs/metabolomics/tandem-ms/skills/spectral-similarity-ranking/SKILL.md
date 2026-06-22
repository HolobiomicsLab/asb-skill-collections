---
name: spectral-similarity-ranking
description: Use when you have a query MS/MS spectrum and need to identify the -matching library spectrum from a large spectral database, particularly when the research goal requires distinguishing between exact matches and structural analogues without separate workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2Query
  - MS2Deepscore
  - matchms
  - RDKit
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-ranking

## Summary

Rank candidate library spectra against a query MS/MS spectrum using machine-learning-derived similarity scores and spectral feature overlap to identify the most likely exact match or structural analogue. This skill combines fast spectral similarity pre-filtering with refined ranking to optimize analogue and exact-match detection simultaneously.

## When to use

Apply this skill when you have a query MS/MS spectrum and need to identify the best-matching library spectrum from a large spectral database, particularly when the research goal requires distinguishing between exact matches and structural analogues without separate workflows. Use it after query spectra have been parsed into standard m/z and intensity pairs and a pre-computed library with spectral embeddings is available.

## When NOT to use

- Input spectra have not been preprocessed or clustered; if your MS data contains many redundant spectra per feature, cluster or apply feature selection first (e.g., via MZMine) before ranking.
- Library spectra lack pre-computed MS2Deepscore embeddings; re-ranking depends on fast similarity pre-filtering and cannot be applied to raw, unembedded libraries.
- Ion mode of query spectra is unknown or mixed; MS2Query models are trained separately for positive and negative ion modes and will not transfer across modes.

## Inputs

- query MS/MS spectrum (m/z and intensity pairs in standard format: mzML, MGF, MSP, mzXML, or pickled matchms object)
- spectral library with pre-computed MS2Deepscore embeddings in SQLite format
- pre-trained random forest model for MS2Query (ion-mode-specific: positive or negative)

## Outputs

- ranked list of candidate library matches, one per query spectrum
- MS2Query model prediction score (0–1) for the top candidate
- library identifier, precursor m/z, and preliminary match score for each match
- precursor m/z difference column to distinguish exact matches from analogues
- estimated molecular class annotations for the matched library compound

## How to apply

First, compute MS2Deepscore spectral similarity scores between the query spectrum and all library spectra using pre-computed embeddings; this avoids expensive full-library comparison and yields scores very quickly. Select the top 2000 library spectra by MS2Deepscore without precursor m/z prefiltering to preserve analogue candidates. Then apply a random forest model that re-ranks these candidates by combining five features: precursor m/z difference, spectral feature overlap, and three derived similarity metrics. The random forest outputs a prediction score between 0 and 1 for each candidate. Select the highest-scoring candidate as the best match and filter out predictions below a threshold (0.7 for high-confidence analogues and exact matches; 0.6–0.7 range for exploratory analysis; below 0.6 generally discarded). The precursor m/z difference column can optionally stratify results into exact matches (near-zero difference) versus analogues.

## Related tools

- **MS2Deepscore** (Computes fast spectral similarity embeddings and scores between query and library spectra; used for initial candidate pre-filtering (top 2000))
- **MS2Query** (Main tool housing the random forest re-ranking model and candidate selection workflow; orchestrates pre-filtering and ranking) — https://github.com/iomega/ms2query
- **matchms** (Python library for spectral data parsing and manipulation; accepts and serializes MS/MS spectra in multiple formats)
- **RDKit** (Computes molecular class annotations from matched library compound structures (SMILES/InChI/InChIKey))

## Examples

```
from ms2query.run_ms2query import run_complete_folder
from ms2query.ms2library import create_library_object_from_one_dir
ms2library = create_library_object_from_one_dir('./ms2query_library_files')
run_complete_folder(ms2library, './ms2_spectra_directory')
```

## Evaluation signals

- Top candidate score distribution is concentrated near 1.0 for true positives (correct exact matches or literature-verified analogues) and near 0.0 for false positives.
- Precursor m/z difference for true exact matches is near zero (< 5 ppm typical tolerance); analogues show larger m/z differences consistent with structural modifications.
- When manual curation or reference standards are available, recall and precision at thresholds 0.6, 0.7, and 0.8 match or exceed published benchmarks (MS2Query outperforms Cosine Score and Modified Cosine in the literature).
- Results CSV file contains all expected columns: query spectrum identifier, top library match identifier, precursor m/z difference, ms2query_model_prediction, and molecular class annotations.
- Analogues are correctly ranked above/below exact matches when both are present in the library, as indicated by the MS2Query prediction score weighting precursor m/z and spectral feature overlap.

## Limitations

- MS2Query does not perform peak picking or de-replication; input spectra should be preprocessed (e.g., via MZMine) to reduce redundancy and improve ranking signal.
- Pre-filtering to top 2000 candidates by MS2Deepscore may exclude distant analogues with low initial similarity but high structural relevance; no precursor m/z prefiltering mitigates this but does not eliminate it.
- Random forest model is trained on GNPS library (2021-12-15 snapshot); performance on compounds outside GNPS chemical space or from highly specialized libraries is not characterized.
- Ion-mode-specific models exist only for positive and negative modes; detection of mixed-ion-mode spectra or spectra of unknown polarity will fail or produce invalid matches.
- Streamlit web app has been archived and is no longer maintained; command-line and programmatic Python interfaces are the supported paths forward.

## Evidence

- [readme] By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly. The top 2000 spectra with the highest MS2Deepscore are selected.: "By using pre-computed MS2Deepscore embeddings for library spectra, this full-library comparison can be computed very quickly. The top 2000 spectra with the highest MS2Deepscore are selected."
- [readme] MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library and query spectrum and the highest scoring library match is selected.: "MS2Query optimizes re-ranking the best analogue or exact match at the top by using a random forest that combines 5 features. The random forest predicts a score between 0 and 1 between each library"
- [readme] This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good match/analogue.: "This column contains a score, which indicates the likelihood that the found match is a good match. This score ranges between 0 and 1, the closer this score is to 1 the more likely that it is a good"
- [readme] To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results below 0.6 can often best be discarded.: "To give a general indication, a score > 0,7 has many good analogues and exact matches. In the range of 0.6-0.7, the results can still be useful, but should be analysed with more caution and results"
- [readme] In contrast to other analogue search methods, no preselection on precursor m/z is performed.: "In contrast to other analogue search methods, no preselection on precursor m/z is performed."
- [readme] If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since exact matches should have no precursor mz difference.: "If it is important to separate potential exact matches from potential analogues for your research question, the column with the precursor mz difference can be used to separate these results, since"
