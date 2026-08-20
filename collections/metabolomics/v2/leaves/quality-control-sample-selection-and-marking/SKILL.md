---
name: quality-control-sample-selection-and-marking
description: Use when your metabolomics dataset contains samples analyzed across multiple
  batches or runs, and you have sample-level metadata (sampledata) with a 'type' or
  classification field. You intend to apply QC-aware normalization methods (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - R
  - NormalizeMets
  - RStudio
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-018-1347-7
  title: NormalizeMets
evidence_spans:
- The R software environment can be downloaded for free from the Comprehensive R Archive
  Network (CRAN)
- 'Install the NormalizeMets package by using the following function: `install.packages("NormalizeMets")`'
- The use of RStudio is also recommended. RStudio is an integrated development environment
  (IDE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_normalizemets_cq
    doi: 10.1007/s11306-018-1347-7
    title: NormalizeMets
  dedup_kept_from: coll_normalizemets_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-018-1347-7
  all_source_dois:
  - 10.1007/s11306-018-1347-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quality-control-sample-selection-and-marking

## Summary

Identify and designate quality-control (QC) samples within a metabolomics dataset by leveraging sample metadata annotations, enabling downstream normalization and batch-effect correction. This skill is essential for preparing data for RLSC and other QC-sample-dependent normalization methods.

## When to use

Your metabolomics dataset contains samples analyzed across multiple batches or runs, and you have sample-level metadata (sampledata) with a 'type' or classification field. You intend to apply QC-aware normalization methods (e.g., RLSC via NormQcsamples, or internal-standard or QC-metabolite methods via NormQcmets) that require explicit identification of QC samples to model and correct batch variation.

## When NOT to use

- Your dataset contains no technical replicates or QC samples; QC-sample-based normalization requires explicit QC replicates to estimate batch structure.
- QC samples are already fully integrated into the feature matrix without metadata linking; you cannot retrospectively recover QC status from intensity patterns alone.
- You plan to use only univariate scaling methods (e.g., median, mean, sum normalization) that do not leverage QC sample behavior; selection and marking would be wasted effort.

## Inputs

- sampledata: dataframe with unique sample names as row names; must include 'type' or 'class' column identifying sample category (e.g., 'QC', 'sample') and 'order' column with run sequence
- featuredata: metabolomics intensity matrix (rows=samples, columns=metabolites) in same row order as sampledata

## Outputs

- annotated sampledata: sampledata dataframe with QC samples flagged and sorted by run order
- QC sample index: vector or logical flag identifying which rows in featuredata and sampledata correspond to QC samples

## How to apply

Inspect the sampledata dataframe to identify a column (commonly 'type' or 'class') that distinguishes QC samples from biological samples. QC samples are typically technical replicates or pooled reference materials analyzed at regular intervals throughout the run. Subset or flag rows in sampledata where this column equals 'QC' or a similar designation. Ensure sampledata is sorted by the 'order' column (run sequence) before passing to normalization functions; this ordering is critical for RLSC to correctly model drift. Document which rows are QC samples in the metadata so downstream normalization functions can access and use them to estimate and remove systematic variation. Verify that QC samples are distributed throughout the run (not clustered at the beginning or end) to capture temporal batch effects.

## Related tools

- **NormalizeMets** (R package containing NormQcsamples and NormQcmets functions that accept marked QC samples as input for RLSC and other QC-aware normalization methods) — https://github.com/metabolomicstats/NormalizeMets
- **RStudio** (integrated development environment for R; recommended for inspecting and manipulating sampledata metadata)
- **R** (statistical computing environment; used to subset, flag, and sort sampledata and featuredata)

## Examples

```
# Load sampledata; inspect and flag QC samples
library(NormalizeMets)
data(Didata)
sampledata_sorted <- sampledata[order(sampledata$order), ]
qc_idx <- which(sampledata_sorted$type == "QC")
# Pass to NormQcsamples for RLSC normalization
featuredata_norm <- NormQcsamples(featuredata, sampledata_sorted, method='rlsc', span=0, deg=2, lg=TRUE)
```

## Evaluation signals

- sampledata contains a populated 'type' or 'class' column with at least one 'QC' entry and at least one non-QC entry (e.g., 'sample'); no missing values in this column for rows to be used.
- sampledata is sorted by the 'order' column in ascending sequence with no gaps; verify using all(diff(sampledata$order) > 0) or equivalent.
- QC samples are distributed across the run (not all at start/end); verify by inspecting the 'order' values of QC-flagged rows and checking for temporal coverage (e.g., QC samples appear in first quartile, middle, and last quartile of the run).
- Dimension consistency: nrow(sampledata) == nrow(featuredata) and row names match exactly; no samples lost or reordered during QC flagging.
- Passing marked QC samples to NormQcsamples produces a normalized featuredata matrix with no errors or warnings related to missing QC sample indices; output dimensions match input.

## Limitations

- QC sample designation requires pre-existing metadata; if sampledata lacks a 'type' field or QC samples are not recorded, this skill cannot proceed.
- Sparse or unevenly distributed QC samples (e.g., only at run start or end) limit the ability of downstream RLSC to model and correct drift; RLSC assumes QC samples span the temporal range.
- This skill marks and selects QC samples but does not validate their analytical quality (e.g., whether QC intensities are reproducible or outlying); quality assessment is a separate step (e.g., via RlaPlots or PcaPlots on QC subsets).
- The R package requires R ≥ 3.4.3; older versions may not support NormQcsamples or may have incompatible dependencies.

## Evidence

- [other] Sort featuredata and sampledata by run order (sampledata$order column). Call NormQcsamples with the sorted featuredata and sampledata, specifying method='rlsc': "Sort featuredata and sampledata by run order (sampledata$order column). Call NormQcsamples with the sorted featuredata and sampledata, specifying method='rlsc'"
- [readme] sampledata is a dataframe that contains sample-specific information. These information can include sample type, order of analysis, factors of interest and other sample-specific data relevant to the analysis. Unique sample names need to be provided as row names.: "sampledata is a dataframe that contains sample-specific information. These information can include sample type, order of analysis, factors of interest and other sample-specific data relevant to the"
- [other] NormQcsamples<- function(featuredata, sampledata, method = c('rlsc'), span = 0, deg = 2, lg = TRUE...: "NormQcsamples<- function(featuredata, sampledata, method = c("rlsc"), span = 0, deg = 2, lg = TRUE..."
- [readme] Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation.: "Metabolomics data are inevitably subject to a component of unwanted variation, due to factors such as batch effects, matrix effects, and confounding biological variation."
