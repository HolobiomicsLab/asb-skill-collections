---
name: motif-annotation-correlation-analysis
description: Use when you have a chromVARDeviations object with multiple annotation sets (such as JASPAR motifs and kmers) and need to determine which annotation pairs are redundant (high correlation) versus synergistic (high synergy z-scores).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0654
  tools:
  - chromVAR
  - R
  - SummarizedExperiment
  - Matrix
  - motifmatchr
derived_from:
- doi: 10.1038/nmeth.4401
  title: chromvar
evidence_spans:
- chromVAR is an R package for the analysis of sparse chromatin accessibility
- computeVariability(dev)
- An R package for the analysis of sparse chromatin accessibility
- library(chromVAR)
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

# motif-annotation-correlation-analysis

## Summary

Quantify redundancy and synergy between pairs of genomic annotation sets (e.g., motifs and kmers) in chromatin accessibility data using correlation and synergy metrics. This skill identifies which annotation pairs co-occur by chance versus providing complementary information about chromatin variability.

## When to use

Use this skill when you have a chromVARDeviations object with multiple annotation sets (such as JASPAR motifs and kmers) and need to determine which annotation pairs are redundant (high correlation) versus synergistic (high synergy z-scores). Typical triggers include comparing motif-based annotations to sequence-based features, or evaluating whether adding a second annotation set provides independent information beyond an existing set.

## When NOT to use

- Annotations from a single set only (correlation and synergy require at least two sets)
- Raw fragment count matrices that have not undergone bias correction and deviation computation
- Data in which peaks have not been pre-filtered for non-overlapping regions and sufficient quality

## Inputs

- chromVARDeviations object with precomputed bias-corrected deviations and z-scores
- Annotation matrix with named rows (peaks/regions) and columns (annotation identifiers)
- Two subsets of annotation indices (e.g., motif_ix, kmer_ix) defining the annotation sets to compare

## Outputs

- Correlation matrix (named rows and columns) as CSV file
- Synergy scores table (annotation pair names, z-scores, p-values) as CSV file

## How to apply

Load a chromVARDeviations object containing precomputed bias-corrected deviations and z-scores. Subset the annotation matrix to the two annotation sets of interest by selecting their respective column indices (e.g., motif_ix columns and kmer_ix columns). Apply getAnnotationCorrelation to compute pairwise Pearson correlations between the annotation sets across all samples, producing a correlation matrix with named rows and columns indicating annotation pairs. Apply getAnnotationSynergy to compute z-scores that compare observed variance for peaks containing both annotations against a random subsample of peaks with only the higher-variability annotation. The synergy z-score indicates whether the paired annotations explain more variance together than expected by chance. Export both the correlation matrix and synergy scores (z-scores and p-values) as CSV files with preserved headers for downstream interpretation.

## Related tools

- **chromVAR** (Core package providing getAnnotationCorrelation and getAnnotationSynergy functions for computing redundancy and synergy metrics between annotation sets) — https://github.com/GreenleafLab/chromVAR
- **SummarizedExperiment** (R/Bioconductor class used to structure the chromVARDeviations object and organize annotations, samples, and assays)
- **Matrix** (R package providing sparse matrix operations for efficient handling of large annotation matrices)
- **motifmatchr** (Used upstream to match motifs to peaks and produce motif annotation indices input to this workflow) — https://github.com/GreenleafLab/motifmatchr

## Examples

```
# After loading chromVARDeviations object 'dev' with motif and kmer annotations
corr_matrix <- getAnnotationCorrelation(dev[, c(motif_ix_cols, kmer_ix_cols)])
synergy_scores <- getAnnotationSynergy(dev, annotation_ix = c(motif_ix_cols, kmer_ix_cols))
write.csv(corr_matrix, 'annotation_correlations.csv', row.names=TRUE, col.names=TRUE)
write.csv(synergy_scores, 'annotation_synergy.csv', row.names=FALSE)
```

## Evaluation signals

- Correlation matrix is symmetric (cij = cji), contains values between -1 and 1, and has row and column names matching input annotation identifiers
- Synergy z-scores and p-values are properly computed; positive z-scores indicate synergy (non-redundant information), while negative or near-zero z-scores indicate redundancy
- CSV exports contain preserved headers with annotation pair names clearly identifying which two sets were compared
- No NaN or infinite values in correlation or synergy outputs; missing values indicate insufficient peaks meeting the comparison criteria
- Synergy computation uses random subsampling of the higher-variability annotation set, so results are reproducible only with fixed random seed

## Limitations

- Synergy z-scores depend on the size and composition of random subsamples; results may vary between runs unless random seed is fixed
- Requires that both annotation sets are already present and properly indexed in the chromVARDeviations object; filtering to non-overlapping peaks must be performed upstream
- Correlation and synergy metrics are sensitive to the quality and completeness of deviation computation; biased or incomplete bias correction will inflate or deflate both metrics
- The synergy metric assumes that the higher-variability annotation set is the reference; swapping which set is treated as reference may alter interpretation

## Evidence

- [other] chromVAR provides functions to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples: "chromVAR provides functions to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [other] getAnnotationCorrelation computes pairwise Pearson correlations between annotation sets: "Apply getAnnotationCorrelation to compute pairwise Pearson correlations between the two annotation sets across all samples, outputting a correlation matrix with named rows and columns"
- [other] getAnnotationSynergy computes z-scores for variability synergy by comparing observed variance for peaks containing both annotations against a random subsample: "Apply getAnnotationSynergy to compute z-scores for variability synergy, comparing the observed variance for peaks containing both annotations against a random subsample of peaks with only the"
- [other] Load the chromVARDeviations object containing precomputed bias-corrected deviations and z-scores: "Load the chromVARDeviations object containing precomputed bias-corrected deviations and z-scores for the annotation set"
- [other] Subset annotation matrix and export results as CSV files with headers preserved: "Export the correlation matrix as a named CSV file with row and column headers preserved, and the synergy scores as a second CSV file with annotation pair names, synergy z-scores, and p-values"
