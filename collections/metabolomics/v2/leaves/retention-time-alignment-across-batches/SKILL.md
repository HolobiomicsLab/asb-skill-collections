---
name: retention-time-alignment-across-batches
description: Use when you have extracted peaks from multiple LC/HRMS batches (n >
  500 samples across different analytical runs or days) and observe systematic retention
  time drift or offset between batches, preventing reliable cross-batch peak matching
  on m/z and RT alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IDSL.IPA
  - R
  - IDSL.UFA
  - IDSL.UFAx
  techniques:
  - LC-MS
  - GC-MS
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

# retention-time-alignment-across-batches

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Harmonize retention time values across multiple LC/HRMS batches to align peaks with equivalent m/z and chromatographic profiles, enabling consistent peak-to-compound mapping in population-scale untargeted metabolomics studies. This is essential for multi-batch peak alignment and accurate metabolite quantification across large cohorts.

## When to use

Apply this skill when you have extracted peaks from multiple LC/HRMS batches (n > 500 samples across different analytical runs or days) and observe systematic retention time drift or offset between batches, preventing reliable cross-batch peak matching on m/z and RT alone. The skill is triggered when peaks with identical or near-identical mass-to-charge values appear at different retention times across batches, indicating batch-level chromatographic variation that must be corrected before alignment and annotation.

## When NOT to use

- Input is already a feature table (peak alignment matrix) with pre-corrected RTs from another tool (e.g., xcms or MZmine 2); applying redundant RT correction will introduce unnecessary noise.
- Single-batch analysis or data from a single analytical run with no inter-batch variation; RT correction is only meaningful across distinct batches or runs.
- Data lacks sufficient endogenous reference peaks (< 5 high-confidence, consistently detected peaks per batch), as the RT correction algorithm requires stable anchors to compute reliable shift functions.

## Inputs

- Extracted peak tables from multiple LC/HRMS batches (mzXML, mzML, or netCDF format)
- Peak properties table with retention time (RT in minutes), m/z (mass-to-charge ratio), peak area, and intensity for each peak in each batch
- Endogenous reference markers (list of m/z-RT pairs or automatic selection from high-intensity stable peaks)

## Outputs

- Retention-time-corrected peak table with harmonized RT values across all batches
- Aligned peak height matrix (gap-filled and non-gap-filled) for downstream statistical analysis
- RT correction factor per batch (drift/offset quantification for QC documentation)

## How to apply

Load extracted peaks from all batches into IDSL.IPA with their retention time (RT) and m/z values. Apply the retention time correction algorithm, which uses endogenous reference markers (stable peaks present across all batches) to compute batch-specific RT shift functions. These functions are then applied to adjust all peak RTs to a common reference frame, harmonizing retention times across batches. The corrected peak table is generated with standardized RT and m/z coordinates, enabling subsequent peak alignment and annotation steps. Success hinges on the availability of sufficient endogenous reference peaks (typically 10–50 high-intensity, low-variance peaks per batch) that are consistently detected across all analytical runs.

## Related tools

- **IDSL.IPA** (Implements retention time correction algorithm as part of integrated peak analysis suite; executes RT harmonization across batches using endogenous reference markers) — https://github.com/idslme/IDSL.IPA
- **R** (Statistical computing environment in which IDSL.IPA runs; enables custom parameter tuning and batch processing via parameter spreadsheet)
- **IDSL.UFA** (Downstream molecular formula annotation tool that consumes RT-corrected and aligned peaks for compound identification) — https://github.com/idslme/IDSL.UFA
- **IDSL.UFAx** (Extended molecular formula annotation tool for chemical formula assignment on RT-aligned peak tables) — https://github.com/idslme/IDSL.UFAx

## Examples

```
library(IDSL.IPA)
IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- RT standard deviation within each m/z tolerance window (±5 ppm) is reduced after correction compared to pre-correction data, indicating successful harmonization.
- Peak alignment rate (percentage of peaks successfully matched across batches post-correction) is higher than pre-correction, verifiable by comparing peaklist intersection sizes.
- Endogenous reference peak RTs converge to within ±0.5 min across all batches after correction, confirming that batch-level drift functions were estimated and applied correctly.
- Gap-filled peak height matrix shows increased correlation between replicates (within-batch samples) compared to pre-correction, and reduced artificial clustering by batch in PCA or unsupervised clustering.
- Output peaklists in 'peak_alignment' directory contain aligned (m/z, RT) pairs consistent with literature retention index values for known metabolites in the sample type.

## Limitations

- RT correction accuracy depends on the availability of sufficient, stable endogenous reference peaks; if reference peaks are rare or themselves subject to batch-specific variation, correction may be unreliable.
- Non-linear RT drift (e.g., RT shift varies across the chromatographic time range) may not be fully captured by global batch-wise shift functions; localized deviations could persist.
- Extreme batch outliers (e.g., a single run with very large RT shift or instrumental malfunction) may skew RT correction parameters if robust statistical methods are not applied; outlier batches should be identified and excluded or reanalyzed.
- RT correction assumes comparable chromatographic conditions (temperature, column age, mobile phase composition) across batches; systematic changes in method parameters between batches may invalidate correction assumptions.

## Evidence

- [other] How does IDSL.IPA implement retention time correction to align peaks across multiple batches in LC/HRMS data?: "retention time correction across multiple batches and peak annotation"
- [other] Load extracted peaks from multiple batches with their retention time and mass-to-charge values into IDSL.IPA.: "Load extracted peaks from multiple batches with their retention time and mass-to-charge values into IDSL.IPA"
- [other] Apply retention time correction algorithm across batches to align peaks with similar m/z and RT profiles.: "Apply retention time correction algorithm across batches to align peaks with similar m/z and RT profiles"
- [readme] IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction across multiple batches and peak annotation.: "suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction across multiple"
- [readme] Retention time correction using endogenous reference markers for multi-batch large scale studies: "Retention time correction using endogenous reference markers for multi-batch large scale studies"
- [readme] extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects: "extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects"
