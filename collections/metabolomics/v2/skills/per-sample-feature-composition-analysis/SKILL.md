---
name: per-sample-feature-composition-analysis
description: Use when when you have aligned and quantified mass spectrometry features
  from multiple natural extracts (via MZmine2/3), paired with in silico annotation
  results (ISDB or SIRIUS), and you need to prioritize samples for chemical discovery
  based on the proportion of unannotated, extract-specific.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - SIRIUS
  - Ion Identity
  - Inventa
  - MEMO
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time'
  columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/),
  is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico
  annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Per-sample feature composition analysis

## Summary

Quantify the structural novelty potential of individual samples in a natural extract set by computing the ratio of specific non-annotated features to total features (Feature Component), integrated with optional annotation filtering and Ion Identity redundancy reduction. This metric identifies samples enriched in unannotated, sample-specific compounds.

## When to use

When you have aligned and quantified mass spectrometry features from multiple natural extracts (via MZmine2/3), paired with in silico annotation results (ISDB or SIRIUS), and you need to prioritize samples for chemical discovery based on the proportion of unannotated, extract-specific peaks rather than global similarity or taxonomy alone.

## When NOT to use

- Input is a pre-processed feature matrix with already-collapsed or pre-filtered features (e.g., from deconvolution or consensus workflows); recomputing specificity may lose or duplicate information.
- Annotation results are unavailable or not quality-filtered; FC will be biased by false positive or low-confidence annotations.
- Sample set is very small (n < 3–5); feature specificity thresholds become unstable and single-sample outliers dominate the ranking.

## Inputs

- MZmine2 or MZmine3 quantitative feature table (Peak area, row m/z, row retention time)
- GNPS metadata table (GNPS format, with ATTRIBUTE_Species and ATTRIBUTE_Organe headers)
- ISDB annotation results or SIRIUS compound_identification.tsv (with quality metrics)
- Ion Identity grouping results (optional, for feature redundancy reduction)

## Outputs

- Per-sample Feature Component (FC) ratio (0–1 scale)
- Per-sample annotated and unannotated feature counts
- Per-sample feature specificity breakdown
- TSV file with ranked samples, component values, and priority scores

## How to apply

Load the MZmine peak area table (retaining only 'Peak area', 'row m/z', and 'row retention time' columns) and metadata. Filter annotation results by user-defined thresholds (ppm_error, shared_peaks, cosine score for ISDB; ZodiacScore and ConfidenceScore for SIRIUS). Compute feature specificity as the proportion of samples in the extract set where each feature is detected; retain features exceeding a min_specificity threshold (e.g., 90%). Classify each feature as annotated or unannotated based on the filtered annotations, optionally applying Ion Identity grouping to collapse redundant isobaric features. For each sample, calculate FC as (count of specific non-annotated features) / (total features in that sample). Output per-sample FC ratios and normalized component breakdowns to identify samples with high novelty potential.

## Related tools

- **MZmine2** (Peak detection, alignment, and quantification; provides Peak area, m/z, and retention time columns as input)
- **MZmine3** (Modern successor to MZmine2 for feature extraction and quantification; compatible input format)
- **timaR** (In silico annotation and taxonomically informed reweighting of ISDB and spectral library matches) — https://taxonomicallyinformedannotation.github.io/tima-r/index.html
- **SIRIUS** (Molecular formula and compound identification; produces ZodiacScore and ConfidenceScore metrics for filtering) — https://bio.informatik.uni-jena.de/software/sirius/
- **Ion Identity** (Feature grouping and redundancy reduction to collapse isobaric and adduct variants before FC computation)
- **Inventa** (Reference implementation that orchestrates feature filtering, specificity computation, annotation integration, and per-sample FC ratio calculation) — https://github.com/luigiquiros/inventa
- **MEMO** (Complementary MS2-based sample vectorization for outlier detection and Similarity Component scoring (optional enhancement)) — https://github.com/mandelbrot-project/memo

## Examples

```
# In the Inventa Jupyter notebook: set quantitative_data_filename='MZmine_quant.csv', annotation_preference=0 (non-annotated only), min_specificity=90, ppm_error=5, cosine=0.7, min_ZodiacScore=0.9; then call the FC calculation step to produce per-sample FC ratios in the results TSV.
```

## Evaluation signals

- Per-sample FC values fall within [0, 1] and sum of annotated and non-annotated feature counts equals total feature count per sample (schema consistency).
- Feature specificity values are monotonic: features retained have specificity ≥ min_specificity threshold; features below threshold are excluded.
- Annotation filtering reduces the total number of annotated features (before vs. after) without introducing negative counts or orphaned features.
- Samples with higher FC scores exhibit lower total annotation coverage relative to their feature count; manually inspecting top-ranked samples confirms presence of unannotated peaks.
- Ion Identity grouping (if used) reduces total feature count per sample without changing FC rank order by more than a small tolerance (feature collapse should be deterministic).

## Limitations

- FC metric is independent of annotation confidence or spectral quality; a feature marked 'unannotated' because it failed a strict cosine threshold (e.g., 0.7) will contribute equally to FC as a truly unknown compound.
- Feature specificity threshold (e.g., 90%) is user-defined and sensitive to extract set composition; small or redundant extract sets may yield unstable or uninformative specificity values.
- Ion Identity grouping requires prior untargeted networking and may not be applicable to all mass spectrometry platforms (e.g., low-resolution ToF).
- FC does not account for biological or ecological context; high-FC samples may reflect contamination, cultivation artifacts, or non-novel but rare features rather than true chemical discovery potential.
- No changelog or version tracking in the article or referenced tools; reproducibility across inventa updates is not guaranteed.

## Evidence

- [methods] The Feature Component is computed as the ratio of the number of specific non-annotated features to the total number of features for each extract.: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."
- [methods] Load MZmine2 or MZmine3 quantitative feature table extracting peak area, m/z, and retention time columns, then filter ISDB annotations by ppm_error, shared_peaks, cosine score, and min_score_final threshold; filter SIRIUS by min_ZodiacScore and min_ConfidenceScore.: "Load the quantitative feature table from MZmine2 or MZmine3, extracting peak area, m/z, and retention time columns. Load metadata and annotation results (timaR ISDB output and/or SIRIUS"
- [methods] Compute feature specificity for each feature as the proportion of samples in the extract set where that feature is present; retain features exceeding min_specificity threshold.: "Compute feature specificity for each feature as the proportion of samples in the extract set where that feature is present; retain features exceeding min_specificity threshold (e.g., 90%)."
- [methods] Mark features as annotated or unannotated based on filtered annotation results; optionally apply Ion Identity grouping to reduce redundant features.: "Mark features as annotated or unannotated based on filtered annotation results; optionally apply Ion Identity grouping to reduce redundant features."
- [methods] For each sample, calculate FC as (count of specific non-annotated features) / (total features in sample); output per-sample FC ratio and component breakdown.: "For each sample, calculate FC as (count of specific non-annotated features) / (total features in sample); output per-sample FC ratio and component breakdown."
- [readme] MZmine output format uses only the 'Peak area', 'row m/z' and 'row retention time' columns. Inventa takes input directly from MZmine2 or MZmine 3.: "MZmine output format using only the 'Peak area', 'row m/z', and 'row retention time' columns. ... Inventa takes input directly from MZmine2 or MZmine 3"
- [readme] Inventa is capable to perform the calculations based on the results from Ion Identity, reducing the total number of features.: "Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features."
