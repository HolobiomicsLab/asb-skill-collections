---
name: transcription-factor-motif-matching
description: Use when you have corrected ATAC-seq footprint scores (from ATACorrect and ScoreBigwig) at open chromatin regions and a motif database (e.g., JASPAR PWMs), and you need to determine which TF motif matches are actually occupied across one or more experimental conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0239
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0654
  tools:
  - TOBIAS
  - TOBIAS BINDetect
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS FormatMotifs
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

# Transcription Factor Motif Matching

## Summary

Match position weight matrix (PWM) motifs to genomic sequences at footprint sites to identify putative transcription factor binding sites, then classify them as bound or unbound using footprint score intensity. This bridges sequence-level TF recognition with empirical occupancy signals from ATAC-seq.

## When to use

You have corrected ATAC-seq footprint scores (from ATACorrect and ScoreBigwig) at open chromatin regions and a motif database (e.g., JASPAR PWMs), and you need to determine which TF motif matches are actually occupied across one or more experimental conditions. Use this skill when you want to move from sequence homology to occupancy-based binding predictions.

## When NOT to use

- Input footprint scores are uncorrected or not derived from ATAC-seq Tn5 insertion patterns; use ATACorrect first.
- You only have raw ATAC-seq peaks without footprint score calculations; ScoreBigwig must precede BINDetect.
- Your motif database is not in JASPAR or TOBIAS-compatible PWM format; use FormatMotifs to convert first.

## Inputs

- Aligned ATAC-seq BAM file(s)
- Corrected footprint score bigWig file(s) from ATACorrect and ScoreBigwig
- Peak or region BED file(s) (open chromatin regions)
- Motif database file (JASPAR PWM or TOBIAS-compatible format)

## Outputs

- BINDetect output table with per-motif occupancy predictions
- Binding probability scores and differential occupancy metrics
- CSV/TSV table: TF motif ID, genomic coordinates, occupancy state, confidence scores, condition-specific binding metrics

## How to apply

Load aligned ATAC-seq BAM files and corresponding corrected footprint score bigWig files (output from prior TOBIAS preprocessing steps). Prepare or curate a motif database in TOBIAS-compatible format (e.g., JASPAR PWMs) containing the transcription factors of interest. Run TOBIAS BINDetect to scan the genome for motif matches and compare signal intensity (footprint depletion) at each motif site across experimental conditions, using the footprint scores to discriminate bound from unbound sites. BINDetect outputs a per-motif table with occupancy predictions, binding probabilities, and differential occupancy scores. Parse and format results as a structured table (CSV/TSV) with columns for TF motif ID, genomic coordinates, occupancy state (bound/unbound), confidence scores, and condition-specific binding metrics.

## Related tools

- **TOBIAS BINDetect** (Core tool that scans motif matches against footprint scores and estimates bound/unbound state and differential occupancy across conditions) — https://github.com/loosolab/TOBIAS/wiki/BINDetect
- **TOBIAS ATACorrect** (Prerequisite: corrects Tn5 insertion bias in ATAC-seq signal to prepare footprint scores for motif matching) — https://github.com/loosolab/TOBIAS/wiki/ATACorrect
- **TOBIAS ScoreBigwig** (Prerequisite: calculates footprint scores from corrected cutsites at regulatory regions) — https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig
- **TOBIAS FormatMotifs** (Utility to convert and standardize motif file formats before use with BINDetect) — https://github.com/loosolab/TOBIAS/wiki/FormatMotifs

## Examples

```
TOBIAS BINDetect --signals corrected.bw --peaks regions.bed --motifs jaspar_motifs.txt --outdir results
```

## Evaluation signals

- BINDetect output contains no null or malformed entries for TF motif ID, genomic coordinates, or occupancy scores.
- Binding probability scores fall within [0, 1] range; differential occupancy metrics reflect expected directionality (e.g., increased footprint depletion = increased occupancy).
- Results can be cross-validated by PlotAggregate or PlotHeatmap visualization: bound motif sites should show visible Tn5 insertion depletion (footprint) in aggregated signal.
- Occupancy predictions are consistent with condition-specific chromatin accessibility (e.g., bound TFs in accessible peaks).
- Motif match coordinates align with peak regions and do not extend substantially beyond input BED region boundaries.

## Limitations

- Quality and composition of the motif database strongly affect specificity; closely related TF motifs may be difficult to disambiguate without additional epigenetic context.
- BINDetect requires comparison across at least two conditions for reliable differential binding; single-sample analysis is less informative.
- TOBIAS was originally developed for bulk ATAC-seq; single-cell scATAC-seq requires aggregation into pseudobulk BAM files per cell type, and result quality depends on cell clustering quality and sequencing depth per cluster.
- Footprinting signal is only detectable at sufficiently high read depth; shallow ATAC-seq libraries may lack power to detect weak or transient TF binding.
- Motif matches near peak edges or in low-complexity sequence regions may yield unreliable occupancy predictions due to insufficient signal context.

## Evidence

- [other] TOBIAS BINDetect identifies bound and unbound TF sites through motif matching and footprint score comparison: "Run TOBIAS BINDetect with the footprint scores and motif matches as input, comparing signal intensity at motif sites across experimental conditions to discriminate bound from unbound sites."
- [readme] Footprints reveal TF occupancy via Tn5 insertion depletion patterns: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] BINDetect outputs occupancy predictions and condition-specific metrics per motif: "Parse BINDetect output table containing per-motif occupancy predictions, binding probabilities, and differential occupancy scores across conditions."
- [other] TOBIAS workflow prerequisites and dependencies: "Load aligned ATAC-seq BAM files and corresponding peak/footprint score files (output from prior TOBIAS preprocessing steps)."
- [other] Motif database requirement and format: "Prepare a motif database or use TOBIAS-compatible motif file (e.g., JASPAR-format PWMs) containing transcription factor motifs."
