---
name: transcription-factor-cooperative-binding-detection
description: Use when you have a chromVARDeviations object with precomputed bias-corrected deviations and z-scores for multiple annotation sets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2940
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3169
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

# Transcription Factor Cooperative Binding Detection

## Summary

Quantify redundancy and synergy between pairs of transcription factor (TF) annotations in chromatin accessibility data by computing correlation and synergy scores. This skill identifies whether two TF motifs or annotation sets show independent variation or cooperative/synergistic patterns in chromatin accessibility across cells or samples.

## When to use

Apply this skill when you have a chromVARDeviations object with precomputed bias-corrected deviations and z-scores for multiple annotation sets (e.g., JASPAR motifs and kmers), and you want to determine which pairs of annotations are redundant (highly correlated) versus synergistic (variability in peaks with both annotations exceeds expectation from either annotation alone).

## When NOT to use

- The chromVARDeviations object has not been bias-corrected or deviations have not yet been computed—run computeDeviations and addGCBias first.
- You are comparing more than two annotation sets at once—this skill is pairwise; use alternative multi-way interaction methods for >2 sets.
- Your goal is clustering or dimensionality reduction rather than annotation relationship characterization—use kmers + PCA or SnapATAC for those tasks.

## Inputs

- chromVARDeviations object with precomputed deviations and z-scores
- Annotation matrix or SummarizedExperiment assay subset (two annotation sets)

## Outputs

- Correlation matrix (CSV with named rows and columns)
- Synergy scores table (CSV with annotation pair names, z-scores, and p-values)

## How to apply

Load the chromVARDeviations object containing precomputed bias-corrected deviations and z-scores. Subset the annotation matrix to include only the two annotation sets of interest by selecting their respective columns (e.g., motif_ix for JASPAR motifs and kmer_ix for kmers). Apply getAnnotationCorrelation to compute pairwise Pearson correlations between the two sets across all samples, producing a correlation matrix with named rows and columns. Apply getAnnotationSynergy to compute z-scores comparing the observed variance for peaks containing both annotations against a random subsample of peaks with only the higher-variability annotation; this yields z-scores and p-values for each annotation pair. Export both results as named CSV files preserving row and column headers for downstream interpretation and visualization.

## Related tools

- **chromVAR** (R package providing getAnnotationCorrelation and getAnnotationSynergy functions for quantifying annotation set relationships in sparse chromatin accessibility data) — https://github.com/GreenleafLab/chromVAR
- **SummarizedExperiment** (Data structure class for storing bias-corrected deviations assays and annotation metadata with subsetting and extraction methods)
- **Matrix** (R package for efficient sparse matrix representation and operations on large annotation-by-sample matrices)
- **motifmatchr** (Package used upstream to match JASPAR motifs to peaks, producing the motif_ix annotation matrix input) — https://github.com/GreenleafLab/motifmatchr

## Examples

```
# Load deviations and subset annotations
dev_subset <- dev[, c(motif_ix_cols, kmer_ix_cols)]
corr_matrix <- getAnnotationCorrelation(dev_subset[,motif_ix_cols], dev_subset[,kmer_ix_cols])
synergy_scores <- getAnnotationSynergy(dev_subset[,c(motif_ix_cols, kmer_ix_cols)])
write.csv(corr_matrix, 'annotation_correlations.csv')
write.csv(synergy_scores, 'annotation_synergy.csv')
```

## Evaluation signals

- Correlation matrix has symmetric structure with correlation values in [-1, 1] range and diagonal values equal to 1.0
- Synergy z-scores and p-values are present for all annotation pairs with consistent column headers (annotation pair name, z-score, p-value)
- Row and column names in correlation matrix match the annotation set names used in subsetting; CSV headers are preserved without corruption
- P-values are in [0, 1] range; z-scores follow expected standard normal distribution (mostly between -3 and +3 unless extreme synergy is present)
- Synergistic pairs (positive z-scores, low p-values) show lower pairwise correlations than redundant pairs, indicating distinct biological signals

## Limitations

- Synergy computation is sensitive to the random subsampling procedure for the null distribution; results may vary slightly between runs unless a seed is set
- The method assumes that peaks can be cleanly classified as containing or not containing each annotation; overlapping or ambiguous peak boundaries may inflate synergy scores
- Pairwise correlation is a linear metric and may miss non-linear or conditional relationships between annotation sets
- Large annotation sets (thousands of motifs or kmers) produce very large correlation matrices that are memory-intensive to export and interpret
- SnapATAC outperforms chromVAR for clustering tasks, so if the downstream goal is cell-type discovery rather than annotation characterization, alternative methods should be considered

## Evidence

- [other] getAnnotationCorrelation_and_synergy_quantify_relationships: "Apply getAnnotationCorrelation to compute pairwise Pearson correlations between the two annotation sets across all samples, outputting a correlation matrix with named rows and columns. Apply"
- [other] chromVAR_identifies_annotation_relationships: "chromVAR provides functions to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples, enabling analysis of annotation"
- [other] deviations_object_prerequisite: "Load the chromVARDeviations object containing precomputed bias-corrected deviations and z-scores for the annotation set."
- [readme] chromVAR_core_finding: "chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data. The package aims to identify motifs or other genomic annotations"
- [readme] JASPAR_motif_annotation_integration: "The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs"
