---
name: deviation-score-computation-and-interpretation
description: Use when you have filtered ATAC-seq peak counts, matched motifs to those peaks, and want to measure which transcription factor motifs show elevated or reduced accessibility relative to GC-content and accessibility-matched background expectations—particularly when annotating TF motif usage across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0102
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

# Deviation-score computation and interpretation

## Summary

Compute bias-corrected deviation scores that quantify motif-associated variability in chromatin accessibility across samples using chromVAR's computeDeviations function. This skill enables identification of transcription factor motifs driving cell-to-cell or sample-to-sample epigenetic heterogeneity in ATAC-seq data.

## When to use

Apply this skill when you have filtered ATAC-seq peak counts, matched motifs to those peaks, and want to measure which transcription factor motifs show elevated or reduced accessibility relative to GC-content and accessibility-matched background expectations—particularly when annotating TF motif usage across cell populations or when exploring which regulatory elements drive chromatin variability.

## When NOT to use

- Input peak counts are not filtered by sample quality (depth < 1500 reads or in-peak fraction < 0.15); filterSamples must precede this skill.
- Peaks have not been reduced to non-overlapping set; overlapping peaks violate the background-matching assumptions underlying bias correction.
- Motifs have not been matched to peaks; computeDeviations requires an explicit motif match matrix, not raw motif sequences.

## Inputs

- SummarizedExperiment object with filtered peak counts (samples × peaks)
- GC bias annotations in rowData (output from addGCBias)
- Expected accessibility matrix (output from computeExpectations)
- Motif-to-peak match matrix (logical matrix from matchMotifs)
- Background peak indices (output from getBackgroundPeaks)

## Outputs

- chromVARDeviations SummarizedExperiment object with two assays: 'deviations' (bias-corrected z-scores, motifs × samples) and 'deviationScores' (raw deviations, motifs × samples)
- Row names correspond to motif identifiers
- Column names correspond to sample/cell identifiers

## How to apply

After filtering samples (min_depth ≥1500, min_in_peaks ≥0.15) and peaks (non-overlapping set), add GC content bias to rowData using addGCBias() with the reference genome, compute expected accessibility using computeExpectations() on filtered counts, and generate GC- and accessibility-matched background peaks using getBackgroundPeaks(). Then invoke computeDeviations() with the filtered SummarizedExperiment object, motif match matrix (from matchMotifs), background peaks, and expected accessibility; this returns a SummarizedExperiment with two assays: 'deviations' (bias-corrected z-scores) and 'deviationScores' (raw deviation magnitudes). Validate the output by checking that row count equals motif count, column count equals sample count, and that score distributions reflect expected variability patterns without extreme outliers.

## Related tools

- **chromVAR** (Computes bias-corrected deviation scores and returns SummarizedExperiment with deviations and deviationScores assays) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (Produces motif-to-peak match matrix input to computeDeviations) — https://github.com/GreenleafLab/motifmatchr
- **SummarizedExperiment** (Data structure for storing filtered counts, bias annotations, and output deviations)
- **BiocParallel** (Enables parallelization of computeDeviations across motifs and samples)
- **BSgenome.Hsapiens.UCSC.hg19** (Reference genome required for GC bias calculation during preprocessing (addGCBias))

## Examples

```
dev <- computeDeviations(object = counts_filtered, annotations = motif_ix)
```

## Evaluation signals

- Output object is a valid SummarizedExperiment with exactly two named assays: 'deviations' and 'deviationScores'
- Number of rows equals the count of unique matched motifs; number of columns equals the count of filtered samples
- Deviation scores (z-scores in 'deviations' assay) are normally distributed around zero with typical range ≈ [-3, +3] reflecting background-corrected accessibility
- Raw deviationScores are positive and larger in magnitude than deviations, indicating pre-standardization magnitudes
- No rows or columns contain all NaN or all zero values, indicating successful background peak matching for all motifs and samples

## Limitations

- Bias correction assumes GC content is the primary confounding factor in accessibility variability; technical artifacts not captured by GC bias will remain in deviation scores.
- Background peak selection must be matched on both GC content and accessibility; if the peak set is strongly skewed in GC composition or accessibility distribution, background matching may be incomplete.
- chromVAR has been superseded by newer methods such as SnapATAC for clustering tasks; deviation scores are best used for motif annotation within pre-determined cell populations rather than for unsupervised cell identification.
- Requires non-overlapping peak set; overlapping peaks violate the assumption that each peak represents an independent regulatory element and can produce spurious motif associations.

## Evidence

- [intro] Bias correction and background matching rationale: "The computeDeviations function returns a SummarizedExperiment object containing deviation scores that quantify motif-associated variability in chromatin accessibility across samples"
- [intro] Complete preprocessing pipeline order: "applying filterSamples, filterPeaks, addGCBias, computeExpectations, and getBackgroundPeaks preprocessing steps"
- [intro] Sample filtering parameters: "filterSamples() with min_depth=1500 and min_in_peaks=0.15 to remove low-quality cells"
- [intro] Output structure validation: "The function `computeDeviations` returns a SummarizedExperiment with two "assays""
- [readme] Recommended use case for motif annotation: "chromVAR may be complementary to some other methods, as a way of annotating TF motif usage in cells & clusters"
- [readme] Clustering performance caveat: "newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper"
