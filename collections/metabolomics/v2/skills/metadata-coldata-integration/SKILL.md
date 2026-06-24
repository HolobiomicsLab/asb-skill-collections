---
name: metadata-coldata-integration
description: Use when when you have generated a feature abundance matrix from mzrtsim()
  peak list simulation with known sample-level attributes (condition assignments,
  batch labels, sample identifiers) and need to package this into a SummarizedExperiment
  object for Bioconductor-compatible analysis pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - SummarizedExperiment
  - mzrtsim
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
  BiocManager::install("mzrtsim")
- For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps
  the simulation in a `SummarizedExperiment`
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-coldata-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct and integrate sample-level metadata (colData) into a SummarizedExperiment object to expose simulated LC/GC-MS feature tables through standard Bioconductor accessors. This skill bridges peak list simulation output with the SummarizedExperiment data structure, enabling downstream batch correction and normalization workflows.

## When to use

When you have generated a feature abundance matrix from mzrtsim() peak list simulation with known sample-level attributes (condition assignments, batch labels, sample identifiers) and need to package this into a SummarizedExperiment object for Bioconductor-compatible analysis pipelines that expect colData metadata.

## When NOT to use

- Input data is already in SummarizedExperiment format — skip directly to accessor verification
- Raw .mzML files or peak list CSVs without prior feature table aggregation — use simmzml() or mzrtsim() first
- When colData metadata is incomplete or inconsistent with the number of samples in the feature matrix

## Inputs

- feature abundance matrix from mzrtsim() output
- simulation parameters (condition assignments, batch labels, sample identifiers)

## Outputs

- SummarizedExperiment object with 'counts' assay
- SummarizedExperiment object with populated colData

## How to apply

Extract the feature abundance matrix from mzrtsim() output and reshape it into matrix format suitable for the 'counts' assay slot. Construct a data frame (colData) containing sample-level metadata such as sample identifiers, condition labels, and batch assignments sourced directly from the simulation parameters. Create a SummarizedExperiment object using SummarizedExperiment() constructor, passing the counts matrix as the primary assay and the colData frame as column metadata. Verify that the resulting object exposes counts via assay() accessor and colData via colData() accessor per Bioconductor conventions. This approach ensures compatibility with downstream batch correction methods (bccenter, bcscaling, bcpareto, bcrange, bcvast, bclevel) that expect standard SummarizedExperiment slots.

## Related tools

- **SummarizedExperiment** (Container class used to construct the S4 object holding counts assay and colData slots) — https://bioconductor.org/packages/SummarizedExperiment/
- **mzrtsim** (Upstream peak list simulation tool that generates feature tables with condition and batch effects to be wrapped) — https://github.com/yufree/mzrtsim
- **R** (Host language for SummarizedExperiment construction and Bioconductor accessor methods)

## Examples

```
# After calling mzrtsim() to generate feature_table and sim_params
se <- SummarizedExperiment::SummarizedExperiment(
  assays = list(counts = feature_matrix),
  colData = data.frame(sample_id = sim_params$samples, condition = sim_params$conditions, batch = sim_params$batches)
)
assay(se, 'counts'); colData(se)
```

## Evaluation signals

- SummarizedExperiment object instantiates without errors and class(se) == 'SummarizedExperiment'
- assay(se, 'counts') returns a numeric matrix with dimensions matching input feature table (features × samples)
- colData(se) returns a DataFrame with row count equal to number of samples and columns matching metadata attributes (e.g., condition, batch, sample_id)
- colData row names correspond exactly to column names of the counts assay (no misalignment of samples)
- Object is serializable and readable by downstream Bioconductor batch correction functions expecting colData slots

## Limitations

- colData must have exactly as many rows as the counts matrix has columns; mismatch causes SummarizedExperiment() construction to fail
- Metadata column names are case-sensitive and must match expectations of downstream batch correction pipelines (e.g., 'condition', 'batch')
- SummarizedExperiment does not validate biological plausibility of metadata-feature associations — mismatched batch/condition assignments will propagate silently into downstream normalization

## Evidence

- [abstract] metadata-coldata-integration: "For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`"
- [other] colData construction from simulation parameters: "Construct column metadata (colData) from simulation parameters including sample identifiers, condition assignments, and batch labels."
- [other] assay and colData accessor verification: "Verify that the resulting object exposes counts via the assay() accessor and colData via the colData() accessor per Bioconductor conventions."
- [other] feature matrix reshaping into counts slot: "Extract the feature abundance matrix and reshape it into a matrix format suitable for the 'counts' assay slot."
- [other] SummarizedExperiment constructor usage: "Create a SummarizedExperiment object using SummarizedExperiment() with the counts matrix as the primary assay and colData containing sample-level metadata."
