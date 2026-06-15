---
name: positional-distribution-profile-aggregation-and-visualization
description: Use when you have ATAC-seq BAM alignments with classified motif sites (bound vs. unbound based on chromatin accessibility or binding thresholds) and wish to detect and visualize the characteristic Tn5 insertion depletion signal (footprints) around transcription factor binding sites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3673
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS PlotAggregate
  - TOBIAS PlotHeatmap
  - TOBIAS BINDetect
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

# positional-distribution-profile-aggregation-and-visualization

## Summary

Aggregate and visualize Tn5 insertion counts across fixed-width genomic windows flanking regulatory sites (e.g., transcription factor binding motifs) to reveal characteristic footprint patterns—depletion of insertions at protein-bound sites versus uniform accessibility at unbound sites. This skill is essential for footprinting analysis in ATAC-seq to distinguish bound from unbound regulatory elements.

## When to use

Apply this skill when you have ATAC-seq BAM alignments with classified motif sites (bound vs. unbound based on chromatin accessibility or binding thresholds) and wish to detect and visualize the characteristic Tn5 insertion depletion signal (footprints) around transcription factor binding sites. Use it to validate that your binding site classification reflects genuine protein occupancy rather than sequence motif occurrence alone.

## When NOT to use

- Input BAM file has not been deduplicated or quality-filtered; raw, uncorrected ATAC-seq data with high technical bias will obscure genuine footprints.
- Motif site classification is based on sequence matching alone without chromatin accessibility or binding evidence; unanchored motif predictions do not reliably partition bound from unbound sites.
- Genomic windows are too narrow (< ±40 bp) to capture the full footprint width, or too wide (> ±200 bp) to resolve the depletion peak clearly.

## Inputs

- ATAC-seq BAM file with aligned Tn5 insertion reads (corrected for Tn5 bias if available)
- BED file of motif site coordinates classified as bound or unbound
- Reference genome (FASTA) if performing bias correction beforehand
- Peak coordinates (BED) defining open chromatin regions

## Outputs

- Tabular matrix of Tn5 insertion counts by genomic position and site class (bound/unbound)
- Aggregated insertion profile plots (line plots or heatmaps) for bound vs. unbound sites
- Positional statistics (mean, standard deviation) per window position and site class
- Footprint score or depletion depth metrics quantifying the signal difference

## How to apply

Extract Tn5 insertion positions from corrected ATAC-seq cutsites within fixed-width windows (e.g., ±100 bp) centered on each classified motif site. Aggregate insertion counts per position bin across all sites within each class (bound/unbound), computing positional statistics (mean, standard deviation) to reveal the distribution profile. Generate aggregated visualizations (line plots or heatmaps) overlaying bound and unbound site profiles side-by-side; the bound sites should exhibit a pronounced central depletion (footprint) flanked by peaks, while unbound sites show uniform accessibility. Compare the depth and width of depletion, and statistical significance of the difference between classes, to confirm the footprinting signal is genuine and not an artifact of sequence bias.

## Related tools

- **TOBIAS ATACorrect** (Corrects Tn5 insertion bias in ATAC-seq cutsites prior to aggregation, essential for accurate footprint signal detection) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculates footprint scores from corrected cutsites within regulatory regions, producing the normalized signal input for aggregation) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Generates aggregated ATAC-seq signal plots combining .bed and .bw files to visualize footprints across bound and unbound sites) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotHeatmap** (Produces heatmaps and aggregate plots of ATAC-seq signals to visualize footprints across multiple sites and conditions) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (Uses aggregated footprint scores to estimate differentially bound motifs based on positional signal profiles) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS PlotAggregate --signals corrected.bw --regions bound_motifs.bed unbound_motifs.bed --output footprint_aggregate.pdf --flank 100
```

## Evaluation signals

- Bound sites exhibit a statistically significant central depletion (reduction in mean insertion count) relative to flanking regions, absent in unbound sites.
- The footprint depletion width and depth are consistent with known TF binding site dimensions (typically 10–20 bp core depletion with ±5–10 bp flanking peaks).
- Aggregation includes sufficient site replicates (n > 50) to generate smooth, reproducible profiles; individual site noise is averaged out.
- Unbound motif sites show flat, uniform insertion profiles without central depletion, demonstrating that the bound/unbound classification is valid.
- Visualization clearly separates the two site classes by visual inspection; quantitative footprint scores (if computed) differ significantly between classes (e.g., t-test p < 0.05 or equivalent).

## Limitations

- Footprint signal quality depends critically on Tn5 bias correction; uncorrected or poorly corrected data will confound genuine protein occupancy with transposase sequence preference.
- Aggregation assumes that all motif sites of the same class share similar protein occupancy kinetics and chromatin context; heterogeneous binding dynamics or cell-type-specific occupancy will dampen the aggregated signal.
- Window size (±bp flanking) must be chosen to match the expected footprint width; windows that are too narrow miss flanking peaks, and too wide dilute the central depletion.
- Low coverage regions or sparse Tn5 insertions at specific sites introduce noise and reduce statistical power to detect footprints; depth filtering may be necessary.
- The skill does not inherently account for multi-motif sites or overlapping binding events; co-occupancy or competitive binding may alter insertion profiles in ways not explained by single-site classification.

## Evidence

- [other] Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites within each class (bound/unbound).: "Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites"
- [other] Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position. Tabulate results as a matrix of insertion counts by position and site class; generate visualization showing insertion profiles across bound and unbound sites to confirm footprint depletion signal in bound sites.: "Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position. Tabulate results as a matrix of insertion counts by position and site class; generate"
- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [readme] PlotAggregate: Plot aggregated ATAC-seq signals in combinations of .bed/.bw to visualize footprints: "PlotAggregate: Plot aggregated ATAC-seq signals in combinations of .bed/.bw to visualize footprints"
- [readme] ATAC-seq (Assay for Transposase-Accessible Chromatin using high-throughput sequencing) is a sequencing assay for investigating genome-wide chromatin accessibility. The assay applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin: "ATAC-seq (Assay for Transposase-Accessible Chromatin using high-throughput sequencing) is a sequencing assay for investigating genome-wide chromatin accessibility. The assay applies a Tn5 Transposase"
