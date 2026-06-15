---
name: genome-sequence-matching-for-nucleotide-patterns
description: Use when you have filtered peak or chromatin accessibility counts and need to annotate each peak with the presence or absence of specific DNA sequence patterns—either predefined motifs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0346
  edam_topics:
  - http://edamontology.org/topic_0157
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
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

# Genome-sequence matching for nucleotide patterns

## Summary

Match short nucleotide sequences (kmers or transcription factor motifs) to a reference genome to generate binary annotation matrices for downstream chromatin accessibility analysis. This skill converts genomic annotations into features suitable for deviation and variability computation in sparse ATAC-seq data.

## When to use

You have filtered peak or chromatin accessibility counts and need to annotate each peak with the presence or absence of specific DNA sequence patterns—either predefined motifs (e.g., JASPAR transcription factor motifs) or kmers of a chosen length (6, 7, or higher)—to test whether particular sequences are associated with chromatin accessibility variability across cells or samples.

## When NOT to use

- Peak coordinates are not already defined or filtered; use filterPeaks and peak-calling workflows first.
- You are performing de novo motif discovery rather than matching known motifs/kmers to peaks.
- Your input is RNA-seq or gene expression data rather than ATAC/DNAse-seq counts; chromatin accessibility annotation is not applicable.
- You already have precomputed deviation scores or a finalized feature table and do not need to re-annotate peaks.

## Inputs

- Filtered chromatin accessibility counts object (SummarizedExperiment with peaks × samples/cells matrix)
- Reference genome (BSgenome object, e.g., BSgenome.Hsapiens.UCSC.hg19)
- Motif collection (PWM list or GRanges, e.g., from getJasparMotifs) OR kmer length integer (6, 7, etc.)

## Outputs

- Binary annotation matrix (features × peaks): rows are kmers or motifs, columns are peaks, values are 0/1
- Motif index or kmer index object (passed to computeDeviations for deviation scoring)

## How to apply

Load a reference genome (e.g., BSgenome.Hsapiens.UCSC.hg19) and your filtered peak/counts object. For motif matching, retrieve motifs from a database (e.g., JASPAR using getJasparMotifs) and apply matchMotifs from the motifmatchr package to identify which peaks contain which motifs, producing a binary matrix. Alternatively, for kmer-based annotation, call matchKmers with your desired kmer length (e.g., 6 or 7) on the counts object and genome, which returns a kmer annotation index. The resulting matrix rows correspond to kmers/motifs and columns correspond to peaks; entries are 1 if the pattern is present, 0 otherwise. This annotation matrix is then passed to computeDeviations to compute per-sample/cell deviation scores relative to the overall kmer/motif frequency.

## Related tools

- **motifmatchr** (Matches JASPAR or user-supplied transcription factor motifs (as position weight matrices) to peaks in the filtered counts object using matchMotifs function.) — https://github.com/GreenleafLab/motifmatchr
- **chromVAR** (Wraps kmer and motif matching workflow; provides matchKmers and computeDeviations functions to generate and score annotation matrices.) — https://github.com/GreenleafLab/chromVAR
- **BSgenome.Hsapiens.UCSC.hg19** (Provides the hg19 reference genome sequence required by matchKmers and matchMotifs to scan peaks for nucleotide patterns.)
- **SummarizedExperiment** (Data structure holding filtered peak counts and their annotations; required input and output container.)

## Examples

```
matchKmers(6, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19); dev <- computeDeviations(object=counts_filtered, annotations=kmer_ix_6mer)
```

## Evaluation signals

- Annotation matrix dimensions: rows = number of kmers (4^k for k-mers) or motifs; columns = number of peaks; verify no missing or unexpected row/column counts.
- Sparsity and coverage: at least some peaks should match at least one kmer/motif (non-zero columns); all-zero rows may indicate a kmer/motif never present in the peak set (expected for rare patterns).
- Binary encoding: all matrix entries are 0 or 1; no negative values, NaN, or floating-point artifacts.
- Downstream computeDeviations execution: annotation matrix should be compatible with computeDeviations(counts_filtered, annotation_matrix); if dimensions or format are wrong, a clear error message will result.
- Kmer size effect on variability: when comparing 6-mer vs. 7-mer annotations on the same counts, 7-mers should yield higher mean/median variability scores, consistent with the finding that longer kmers provide finer granularity and higher sample-to-sample variation.

## Limitations

- Kmer matching is computationally expensive for very large genomes or very long kmers; consider serial execution (SerialParam) or disk-based backends for large-scale analyses.
- Motif matching quality depends on PWM accuracy and scoring thresholds; JASPAR motifs are curated but may not capture all functional variants of a transcription factor binding site.
- Rare or long kmers (e.g., 8-mers or longer) may have limited coverage across the peak set, resulting in many zero-count rows in the annotation matrix and reduced statistical power.
- The method assumes peaks are non-overlapping and correctly defined; overlapping peaks from unfiltered data may lead to ambiguous or double-counted matches.
- SnapATAC outperforms chromVAR for clustering tasks; use this skill for motif/kmer annotation and variability discovery, not as the primary method for cell clustering.

## Evidence

- [other] Generate 6-mer kmer annotation matrix using matchKmers: "Generate 6-mer kmer annotation matrix using matchKmers(6, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19)"
- [other] motifmatchr finds which peaks contain which motifs: "The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs"
- [other] chromVAR identifies motifs associated with variability: "chromVAR is an R package for the analysis of sparse chromatin accessibility data from single cell or bulk ATAC or DNAse-seq data. The package aims to identify motifs or other genomic annotations"
- [other] Kmers plus PCA variant for clustering: "Using kmers + PCA appears to be the best variant of chromVAR for clustering"
- [other] 7-mers yield higher variability than 6-mers: "extract and tabulate mean, median, and standard deviation of variability scores for both kmer sets, then compare distributions to confirm 7-mers yield higher variability than 6-mers"
