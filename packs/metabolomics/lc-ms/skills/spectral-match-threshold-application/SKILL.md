---
name: spectral-match-threshold-application
description: Use when after running spectral matching (e.g., GNPS library search, SIRIUS in silico annotation) and obtaining an annotation table with confidence scores, apply threshold filtering to remove low-confidence or spurious matches before downstream analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SIRIUS
  - GNPS
  - Inventa
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans: []
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

# Spectral Match Threshold Application

## Summary

Apply confidence score cutoffs to MS/MS spectral annotations to retain only high-quality matches from spectral databases or in silico prediction tools. This skill filters annotation tables by requiring matches to meet or exceed user-defined thresholds on metrics like cosine similarity, shared peak count, and mass accuracy.

## When to use

After running spectral matching (e.g., GNPS library search, SIRIUS in silico annotation) and obtaining an annotation table with confidence scores, apply threshold filtering to remove low-confidence or spurious matches before downstream analysis (e.g., Feature Component calculation, chemical class assignment, or priority scoring in natural product discovery).

## When NOT to use

- Input is already a curated or manually validated annotation set — re-filtering may introduce unnecessary data loss.
- Thresholds are not defined or justified for your annotation source — arbitrary cutoffs risk over-filtering or under-filtering.
- You need to preserve all annotations for comparison or exploratory analysis — thresholding is irreversible without the original file.

## Inputs

- Annotation table in TSV format (e.g., compound_identification.tsv from SIRIUS, GNPS spectral library matches, or ISDB database search results)
- Metadata defining threshold parameters (cosine, shared_peaks, ppm_error, min_ZodiacScore, min_ConfidenceScore, min_score_final)

## Outputs

- Filtered annotation table (TSV format) containing only rows meeting all confidence thresholds
- Annotation count summary (rows retained vs. removed)

## How to apply

Load the annotation table (TSV format with confidence score columns such as cosine, Zodiac score, or shared peak counts). Define threshold parameters: minimum cosine similarity (e.g., 0.7), minimum shared peaks (e.g., 10), maximum ppm mass error (e.g., 5 ppm), and annotation-specific confidence cutoffs (e.g., min_ZodiacScore = 0.9 for SIRIUS, min_score_final = 0.0 for ISDB). Apply these thresholds sequentially or in combination as boolean filters to retain only rows meeting all criteria. Write the filtered table to a new TSV file preserving all original columns for retained rows. Validate the output by confirming row count is ≤ input row count and spot-checking that all remaining annotations meet the specified thresholds.

## Related tools

- **SIRIUS** (Generates Zodiac and Cosmic confidence scores for in silico molecular formula and structure annotation; output filtered by min_ZodiacScore threshold) — https://bio.informatik.uni-jena.de/software/sirius/
- **GNPS** (Performs spectral library matching to generate cosine similarity and shared peak metrics; thresholds applied to clean up annotations before downstream analysis) — https://gnps.ucsd.edu
- **Inventa** (Implements threshold filtering for ppm_error, shared_peaks, cosine, min_ZodiacScore, min_ConfidenceScore, and min_score_final as part of annotation cleaning and Feature Component calculation) — https://github.com/luigiquiros/inventa

## Examples

```
# In Inventa notebook:
min_ZodiacScore = 0.9  # Retain only SIRIUS annotations with Zodiac score ≥ 0.9
ppm_error = 5          # Retain annotations within 5 ppm mass error
shared_peaks = 10      # Retain matches with ≥10 shared MS2 peaks
cosine = 0.7           # Retain spectral matches with cosine similarity ≥ 0.7
# Filter is applied during annotation cleaning before Feature Component calculation
```

## Evaluation signals

- Output row count is ≤ input row count (no rows added, only removed or retained).
- All retained rows have cosine ≥ threshold, shared_peaks ≥ threshold, ppm_error ≤ threshold, and (if applicable) min_ZodiacScore ≥ threshold.
- No rows in output violate any of the specified filter criteria; spot-check a sample of retained rows.
- Filter parameter values are documented and match the analysis goal (e.g., high stringency for Feature Component vs. exploratory annotation).
- Output file retains all original columns and metadata, with no unintended data loss.

## Limitations

- Threshold values are user-defined and dataset-specific; suboptimal thresholds may result in over-filtering (missing true annotations) or under-filtering (retaining false positives).
- Different annotation sources (SIRIUS, GNPS, ISDB) use different scoring metrics; thresholds cannot be directly transferred between sources.
- Thresholding assumes independence between scoring dimensions (cosine, shared peaks, ppm error); some metrics may be correlated, potentially biasing the filtered set.
- No automatic mechanism to validate whether retained annotations are chemically or biologically plausible; manual curation may be needed for high-stakes applications.

## Evidence

- [other] min_ZodiacScore = 0.9 #cut-off filter for considering a sirius annotation valable: "min_ZodiacScore = 0.9 #cut-off filter for considering a sirius annotation valable"
- [other] The min_ZodiacScore filtering mechanism applies a cut-off threshold of 0.9 to retain only SIRIUS annotations meeting or exceeding this confidence score, removing lower-scoring rows from the annotation table.: "The min_ZodiacScore filtering mechanism applies a cut-off threshold of 0.9 to retain only SIRIUS annotations meeting or exceeding this confidence score"
- [other] Parse the Zodiac score column and apply a minimum threshold filter (min_ZodiacScore = 0.9) to retain only rows where Zodiac score is ≥ 0.9.: "Parse the Zodiac score column and apply a minimum threshold filter (min_ZodiacScore = 0.9) to retain only rows where Zodiac score is ≥ 0.9"
- [other] ppm_error = 5 # min error in ppm to consider an annotation valable: "ppm_error = 5 # min error in ppm to consider an annotation valable"
- [other] shared_peaks = 10 # min number of shared peaks between the MS2 experimental and MS2 fro, the database, to consider an annotation valable: "shared_peaks = 10 # min number of shared peaks between the MS2 experimental and MS2 fro, the database"
- [other] cosine = 0.7 # min cosine score to consider an annotation valable: "cosine = 0.7 # min cosine score to consider an annotation valable"
- [other] Write the filtered annotation table to a new TSV file, retaining all original columns for retained rows.: "Write the filtered annotation table to a new TSV file, retaining all original columns for retained rows"
- [other] For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks: "For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks"
