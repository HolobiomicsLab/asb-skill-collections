---
name: transcription-factor-footprint-scoring
description: Use when after bias-corrected ATAC-seq signal tracks (bigWig files) have been generated and you need to quantify transcription factor binding strength within open chromatin regions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3169
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

# transcription-factor-footprint-scoring

## Summary

Compute genome-wide footprint enrichment scores from bias-corrected ATAC-seq signal to quantify transcription factor occupancy at regulatory sites. This skill detects the characteristic depletion of Tn5 insertions around protein-bound DNA regions and enables comparative analysis of TF binding across experimental conditions.

## When to use

Apply this skill after bias-corrected ATAC-seq signal tracks (bigWig files) have been generated and you need to quantify transcription factor binding strength within open chromatin regions. Use it when you have peak annotations or known transcription factor binding site (TFBS) motif coordinates and want to measure footprint enrichment across conditions for differential occupancy analysis.

## When NOT to use

- Raw ATAC-seq BAM files have not yet been corrected for Tn5 insertion bias—use ATACorrect first.
- Input is already a pre-computed feature table or motif count matrix; footprint scoring requires raw bias-corrected signal.
- Experimental design lacks a suitable control or comparison condition; differential scoring requires at least two distinct conditions.

## Inputs

- bias-corrected bigWig files (from TOBIAS ATACorrect)
- peak BED file (accessible chromatin regions)
- reference genome FASTA (optional, for motif annotation)
- transcription factor motif file (for BINDetect; standard PWM formats)

## Outputs

- footprint score BED or bigWig file (per-region enrichment values)
- differential transcription factor occupancy table (.tsv; TF names, footprint scores, p-values)
- summary visualization (.pdf or .png; top differential TFs, occupancy changes, representative footprint patterns)

## How to apply

Run TOBIAS ScoreBigwig on bias-corrected bigWig files (output from ATACorrect) with peak BED annotations to calculate footprint enrichment scores genome-wide. The tool computes per-site footprint signal by measuring the relative depletion of Tn5 insertions at each peak, capturing the characteristic pattern of protein-bound regions. For differential analysis, generate footprint scores independently for each experimental condition, then apply TOBIAS BINDetect to compare scores at motif-annotated TFBS sites between conditions, producing a ranked table of transcription factors with statistical significance metrics for differential occupancy.

## Related tools

- **TOBIAS ATACorrect** (upstream step: corrects Tn5 insertion bias in ATAC-seq BAM files to produce clean signal tracks required for footprint scoring) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (core tool: calculates per-region footprint enrichment scores from corrected bigWig signal and peak annotations) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (downstream step: performs differential transcription factor occupancy analysis by comparing footprint scores at motif sites between conditions) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (visualization: generates aggregated footprint plots across sets of TFBS to validate occupancy patterns) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS ScoreBigwig --signal condition1_corrected.bw --peaks peaks.bed --output condition1_footprints.bed && TOBIAS BINDetect --signals condition1_footprints.bed condition2_footprints.bed --peaks peaks.bed --motifs motifs.bed --outdir bindetect_results
```

## Evaluation signals

- Footprint score bigWig files contain numeric values (enrichment signals) in expected range for the sequencing depth and peak sizes; median footprint score should be positive across regulatory regions.
- Differential occupancy table includes all input transcription factors with non-null footprint scores, p-values, and fold-change (occupancy difference) for both conditions; table is sorted by statistical significance.
- Summary visualization shows clear separation of top differential TFs between conditions; representative footprint plots display visible Tn5 insertion depletion (negative signal) flanking known TFBS motifs in high-occupancy samples.
- Consistency check: footprint scores at strong TFBS (high motif match scores) should be higher than at weak or non-motif regions within the same peak set; condition-specific differences align with known biology or experimental design.
- No missing or zero scores for peaks that pass quality thresholds; output file format matches TOBIAS specifications (BED/TSV with correct column order and metadata).

## Limitations

- Footprint quality depends critically on sequencing depth and read quality; shallow ATAC-seq libraries may show weak or noisy footprint signals, reducing power to detect differential occupancy.
- Tn5 insertion bias correction assumes the bias model learned from the input BAM file is representative; severe batch effects or library-specific biases may not be fully corrected.
- Footprint scoring assumes protein-bound sites produce characteristic insertion depletion; other chromatin features (e.g., nucleosome positioning, DNA structure) can mimic or obscure footprints, confounding TF binding inference.
- Single-cell ATAC-seq data requires pseudobulk aggregation by cell type/condition prior to footprinting; quality of footprinting analysis depends on cell clustering and sufficient per-cluster coverage (README notes this is 'paramount').
- BINDetect differential analysis relies on accurate motif annotations; incomplete or incorrect motif databases will miss true differential TFs or rank false positives.

## Evidence

- [readme] ATAC-seq footprinting detects TF binding via insertion depletion: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [readme] ScoreBigwig calculates footprint scores from corrected signal: "[ScoreBigwig]: Calculate footprint scores from corrected cutsites"
- [readme] BINDetect estimates differential TF binding from footprint scores and motifs: "[BINDetect]: Estimation of differentially bound motifs based on scores, sequence and motifs"
- [other] Workflow applies footprinting to detect differential TF occupancy across conditions: "Execute TOBIAS FootprintScores to compute footprint enrichment signals genome-wide for each condition. 4. Apply TOBIAS BINDetect to perform differential transcription factor occupancy analysis"
- [other] Output includes differential TF table with statistical metrics and visualization: "Generate differential TF occupancy results table (.tsv) containing TF names, footprint scores, and statistical significance metrics. 6. Create summary visualization (.pdf or .png) showing top"
