---
name: m-z-rt-feature-matching
description: Use when you have extracted peaks from multiple LC/HRMS batches (n > 1) with their m/z and RT values, and you need to identify and align peaks representing the same compound across batches to build a consensus feature matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - IDSL.IPA
  - R
  - MZmine 2
  - xcms
  techniques:
  - LC-MS
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

# m/z-rt-feature-matching

## Summary

Align and match peaks across multiple LC/HRMS batches by harmonizing their mass-to-charge (m/z) and retention time (RT) coordinates, enabling construction of unified peak tables for population-scale untargeted metabolomics studies. This skill corrects for batch-to-batch RT drift while preserving mass accuracy, permitting detection of the same compounds across different instrument runs and sample cohorts.

## When to use

Apply this skill when you have extracted peaks from multiple LC/HRMS batches (n > 1) with their m/z and RT values, and you need to identify and align peaks representing the same compound across batches to build a consensus feature matrix. Typical trigger: individual batch peaklists exist in R data or CSV format with columns for m/z, RT, peak area, and intensity; batches show RT drift or offset; goal is population-scale untargeted analysis (n > 500 samples).

## When NOT to use

- Input data is already a unified feature table or consensus matrix — skip to downstream annotation/statistical analysis.
- Only single-batch or single-file data is available — retention time correction is designed for multi-batch alignment and will not improve single-batch peak detection.
- MS/MS or high-energy fragmentation data (MS2) is the primary input — IDSL.IPA operates on MS1 level data; use this skill only after MS1 extraction.

## Inputs

- Individual batch peaklists (mzXML, mzML, or netCDF LC/HRMS data files)
- Peak table with m/z, retention time, and intensity columns per batch
- IPA parameter spreadsheet with batch locations and processing configuration
- Endogenous reference markers or RT correction model (optional, for multi-batch RT alignment)

## Outputs

- Aligned peak table with harmonized m/z and corrected RT values across all batches
- Peak alignment matrix in 'peak_alignment' directory (CSV and R data formats)
- Individual peaklists per batch in 'peaklists' directory (post-correction)
- Gap-filled intensity/area tables for aligned features across all samples

## How to apply

Load extracted peak tables from all batches into IDSL.IPA with their m/z and RT coordinates. IDSL.IPA applies recursive mass correction first to standardize m/z values across batches, then uses retention time correction with endogenous reference markers (or algorithmic alignment) to harmonize RT values across batches, clustering peaks with similar m/z and corrected RT into aligned features. Parameters are configured via the IPA parameter spreadsheet (PARAM0007 for input location, PARAM0010 for output). The algorithm generates aligned peak tables in the 'peak_alignment' directory with harmonized m/z-RT coordinates and aggregated intensities or areas across batches. Correctness is verified by checking that (1) peaks from the same compound in different batches are collapsed to a single row, (2) m/z values align within expected mass accuracy (typically < 5 ppm for HRMS), and (3) RT values are smoothly distributed across the corrected retention window.

## Related tools

- **IDSL.IPA** (Suite implementing recursive mass correction, retention time correction across batches, and peak alignment algorithms; orchestrates EIC candidate generation, peak detection, peak property evaluation, and peak annotation) — https://github.com/idslme/IDSL.IPA
- **R** (Runtime environment and statistical programming language for IDSL.IPA execution and parameter configuration via spreadsheet interface)
- **MZmine 2** (Alternative peak picking and alignment tool for LC/HRMS data; IDSL.IPA outperforms this tool in sensitivity and specificity)
- **xcms** (Comparative peak detection and alignment R package for LC/HRMS; IDSL.IPA demonstrates superior performance)

## Examples

```
library(IDSL.IPA)
IPA_workflow("/path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Verify that peaks with identical or near-identical m/z (within 5 ppm) and similar RT across batches are grouped into single aligned features with no duplicates.
- Check that corrected RT values show smooth, consistent distribution across batches and that RT drift between batches is minimized (inspect RT variance across samples in the alignment table).
- Confirm that mass accuracy is preserved: compare m/z values pre- and post-correction; recursive mass correction should reduce systematic m/z bias across batches.
- Validate peak alignment completeness: count number of aligned features vs. total peaks detected; assess gap-filling rate (percentage of feature-sample combinations filled vs. missing).
- Cross-check with downstream annotation: aligned m/z-RT pairs should yield consistent molecular formula matches or library hits across all batches for the same compound.

## Limitations

- Requires multi-batch data with sufficient overlap in RT and m/z space; single-batch analysis will not benefit from retention time correction.
- RT correction depends on availability of endogenous reference markers or algorithmic detection of invariant peaks across batches; poorly chosen or absent reference markers will degrade alignment quality.
- Performance scales with sample size and complexity; population-scale studies (n > 500) are the intended use case; smaller studies may not show robust corrections.
- Sensitive to parameter selection (PARAM0006 thread count, EIC candidate thresholds, mass and RT tolerance windows); suboptimal parameters can produce misaligned peaks or missed features.
- No changelog is formally published, limiting traceability of algorithmic changes and version-to-version reproducibility.

## Evidence

- [intro] retention time correction across multiple batches and peak annotation: "IDSL.IPA is a suite of new algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation, recursive mass correction, retention time correction"
- [readme] retention time correction using endogenous reference markers: "Retention time correction using endogenous reference markers for multi-batch large scale studies"
- [readme] multi-batch peak alignment workflow with parameter spreadsheet: "To process your mass spectrometry data (mzXML, mzML, netCDF), download the IPA parameter spreadsheet and select the parameters accordingly and then use this spreadsheet as the input for the"
- [intro] population-scale studies with LC/HRMS data: "extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects"
- [readme] peak alignment output structure and directories: "Peak alignment tables in the 'peak_alignment' directory. Individual peaklists for each HRMS file in .Rdata and .csv formats in the 'peaklists' directory."
