---
name: differential-tf-occupancy-analysis
description: Use when you have aligned ATAC-seq BAM files and peak annotations from two or more experimental conditions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_0749
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS BINDetect
  - TOBIAS PlotAggregate
derived_from:
- doi: 10.1038/s41467-020-18035-1
  title: tobias
evidence_spans:
- '**TOBIAS** is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tobias
    doi: 10.1038/s41467-020-18035-1
    title: tobias
  dedup_kept_from: coll_tobias
schema_version: 0.2.0
---

# differential-tf-occupancy-analysis

## Summary

Identify transcription factors with significantly altered binding occupancy between two ATAC-seq conditions by correcting for Tn5 insertion bias, computing footprint enrichment scores, and performing differential binding detection at known transcription factor binding sites (TFBS). This skill leverages the visible depletion of Tn5 insertions around protein-bound sites (footprints) to quantify condition-specific changes in TF occupancy.

## When to use

You have aligned ATAC-seq BAM files and peak annotations from two or more experimental conditions (e.g., treated vs. control, different timepoints, or different cell states) and want to discover which transcription factors show statistically significant changes in chromatin binding occupancy between those conditions, not just differences in open chromatin accessibility.

## When NOT to use

- Input is single-condition ATAC-seq data with no biological replicate or comparison group — differential analysis requires at least two conditions.
- The ATAC-seq peaks were generated from single-cell clusters without adequate pseudobulk aggregation; TOBIAS requires sufficient sequencing depth per condition to detect footprints reliably.
- You are interested only in differences in open chromatin peaks, not in transcription factor binding occupancy; standard peak-calling and differential accessibility tools (e.g., DESeq2 on peak counts) are more appropriate.

## Inputs

- BAM files (aligned ATAC-seq reads, one per condition)
- Peak annotations in BED format (open chromatin regions)
- Reference genome FASTA file
- Motif database (JASPAR, HOCOMOCO, or similar format supported by TOBIAS)

## Outputs

- Uncorrected and bias-corrected BigWig files (.bw) of Tn5 insertion signal per condition
- Footprint score BigWig files (.bw) per condition
- BINDetect differential occupancy results table (.tsv) with TF names, footprint scores, fold-changes, and statistical significance metrics (p-values, adjusted p-values)
- PDF or PNG summary visualizations showing top differential TFs and representative footprint patterns

## How to apply

First, run TOBIAS ATACorrect on each condition's BAM file to remove Tn5 transposase sequence preference bias, generating corrected insertion bias signals. Then apply TOBIAS ScoreBigwig (or FootprintScores) to compute footprint enrichment scores genome-wide for each condition, which quantifies the characteristic depletion of Tn5 insertions at bound sites. Finally, run TOBIAS BINDetect using the corrected footprint scores and a motif database to estimate bound vs. unbound status at all known TFBS motif occurrences, comparing the two conditions to identify transcription factors with significant changes in occupancy. BINDetect outputs differential occupancy statistics (e.g., p-values, fold-changes) for each TF, which can be filtered and visualized to highlight the most dramatically changing factors.

## Related tools

- **TOBIAS ATACorrect** (Corrects Tn5 insertion bias in ATAC-seq BAM files to remove sequence preference artifacts that mask true footprint signals) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculates footprint scores from corrected cutsites to quantify transcription factor binding signals genome-wide) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (Estimates bound/unbound status of transcription factor binding sites and compares occupancy between conditions to identify differentially bound motifs) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Visualizes aggregated footprint patterns and condition-specific occupancy changes at representative TFBS) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS ATACorrect --bam condition1.bam --genome genome.fa --peaks peaks.bed --outdir atac_corrected --prefix cond1 && TOBIAS ScoreBigwig --signal atac_corrected/cond1_corrected.bw --regions peaks.bed --output cond1_footprints.bw && TOBIAS BINDetect --signals cond1_footprints.bw cond2_footprints.bw --motifs motifs.meme --peaks peaks.bed --outdir bindetect_results
```

## Evaluation signals

- Corrected BigWig files show expected footprint signals (depletion of insertions at protein-bound sites) distinct from uncorrected bias signals in visual inspection (ATACorrect PDF output).
- Footprint score distributions are statistically distinct between conditions (e.g., Kolmogorov–Smirnov test or visual comparison of score histograms per condition).
- BINDetect results include valid statistical metrics (p-values and adjusted p-values are well-calibrated; histogram of p-values shows enrichment at low values for true differential TFs).
- Top differential TFs identified by BINDetect show consistent directionality in fold-changes and align with known biology of the compared conditions (e.g., expected developmental regulators are upregulated in later timepoints).
- Representative footprint visualizations (PlotAggregate or PlotTracks) clearly show condition-specific differences in Tn5 insertion depletion at top differential TFBS.

## Limitations

- TOBIAS footprinting requires high sequencing depth (~50M+ reads per condition) to reliably detect footprints; shallow ATAC-seq libraries may yield noisy or undetectable signals.
- The accuracy of differential occupancy depends on the quality and completeness of the input motif database; missing or incorrectly annotated motifs will not be detected.
- TOBIAS was originally developed for bulk ATAC-seq; application to single-cell data requires generating pseudobulk BAM files from cell clusters, and the quality depends critically on cell clustering and per-cell sequencing depth (see SC-Framework recommendation in README).
- Differential occupancy is inferred from footprint score changes at motif sites, not direct measurement of TF binding; results should be validated with orthogonal techniques (e.g., ChIP-seq, electrophoretic mobility shift assay) when possible.

## Evidence

- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [readme] TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data: "TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data"
- [readme] Correction of Tn5 insertion bias, Calculation of footprint scores within regulatory regions, Estimation of bound/unbound transcription factor binding sites: "Correction of Tn5 insertion bias; Calculation of footprint scores within regulatory regions; Estimation of bound/unbound transcription factor binding sites"
- [other] ATAC-seq footprinting analysis can detect transcription factor binding through the visible depletion of Tn5 insertions around protein-bound sites, providing a basis for differential occupancy analysis across conditions: "ATAC-seq footprinting analysis can detect transcription factor binding through the visible depletion of Tn5 insertions around protein-bound sites, providing a basis for differential occupancy"
- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase"
