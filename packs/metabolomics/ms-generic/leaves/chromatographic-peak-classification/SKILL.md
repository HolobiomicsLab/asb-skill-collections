---
name: chromatographic-peak-classification
description: Use when you have (1) a benchmark dataset of reference peaks with validated m/z, retention time boundaries, and isotopologue assignments, and (2) NPP output feature tables (unaligned and aligned) from tools like XCMS, MZmine 2, or MS-DIAL that you wish to evaluate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzRAPP
  - R
  - enviPat
  - XCMS
  - MZmine 2
  - Skyline
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-classification

## Summary

Classify benchmark chromatographic peaks detected by non-targeted preprocessing (NPP) tools into status categories (found, split, missing, misaligned) by matching against reference peaks with known m/z, retention time boundaries, and isotopologue identities. This enables quantitative assessment of NPP reliability in LC-HRMS metabolomics.

## When to use

Apply this skill when you have (1) a benchmark dataset of reference peaks with validated m/z, retention time boundaries, and isotopologue assignments, and (2) NPP output feature tables (unaligned and aligned) from tools like XCMS, MZmine 2, or MS-DIAL that you wish to evaluate. Use it to generate a matching record that quantifies how well the NPP tool recovered, split, or missed the known peaks.

## When NOT to use

- NPP output is already a curated, manually validated peak list — use this skill on raw automated NPP results, not manually post-processed features.
- Benchmark peaks lack isotopologue boundary information or retention time windows — this skill requires precise chromatographic boundaries for all enviPat-predicted isotopologues.
- Input mzML files are not centroided — mzRAPP requires centroided mzML format; use MSconvert to prepare raw vendor files first.

## Inputs

- Benchmark peak CSV file (molecule identifier, m/z value, retention time boundaries, isotopologue identifier, adduct type)
- NPP unaligned feature table (m/z, retention time, peak intensity/area)
- NPP aligned feature table (m/z, aligned retention time, peak intensity/area)
- Sample metadata and target molecule file

## Outputs

- Matched record CSV table with columns: benchmark peak ID, matching status (found/split/missing/misaligned), matched NPP feature ID, confidence scores, isotopologue validation flags
- Performance metrics per NPP tool: percentage of peaks found (83–99%), percentage of split peaks, percentage with degenerated isotopologue ratio (1–53%)

## How to apply

Load benchmark peaks (with m/z, retention time boundaries, isotopologue identifiers, adduct types) and NPP output feature tables into mzRAPP. For each benchmark peak, apply m/z matching with 6 ppm precision tolerance and 5 ppm accuracy threshold to identify candidate NPP features. Narrow candidates using retention-time windowing to the expected chromatographic boundaries. For isotopologue clusters, validate peak shape correlation (Pearson r ≥ 0.85) with the most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%. Assign each benchmark peak to one of four categories: 'found' (single NPP match), 'split' (multiple NPP matches), 'missing' (no NPP match), or 'misaligned' (detected outside expected RT window). Generate a matched record CSV containing benchmark peak ID, classification status, matched NPP feature ID if found, confidence scores, and isotopologue validation flags for both unaligned and aligned feature tables.

## Related tools

- **mzRAPP** (Primary tool implementing benchmark–NPP peak matching, isotopologue validation, and classification workflow) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Predicts isotopologue m/z and abundance patterns for target molecules; integrated into mzRAPP for isotopologue envelope definition)
- **XCMS** (Example NPP tool whose output feature tables are classified by this skill; generates unaligned and aligned feature matrices)
- **MZmine 2** (Alternative NPP tool for which this skill classifies detected peaks; output compared against benchmark)
- **Skyline** (Optional downstream tool for manual inspection and export of benchmark peaks with validated retention time boundaries)
- **R** (Environment for running mzRAPP and reproducing matching/classification via library(mzRAPP) or R scripts)

## Examples

```
library(mzRAPP); benchmark <- read.csv('Benchmark_MTBLS267.csv'); npp_unaligned <- read.csv('XCMS_Run1_unaligned_peaks.csv'); npp_aligned <- read.csv('XCMS_Run1_aligned_peaks.csv'); matched_record <- classifyPeaks(benchmark, npp_unaligned, npp_aligned, mz_tol_ppm = 6, rt_tol_ppm = 5, iso_ratio_threshold = 0.30, cor_threshold = 0.85); write.csv(matched_record, 'XCMS_Run1_classification.csv')
```

## Evaluation signals

- Benchmark dataset composition is confirmed: exactly 47 molecules, 157 features (adducts + isotopologues), 2870 total peaks extracted and validated before classification.
- All benchmark peaks are assigned to exactly one of four classes (found/split/missing/misaligned); no unclassified records remain.
- For 'found' peaks, matched NPP feature m/z is within 6 ppm precision and 5 ppm accuracy of benchmark; retention time is within provided boundaries.
- For isotopologue clusters classified as 'found', peak shape correlation to most abundant isotopologue is ≥ 0.85 and isotopologue ratio bias is < 30%.
- Performance summary statistics (e.g., 'XCMS detected 93–99% of peaks post-alignment with 3–20% degenerated IR') are generated and match expected ranges from comparable NPP runs.

## Limitations

- Classification accuracy depends critically on accurate retention time boundaries and isotopologue m/z predictions; incomplete or incorrect boundary specification will inflate 'missing' or 'misaligned' counts.
- The 30% isotopologue ratio bias threshold and 0.85 Pearson correlation cutoff are fixed; peaks near these boundaries may be sensitivity-dependent and require manual review.
- Benchmark peaks with poor chromatographic resolution or overlapping isotopologue signals may be incorrectly split or misclassified when NPP reports multiple co-eluting features.
- Classification does not account for chemical background, matrix effects, or instrument drift; benchmark data should be acquired under consistent, representative conditions.
- Split classification (one benchmark peak matching multiple NPP features) may reflect genuine NPP over-segmentation or may arise from isotopologue doublets not fully resolved in the benchmark; additional curation may be needed.

## Evidence

- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [other] For each benchmark peak, apply m/z matching with specified precision tolerance (6 ppm) and accuracy threshold (5 ppm) to candidate NPP features.: "apply m/z matching with specified precision tolerance (6 ppm) and accuracy threshold (5 ppm) to candidate NPP features"
- [other] Apply retention-time windowing to narrow candidate matches to the expected chromatographic boundaries provided in the benchmark.: "Apply retention-time windowing to narrow candidate matches to the expected chromatographic boundaries provided in the benchmark"
- [other] Classify each benchmark peak as 'found', 'split' (matched to multiple NPP peaks), 'missing', or 'misaligned' based on the matching result in both unaligned and aligned feature tables.: "Classify each benchmark peak as 'found', 'split' (matched to multiple NPP peaks), 'missing', or 'misaligned' based on the matching result"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 are removed"
- [methods] XCMS run 1 detected 83-94% of peaks with 28-53% degenerated isotopologue ratio. XCMS run 3 improved detection to 93-99% of peaks with 3-20% degenerated isotopologue ratio.: "XCMS run 1 detected 83-94% of peaks with 28-53% degenerated isotopologue ratio; XCMS run 3 improved detection to 93-99% of peaks with 3-20% degenerated isotopologue ratio"
