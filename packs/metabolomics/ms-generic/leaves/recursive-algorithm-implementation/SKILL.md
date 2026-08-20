---
name: recursive-algorithm-implementation
description: Use when after peak detection on LC/HRMS data (mzXML, mzML, netCDF formats) when m/z values require refinement for improved mass accuracy in untargeted metabolomics workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - IDSL.IPA
  - R
  - IDSL.UFA
  - IDSL.UFAx
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
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

# Reconstruct the recursive mass correction stage

## Summary

Apply a recursive mass correction algorithm to refine m/z accuracy of LC/HRMS peaks after initial detection, using internal reference standards or lock masses to recalibrate mass coordinates across population-scale untargeted datasets.

## When to use

After peak detection on LC/HRMS data (mzXML, mzML, netCDF formats) when m/z values require refinement for improved mass accuracy in untargeted metabolomics workflows. This is especially critical in population-scale studies (n > 500) where systematic mass drift or calibration drift across batches degrades feature alignment and annotation fidelity.

## When NOT to use

- Input peaks already post-corrected by another tool or workflow (prevents double-correction artifacts).
- Single-file or low-throughput analyses where mass drift is negligible (recursive correction is optimized for population-scale batch effects).
- Targeted workflows with predefined m/z tolerances if mass refinement is not a stated objective.

## Inputs

- Detected peaks table (Rdata or CSV format) with columns: m/z, retention time, peak area, and peak properties (signal-to-noise ratio, peak width, asymmetry factor, etc.)
- Reference mass standards or lock masses (internal or external calibration compounds with known m/z values)
- Parameter spreadsheet (IPA_parameters.xlsx) with mass correction settings enabled

## Outputs

- Corrected peaks table (Rdata and CSV formats) with updated m/z coordinates
- Pre- and post-correction m/z accuracy metrics (e.g., mass error in ppm, standard deviation of mass error)
- Mass correction calibration curve or coefficients applied

## How to apply

Load the detected peaks table containing m/z values and peak properties from the prior peak detection stage. IDSL.IPA implements recursive mass correction as part of its processing pipeline; invoke it via the `IPA_workflow` function with the IPA parameter spreadsheet configured to enable mass correction. The algorithm recalibrates m/z values using endogenous or external reference markers (lock masses). Pre- and post-correction m/z accuracy should be quantified and compared; export the final corrected peak dataset for downstream retention time correction and peak annotation. The correction operates at the MS1 level and is applied batch-wise or across the entire dataset depending on parameter configuration.

## Related tools

- **IDSL.IPA** (Implements recursive mass correction algorithm as part of the peak processing suite; coordinates EIC candidate generation, peak detection, property evaluation, and mass/retention-time correction) — https://github.com/idslme/IDSL.IPA
- **R** (Host language for IDSL.IPA package and execution of `IPA_workflow` function)
- **IDSL.UFA** (Downstream integration: molecular formula annotation on mass-corrected peaks) — https://github.com/idslme/IDSL.UFA
- **IDSL.UFAx** (Downstream integration: extended molecular formula annotation on mass-corrected peaks) — https://github.com/idslme/IDSL.UFAx

## Examples

```
library(IDSL.IPA)
IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Mass error (ppm) post-correction should be ≤ 5 ppm (typical HRMS tolerance) and lower than pre-correction error; inspect histogram/distribution of corrected mass errors.
- Standard deviation of mass error across the peak set should decrease after correction; quantify reduction as a percentage.
- Aligned peak tables downstream should show improved feature overlap and reduced m/z jitter when peaks from multiple files are aligned post-correction.
- Pre- vs. post-correction m/z coordinates should differ only by small, systematic offsets (not random noise); validate that correction is repeatable and not introducing artifacts.
- Annotation rate (successful matches to a reference compound database) should increase after mass correction, as refined m/z values improve hit quality.

## Limitations

- Recursive mass correction depends on the availability and accurate identification of reference standards or lock masses; poor reference mass selection will propagate systematic error.
- Performance degrades if the detected peaks table contains false positives or low-confidence peaks; upstream peak detection quality directly impacts correction fidelity.
- Multi-batch datasets require careful alignment of reference masses or retention-time markers across batches; if batch effects are severe or references shift, correction may fail or introduce batch-specific biases.
- The algorithm is optimized for LC/HRMS data (mzXML, mzML, netCDF); applicability to other ionization methods or mass analyzers is not explicitly stated.

## Evidence

- [other] Load detected peaks table containing m/z values and peak properties from prior detection step. Apply recursive mass correction algorithm as implemented in IDSL.IPA to recalibrate m/z values using internal reference standards or lock masses.: "Load detected peaks table containing m/z values and peak properties from prior detection step. Apply recursive mass correction algorithm as implemented in IDSL.IPA to recalibrate m/z values using"
- [other] IDSL.IPA includes a recursive mass correction algorithm as part of its suite of peak processing algorithms, applied after peak detection to refine mass accuracy of detected peaks.: "IDSL.IPA includes a recursive mass correction algorithm as part of its suite of peak processing algorithms, applied after peak detection to refine mass accuracy of detected peaks."
- [readme] IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction across multiple batches and peak annotation.: "IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction"
- [readme] Retention time correction using endogenous reference markers for multi-batch large scale studies: "Retention time correction using endogenous reference markers for multi-batch large scale studies"
- [readme] Analyzing population size untargeted studies (n > 500): "Analyzing population size untargeted studies (n > 500)"
