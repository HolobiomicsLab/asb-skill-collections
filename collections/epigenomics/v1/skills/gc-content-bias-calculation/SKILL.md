---
name: gc-content-bias-calculation
description: Use when you have a SummarizedExperiment object containing peak counts from single-cell or bulk ATAC-seq/DNAse-seq data and need to prepare it for unbiased motif deviation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0236
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3169
  tools:
  - chromVAR
  - R
  - motifmatchr
  - SummarizedExperiment
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

# gc-content-bias-calculation

## Summary

Compute and annotate GC content bias for peaks in chromatin accessibility data to enable bias-corrected deviation scoring. This preprocessing step accounts for systematic GC-dependent biases in ATAC-seq or DNAse-seq fragment counts before motif matching and deviation computation.

## When to use

Apply this skill when you have a SummarizedExperiment object containing peak counts from single-cell or bulk ATAC-seq/DNAse-seq data and need to prepare it for unbiased motif deviation analysis. The skill is required before filterSamples, motif matching, and computeDeviations steps to ensure deviation scores reflect true biological variability rather than GC-driven sequencing artifacts.

## When NOT to use

- Peak regions are not defined or rowRanges of the SummarizedExperiment is empty.
- Reference genome sequences are unavailable for your organism of interest.
- Input data is already bias-corrected by another method (e.g., pre-normalized counts).

## Inputs

- SummarizedExperiment object with peak counts (rowRanges defined as GRanges, assays containing count matrix)
- BSgenome reference object (e.g., BSgenome.Hsapiens.UCSC.hg19)

## Outputs

- SummarizedExperiment object with updated rowData containing 'bias' column (GC content fraction per peak)

## How to apply

Load a reference genome (e.g., BSgenome.Hsapiens.UCSC.hg19) and pass it to the addGCBias() function along with your SummarizedExperiment object containing peak regions in rowRanges. The function computes the GC content fraction for each peak and adds a 'bias' column to rowData. This bias annotation is then used internally by subsequent functions (computeExpectations, getBackgroundPeaks, computeDeviations) to match peaks by GC content when generating background sets and computing expected accessibility, ensuring that deviation scores are normalized for GC-driven biases in chromatin accessibility.

## Related tools

- **chromVAR** (Primary R package containing addGCBias() function and downstream functions that consume the bias annotation) — https://github.com/GreenleafLab/chromVAR
- **BSgenome.Hsapiens.UCSC.hg19** (Reference genome package providing DNA sequences needed to compute GC content for each peak)
- **SummarizedExperiment** (Data container class that holds peak counts and rowData (including bias annotations))

## Examples

```
example_counts <- addGCBias(example_counts, genome = BSgenome.Hsapiens.UCSC.hg19)
```

## Evaluation signals

- rowData of output SummarizedExperiment contains a 'bias' column with numeric values representing GC fraction (range 0–1) for each peak
- Bias values are distributed across the expected range; no missing or out-of-range values
- Number of rows (peaks) and columns (samples) are unchanged; only metadata is added
- Downstream computeDeviations() call executes without error, indicating bias annotation is recognized and used by background peak matching

## Limitations

- The function requires complete and valid rowRanges (peak coordinates) in the input SummarizedExperiment; peaks with missing or overlapping coordinates may produce unexpected bias values.
- GC bias calculation is species-specific and requires a matching reference genome; using a mismatched genome will yield incorrect bias annotations.
- This skill addresses only GC-driven sequencing bias; other technical biases (e.g., mappability, repeat content) are not accounted for by addGCBias() alone.
- The chromVAR documentation notes that SnapATAC outperforms chromVAR for clustering tasks, suggesting that bias correction alone may not address all sources of technical variation in sparse single-cell ATAC data.

## Evidence

- [other] The function `addGCBias` returns an updated SummarizedExperiment with a new rowData column named "bias": "The function `addGCBias` returns an updated SummarizedExperiment with a new rowData column named "bias""
- [other] Add GC content bias to rowData using addGCBias() with the reference genome.: "Add GC content bias to rowData using addGCBias() with the reference genome."
- [readme] chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data: "chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data"
- [readme] The package aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples.: "The package aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
