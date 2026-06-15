---
name: chromatin-accessibility-deviation-computation
description: Use when when you have filtered ATAC-seq or DNAse-seq peak counts (after GC bias correction, sample filtering, and peak filtering) and wish to measure how strongly each annotation (motif or kmer) influences chromatin accessibility variability in each sample relative to a background expectation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3233
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - chromVAR
  - R
  - motifmatchr
  - SummarizedExperiment
  - BiocParallel
  - BSgenome.Hsapiens.UCSC.hg19
  - Matrix
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

# chromatin-accessibility-deviation-computation

## Summary

Compute deviation scores that quantify how individual cells or samples deviate from the expected chromatin accessibility pattern for specific genomic annotations (motifs or kmers). This transforms sparse ATAC-seq counts into bias-corrected deviation matrices suitable for identifying annotation-accessibility associations.

## When to use

When you have filtered ATAC-seq or DNAse-seq peak counts (after GC bias correction, sample filtering, and peak filtering) and wish to measure how strongly each annotation (motif or kmer) influences chromatin accessibility variability in each sample relative to a background expectation.

## When NOT to use

- Input counts have not been bias-corrected with addGCBias or filtered with filterSamples/filterPeaks; computeDeviations requires preprocessed, quality-filtered input.
- Annotation matrix is already in a non-sparse, dense format unsuitable for chromVAR's internal optimization; use sparse Matrix objects.
- Goal is only clustering or dimensionality reduction without annotation interpretation; newer methods like SnapATAC outperform chromVAR for clustering tasks.

## Inputs

- SummarizedExperiment with peak-by-sample counts matrix (bias-corrected, filtered for sample depth ≥1500 and in-peak fraction ≥0.15, peaks non-overlapping)
- Sparse annotation matrix (rows=peaks, columns=annotations) from matchMotifs or matchKmers

## Outputs

- chromVARDeviations SummarizedExperiment object with two assays: 'deviations' (peak-annotation-by-sample deviation scores) and 'z' (z-score normalized deviations)

## How to apply

Load the filtered SummarizedExperiment counts object and match annotations (motifs via matchMotifs or kmers via matchKmers) to generate a sparse annotation matrix. Pass both the counts and annotation matrix to computeDeviations, which internally computes per-annotation accessibility deviations as the difference between observed and bias-expected accessibility, producing z-scores normalized across samples. The resulting SummarizedExperiment contains two assays: deviations (raw deviation scores) and z-scores (standardized across samples); these serve as input for downstream variability, correlation, or synergy analyses. The key rationale is that deviation computation accounts for GC content bias and library size differences, enabling fair cross-sample comparisons of annotation-specific accessibility patterns.

## Related tools

- **chromVAR** (Primary package providing computeDeviations function and SummarizedExperiment/chromVARDeviations classes) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (Matches motif position weight matrices to peak sequences; produces annotation matrix input for computeDeviations) — https://github.com/GreenleafLab/motifmatchr
- **BSgenome.Hsapiens.UCSC.hg19** (Provides genome sequence for kmer matching and motif matching operations)
- **SummarizedExperiment** (Bioconductor class for storing counts matrix, peak metadata, and sample metadata)
- **Matrix** (Sparse matrix representation used internally by chromVAR for efficient computation)
- **BiocParallel** (Optional parallelization backend; register parameter choice (SerialParam, MulticoreParam, or SnowParam) before computeDeviations)

## Examples

```
dev <- computeDeviations(object = counts_filtered, annotations = motif_ix)
```

## Evaluation signals

- Output object is a valid chromVARDeviations inheriting from SummarizedExperiment with exactly two assays ('deviations' and 'z')
- Deviations assay dimensions are (number_of_annotations × number_of_samples) and z-scores have mean ~0 and std ~1 within each sample
- Z-scores are centered and scaled per sample (not globally), confirming bias correction and normalization are internally applied
- All deviation and z-score values are numeric and finite (no NaN or Inf); missing values indicate failed annotation-peak matches
- Downstream variability or correlation analyses (e.g., computeVariability, getAnnotationCorrelation) on the output object execute without error and produce expected dimensions

## Limitations

- computeDeviations assumes input counts are sparse and bias-corrected; dense or uncorrected input may produce misleading deviation scores.
- Deviation computation is sensitive to annotation-matching quality; low specificity in motif matching or kmer matches will introduce noise into deviation scores.
- Performance degrades with very large numbers of annotations (e.g., >50,000 kmers) or samples; batch processing or annotation subsetting may be necessary.
- Z-score normalization is per-sample; cross-sample comparisons of absolute deviations should use the raw 'deviations' assay, not 'z'.

## Evidence

- [intro] computeDeviations computes bias-corrected deviations: "The function `computeDeviations` returns a SummarizedExperiment with two "assays""
- [intro] deviation computation is central to annotation-variability association: "aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [intro] kmer matching produces annotation input for deviations: "matchKmers(6, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19), then compute deviations with computeDeviations(counts_filtered, kmer_ix_6mer)"
- [intro] GC bias correction is prerequisite: "The function `addGCBias` returns an updated SummarizedExperiment with a new rowData column named "bias""
- [intro] Sample and peak filtering are prerequisites: "it is advisable to filter out samples with insufficient reads using filterSamples"
