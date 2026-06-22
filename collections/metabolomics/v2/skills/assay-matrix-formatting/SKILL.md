---
name: assay-matrix-formatting
description: Use when after generating a feature table via mzrtsim() containing simulated peak abundances across samples with condition and batch effects, and you need to expose the abundance data through Bioconductor's SummarizedExperiment interface for use with standard accessor functions (assay(), colData()).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - SummarizedExperiment
  - mzrtsim
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager") BiocManager::install("mzrtsim")
- For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`
- github.com__yufree__mzrtsim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzrtsim_cq
schema_version: 0.2.0
---

# assay-matrix-formatting

## Summary

Transform simulated LC/GC-MS peak list feature tables into a matrix format suitable for storage in the 'counts' assay slot of a SummarizedExperiment object. This enables seamless integration with Bioconductor workflows and standard accessors for downstream metabolomics analysis.

## When to use

Apply this skill after generating a feature table via mzrtsim() containing simulated peak abundances across samples with condition and batch effects, and you need to expose the abundance data through Bioconductor's SummarizedExperiment interface for use with standard accessor functions (assay(), colData()).

## When NOT to use

- Input is already a SummarizedExperiment object or other Bioconductor container—use directly without reformatting.
- Raw .mzML files have not yet been processed to a feature table—apply mzrtsim() or a peak-picking workflow first.
- Feature abundance values are non-numeric or contain missing values without imputation strategy.

## Inputs

- feature table output from mzrtsim() (matrix or data.frame with m/z features as rows and samples as columns)
- simulation parameters (condition assignments, batch labels, sample identifiers)

## Outputs

- SummarizedExperiment object with 'counts' assay slot
- colData DataFrame with sample metadata (sample ID, condition, batch)

## How to apply

Extract the feature abundance matrix from the mzrtsim() output (samples as columns, features/m/z values as rows). Reshape this matrix into a numeric matrix format with features as rows and samples as columns, ensuring all values are integer or numeric counts. Construct column metadata (colData) as a DataFrame containing sample identifiers, condition assignments (e.g., control vs. treatment), and batch labels derived directly from the simulation parameters passed to mzrtsim(). Create a SummarizedExperiment object by passing the reshaped matrix as the 'counts' assay and the colData as the sample-level metadata. Verify accessibility by confirming that assay(se) returns the counts matrix and colData(se) returns the sample metadata with correct dimensions and column names.

## Related tools

- **mzrtsim** (Generates simulated LC/GC-MS feature tables with condition and batch effects to be formatted into assay matrices) — https://github.com/yufree/mzrtsim
- **SummarizedExperiment** (Bioconductor container that holds the formatted assay matrix and provides standard accessors (assay(), colData()) for matrix and metadata retrieval)
- **R** (Programming environment for reshaping matrices and constructing SummarizedExperiment objects)

## Examples

```
# Simulate feature table, extract abundance matrix, construct colData, and wrap in SummarizedExperiment
library(mzrtsim)
library(SummarizedExperiment)
ft <- mzrtsim(n_features=100, n_samples=20)
counts_matrix <- as.matrix(ft[, -1])
coldata <- DataFrame(sample_id=colnames(ft)[-1], condition=rep(c('ctrl','treat'), each=10), batch=rep(1:2, 10))
se <- SummarizedExperiment(assays=list(counts=counts_matrix), colData=coldata)
```

## Evaluation signals

- SummarizedExperiment object instantiates without error and passes validObject() checks.
- assay(se) returns a numeric matrix with dimensions matching (n_features, n_samples) and no NA values in counts.
- colData(se) contains all expected sample-level metadata columns (sample ID, condition, batch) with correct nrow matching ncol of assay matrix.
- Column names of assay matrix match row names of colData, confirming sample alignment.
- Accessor functions assay() and colData() execute and return data with correct classes (matrix and DataFrame, respectively).

## Limitations

- Requires that simulated feature abundances are already in numeric matrix form; raw .mzML files must be converted to peak lists first.
- SummarizedExperiment slot structure assumes a single 'counts' assay; multiple assays (e.g., raw intensity, normalized intensity) would require additional assay() assignments.
- Metadata columns (condition, batch) must be explicitly provided from mzrtsim() parameters; if these are missing or misaligned, colData construction will fail or produce incorrect sample assignments.
- No automatic handling of missing values or features with zero abundance across all samples; pre-filtering may be needed depending on downstream analysis.

## Evidence

- [other] Extract the feature abundance matrix and reshape it into a matrix format suitable for the 'counts' assay slot.: "Extract the feature abundance matrix and reshape it into a matrix format suitable for the 'counts' assay slot."
- [other] Construct column metadata (colData) from simulation parameters including sample identifiers, condition assignments, and batch labels.: "Construct column metadata (colData) from simulation parameters including sample identifiers, condition assignments, and batch labels."
- [other] mzrtsim_se() produces a SummarizedExperiment object containing a 'counts' assay and colData that can be accessed via standard Bioconductor accessors such as SummarizedExperiment::assay() and SummarizedExperiment::colData().: "produces a SummarizedExperiment object containing a 'counts' assay and colData that can be accessed via standard Bioconductor accessors such as SummarizedExperiment::assay() and"
- [readme] For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`: "For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`"
- [readme] `mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods.: "`mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods."
