---
name: experiment-design-specification-for-clustering
description: Use when you have a CSV feature table from XCMS or other MS feature detection tools and are about to run RAMClustR clustering, but need to encode which samples are QC replicates, which batch they belong to, and their run order.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - RAMClustR
  - R
  - dynamicTreeCut
  - XCMS
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# experiment-design-specification-for-clustering

## Summary

Define and encode the experimental design metadata (sample groupings, batch information, QC tags, run order) required by RAMClustR to properly normalize feature intensities and perform unsupervised clustering of metabolomics features. This specification bridges raw feature tables and clustering by capturing which samples belong to which experimental conditions, batches, and quality control cohorts.

## When to use

You have a CSV feature table from XCMS or other MS feature detection tools and are about to run RAMClustR clustering, but need to encode which samples are QC replicates, which batch they belong to, and their run order. RAMClustR requires this metadata to apply batch correction and QC-based normalization before clustering, especially when samples span multiple analytical batches or contain QC injections for drift correction.

## When NOT to use

- Input samples lack batch or run-order metadata — normalization cannot correct for systematic drift if these dimensions are unknown.
- All samples are from a single analytical run with no QC replicates — batch correction is unnecessary, though QC-based drift correction cannot be applied.
- Feature table has already been normalized or batch-corrected by upstream preprocessing — specifying ExpDes again may introduce double-correction artifacts.

## Inputs

- CSV file with phenotype/experimental design metadata (one row per sample; columns: sample name, batch, run order, QC tag)
- Feature table CSV with sample names as column headers (from XCMS or similar tool)

## Outputs

- Validated experimental design object embedded in RAMClustR input, enabling batch and QC normalization
- Batch-corrected and QC-normalized feature abundance matrix (output from ramclustR after applying design)

## How to apply

Prepare a phenotype/experimental design CSV with one row per sample and columns for sample name, batch identifier, run order (sequence position), and QC tag (e.g., 'QC' for quality control samples, blank sample designation). Pass this file to ramclustR via the `pheno_csv` parameter. The function internally uses three vectors (batch, order, qc) extracted from this metadata to apply feature-centric normalization: first correcting each feature's intensity by comparing batch median intensity to the full dataset median, then applying local QC median vs. global median corrections to account for run-order drift. Ensure the sample names in the phenotype file exactly match the column headers in your feature table. The order of rows in the phenotype file should correspond to the order of sample columns in the feature table, or use explicit sample name matching if the function supports it.

## Related tools

- **XCMS** (Generates the initial feature table (mz/RT pairs and intensities) that is paired with experimental design for normalization and clustering)
- **RAMClustR** (Consumes the phenotype/experimental design metadata to normalize features by batch and QC before performing unsupervised clustering) — https://github.com/cbroeckl/RAMClustR
- **dynamicTreeCut** (Hierarchical clustering package used internally by RAMClustR after feature normalization is complete)

## Examples

```
ramclustobj <- ramclustR(ms = 'peaks.csv', pheno_csv = 'phenoData.csv', st = 5, maxt = 1, blocksize = 1000)
```

## Evaluation signals

- Sample names in phenotype CSV exactly match column headers in feature table (no mismatches or case-sensitivity errors).
- Batch and QC tag columns contain only expected category values (no null/NA entries for required fields; QC tag is consistent across replicates).
- Output RC object's feature intensity matrix shows reduced variance within QC replicates after batch correction, compared to input feature table.
- Clustering dendrograms or RC$clust object show features from the same compound grouped together; features with similar retention times (±tolerance) and quantitative trends cluster in the same group.
- If batch effect was present, downstream RC object annotations and spectral matching scores should improve or remain stable (not degrade) after normalization.

## Limitations

- Phenotype metadata must be manually curated or extracted from instrument run logs; no automated parsing from raw MS file headers is described.
- Feature-centric normalization assumes QC samples were injected at sufficient frequency and are representative of full-dataset performance; sparse QC sampling may leave systematic drift uncorrected.
- Run-order correction is applied uniformly across all features; compounds with genuine run-order-dependent behavior (e.g., carryover or detector saturation) may be mis-corrected.
- No changelog or version history is provided, so parameter names and phenotype CSV schema may change between RAMClustR versions without documented migration guidance.

## Evidence

- [readme] Phenotype CSV schema and parameters: "pheno_csv = pheno, ... Column with sample name is expected to be first (by default). These can be adjusted with the `featdelim` and `sampNameCol` parameters."
- [other] Batch/QC/order vector requirements and normalization logic: "batch.qc. normalization requires input of three vectors (1) batch (2) order (3) qc. This is a feature centric normalization approach which adjusts signal intensities first by comparing batch median"
- [intro] Relationship between experimental design and RAMClustR feature matching: "two features derived from the same compound will have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [other] ExpDes parameter usage in main ramclustR function call: "Execute ramclustR function on the MS-only feature table, specifying experiment design parameters to generate the first RC object"
