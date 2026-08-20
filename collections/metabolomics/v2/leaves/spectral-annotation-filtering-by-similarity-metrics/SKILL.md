---
name: spectral-annotation-filtering-by-similarity-metrics
description: Use when after running GNPS molecular networking, SIRIUS compound identification,
  or ISDB in silico annotation on LC-MS/MS data, when you have provisional annotations
  for features but need to filter them to retain only high-confidence matches before
  calculating novelty scores, detecting chemical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - CANOPUS
  - MEMO
  - GNPS
  - SIRIUS
  - ISDB
  - MZmine2/MZmine3
  - Inventa
  techniques:
  - LC-MS
  license_tier: open
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
- 'Class Component (CC): a score considering the presence of predicted known chemical
  classes new to the species'
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

# Spectral Annotation Filtering by Similarity Metrics

## Summary

Filter and retain high-confidence mass spectrometry annotations by applying empirical similarity thresholds (cosine score, shared peaks, ppm error, and ZodiacScore) to in silico or database-matched compound identities. This skill ensures that only structurally plausible annotations meeting multi-dimensional spectral agreement criteria are used in downstream metabolomic analysis.

## When to use

After running GNPS molecular networking, SIRIUS compound identification, or ISDB in silico annotation on LC-MS/MS data, when you have provisional annotations for features but need to filter them to retain only high-confidence matches before calculating novelty scores, detecting chemical classes, or building metabolite inventories. Use when combining annotations from multiple sources (GNPS, SIRIUS, ISDB) and parameter heterogeneity requires standardization.

## When NOT to use

- When input annotations are already manually curated or from a small, highly curated reference library (e.g. pure standards)—threshold-based filtering may over-filter or introduce bias.
- When spectral data are from different ionization modes or MS instruments not represented in your reference database—similarity metrics may be artificially low and thresholds inappropriate.
- When the goal is exploratory annotation ranking rather than strict novelty filtering—excessive filtering may obscure biological signals and lower Feature Component scores artificially.

## Inputs

- GNPS molecular networking job results with candidate annotations
- SIRIUS compound_identification.tsv with ZodiacScore and ConfidenceScore columns
- ISDB in silico annotation results with cosine similarity and shared peaks
- MZmine2/MZmine3 feature table with m/z and retention time
- Annotation metadata table specifying annotation source (GNPS/SIRIUS/ISDB) and associated scores

## Outputs

- Filtered annotation table retaining only high-confidence matches meeting all similarity thresholds
- Binary indicator column marking which features retain annotations after filtering
- Filtered Feature Component (FC) input: non-annotated feature set after removal of low-confidence annotations
- Summary statistics on annotation retention rate and threshold application per annotation source

## How to apply

Apply four complementary similarity and scoring filters in sequence: (1) cosine similarity ≥ 0.7 to ensure MS2 spectral overlap; (2) shared_peaks ≥ 10 to confirm that experimental and library MS2 spectra have minimum fragment agreement; (3) ppm_error ≤ 5 to retain only mass matches within 5 ppm tolerance; (4) for SIRIUS annotations, apply min_ZodiacScore ≥ 0.9 to filter by structural plausibility scored by the Zodiac ranking system. For ISDB annotations, optionally apply min_score_final ≥ 0.0 (or higher if stricter filtering is required). These thresholds are user-configurable and should be adjusted based on instrument resolution, ionization mode, and database characteristics. The filtering workflow reduces false-positive annotations while preserving structurally relevant features for novelty discovery and component scoring.

## Related tools

- **GNPS** (Source of molecular networking job ID and candidate annotations; provides cosine-based spectral matching results)
- **SIRIUS** (Generates compound_identification.tsv with ZodiacScore and ConfidenceScore for de novo structure elucidation; output filtered by min_ZodiacScore threshold) — https://bio.informatik.uni-jena.de/software/sirius/
- **ISDB** (In silico spectral library matching; annotations filtered by cosine score, shared peaks, and ppm error thresholds)
- **MZmine2/MZmine3** (Feature detection and quantification; input feature table used to map filtered annotations back to features)
- **Inventa** (Applies these filtering parameters during Feature Component and downstream novelty scoring pipeline; accepts cleaned annotation tables from this skill) — https://github.com/luigiquiros/inventa

## Examples

```
ppm_error = 5; shared_peaks = 10; cosine = 0.7; min_ZodiacScore = 0.9; min_ConfidenceScore = 0.0; annotations_filtered = annotations[(annotations['ppm_error'] <= ppm_error) & (annotations['shared_peaks'] >= shared_peaks) & (annotations['cosine'] >= cosine) & (annotations['ZodiacScore'] >= min_ZodiacScore)].copy()
```

## Evaluation signals

- Verify that the number of retained annotations is strictly ≤ the input annotation count; confirm 0% false-positive retention.
- Check that all retained annotations meet ALL four thresholds simultaneously (cosine ≥ 0.7 AND shared_peaks ≥ 10 AND ppm_error ≤ 5 AND ZodiacScore ≥ 0.9); no annotation should pass if any single threshold fails.
- Confirm that the filtered annotation table has no null values in the similarity metric columns and that Feature Component (FC) is recomputed as ratio of (non-annotated features after filtering) / (total features).
- Validate that output retains all expected columns from input (m/z, retention time, annotation source, cosine, shared_peaks, ppm_error, ZodiacScore, ConfidenceScore) and adds a binary 'filtered_pass' column.
- Spot-check 5–10 borderline annotations (e.g., cosine = 0.70, shared_peaks = 10) to confirm threshold application is consistent and reproducible.

## Limitations

- Thresholds are empirically derived and may be overly stringent or permissive for atypical sample types (e.g., lipids, halogenated compounds, sulfated metabolites) not well-represented in SIRIUS or ISDB reference databases.
- Filtering assumes that cosine similarity, shared peaks, and ppm error are orthogonal metrics; in practice, high cosine scores often co-occur with high shared_peaks, reducing the effective filtering stringency.
- When annotations from SIRIUS and ISDB are combined, their confidence scores (ZodiacScore vs. score_final) may not be directly comparable; separate threshold application per source is advised but is not automated in the referenced Inventa notebook.
- No changelog found for threshold parameter versioning; it is unclear whether thresholds (ppm=5, cosine=0.7, shared_peaks=10) were optimized for a specific MS instrument class or are general recommendations.
- Filtering does not account for false-negatives: some true metabolites may fall below thresholds due to poor ionization, low abundance, or database incompleteness, reducing the reported Feature Component and potentially underestimating novelty.

## Evidence

- [other] For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks: "For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks"
- [other] cosine = 0.7 # min cosine score to consider an annotation valable: "cosine = 0.7 # min cosine score to consider an annotation valable"
- [other] min_ZodiacScore = 0.9 #cut-off filter for considering a sirius annotation valable: "min_ZodiacScore = 0.9 #cut-off filter for considering a sirius annotation valable"
- [other] min_ConfidenceScore = 0.0 #cut-off filter for considering a sirius annotation valable: "min_ConfidenceScore = 0.0 #cut-off filter for considering a sirius annotation valable"
- [other] Calculate Feature Component (FC) as ratio of specific non-annotated features (with specificity ≥ min_specificity threshold of 90%) over total features per sample, optionally incorporating ISDB and SIRIUS annotations filtered by ppm_error=5, shared_peaks=10, cosine=0.7, min_ZodiacScore=0.9, min_ConfidenceScore=0.0.: "Calculate Feature Component (FC) as ratio of specific non-annotated features (with specificity ≥ min_specificity threshold of 90%) over total features per sample, optionally incorporating ISDB and"
- [other] Set annotation cleaning parameters (ppm_error, shared_peaks, cosine, ionisation_mode): "Set annotation cleaning parameters (ppm_error, shared_peaks, cosine, ionisation_mode)"
