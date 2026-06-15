---
name: kmer-annotation-matrix-assembly
description: Use when you have filtered peak counts from ATAC or DNase-seq data (with GC bias correction and sample/peak filtering applied) and want to annotate peaks by k-mer content rather than known transcription factor motifs—particularly when comparing how k-mer size affects the magnitude of chromatin.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - chromVAR
  - R
  - motifmatchr
  - SummarizedExperiment
  - Matrix
  - BiocParallel
  - BSgenome.Hsapiens.UCSC.hg19
derived_from:
- doi: 10.1038/nmeth.4401
  title: chromvar
evidence_spans:
- chromVAR is an R package for the analysis of sparse chromatin accessibility
- computeVariability(dev)
- An R package for the analysis of sparse chromatin accessibility
- library(chromVAR)
- library(motifmatchr)
- library(SummarizedExperiment)
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

# kmer-annotation-matrix-assembly

## Summary

Generate k-mer annotation matrices that map short DNA sequence motifs (6-mers or 7-mers) to peaks in chromatin accessibility data, enabling subsequent deviation and variability scoring in chromVAR workflows. This is a prerequisite for motif-agnostic annotation of chromatin accessibility variability.

## When to use

You have filtered peak counts from ATAC or DNase-seq data (with GC bias correction and sample/peak filtering applied) and want to annotate peaks by k-mer content rather than known transcription factor motifs—particularly when comparing how k-mer size affects the magnitude of chromatin accessibility variability scores.

## When NOT to use

- You already have known transcription factor motif annotations and want to use matched motifs instead of k-mers.
- Your peak set contains overlapping peaks—apply filterPeaks() first to remove overlaps before k-mer annotation.
- You lack a reference genome object appropriate for your organism and assembly.

## Inputs

- SummarizedExperiment counts object (filtered, GC-bias corrected, with min_depth ≥ 1500 and min_in_peaks ≥ 0.15)
- Reference genome object (BSgenome, e.g., BSgenome.Hsapiens.UCSC.hg19)
- k-mer length integer (e.g., 6 or 7)

## Outputs

- Sparse binary matrix of k-mer annotations (rows = k-mers, columns = peaks)
- chromVAR kmer_ix object suitable for input to computeDeviations()

## How to apply

Load the filtered SummarizedExperiment counts object and call matchKmers() with the desired k-mer length (6, 7, or other integer) and a reference genome (e.g., BSgenome.Hsapiens.UCSC.hg19). The function returns a sparse binary matrix where rows are k-mers and columns are peaks, with 1 indicating presence of that k-mer in the peak sequence. Repeat for multiple k-mer sizes if performing comparative analysis (e.g., 6-mers vs. 7-mers) to assess how motif granularity affects downstream deviation computation and variability scoring. The resulting annotation matrix is then passed directly to computeDeviations() for deviation scoring.

## Related tools

- **chromVAR** (Main package providing matchKmers() and computeDeviations() functions for k-mer annotation and deviation scoring) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (Dependency providing sequence-matching infrastructure used by matchKmers()) — https://github.com/GreenleafLab/motifmatchr
- **BSgenome.Hsapiens.UCSC.hg19** (Reference genome object required as input to matchKmers() for sequence lookup)
- **SummarizedExperiment** (Data structure class for storing counts and peak metadata)
- **BiocParallel** (Optional parallelization framework for faster k-mer matching on large peak sets)

## Examples

```
kmer_ix_6mer <- matchKmers(6, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19)
kmer_ix_7mer <- matchKmers(7, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19)
```

## Evaluation signals

- Resulting annotation matrix is sparse (not dense) and has dimensions: number of unique k-mers (rows) × number of peaks (columns).
- Matrix contains only binary values (0 or 1), indicating k-mer presence/absence in each peak.
- For a given k-mer size, the number of unique k-mers should be consistent with sequence diversity (7-mers will have up to 4^7 = 16,384 possible values; 6-mers up to 4^6 = 4,096).
- Downstream computeDeviations() runs without error and produces a deviation object with matching dimensions.
- Variability scores computed on 7-mer annotations are higher in magnitude (mean/median/std dev) than those from 6-mers, confirming expected granularity effect.

## Limitations

- matchKmers() requires a pre-filtered, non-overlapping peak set; overlapping peaks must be removed by filterPeaks() beforehand.
- k-mer matching is sequence-based only and does not account for TF binding affinity or biological context; consider complementing with motif-based approaches for functional interpretation.
- Larger k-mer sizes (e.g., 8-mers) generate increasingly sparse matrices and may reduce statistical power if peak sets are small.
- The choice of reference genome assembly is critical; mismatched assemblies will result in incorrect or missing k-mer matches.

## Evidence

- [other] Generate 6-mer kmer annotation matrix using matchKmers(6, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19): "Generate 6-mer kmer annotation matrix using matchKmers(6, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19)"
- [readme] Using kmers + PCA appears to be the best variant of chromVAR for clustering: "Using kmers + PCA appears to be the best variant of chromVAR for clustering"
- [other] chromVAR supports kmer-based annotation approaches as a viable method for analyzing chromatin accessibility variability: "chromVAR supports kmer-based annotation approaches as a viable method for analyzing chromatin accessibility variability, with kmers being suitable for deviation computation workflows"
- [readme] The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs: "The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs"
