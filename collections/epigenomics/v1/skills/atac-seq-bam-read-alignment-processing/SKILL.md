---
name: atac-seq-bam-read-alignment-processing
description: Use when when you have aligned ATAC-seq BAM files and need to quantify Tn5 transposase insertion patterns around specific genomic coordinates (motif sites, peaks, regulatory regions) to detect transcription factor occupancy footprints or compare chromatin accessibility between bound and unbound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0654
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS PlotAggregate
  - TOBIAS PlotHeatmap
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

# atac-seq-bam-read-alignment-processing

## Summary

Extract and aggregate Tn5 insertion positions from aligned ATAC-seq BAM files within fixed-width windows around genomic features (e.g., transcription factor binding motifs) to enable footprint detection and chromatin accessibility analysis. This processing step bridges raw sequencing alignments to footprinting signal by computing positional distributions of insertion events.

## When to use

When you have aligned ATAC-seq BAM files and need to quantify Tn5 transposase insertion patterns around specific genomic coordinates (motif sites, peaks, regulatory regions) to detect transcription factor occupancy footprints or compare chromatin accessibility between bound and unbound sites. Apply this skill after read alignment but before footprint scoring or differential binding analysis.

## When NOT to use

- Input BAM file is not properly coordinate-sorted or lacks proper pair information—preprocessing alignment files is a prerequisite, not a use of this skill.
- Target coordinates are undefined or lack biological annotation; this skill requires specific genomic intervals (motifs, peaks, etc.), not unstructured genomic regions.
- The analysis goal is to detect novel accessible regions genome-wide rather than footprinting at known or predicted binding sites; use peak calling instead.

## Inputs

- Aligned ATAC-seq BAM file (coordinate-sorted, with read pairs)
- Genomic coordinates in BED format (transcription factor motif sites, peaks, or other regulatory regions)
- Classification/annotation of sites as bound or unbound (thresholded by accessibility signal or binding confidence)

## Outputs

- Insertion count matrix (positions × site class)
- Positional distribution statistics (mean, standard deviation per position per class)
- Aggregate insertion profile plot or heatmap visualization showing footprint depletion at bound sites
- Corrected or raw insertion bigWig files (optional, for downstream visualization)

## How to apply

Load the ATAC-seq BAM file and define fixed-width flanking windows (e.g., ±100 bp) around target genomic coordinates such as transcription factor motif sites. Extract the Tn5 insertion positions from properly paired and aligned reads in the BAM file—typically using the 5′ end of the forward read as the cut site to represent the point of transposase insertion. Bin insertions by their genomic position relative to the window center and aggregate insertion counts per position bin across all sites within each class (e.g., bound vs. unbound based on chromatin accessibility thresholds). Compute positional distribution statistics (mean, standard deviation) for each window position and class. Output results as a matrix of insertion counts indexed by position and site class, and generate visualizations (aggregate plots or heatmaps) showing the insertion profile—depleted signal at bound sites indicates successful footprint detection.

## Related tools

- **TOBIAS ATACorrect** (Corrects Tn5 insertion bias in cut-site signal before position aggregation to improve footprint detection accuracy) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculates footprint scores from corrected cutsite signals within windows after insertion position aggregation) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Visualizes aggregated Tn5 insertion profiles across bound and unbound sites to confirm footprint depletion signal) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotHeatmap** (Generates heatmaps of aggregated insertion counts across sites and conditions for footprint visualization) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS PlotAggregate --signal corrected.bw --regions bound_motifs.bed --output bound_footprint.pdf && TOBIAS PlotAggregate --signal corrected.bw --regions unbound_motifs.bed --output unbound_footprint.pdf
```

## Evaluation signals

- Aggregated insertion count profiles for bound sites exhibit visible depletion (reduced counts) at the central motif region (±20–50 bp from site center) compared to flanking regions, indicating successful footprint detection.
- Unbound or non-binding sites show relatively flat or uniform insertion distributions across the window without central depletion, confirming class separation.
- Insertion count matrix is properly indexed by genomic position and site class; no missing or malformed bins.
- Visualization output (aggregate plot or heatmap) is interpretable and shows clear distinction between bound and unbound insertion profiles; footprint feature is visually evident.
- Position-by-position statistics (mean ± SD) are computed consistently across all sites within each class; variance is reasonable (not zero or undefined).

## Limitations

- Quality of footprint signal depends critically on the classification (bound vs. unbound) threshold used; misclassified sites will degrade the aggregate signal.
- Tn5 transposase exhibits sequence-dependent insertion bias; raw insertion counts may not reflect true chromatin accessibility without prior bias correction (e.g., via TOBIAS ATACorrect).
- Single-cell ATAC-seq data requires aggregation into pseudobulk BAM files by cell type or cluster before this skill can be applied effectively; cell quality and clustering fidelity are critical prerequisites.
- Very weak or shallow footprints may not be visually apparent or statistically significant in aggregates from small numbers of binding sites or low-coverage data.
- Fixed window size (e.g., ±100 bp) is a design choice that must be justified biologically; windows that are too large may obscure footprint structure, while windows that are too small may undersample the depletion signal.

## Evidence

- [other] Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites within each class (bound/unbound). Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position.: "Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites"
- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [readme] ATAC-seq applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome: "ATAC-seq applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome"
- [readme] Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters.: "Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from"
- [other] Tabulate results as a matrix of insertion counts by position and site class; generate visualization showing insertion profiles across bound and unbound sites to confirm footprint depletion signal in bound sites.: "Tabulate results as a matrix of insertion counts by position and site class; generate visualization showing insertion profiles across bound and unbound sites to confirm footprint depletion signal in"
