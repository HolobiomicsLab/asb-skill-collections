---
name: sparse-matrix-subset-indexing
description: Use when when you have a chromVARDeviations object with multiple annotation sets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - chromVAR
  - R
  - SummarizedExperiment
  - Matrix
derived_from:
- doi: 10.1038/nmeth.4401
  title: chromvar
evidence_spans:
- chromVAR is an R package for the analysis of sparse chromatin accessibility
- computeVariability(dev)
- An R package for the analysis of sparse chromatin accessibility
- library(chromVAR)
- library(SummarizedExperiment)
- library(Matrix)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chromvar
    doi: 10.1038/nmeth.4401
    title: chromvar
  dedup_kept_from: coll_chromvar
schema_version: 0.2.0
---

# sparse-matrix-subset-indexing

## Summary

Subset annotation matrices within chromVAR Deviations objects by selecting specific rows (annotation sets) or columns (samples) using standard R indexing to isolate feature pairs of interest before computing correlation or synergy metrics. This is a foundational data manipulation step that preserves sparsity and enables targeted pairwise annotation analysis.

## When to use

When you have a chromVARDeviations object with multiple annotation sets (e.g., JASPAR motif indices and kmer indices) and you need to isolate two specific annotation sets for correlation or synergy computation, or when you wish to exclude low-quality or irrelevant samples before annotation relationship analysis.

## When NOT to use

- Input annotation matrix is already filtered to a single annotation set or fewer than two sets (nothing to subset).
- Performing whole-matrix analysis intended to compare all annotation pairs simultaneously; subsetting prematurely may exclude relevant cross-set comparisons.
- Working with a dense matrix representation; sparse subsetting assumes sparse Matrix format to preserve efficiency.

## Inputs

- chromVARDeviations object with annotation matrix (assay)
- Column/row indices or names identifying the two annotation sets of interest

## Outputs

- Subsetted sparse matrix of annotations (typically Matrix::dgCMatrix or similar)
- Annotation pair identifiers (e.g., motif_ix and kmer_ix column names)

## How to apply

Load the chromVARDeviations object containing precomputed bias-corrected deviations and z-scores. Identify the column indices (or names) corresponding to the two annotation sets of interest in the annotation matrix—for example, motif_ix columns for JASPAR motifs and kmer_ix columns for kmers. Use standard R matrix subsetting syntax (e.g., `annotations[, c(motif_cols, kmer_cols)]` or by named column selection) to extract the subset. Verify that the resulting matrix retains the sparse Matrix format to avoid memory overhead. The subsetted matrix then serves as input to downstream functions like getAnnotationCorrelation or getAnnotationSynergy, which operate on pairs of annotations across all retained samples.

## Related tools

- **chromVAR** (Provides the SummarizedExperiment-based chromVARDeviations object structure and downstream functions (getAnnotationCorrelation, getAnnotationSynergy) that consume subsetted annotation matrices) — https://github.com/GreenleafLab/chromVAR
- **SummarizedExperiment** (Base class used by chromVARDeviations; defines the assay() accessor and matrix subsetting semantics)
- **Matrix** (Provides the sparse matrix representation (dgCMatrix) that stores annotation data; subsetting preserves sparsity)
- **R** (Language for executing matrix indexing operations and subsetting syntax)

## Examples

```
library(chromVAR); data(example_counts, package = "chromVAR"); motif_ix <- matchMotifs(motifs, counts_filtered, genome = BSgenome.Hsapiens.UCSC.hg19); kmer_ix <- list(...); subsetted <- cbind(assay(motif_ix)[, 1:50], assay(kmer_ix)[, 1:20]); corr <- getAnnotationCorrelation(subsetted)
```

## Evaluation signals

- Subsetted matrix retains correct row count (number of peaks) and column count matches exactly the union of the two selected annotation sets.
- Matrix remains in sparse format (confirmed by class(subsetted_matrix) returning 'dgCMatrix' or similar, not 'matrix').
- Column and row names are preserved and correctly match the source annotation labels.
- Downstream getAnnotationCorrelation and getAnnotationSynergy functions accept the subsetted matrix without error and produce named outputs with correct annotation pair identifiers.
- No spurious zero-inflation or data loss; non-zero entry count in subsetted matrix is a subset of the original.

## Limitations

- Subsetting by integer indices is error-prone if annotation column order is unknown; named subsetting is preferred but requires that all annotations are named in the assay matrix.
- Large annotation sets may still produce large subsetted matrices if the two selected sets are high-dimensional; memory usage scales with union of selected annotation counts.
- Subsetting does not perform quality filtering (e.g., removing low-variance annotations); use filterPeaks or filterSamples before subsetting for that purpose.

## Evidence

- [other] Subset the annotation matrix to include only the two annotation sets of interest (e.g., motif_ix columns for JASPAR motifs and kmer_ix columns for kmers).: "Subset the annotation matrix to include only the two annotation sets of interest (e.g., motif_ix columns for JASPAR motifs and kmer_ix columns for kmers)."
- [intro] chromVAR provides functions to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples: "chromVAR aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [intro] The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs: "The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs"
- [readme] chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data: "chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data"
