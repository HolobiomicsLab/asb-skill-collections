---
name: mass-spectrometry-calibration
description: Use when after peak detection when you have a detected peaks table with
  m/z values and need to correct systematic mass drift or inaccuracy before peak alignment
  across multiple batches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - IDSL.IPA
  - R
  techniques:
  - mass-spectrometry
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

# mass-spectrometry-calibration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Recursive mass correction refines m/z accuracy of detected peaks in untargeted LC/HRMS data by recalibrating mass coordinates using internal reference standards or lock masses. This skill is essential for multi-batch population-scale studies where consistent mass accuracy across samples directly impacts peak alignment, annotation reliability, and downstream compound identification.

## When to use

Apply this skill after peak detection when you have a detected peaks table with m/z values and need to correct systematic mass drift or inaccuracy before peak alignment across multiple batches. Particularly critical in population-scale untargeted LC/HRMS studies (n > 500) where batch-to-batch variation accumulates and impacts m/z alignment fidelity.

## When NOT to use

- Input peaks table has already been externally calibrated or is from targeted analysis with predetermined m/z windows.
- Internal reference standards or lock masses are unavailable or unreliable across the batch.
- Single-sample analysis where batch-to-batch correction is not applicable.

## Inputs

- Detected peaks table (with m/z values, retention time, and peak properties from peak detection step)
- Internal reference standard list or lock mass calibrant identities
- Mass spectrometry raw data (mzXML, mzML, or netCDF format)

## Outputs

- Corrected peaks table with recalibrated m/z values
- Pre- and post-correction m/z accuracy metrics and comparison report
- Mass calibration curve or correction model used

## How to apply

Load the detected peaks table containing m/z values and peak properties from the prior peak detection step. Apply IDSL.IPA's recursive mass correction algorithm, which recalibrates m/z coordinates using internal reference standards or lock masses to correct for instrumental drift and systematic bias. The algorithm iteratively refines mass accuracy by leveraging known-mass reference compounds or endogenous markers stable across the batch. Generate a corrected peak table with updated m/z coordinates. Validate correction by comparing pre- and post-correction m/z accuracy metrics (e.g., ppm error distributions) and confirm that m/z shifts are within acceptable tolerance before exporting the final corrected peak dataset for downstream alignment and annotation.

## Related tools

- **IDSL.IPA** (Implements recursive mass correction algorithm as part of peak processing suite; applies m/z recalibration using internal reference standards) — https://github.com/idslme/IDSL.IPA
- **R** (Programming language environment for executing IDSL.IPA mass correction functions) — https://cran.r-project.org/package=IDSL.IPA

## Examples

```
library(IDSL.IPA); IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- M/z error (ppm) distribution narrows and shifts toward zero after correction compared to pre-correction state.
- Internal reference standards recover expected m/z values within instrumental tolerance (typically ≤5 ppm for HRMS).
- Corrected peaks successfully align across multiple batches with reduced m/z mismatch artifacts.
- No systematic m/z drift remains as a function of retention time or scan order.
- Peak counts and properties (area, width, S/N) remain unchanged post-correction, confirming that mass calibration does not introduce false peak loss or duplication.

## Limitations

- Requires availability and stability of internal reference standards or lock masses across all samples in the batch; poor calibrant recovery degrades correction quality.
- Recursive algorithm convergence depends on parameter tuning (number of iterations, reference mass weighting); suboptimal settings may under- or over-correct.
- Correction accuracy is limited by instrument mass resolution and stability; very long analytical runs or instrument drift exceeding reference standard capacity may necessitate sub-batch recalibration.
- No changelog available in the repository, so version-specific algorithm changes are not explicitly documented.

## Evidence

- [other] IDSL.IPA includes a recursive mass correction algorithm as part of its suite of peak processing algorithms, applied after peak detection to refine mass accuracy of detected peaks.: "IDSL.IPA includes a recursive mass correction algorithm as part of its suite of peak processing algorithms, applied after peak detection to refine mass accuracy of detected peaks."
- [other] Load detected peaks table containing m/z values and peak properties from prior detection step. Apply recursive mass correction algorithm as implemented in IDSL.IPA to recalibrate m/z values using internal reference standards or lock masses.: "Apply recursive mass correction algorithm as implemented in IDSL.IPA to recalibrate m/z values using internal reference standards or lock masses."
- [readme] recursive mass correction, retention time correction across multiple batches and peak annotation are part of the workflow: "IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction"
- [other] Compare pre- and post-correction m/z accuracy metrics and export final corrected peak dataset.: "Compare pre- and post-correction m/z accuracy metrics and export final corrected peak dataset."
- [readme] Population scale untargeted LC/HRMS studies context: "IDSL.IPA generates comprehensive and high-quality datasets from untargeted analysis of organic small molecules for population-size studies."
