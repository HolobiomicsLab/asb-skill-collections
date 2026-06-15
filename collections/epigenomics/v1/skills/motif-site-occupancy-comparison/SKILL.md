---
name: motif-site-occupancy-comparison
description: Use when you have bias-corrected ATAC-seq footprint signals (BigWig files) from two or more distinct conditions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0438
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0204
  tools:
  - TOBIAS
  - TOBIAS BINDetect
  - TOBIAS ScoreBigwig
  - TOBIAS PlotAggregate
  - TOBIAS ATACorrect
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

# motif-site-occupancy-comparison

## Summary

Compare transcription factor occupancy at known motif binding sites across two or more ATAC-seq conditions by applying footprint scoring and differential binding detection. This skill detects which transcription factors show altered chromatin occupancy between conditions by leveraging the visible depletion of Tn5 insertions around protein-bound sites.

## When to use

You have bias-corrected ATAC-seq footprint signals (BigWig files) from two or more distinct conditions (e.g., different developmental stages, treatment vs. control) and a catalog of known transcription factor binding site motifs (in JASPAR, TRANSFAC, or similar format), and you want to identify which TFs show statistically significant changes in occupancy/binding intensity between conditions.

## When NOT to use

- Input ATAC-seq data has not been corrected for Tn5 insertion bias; run ATACorrect first.
- You lack motif annotations or a reference TF binding site catalog; differential occupancy analysis requires known binding site locations.
- Your experiment has only a single condition or replicates that cannot be grouped; comparison requires at least two distinct biological conditions.

## Inputs

- Bias-corrected ATAC-seq BigWig files (.bw) for each condition
- Peak region annotation (.bed file, typically from MACS2 or similar)
- Transcription factor motif catalog (.txt, .jaspar, or .pwm format)
- Reference genome sequence (.fa or .2bit)

## Outputs

- Differential TF occupancy results table (.tsv) with TF names, footprint scores per condition, fold-changes, and p-values
- Visualization of top differential TFs showing occupancy changes and representative footprint patterns (.pdf or .png)
- BINDetect binding site predictions (.bed) with occupancy estimates per condition

## How to apply

First, compute genome-wide footprint enrichment scores for each condition using the bias-corrected ATAC-seq signal and a set of reference motifs. Then apply differential binding detection (BINDetect) which compares footprint patterns at annotated TFBS motif sites between conditions, accounting for both footprint score changes and underlying sequence context. BINDetect produces a ranked list of TFs with differential occupancy estimates and p-values. Filter results by statistical significance (typically p < 0.05) and effect size thresholds to identify high-confidence differential TF occupancy events. Validate findings by visual inspection of aggregated footprint patterns and representative genomic tracks around top-ranking differential TF sites.

## Related tools

- **TOBIAS BINDetect** (Core tool for differential transcription factor occupancy estimation; compares footprint patterns at known TFBS motif sites between conditions and outputs statistical significance metrics) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculates per-base footprint enrichment scores from bias-corrected ATAC-seq cutsites; required input signal for BINDetect) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Aggregates and visualizes ATAC-seq footprint signals across motif sites to validate differential occupancy findings) — https://github.com/loosolab/TOBIAS
- **TOBIAS ATACorrect** (Prerequisite step; corrects ATAC-seq cutsites for Tn5 insertion sequence bias before footprint scoring) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS BINDetect --signals condition1_corrected.bw condition2_corrected.bw --names Condition1 Condition2 --motifs transcription_factors.jaspar --peaks peaks.bed --outdir bindetect_results
```

## Evaluation signals

- BINDetect output table contains non-zero differential occupancy estimates and valid p-values (0 < p ≤ 1) for all tested TFs
- Top-ranked differential TFs show visually distinct footprint depth changes in aggregated ATAC-seq signal plots between conditions (PlotAggregate output)
- Effect size and statistical significance are concordant: TFs with large occupancy changes have correspondingly low p-values
- Replicate consistency: if multiple replicates per condition exist, differential occupancy calls are reproducible across independent replicates
- Motif sites at differential TF regions show expected Tn5 insertion depletion pattern in raw ATAC-seq signal aligned to the motif consensus

## Limitations

- Footprinting resolution is limited to ~50–200 bp feature size; weak or transient TF binding may not produce detectable footprints. Quality depends critically on sequencing depth and sample preparation.
- BINDetect assumes known motif annotations; novel or condition-specific binding sites not represented in the motif database will be missed. Motif quality and specificity directly affect occupancy predictions.
- Single-cell ATAC-seq data requires aggregation into pseudobulk BAM files by cell type or cluster; clean footprints depend on homogeneous cell populations and adequate sequencing coverage per pseudobulk sample.
- Differential occupancy inference is statistical in nature; biological validation (e.g., ChIP-seq, reporter assays) is recommended for top-ranking candidates.

## Evidence

- [other] ATAC-seq footprinting analysis can detect transcription factor binding through visible depletion of Tn5 insertions around protein-bound sites: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] BINDetect compares footprint patterns at known TFBS motif sites between conditions: "BINDetect: Estimation of differentially bound motifs based on scores, sequence and motifs"
- [other] Footprint scoring computes genome-wide enrichment from bias-corrected ATAC-seq signal: "ScoreBigwig: Calculate footprint scores from corrected cutsites"
- [other] Bias correction of Tn5 insertions is prerequisite for occupancy analysis: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase"
- [other] Visualization is used to validate differential occupancy findings: "Visualization of footprints within and across different conditions"
