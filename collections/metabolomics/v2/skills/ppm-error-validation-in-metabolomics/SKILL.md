---
name: ppm-error-validation-in-metabolomics
description: Use when when annotating m/z features from Cardinal MSImagingExperiment
  objects or LC-MS datasets against metabolite databases (HMDB, Lipidmaps) and you
  need to exclude matches where the mass difference exceeds your instrumental accuracy
  or analysis tolerance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - R
  - Cardinal
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ppm-error-validation-in-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validation of mass spectral annotations by constraining matches to observed m/z values within a specified parts-per-million (ppm) error tolerance relative to theoretical database values. This skill filters false-positive or implausible metabolite matches when annotating high-resolution MS features against reference metabolite databases.

## When to use

When annotating m/z features from Cardinal MSImagingExperiment objects or LC-MS datasets against metabolite databases (HMDB, Lipidmaps) and you need to exclude matches where the mass difference exceeds your instrumental accuracy or analysis tolerance. Apply this skill especially when working with full-scan MS data and multiple adduct types, where permissive matching would introduce ambiguity or spurious annotations.

## When NOT to use

- When working with low-resolution instruments (e.g., unit-mass resolution) where ppm-based filtering is not meaningful; use Da-based tolerance instead.
- When the database already contains instrument-specific m/z values rather than theoretical monoisotopic masses, making ppm recalculation redundant or incorrect.
- When annotations have already been filtered by a stricter downstream mechanism (e.g., pseudo-MS/MS or paired targeted metabolic data refinement); applying ppm validation twice may over-constrain results.

## Inputs

- Cardinal MSImagingExperiment object with m/z features (e.g., 767,528 features from featureData())
- Metabolite reference database (HMDB_db, Lipidmaps_db, or equivalent)
- Observed m/z values (numeric vector or extracted from spectral data)
- Adduct specification list (e.g., c('M-H', 'M+Cl') for negative mode)

## Outputs

- Annotated results data.frame with columns: observed_mz, database_match_name, theoretical_mz, ppm_error, adduct
- Filtered annotation set meeting ppm_error threshold
- Annotation statistics (row count of retained matches, ppm distribution)

## How to apply

During AnnotateSM or AnnotateBigData calls, specify the ppm_error parameter to define the maximum allowable deviation (in ppm) between observed m/z and database monoisotopic mass. For example, use ppm_error=3 for high-resolution instruments or ppm_error=15 for lower-resolution platforms. The annotation function will internally compute the ppm error as (abs(observed_mz - database_mz) / database_mz) × 1e6 and retain only matches where this calculated error ≤ the threshold. Inspect the output annotation data.frame to confirm the ppm_error column reflects your constraint, verify row counts match expected annotation yields (e.g., 67,060 matches for HMDB with ppm=3 and M-H/M+Cl adducts), and validate that no spurious low-confidence hits remain by spot-checking high-ppm-error edge cases.

## Related tools

- **SpaMTP** (R package providing AnnotateSM and AnnotateBigData functions that accept and enforce ppm_error parameters for m/z annotation) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Cardinal** (R package providing MSImagingExperiment class and featureData() accessor to extract m/z values for annotation input) — https://github.com/Vitek-Lab/Cardinal3-vignettes

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = "M+K")
```

## Evaluation signals

- Output annotation data.frame contains a ppm_error column with all values ≤ the specified threshold (e.g., max(ppm_error) ≤ 3).
- Row count of retained annotations matches expected yield for the given database and adduct set (e.g., 67,060 matches for HMDB at ppm=3 with M-H/M+Cl).
- No NaN or Inf values in the ppm_error column; all calculations are well-defined.
- Spot-check: randomly sample 10–20 annotations and manually verify that (abs(observed_mz − theoretical_mz) / theoretical_mz) × 1e6 matches the reported ppm_error.
- Comparison of annotation counts across different ppm thresholds shows monotonic decrease (stricter tolerance → fewer matches).

## Limitations

- ppm tolerance is mass-dependent: the same absolute Da tolerance yields different ppm values at different m/z ranges, which may lead to unequal stringency across the mass spectrum.
- ppm_error validation alone does not resolve isomeric ambiguity or confirm true metabolite identity; it only filters mass-based plausibility.
- The article notes two planned refinement sections ('Pseudo MS/MS-Based Refinement' and 'Refinement with Paired Targeted Metabolic Data') are incomplete, suggesting ppm validation may be complemented by future multi-modal filtering.
- Database quality and completeness affect filtering effectiveness; missing or incorrectly annotated theoretical masses in the reference database will propagate into false positives or false negatives.

## Evidence

- [other] ppm_error=3 and M-H/M+Cl negative adducts: "AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'), polarity='negative'"
- [other] Verification of output structure includes ppm_error column: "confirm presence of observed_mz, database_match_name, ppm_error, and adduct columns"
- [methods] Lower ppm tolerance on different instrument platform: "ppm_error = 15, adducts = "M+K""
- [other] Expected annotation yield at ppm=3 for HMDB: "verify the row count equals the reported 67,060 annotated m/z values"
- [methods] Application of ppm error in AnnotateSM function: "AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15"
