---
name: adduct-ion-prediction-and-filtering
description: 'Use when when annotating m/z features against a metabolite database (HMDB, Lipidmaps, etc.) and the sample preparation, ionization method, or polarity mode favors specific adduct species. For example: negative-mode LC-MS or MS imaging will preferentially generate M-H and halide adducts (M+Cl);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpaMTP
  - R
  - Cardinal
  - HMDB
  - Lipidmaps
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
---

# adduct-ion-prediction-and-filtering

## Summary

Predict and filter metabolite m/z values by specifying expected adduct ion forms (e.g., M-H, M+Cl, M+K) during mass-to-charge annotation to reduce false positives and improve structural assignment confidence in LC-MS and MS imaging data.

## When to use

When annotating m/z features against a metabolite database (HMDB, Lipidmaps, etc.) and the sample preparation, ionization method, or polarity mode favors specific adduct species. For example: negative-mode LC-MS or MS imaging will preferentially generate M-H and halide adducts (M+Cl); positive-mode may favor M+H, M+Na, M+K. Restricting annotation to expected adducts reduces spurious multi-adduct matches and improves annotation specificity.

## When NOT to use

- Input data already contains curated, validated metabolite identities—re-annotation may introduce conflicting adduct assignments.
- Adduct composition is unknown or highly variable across the sample (e.g., mixed ionization modes in a single file)—use unfiltered or permissive adduct lists and validate against standards first.
- PPM error tolerance is misaligned with instrument resolution (e.g., setting ppm_error=3 on a low-resolution quadrupole or ion-trap; result will be zero or very few matches).

## Inputs

- Cardinal MSImagingExperiment object or mass spectrometry feature table (m/z features with intensities)
- Metabolite reference database (HMDB_db, Lipidmaps_db, or equivalent formatted as SpaMTP-compatible object)
- Adduct list (character vector, e.g., c('M-H', 'M+Cl') for negative mode)
- Polarity mode ('negative' or 'positive')
- PPM error tolerance (numeric, typically 3–15 ppm)

## Outputs

- Annotated results data.frame with columns: observed_mz, database_match_name, adduct, ppm_error, and other metadata
- Count of successfully annotated m/z values
- Annotated SpaMTP object (e.g., Cardinal MSImagingExperiment with metadata enriched with adduct and compound identity)

## How to apply

When calling the annotation function (e.g., AnnotateSM or AnnotateBigData), supply the adducts parameter as a character vector of expected adduct forms and set the polarity mode ('negative' or 'positive') to match your instrument configuration. Pair this with an appropriate ppm_error threshold (e.g., 3–15 ppm depending on instrument resolution). The annotation engine will generate candidate matches only for the specified adduct forms, compute observed-to-database m/z differences within the ppm tolerance, and return a filtered results table with adduct identity, observed m/z, database match name, and ppm error. Validate by verifying that (1) the adduct column contains only the specified forms, (2) all ppm errors fall within the specified tolerance, and (3) the annotation count aligns with prior validation studies or positive controls.

## Related tools

- **SpaMTP** (Core R package providing AnnotateSM and AnnotateBigData functions with adduct and polarity parameterization for m/z annotation) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Cardinal** (Underlying mass spectrometry imaging data structure (MSImagingExperiment) and feature extraction (featureData) for m/z input) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **HMDB** (Reference metabolite database used for m/z matching and structural annotation)
- **Lipidmaps** (Alternative reference database for lipid-focused annotation with adduct filtering)

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = c('M+K'), polarity = 'positive')
```

## Evaluation signals

- Adduct column in output contains only the specified adduct forms (e.g., if adducts=c('M-H','M+Cl'), no M+H or M+Na entries appear).
- All ppm_error values in output are ≤ the specified ppm_error parameter (e.g., ppm_error=3 yields max ppm_error ≤ 3.0).
- Annotation count matches expected validation benchmark (e.g., 67,060 annotated m/z for HMDB at ppm=3 with M-H/M+Cl negative adducts as reported in task_002).
- Observed m/z values in the output correspond to actual features in the input feature list (no spurious or out-of-range m/z).
- Comparison with polarity-blind or multi-adduct annotation shows reduced false-positive matches and increased specificity.

## Limitations

- Adduct prediction is deterministic and depends on correct specification of polarity and expected adduct forms; misspecification (e.g., using positive-mode adducts on negative-mode data) yields zero or near-zero annotations.
- PPM error tolerance is instrument-dependent; low-resolution instruments (e.g., ion-trap, quadrupole) may require relaxed tolerances (10–15 ppm), while high-resolution TOF/Orbitrap allows stricter thresholds (≤5 ppm). Inappropriate thresholds lead to under- or over-annotation.
- Adduct filtering assumes a single, dominant ionization pathway; complex samples with multiple simultaneous ionization mechanisms or chemical modifications (e.g., in-source fragmentation, neutral loss adducts) may not be captured by a restricted adduct list.
- Reference database completeness and annotation quality directly limit true-positive matches; even with correct adduct filtering, metabolites absent from or incorrectly annotated in HMDB/Lipidmaps will not be recovered.

## Evidence

- [other] research_question from task_002: "How many m/z values from the HMDB database can be annotated using AnnotateBigData with ppm_error=3 and M-H/M+Cl negative adducts?"
- [other] workflow step from task_002: "Call AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'), polarity='negative'."
- [methods] dataset and method evidence: "AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15"
- [readme] SpaMTP annotation capability: "this package has three major functionalities which include; (1) mass-to-charge ratio (m/z) metabolite annotation"
- [other] adduct and polarity support in SpaMTP: "spotted_Annotated_H_Cl_Adducts | public mouse liver dataset with spotted chemicals standards"
