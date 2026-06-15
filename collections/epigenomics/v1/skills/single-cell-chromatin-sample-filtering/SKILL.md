---
name: single-cell-chromatin-sample-filtering
description: Use when after loading fragment counts into a SummarizedExperiment object (e.g., via getCounts) but before motif matching or deviation computation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
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

# single-cell-chromatin-sample-filtering

## Summary

Remove low-quality single cells or bulk samples from ATAC-seq or DNAse-seq chromatin accessibility data prior to downstream analysis. This quality control step eliminates samples with insufficient sequencing depth or low peak coverage that would compromise motif deviation or clustering accuracy.

## When to use

Apply this skill after loading fragment counts into a SummarizedExperiment object (e.g., via getCounts) but before motif matching or deviation computation. Use it when working with sparse, sample-wise chromatin accessibility data where sequencing depth and in-peak read fraction vary substantially across cells or samples—typical in single-cell ATAC-seq workflows.

## When NOT to use

- Samples are already pre-filtered by the upstream alignment pipeline or cell caller—applying additional filtering may remove too few cells to affect power.
- Input is a pre-aggregated bulk sample matrix without per-sample depth metadata—thresholds become arbitrary.
- Analysis goal is to benchmark filtering sensitivity; use unfiltered data explicitly as a control.

## Inputs

- SummarizedExperiment object with fragment count matrix (from getCounts or similar)
- colData metadata defining sample identifiers and optional grouping variables

## Outputs

- Filtered SummarizedExperiment object with same structure but reduced column dimension (fewer samples)
- Integer vector of retained sample indices (implicit)

## How to apply

Use the filterSamples() function from chromVAR to remove samples falling below user-specified thresholds on two key metrics: (1) min_depth, the minimum total fragment count per sample (e.g., 1500 for single cells), and (2) min_in_peaks, the minimum fraction of reads mapping to called peaks (e.g., 0.15). The rationale is that samples with low sequencing depth produce unreliable motif deviation estimates, while low in-peak fractions indicate either poor ATAC-seq quality or failed library preparation. Filter samples before filterPeaks() to ensure expectations and background peak matching operate on a clean, consistent sample cohort. Validate the filter by comparing pre- and post-filter sample counts and checking that remaining samples meet both criteria.

## Related tools

- **chromVAR** (provides filterSamples() function and SummarizedExperiment container for ATAC-seq counts) — https://github.com/GreenleafLab/chromVAR
- **SummarizedExperiment** (data structure holding counts matrix, rowData (peak annotations), and colData (sample metadata))
- **BiocParallel** (optional parallel backend for computationally intensive downstream steps after filtering)

## Examples

```
counts_filtered <- filterSamples(example_counts, min_depth = 1500, min_in_peaks = 0.15)
```

## Evaluation signals

- Post-filter sample count is strictly less than pre-filter count; no samples are added.
- All retained samples have total depth ≥ min_depth threshold (sum of their count matrix columns).
- All retained samples have in-peak fraction ≥ min_in_peaks (sum of counts in peaks / total counts per sample).
- Row dimension (peaks) is unchanged; only columns (samples) are subsetted.
- colData and rowData structures remain intact and consistent with filtered count matrix.

## Limitations

- Thresholds (min_depth, min_in_peaks) are dataset and cell type–dependent; chromVAR documentation recommends min_depth=1500 for single-cell ATAC but this may be too stringent for sparse or rare cell populations.
- Filtering is univariate per threshold; joint optimization of both criteria (e.g., trading depth for peak fraction) is not performed automatically.
- No correction for batch effects or cell cycle stage; low-quality samples may cluster with dropout rather than true biology if not addressed separately.
- Removal of samples can inflate power in small cohorts; consider downsampling depth-biased cohorts rather than outright filtering in some contexts.

## Evidence

- [intro] filterSamples_description: "it is advisable to filter out samples with insufficient reads using filterSamples"
- [other] filterSamples_parameters: "Filter samples using filterSamples() with min_depth=1500 and min_in_peaks=0.15 to remove low-quality cells"
- [readme] filterSamples_documentation: "counts_filtered <- filterSamples(example_counts, min_depth = 1500, min_in_peaks = 0.15)"
- [intro] output_type_singleexperiment: "The function `computeDeviations` returns a SummarizedExperiment with two "assays""
- [other] workflow_ordering: "Filter samples using filterSamples() with min_depth=1500 and min_in_peaks=0.15 to remove low-quality cells. 5. Filter peaks using filterPeaks()"
