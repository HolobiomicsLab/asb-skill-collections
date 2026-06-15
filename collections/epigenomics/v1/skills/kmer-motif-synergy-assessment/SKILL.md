---
name: kmer-motif-synergy-assessment
description: Use when after computing deviations for both motif and kmer annotations on the same chromVAR dataset, when you need to determine whether kmers and motifs are redundant predictors of chromatin accessibility variability or provide complementary information for downstream clustering, annotation, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0204
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

# kmer-motif-synergy-assessment

## Summary

Quantify redundancy and synergy between kmer and motif annotation sets in chromatin accessibility data using correlation and variance-based synergy metrics. This skill reveals which annotation types capture overlapping or complementary variability signals in chromVAR deviation objects.

## When to use

After computing deviations for both motif and kmer annotations on the same chromVAR dataset, when you need to determine whether kmers and motifs are redundant predictors of chromatin accessibility variability or provide complementary information for downstream clustering, annotation, or feature selection.

## When NOT to use

- Input deviations have not been bias-corrected and z-score normalized
- You only have a single annotation type (e.g., motifs only) and cannot compute pairwise relationships
- Annotation sets are already known to be identical or fully nested (correlation assessment would be redundant)

## Inputs

- chromVARDeviations object with precomputed deviations and z-scores
- Motif annotation set (motif_ix columns)
- Kmer annotation set (kmer_ix columns)

## Outputs

- Correlation matrix (CSV): Pearson correlations between motifs and kmers
- Synergy scores (CSV): annotation pair names, synergy z-scores, and p-values

## How to apply

Load a chromVARDeviations object containing precomputed bias-corrected deviations and z-scores for both motif and kmer annotation sets. Subset the deviation matrix to isolate motif_ix and kmer_ix columns. Apply getAnnotationCorrelation to compute pairwise Pearson correlations between motifs and kmers across all samples, generating a correlation matrix with named rows and columns. Apply getAnnotationSynergy to compute z-scores for variability synergy by comparing the observed variance of peaks containing both annotation types against a random subsample of peaks with only the higher-variability annotation type. Export both matrices as named CSV files to preserve annotation identities and enable downstream interpretation.

## Related tools

- **chromVAR** (Core package providing getAnnotationCorrelation and getAnnotationSynergy functions for computing annotation redundancy and synergy metrics on SummarizedExperiment objects) — https://github.com/GreenleafLab/chromVAR
- **R** (Execution environment for chromVAR and data manipulation)
- **SummarizedExperiment** (Container class for storing chromVARDeviations with assay matrices and annotation metadata)
- **Matrix** (Efficient sparse matrix representation for deviation and annotation sets)

## Examples

```
# Load deviations, subset to motif and kmer annotations
dev_subset <- dev[, c(grep('motif_ix', colnames(dev)), grep('kmer_ix', colnames(dev)))]
# Compute correlation and synergy
corr_matrix <- getAnnotationCorrelation(dev_subset[, 1:100], dev_subset[, 101:200])
synergy_scores <- getAnnotationSynergy(dev_subset)
write.csv(corr_matrix, 'motif_kmer_correlation.csv')
write.csv(synergy_scores, 'motif_kmer_synergy.csv')
```

## Evaluation signals

- Correlation matrix has matching row/column counts for motif and kmer annotations with values in range [-1, 1]
- Synergy z-scores are accompanied by valid p-values (0 ≤ p ≤ 1) reflecting the statistical significance of non-random variance patterns
- CSV exports preserve annotation pair identities (row and column headers) and are parseable in downstream analysis
- Synergy z-scores > 2 or < -2 indicate annotations with significant positive or negative synergy (complementary or redundant behavior)
- Correlation matrix diagonal (where applicable) should reflect expected self-correlation patterns; off-diagonal correlations should be lower if kmers and motifs capture distinct signals

## Limitations

- Synergy computation relies on random subsampling of peaks with single annotations; results may vary slightly between runs unless seed is fixed
- Correlation and synergy metrics assume the deviation z-scores are properly normalized; bias-corrected deviations are mandatory
- High-dimensional annotation sets (thousands of motifs + kmers) may produce dense correlation matrices difficult to visualize or interpret without additional dimensionality reduction
- The method does not account for hierarchical relationships among motifs (e.g., family-level similarities) that could inflate apparent synergy

## Evidence

- [other] motif-kmer-redundancy-definition: "chromVAR provides functions to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [other] synergy-computation-procedure: "Apply getAnnotationSynergy to compute z-scores for variability synergy, comparing the observed variance for peaks containing both annotations against a random subsample of peaks with only the"
- [other] correlation-matrix-output: "Apply getAnnotationCorrelation to compute pairwise Pearson correlations between the two annotation sets across all samples, outputting a correlation matrix with named rows and columns"
- [readme] kmer-clustering-advantage: "Using kmers + PCA appears to be the best variant of chromVAR for clustering, but newer methods such as SnapATAC outperform chromVAR for the clustering tasks"
- [readme] annotation-complementarity-use-case: "chromVAR may be complementary to some other methods, as a way of annotating TF motif usage in cells & clusters rather than cluster identification or embedding"
