---
name: metabolomics-feature-table-conversion
description: Use when you have generated a feature table via mzrtsim() with simulated LC/GC-MS abundances, condition assignments, and batch labels, and you need to pass it to Bioconductor tools (e.g., for batch correction, normalization, or statistical analysis) that expect SummarizedExperiment-class input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01213
  all_source_dois:
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Wrap simulated metabolomics feature tables in SummarizedExperiment for Bioconductor integration

## Summary

Convert peak-list simulation output (feature tables with condition and batch effects) into a SummarizedExperiment object that exposes count data and sample metadata through standard Bioconductor accessors. This enables seamless downstream integration with Bioconductor normalization, batch correction, and analysis workflows.

## When to use

You have generated a feature table via mzrtsim() with simulated LC/GC-MS abundances, condition assignments, and batch labels, and you need to pass it to Bioconductor tools (e.g., for batch correction, normalization, or statistical analysis) that expect SummarizedExperiment-class input.

## When NOT to use

- Input is already a SummarizedExperiment object.
- Raw .mzML spectral data has not yet been processed into a feature table; use simmzml() first to generate raw data simulation output.
- Feature table lacks sample-level metadata (condition, batch) required to populate colData.

## Inputs

- Feature abundance matrix (numeric matrix, features × samples)
- Sample metadata data frame containing condition labels, batch assignments, and sample identifiers

## Outputs

- SummarizedExperiment object with 'counts' assay and colData

## How to apply

Call mzrtsim() to generate a feature abundance matrix with simulated condition and batch effects. Extract the abundance data and reshape it into a samples-by-features matrix format compatible with the 'counts' assay slot. Construct sample-level metadata (colData) by extracting simulation parameters including sample identifiers, condition assignments, and batch labels from the mzrtsim output. Pass both the reshaped counts matrix and colData to the SummarizedExperiment() constructor, which creates an object exposing counts via the assay() accessor and colData via the colData() accessor per Bioconductor conventions. Verify that downstream functions (e.g., batch correction methods like bccenter, bcscaling) can access counts and metadata via standard Bioconductor accessors.

## Related tools

- **mzrtsim** (Generates feature tables with controlled condition and batch effects for input to conversion) — https://github.com/yufree/mzrtsim
- **SummarizedExperiment** (Bioconductor class that wraps the feature table and metadata; provides assay() and colData() accessors) — https://bioconductor.org/packages/SummarizedExperiment
- **R** (Programming environment for data manipulation and SummarizedExperiment object construction)

## Examples

```
library(mzrtsim); library(SummarizedExperiment); sim <- mzrtsim(n = 100, samples = 10, condition = c(0.5, 1.5)); se <- mzrtsim_se(sim); assay(se); colData(se)
```

## Evaluation signals

- SummarizedExperiment object is created without error and inherits from the SummarizedExperiment class.
- assay(object) returns the feature abundance matrix (features × samples) with correct dimensions and numeric values.
- colData(object) returns a DataFrame with sample-level metadata including condition and batch columns matching input.
- Downstream Bioconductor batch correction functions (bccenter, bcscaling, bcpareto, bcrange, bcvast, bclevel) successfully access counts and metadata via standard accessors without conversion errors.
- Sample identifiers in colData match row names of the counts matrix and align with simulation parameter records.

## Limitations

- mzrtsim_se() requires pre-computed feature abundance matrix and metadata; it does not generate the simulation itself—mzrtsim() must be called first.
- SummarizedExperiment construction assumes feature-by-sample matrix orientation; non-standard input formats may require explicit transpose or reshape prior to conversion.
- No automatic validation of metadata consistency (e.g., missing or malformed condition/batch labels) is performed; users must ensure colData completeness.

## Evidence

- [other] mzrtsim_se() produces a SummarizedExperiment object containing a 'counts' assay and colData that can be accessed via standard Bioconductor accessors such as SummarizedExperiment::assay() and SummarizedExperiment::colData().: "mzrtsim_se() produces a SummarizedExperiment object containing a 'counts' assay and colData that can be accessed via standard Bioconductor accessors such as SummarizedExperiment::assay() and"
- [readme] For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`: "For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`"
- [readme] `mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods.: "`mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods."
- [other] 1. Call mzrtsim() to generate a feature table with condition and batch effects. 2. Extract the feature abundance matrix and reshape it into a matrix format suitable for the 'counts' assay slot. 3. Construct column metadata (colData) from simulation parameters including sample identifiers, condition assignments, and batch labels.: "Call mzrtsim() to generate a feature table with condition and batch effects. Extract the feature abundance matrix and reshape it into a matrix format suitable for the 'counts' assay slot. Construct"
