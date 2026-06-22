---
name: ms2-spectral-dissimilarity-scoring
description: Use when you have MS2 fragmentation spectra from multiple metabolomics samples and need to identify samples with unusual spectral profiles that may indicate novel chemistry, independent of feature abundance or annotation status.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3474
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - CANOPUS
  - MEMO
  - GNPS
  - MZmine2 / MZmine3
  - Inventa
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time' columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/), is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- 'Class Component (CC): a score considering the presence of predicted known chemical classes new to the species'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2-Based Spectral Dissimilarity Scoring for Sample Outlier Detection

## Summary

Score natural extract samples based on their general MS2 spectral dissimilarity using the MEMO metric, which generates MS2 fingerprints from peak and neutral loss patterns independent of feature alignment. This identifies spectrally outlier samples to flag potentially novel chemical profiles.

## When to use

Apply this skill when you have MS2 fragmentation spectra from multiple metabolomics samples and need to identify samples with unusual spectral profiles that may indicate novel chemistry, independent of feature abundance or annotation status. Particularly useful when samples have poor feature overlap, strong retention time shifts, or were acquired on different instruments or LC methods.

## When NOT to use

- Input samples are all acquired on identical instruments and LC methods with excellent feature alignment—use feature-based similarity metrics instead.
- MS2 data are unavailable or of poor quality (low spectral resolution, sparse fragmentation patterns).
- The goal is to identify annotation-based novelty rather than spectral dissimilarity; use the Feature or Literature Component instead.

## Inputs

- MS2 fragmentation spectra (from MZmine2/MZmine3 or GNPS)
- Sample metadata (optional: for context and filtering)
- MEMO-format vectorized dissimilarity matrix (MS2 peaks and neutral losses per sample)

## Outputs

- Binary Similarity Component (SC) scores per sample (1=outlier, 0=non-outlier)
- MEMO dissimilarity matrix with outlier annotations
- Machine-learning outlier detection model/results

## How to apply

Load MS2 spectra data and compute a vectorized dissimilarity matrix using the MEMO method, which counts the occurrence of MS2 peaks and neutral losses (relative to precursor m/z) in each sample to generate an MS2 fingerprint. Apply machine-learning-based outlier detection algorithms (e.g., isolation forest, local outlier factor) to the MEMO dissimilarity matrix to assign binary scores: 1 for samples classified as spectral outliers, 0 for others. The rationale is that samples with dissimilar MS2 patterns but similar taxonomy may harbour unexplored chemistry. Use the resulting binary scores as the Similarity Component (SC) in downstream novelty prioritization, where SC=1 indicates high spectral distinctiveness.

## Related tools

- **MEMO** (Computes MS2-based sample vectorization and dissimilarity matrix from peaks and neutral losses; provides input for outlier detection) — https://github.com/mandelbrot-project/memo
- **MZmine2 / MZmine3** (Processes raw MS/MS data and exports MS2 spectra in formats compatible with MEMO and GNPS)
- **GNPS** (Provides standardized MS2 spectral data and metadata formats; job ID used to retrieve spectra)
- **Inventa** (Integrates SC scores into multi-component novelty prioritization pipeline; applies user-defined weights (w3) to SC) — https://github.com/luigiquiros/inventa

## Examples

```
from memo import MEMO; from sklearn.ensemble import IsolationForest; memo = MEMO(ms2_data); dissimilarity_matrix = memo.compute_dissimilarity(); outliers = IsolationForest(contamination=0.1).fit_predict(dissimilarity_matrix); sc_scores = [1 if x == -1 else 0 for x in outliers]
```

## Evaluation signals

- Each sample has exactly one SC score (binary: 0 or 1); no null or out-of-range values.
- Outlier samples detected by ML algorithms have MS2 fingerprints visually distinct from the sample cohort (e.g., via MDS/PCoA or heatmap visualization).
- SC scores are independent of feature annotation status; spectrally outlier samples retain high SC=1 even if annotated features are present.
- Validated outliers correspond to samples with taxonomically distant origins or chemically distinct profiles when cross-checked against metadata.
- Reproducibility check: re-running MEMO + outlier detection on the same input yields identical SC assignments.

## Limitations

- Requires high-quality MS2 spectra; sparse or low-resolution fragmentation patterns reduce discriminatory power and may yield ambiguous outlier assignments.
- Performance depends on machine-learning outlier detection algorithm choice (e.g., isolation forest, local outlier factor); no single algorithm guaranteed optimal for all datasets. Tuning hyperparameters may be necessary.
- MEMO method is agnostic to retention time, so samples with identical MS2 profiles but different chemical origins (isomers, isobars) will not be distinguished.
- Binary SC scoring (0/1) loses nuance; samples near the outlier/non-outlier boundary may be misclassified if the threshold is not carefully chosen.
- Assumes MS2 fragmentation patterns are reproducible across samples and instruments; systematic instrumental drift or method variation can inflate false outlier signals.

## Evidence

- [methods] The Similarity Component (SC) is a complementary score that compares extracts based on their general MS2 spectral information independently from the feature alignment used in FC, using the MEMO: "The Similarity Component (SC) is a complementary score that compares extracts based on their general MS2 spectral information independently from the feature alignment"
- [readme] Ms2 basEd saMple vectorization (MEMO) is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2) of their constituents. The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint"
- [other] The matrix is mined through multiple outlier detection machine learning algorithms to highlight spectrally dissimilar extracts (outliers). An SC value of '1' implies the extract is classified as an outlier within the extract set studied.: "The matrix is mined through multiple outlier detection machine learning algorithms to highlight spectrally dissimilar extracts (outliers)"
- [readme] MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass spectrometers technology: "MEMO suits particularly well to compare chemodiverse samples with poor features overlap, or samples with strong RT shift, acquired using different LC methods or instruments"
