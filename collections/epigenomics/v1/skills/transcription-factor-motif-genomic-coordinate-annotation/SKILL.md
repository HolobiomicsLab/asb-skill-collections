---
name: transcription-factor-motif-genomic-coordinate-annotation
description: Use when you have ATAC-seq BAM files and want to detect transcription factor footprints—characteristic depletion patterns of Tn5 insertions around protein-bound motif sites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0445
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3169
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS BINDetect
  - TOBIAS PlotAggregate
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

# Transcription Factor Motif Genomic Coordinate Annotation

## Summary

Assign genomic coordinates to transcription factor binding motifs using public sequence databases and classify them as bound or unbound based on chromatin accessibility thresholds. This enables stratified analysis of ATAC-seq footprints to distinguish protein-occupied from unoccupied regulatory sites.

## When to use

You have ATAC-seq BAM files and want to detect transcription factor footprints—characteristic depletion patterns of Tn5 insertions around protein-bound motif sites. Motif annotation is the prerequisite step: you must first locate candidate TF binding sites genome-wide, then classify them by binding status, before aggregating insertion counts per position to visualize footprints.

## When NOT to use

- Your ATAC-seq data lacks sufficient read depth or contains poor-quality chromatin accessibility signal—footprints will be obscured and bound/unbound classification unreliable.
- You are analyzing a species or locus without well-characterized TF motif models, or your motif database is known to be incomplete or context-inappropriate.
- Input is already a pre-computed feature table of TF binding events (e.g., ChIP-seq peaks, DNase footprints from another method); use motif annotation only to enrich or validate existing predictions, not to generate them de novo.

## Inputs

- ATAC-seq aligned reads (BAM file)
- Transcription factor motif models (PWM format; e.g., JASPAR or custom database)
- Reference genome FASTA
- Peak or accessibility annotations (BED or BigWig)
- Motif scanning results with genomic coordinates (BED-like)

## Outputs

- Annotated motif sites with genomic coordinates (BED file with bound/unbound classification)
- Position-stratified Tn5 insertion count matrix (bound vs. unbound, by position relative to motif center)
- Footprint visualizations (aggregated insertion profiles per site class)
- Footprint scores (per motif or per site, from TOBIAS ScoreBigwig or BINDetect)

## How to apply

Download or curate a set of transcription factor motif models (position weight matrices) and scan the reference genome to identify all occurrences of each motif, recording genomic start/end coordinates and strand. Overlay motif locations onto ATAC-seq accessibility data (e.g., peak calls, read depth, or footprint scores from TOBIAS ATACorrect output) and apply a signal threshold (e.g., minimum cutsite signal or peak overlap) to classify motif sites as bound or unbound. Extract Tn5 insertion coordinates from aligned BAM files in fixed-width flanking windows (e.g., ±100 bp around motif center) for each class separately. Aggregate insertion counts per genomic position bin across all sites within each class to generate position-specific insertion distributions. Compare insertion profiles: bound sites should show a characteristic central depletion (footprint), while unbound sites exhibit relatively uniform insertion density. Use TOBIAS tools (ATACorrect for bias correction, ScoreBigwig for footprint scoring, BINDetect for bound/unbound estimation) to formalize this classification and scoring.

## Related tools

- **TOBIAS ATACorrect** (Corrects Tn5 insertion bias in ATAC-seq cutsite signal to enable accurate footprint detection at bound vs. unbound motif sites) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculates footprint scores from bias-corrected cutsites, quantifying depletion signal to classify motif sites) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (Estimates bound/unbound transcription factor binding sites based on footprint scores, sequence, and motif models) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Visualizes aggregated ATAC-seq insertion profiles across bound and unbound motif sites to confirm footprint depletion pattern) — https://github.com/loosolab/TOBIAS
- **TOBIAS FormatMotifs** (Converts and harmonizes motif file formats (e.g., JASPAR, MEME) for use in motif scanning and footprint analysis) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS BINDetect --motifs motifs.txt --signals sample_corrected.bw --peaks regions.bed --outdir results/ --genome genome.fa
```

## Evaluation signals

- Motif coordinates are reproducible and consistent with reference genome builds; spot-check a random sample of annotated sites in IGV or a genome browser against sequence homology.
- Bound motif sites exhibit a statistically significant central depletion in Tn5 insertion density compared to flanking regions; unbound sites show flat or random insertion distributions. Quantify this by computing footprint score or insertion fold-change at the motif center.
- Classification into bound/unbound classes is concordant with peak-based or signal-based thresholds: high-accessibility or high-score sites should predominantly be annotated as bound; low or non-overlapping sites as unbound.
- Aggregated insertion profiles (position-wise counts across all bound or unbound sites) are smooth and reproducible when subsampled; noisy or bimodal profiles suggest insufficient motif multiplicity or confounding co-factors.
- Footprint visualization (PlotAggregate or PlotHeatmap output) shows clear separation between bound and unbound site profiles; bound sites should have a characteristic U-shape or V-shaped depletion trough in the center.

## Limitations

- Footprint signal is weak or absent when Tn5 insertion bias has not been corrected; ATACorrect must be applied before reliable bound/unbound classification.
- Motif scanning sensitivity depends critically on PWM quality and chosen p-value or score threshold; incomplete or condition-inappropriate motif databases will miss true sites or inflate false positives.
- Single-cell ATAC-seq requires pseudobulking by cell type or cluster before footprinting analysis; quality of cell clustering and cell filtering directly impact footprint clarity and bound/unbound separability.
- TF binding footprints are context-dependent; a motif may be bound in one condition and unbound in another, so classification must be done per-condition with appropriate signal thresholds.
- Footprints are most reliable in open chromatin regions (peaks) and may be undetectable in closed chromatin; classification of low-accessibility motif sites as unbound can conflate inaccessibility with lack of TF binding.

## Evidence

- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] Classify motif sites as bound or unbound based on chromatin accessibility or binding signal thresholds.: "Classify motif sites as bound or unbound based on chromatin accessibility or binding signal thresholds"
- [other] Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center).: "Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center)"
- [other] Aggregate insertion counts per position bin across all sites within each class (bound/unbound).: "Aggregate insertion counts per position bin across all sites within each class (bound/unbound)"
- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase.: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase"
- [readme] Estimation of bound/unbound transcription factor binding sites: "Estimation of bound/unbound transcription factor binding sites"
