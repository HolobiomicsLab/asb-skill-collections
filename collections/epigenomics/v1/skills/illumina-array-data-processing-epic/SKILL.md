---
name: illumina-array-data-processing-epic
description: Use when you have raw Illumina EPIC or 450k methylation array data (.idat files or beta-valued matrices) and need to perform comprehensive quality assessment, probe correction, batch effect adjustment, and identification of differentially methylated regions or blocks across sample groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0625
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
  - Bumphunter
  - DMRcate
  - Shiny
  - FEM
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# Illumina array data processing (EPIC)

## Summary

End-to-end processing pipeline for Illumina EPIC methylation array data, from raw .idat files through quality control, normalization, batch correction, and differentially methylated region detection. This skill encompasses the complete workflow for analyzing 450k and EPIC array methylation data using ChAMP, a comprehensive R package integrating multiple normalization and statistical methods.

## When to use

You have raw Illumina EPIC or 450k methylation array data (.idat files or beta-valued matrices) and need to perform comprehensive quality assessment, probe correction, batch effect adjustment, and identification of differentially methylated regions or blocks across sample groups.

## When NOT to use

- Input data are already normalized and batch-corrected; use only downstream differential methylation detection methods instead.
- Array type is not EPIC, 450k, EPICv2, or mouse arrays; ChAMPdata does not support other platforms.
- Sample size is extremely small (e.g., n=1–2 per group); statistical power for DMR detection will be insufficient.

## Inputs

- .idat files (raw Illumina array intensity data)
- Beta-valued methylation matrix
- Sample phenotype/group metadata
- ChAMPdata annotation objects (e.g., AnnoEPIC, AnnoEPICv2)

## Outputs

- Quality control plots and metrics
- Normalized beta-value matrix
- Batch-corrected methylation data
- Differentially methylated region (DMR) calls with statistical annotations
- Differentially methylated block detection results
- Copy-number alteration inference results

## How to apply

Load your .idat files or beta-valued matrix using ChAMP's data import functions (e.g., champ.load()). Apply Type-2 probe correction using SWAN, PBC, or BMIQ (BMIQ is default). Perform Functional Normalization from minfi or implement SVD-based batch effect analysis. Correct for multiple batch effects using ComBat if needed. Adjust for cell-type heterogeneity via RefbaseEWAS when applicable. For differential methylation detection, choose between Probe Lasso, Bumphunter, or DMRcate for DMR identification, or use champ.Block() for differentially methylated block detection. Verify no spurious blocks are detected by examining output with Block.GUI() interactive interface when using simulation data (e.g., EPICSimData) to confirm expected behavior.

## Related tools

- **ChAMP** (Primary analysis pipeline integrating data loading, quality control, normalization, batch correction, and DMR/block detection for EPIC and 450k methylation arrays) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package providing CpG-probe manifests and array annotations (AnnoEPIC, AnnoEPICv2) required by ChAMP) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Provides Functional Normalization method integrated into ChAMP workflow)
- **Bumphunter** (DMR detection algorithm available as option within ChAMP.DMR())
- **DMRcate** (DMR detection algorithm available as option within ChAMP.DMR())
- **Shiny** (Powers interactive visualization interfaces (e.g., Block.GUI()) for exploring analysis results)
- **FEM** (Gene module inference integrated into new version of ChAMP for downstream enrichment analysis)

## Examples

```
data(EPICSimData); champ.Block(arraytype='EPIC'); Block.GUI()
```

## Evaluation signals

- Quality control plots display expected distributions (e.g., no systematic failures in detection p-values or intensity patterns across samples).
- Normalized beta-value matrix has values in [0, 1] range with reasonable variance structure after batch correction.
- ComBat-corrected data shows reduced batch effects as verified by SVD visualization (singular values for batch covariates diminished).
- DMR detection on synthetic data (EPICSimData with arraytype='EPIC') yields zero differentially methylated blocks, confirming agreement with documented expected behavior.
- champ.Block() output and Block.GUI() interactive results are consistent and reproducible across multiple runs with identical inputs.

## Limitations

- ChAMP development version (GitHub) is under intensive modification; formally released version on Bioconductor is recommended for production use.
- ChAMPdata must be version ≥2.23.1 to ensure compatibility with current ChAMP; version mismatch may cause annotation failures.
- Block detection is sensitive to simulation dataset properties; real biological datasets may require parameter tuning to avoid missing true blocks or reporting false positives.
- No changelog provided; version-to-version differences and bug fixes are not formally documented outside Bioconductor release notes.
- Cell-type heterogeneity adjustment via RefbaseEWAS requires appropriate reference cell-type definitions; mismatched or unavailable reference data may reduce correction efficacy.

## Evidence

- [readme] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] ChAMP provides a comprehensive pipeline with support for multiple array types and normalization approaches: "The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods"
- [intro] Type-2 probe correction methods available include SWAN, PBC, and BMIQ: "Type-2 probe correction methods include SWAN, Peak Based Correction (PBC) and BMIQ (the default choice)"
- [intro] ChAMP includes functions for DMR and differentially methylated block detection: "For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate"
- [readme] ChAMP supports both 450k and EPIC array types with version 2.29.1 supporting EPICv2: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"
- [intro] EPICSimData is available for testing and validation of block detection workflows: "For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData)"
- [intro] ChAMP provides interactive visualization via Shiny-based interfaces: "The new version ChAMP also provides a series of Shiny and Plotly-based WebBrower Interactive analysis functions"
- [intro] ComBat method is implemented for correction of multiple batch effects: "for correction of multiple batch effects the ComBat method has been implemented"
