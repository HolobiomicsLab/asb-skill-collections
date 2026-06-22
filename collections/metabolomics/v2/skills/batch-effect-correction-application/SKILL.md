---
name: batch-effect-correction-application
description: Use when you have a SummarizedExperiment object containing metabolomics assay data (compound areas, internal standard areas) organized by batch and sample type (including pooled SQC samples), and you need to correct systematic variation across batches before calculating Relative Standard Deviation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - SummarizedExperiment (Bioconductor)
  - mzQualityDashboard
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
---

# batch-effect-correction-application

## Summary

Apply batch correction to metabolomics compound–internal standard ratios using pooled study quality control (SQC) samples as the correction reference. This removes systematic batch effects that inflate compound variability estimates, enabling more reliable internal standard selection and concentration calculations.

## When to use

You have a SummarizedExperiment object containing metabolomics assay data (compound areas, internal standard areas) organized by batch and sample type (including pooled SQC samples), and you need to correct systematic variation across batches before calculating Relative Standard Deviation of QC samples (RSDQC) or estimating compound concentrations.

## When NOT to use

- No pooled QC (SQC) samples are present in the experiment — batch correction requires a reference population that repeats across batches.
- Batch effects are already known to be negligible (e.g., all samples analyzed in a single instrument run on a single day) — correction may introduce noise rather than remove it.
- The compound–internal standard ratio assignment has not yet been performed — batch correction requires pre-calculated ratios as input.

## Inputs

- SummarizedExperiment object with assay slot containing compound areas and internal standard areas
- colData columns: batch identifier, sample type (Study, QC, SQC, Calibration)
- rowData columns: assigned internal standard per compound
- ratio assay (compound area / internal standard area for each sample)

## Outputs

- SummarizedExperiment with new assay slot: ratio_corrected (batch-corrected ratios)
- colData and rowData remain unchanged
- Batch effect parameters (per-batch SQC reference ratios) stored implicitly in the corrected values

## How to apply

Within the mzQuality workflow, batch correction is applied to compound–internal standard ratios by leveraging pooled study quality control (SQC) samples as the reference. The correction accounts for batch-to-batch drift in instrument response by normalizing each sample's ratio against the corresponding batch's SQC ratio. This step is automatically executed by the `doAnalysis` function after ratio calculation (step 1) and before RSDQC calculation (step 5). The corrected ratios replace the raw ratios in the `ratio_corrected` assay slot. Batch information is inferred from the `colData` slot (batch column), and the correction is applied only to study samples and QC samples, preserving calibration line samples if present. The rationale is that SQC samples, being identical pooled material injected repeatedly across batches, capture instrument drift; dividing each sample's ratio by its batch's average SQC ratio neutralizes this drift, reducing spurious variability that would otherwise inflate RSDQC and confound internal standard selection.

## Related tools

- **mzQuality** (Performs batch correction via doAnalysis() function; stores corrected ratios in ratio_corrected assay slot; requires SummarizedExperiment input and SQC sample metadata) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment (Bioconductor)** (Data container for assays, colData, and rowData; enables organized storage of raw and batch-corrected assays)
- **mzQualityDashboard** (Interactive Shiny wrapper around mzQuality; provides GUI-based access to batch correction without R programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **R** (Runtime and statistical environment for mzQuality package execution)

## Examples

```
exp <- doAnalysis(exp = exp)
```

## Evaluation signals

- The ratio_corrected assay exists in the SummarizedExperiment and contains numeric values without NaN/Inf; dimensions match the raw ratio assay.
- RSDQC values computed from ratio_corrected are lower than or equal to those computed from uncorrected ratios for most compounds, indicating batch drift has been removed.
- PCA plot of ratio_corrected shows reduced separation by batch and improved clustering by sample type (study samples grouped, QC samples grouped), compared to PCA of uncorrected ratios.
- Batch-corrected internal standard recommendations (derived from minimum RSDQC) differ from recommendations based on uncorrected ratios, indicating batch correction meaningfully changed the selection.
- SQC sample ratios in the ratio_corrected assay cluster tightly around 1.0 or a stable reference value across batches, confirming drift normalization.

## Limitations

- Requires at least one pooled QC (SQC) sample per batch to serve as a stable reference; batches with no SQC samples cannot be corrected.
- Assumes SQC samples are true replicates of identical material; contamination, degradation, or deliberate variation in SQC preparation will bias the correction.
- If internal standard assignment is suboptimal or missing for some compounds, batch correction of their ratios will propagate that error and may mask rather than reveal it.
- Correction is relative to SQC mean and does not account for non-linear instrumental drift or time-dependent effects within a batch; effectiveness depends on SQC injection frequency.
- Calibration line samples (if present) are not used in batch correction and are typically excluded from downstream QC metric calculations.

## Evidence

- [intro] Batch correction rationale and SQC role: "mzQuality was developed to perform outlier detection, batch correction and other quality control steps without the need for defined phenotypes"
- [readme] Batch correction step in workflow: "Perform batch correction using the pooled study quality control samples (SQC)"
- [readme] Automated batch correction via doAnalysis: "The `doAnalysis` function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality"
- [intro] Batch-corrected ratios enable RSDQC calculation: "Compute batch-corrected compound-to-internal-standard ratios for each QC sample, accounting for batch effects. 4. Calculate the Relative Standard Deviation (RSD) of the batch-corrected ratios for"
- [readme] Output assay storage: "All calculations will be added to the `assay`, `rowData` and `colData` slots of the experiment, or overwrite the values if they are already present."
