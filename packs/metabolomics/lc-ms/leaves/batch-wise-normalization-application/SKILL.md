---
name: batch-wise-normalization-application
description: Use when when processing a SummarizedExperiment containing metabolomics peak areas or intensities organized by batch (e.g., LC-MS/MS runs on different days or instruments), and you have pooled quality control samples injected repeatedly within or across batches to serve as batch anchors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
  - mzQualityDashboard
  - xcms
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-wise-normalization-application

## Summary

Apply batch correction to metabolomics assay data using pooled study quality control (SQC) samples as reference anchors, normalizing compound/internal standard ratios across analytical batches to remove batch-dependent systematic variation while preserving biological signal.

## When to use

When processing a SummarizedExperiment containing metabolomics peak areas or intensities organized by batch (e.g., LC-MS/MS runs on different days or instruments), and you have pooled quality control samples injected repeatedly within or across batches to serve as batch anchors. Apply this skill before selecting compounds or samples for reporting, as batch effects confound QC outlier detection and compound reliability assessment.

## When NOT to use

- Input data lacks pooled quality control samples injected across batches — batch correction requires QC anchors in each batch
- Data are already batch-corrected by an upstream pipeline (e.g., xcms or another preprocessing tool); applying doAnalysis() will recompute and may over-correct
- Study lacks batch labels or batch information is not encoded in colData; the function requires explicit batch assignment to stratify SQC samples

## Inputs

- SummarizedExperiment object from buildExperiment() containing assays with raw compound peak areas, internal standard areas, and colData with batch labels and sample type annotations (QC, study sample, etc.)

## Outputs

- SummarizedExperiment with new assay 'ratio_corrected' containing batch-normalized compound/internal standard ratios
- Updated rowData and colData with batch-correction metadata and downstream QC metrics (RSDQC, background %, presence)
- Diagnostic plots (PCA, boxplots) showing reduced batch clustering in corrected ratios

## How to apply

Within the mzQuality workflow, call doAnalysis() on a SummarizedExperiment built from readData() and buildExperiment(). The function first calculates the ratio between each compound and its assigned internal standard, then performs batch correction by normalizing these ratios against pooled SQC sample values, centering each batch's SQC ratios to a global median. The corrected ratios are stored as a new assay (e.g., 'ratio_corrected'). This normalization uses only QC samples, not study samples, to avoid circular correction. The corrected ratios are then used downstream for outlier testing (Rosner test on QC samples), compound reliability filtering (RSDQC, background signal percentage, QC presence thresholds), and sample flagging. The batch-corrected assay can be visualized with pcaPlot(exp, assay='ratio_corrected') to confirm removal of batch clustering.

## Related tools

- **mzQuality** (Wrapper function doAnalysis() performs batch correction via SQC-based ratio normalization, combined with outlier detection and compound filtering) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Core data structure storing assays (raw/corrected ratios), rowData (compound metadata), and colData (sample metadata including batch labels)) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **mzQualityDashboard** (Interactive Shiny application providing GUI access to doAnalysis() and visualization of batch-corrected assays without programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **xcms** (Upstream peak detection and alignment tool; mzQuality can accept SummarizedExperiment outputs from xcms for batch correction)

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers = TRUE, useWithinBatch = TRUE, removeBadCompounds = TRUE)
```

## Evaluation signals

- PCA plot of batch-corrected ratios (assay='ratio_corrected') shows no distinct clustering by batch; study samples and QC samples distribute according to biological phenotype or sample type, not injection date
- Median compound/internal standard ratio across QC samples within each batch is approximately equal post-correction (check colData after doAnalysis)
- Coefficient of variation (RSDQC) of batch-corrected ratios for QC samples is lower than pre-correction; verify via rowData columns
- Boxplots of batch-corrected ratios per compound show similar interquartile ranges and medians across batches; raw ratios show systematic shifts
- Rosner outlier test on QC samples (post-correction) flags fewer spurious outliers than pre-correction, and outliers correspond to technical issues (e.g., clogged needle) rather than batch membership

## Limitations

- Batch correction assumes that pooled QC samples are representative of all compounds and matrices in the study; if QC recipe omits major matrix components or analytes, correction may be incomplete or biased
- Correction is multiplicative (ratio-based); if a compound or internal standard is absent in QC samples, the ratio is undefined and that compound/sample pair cannot be corrected
- Batch effect removal is only as good as the QC injection frequency; sparse or irregular QC sampling across batches may leave residual drift
- The function does not account for non-linear batch effects or batch–phenotype interactions; if batch and biological grouping are confounded, correction may inadvertently remove real signal

## Evidence

- [intro] Batch correction step via SQC samples: "It features outlier detection, batch-correction using pooled study quality control samples (SQC), filters for removing unreliable compounds"
- [readme] Ratio calculation before batch correction: "Calculate the ratio between the compounds and assigned internal standards, Perform batch correction using the pooled study quality control samples (SQC)"
- [readme] doAnalysis() wrapper performs all steps including batch correction: "For convenience, a wrapper function has been designed that performs all analyses included in this package: exp <- doAnalysis(exp = exp)"
- [readme] Batch-corrected ratios used for downstream QC and visualization: "Principal Component Analysis plot showing the aliquot distribution per type and batch for batch-corrected ratios pcaPlot(exp, assay = "ratio_corrected")"
- [intro] No phenotype required; batch correction is sample-type agnostic: "mzQuality was developed to perform outlier detection, batch correction and other quality control steps without the need for defined phenotypes"
