---
name: peak-m-z-recalibration
description: Use when after peak detection when you have a table of detected peaks
  with m/z values and need to improve mass accuracy for downstream annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - IDSL.IPA
  - R
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory
  for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight
  R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-m/z-recalibration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Recursive mass correction refines m/z accuracy of detected LC/HRMS peaks by recalibrating their mass-to-charge coordinates using internal reference standards or lock masses. This step is applied post-detection to improve mass accuracy metrics across large untargeted metabolomics datasets.

## When to use

Apply this skill after peak detection when you have a table of detected peaks with m/z values and need to improve mass accuracy for downstream annotation. Use it in untargeted LC/HRMS population-scale studies (n > 500) where systematic mass drift or calibration error may affect m/z precision across multiple batches or acquisitions.

## When NOT to use

- Input peaks are already from a targeted method with locked or fixed m/z windows — recursive correction may introduce unnecessary noise.
- Untargeted data were acquired on low-resolution instruments (nominal mass accuracy) — correction tolerances and reference lock mass precision may not justify the algorithm.
- No internal reference standards or endogenous markers are available in the dataset — the algorithm requires calibration anchors to function.

## Inputs

- Detected peaks table (from peak detection stage) containing m/z values, retention times, and peak properties
- Mass spectrometry raw data (mzXML, mzML, or netCDF format) or extracted ion chromatogram (EIC) data
- Internal reference standards or lock mass m/z values (optional; endogenous markers may substitute)

## Outputs

- Corrected peak table with recalibrated m/z values
- Mass accuracy metrics (pre- and post-correction ppm error, calibration statistics)
- Calibration residual data for quality assessment

## How to apply

Load the detected peaks table containing m/z values and peak properties from the prior peak detection stage. Apply the recursive mass correction algorithm implemented in IDSL.IPA, which recalibrates m/z coordinates using internal reference standards (lock masses) or endogenous reference markers available in the dataset. The algorithm iteratively refines mass calibration to minimize systematic error. Generate a corrected peak table with updated m/z coordinates and compare pre- and post-correction m/z accuracy metrics (e.g., ppm error distribution, mass calibration residuals) to verify improvement. Export the final corrected peak dataset for downstream retention time correction and peak annotation workflows.

## Related tools

- **IDSL.IPA** (Provides the recursive mass correction algorithm and integration with full LC/HRMS peak processing pipeline (EIC generation, peak detection, property evaluation, retention time correction, and annotation)) — https://github.com/idslme/IDSL.IPA
- **R** (Language and runtime environment for executing IDSL.IPA package and recursive mass correction workflow)

## Examples

```
library(IDSL.IPA); IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Pre- and post-correction m/z accuracy distribution: post-correction ppm error should be narrower and centered closer to zero than pre-correction values.
- Calibration residuals: systematic mass drift should be minimized; residuals should not show batch or time-dependent patterns.
- Mass calibration statistics (e.g., RMSE, max error): quantitative improvement in mass precision across the m/z range.
- Downstream peak alignment and annotation quality: correctly recalibrated m/z values should improve alignment rates and reduce false monoisotopic peak assignments.
- Isotope pattern coherence: m/z differences between detected isotopologue pairs (e.g., ¹²C/¹³C) should match theoretical mass defect after correction.

## Limitations

- Recursive mass correction depends on availability and accuracy of internal reference standards or lock masses; if reference m/z values are themselves miscalibrated, the algorithm may propagate error.
- Performance in multi-batch studies requires endogenous reference markers (retention time correction anchors) to be present and reliably detected across all samples; sparse or variable reference detection can degrade correction fidelity.
- The algorithm is designed for high-resolution mass spectrometry (HRMS) data; application to nominal-mass or low-resolution data may not yield meaningful improvements.
- No changelog was found in the repository documentation, limiting visibility into algorithm refinements or known issues across IDSL.IPA versions.

## Evidence

- [other] IDSL.IPA includes a recursive mass correction algorithm as part of its suite of peak processing algorithms, applied after peak detection to refine mass accuracy of detected peaks.: "recursive mass correction algorithm as part of its suite of peak processing algorithms, applied after peak detection to refine mass accuracy"
- [other] Load detected peaks table containing m/z values and peak properties from prior detection step. Apply recursive mass correction algorithm as implemented in IDSL.IPA to recalibrate m/z values using internal reference standards or lock masses.: "Load detected peaks table containing m/z values and peak properties from prior detection step. Apply recursive mass correction algorithm as implemented in IDSL.IPA to recalibrate m/z values using"
- [readme] IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction across multiple batches and peak annotation.: "IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction"
- [readme] extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects: "extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects"
- [readme] Retention time correction using endogenous reference markers for multi-batch large scale studies: "Retention time correction using endogenous reference markers for multi-batch large scale studies"
