---
name: tn5-insertion-position-extraction-and-counting
description: Use when you have ATAC-seq BAM files and a set of genomic coordinates (e.g., transcription factor motif sites, peak regions) and need to quantify the spatial distribution of Tn5 cleavage events relative to those coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0204
  - http://edamontology.org/topic_3674
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS PlotAggregate
  - SAMtools
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

# Tn5 insertion position extraction and counting

## Summary

Extract precise Tn5 transposase insertion coordinates from aligned ATAC-seq BAM files and aggregate insertion counts across fixed-width genomic windows to quantify local cleavage patterns. This skill enables detection of transcription factor footprints—characteristic depletion signatures of Tn5 insertions around protein-bound sites—by generating positional insertion matrices for downstream footprint analysis.

## When to use

Apply this skill when you have ATAC-seq BAM files and a set of genomic coordinates (e.g., transcription factor motif sites, peak regions) and need to quantify the spatial distribution of Tn5 cleavage events relative to those coordinates. Essential for footprinting workflows where distinguishing bound from unbound transcription factor binding sites requires evidence of insertion depletion patterns around protein-occupied regions.

## When NOT to use

- Input is single-cell ATAC-seq without pseudobulk aggregation; raw single-cell resolution lacks sufficient signal depth for reliable footprint detection without cell clustering and aggregation.
- Genomic coordinates lack classification (bound vs. unbound status); insertion patterns cannot be compared meaningfully if all sites are treated identically or lack differential binding evidence.
- BAM file is not position-sorted or lacks proper read group headers; coordinate extraction and windowing depend on reliable read alignment and indexing.

## Inputs

- ATAC-seq BAM file (aligned reads with Tn5 cutsite information)
- Genomic coordinate BED file (transcription factor binding motifs, peaks, or regions of interest)
- Site classification labels (bound/unbound status, or condition grouping) — optional but recommended
- Fixed-width window size definition (e.g., ±100 bp around center coordinate)

## Outputs

- Position-by-insertion-count matrix (rows = genomic positions within window, columns = insertion count aggregates per site class)
- Aggregated insertion profiles (mean and SD of insertions per position bin for each site class)
- Visualization of positional insertion distributions (line plots or heatmaps contrasting bound vs. unbound sites)

## How to apply

Extract the 5' end coordinates of aligned reads in the BAM file (representing Tn5 cutsite positions) and bin them into fixed-width windows flanking each genomic coordinate of interest (e.g., ±100 bp around motif centers). Aggregate insertion counts per position bin across all sites within each classification group (bound vs. unbound, or grouped by condition). Compute summary statistics (mean, standard deviation) of Tn5 insertion frequency per window position. The resulting position-by-count matrix reveals footprints as positions with significantly reduced insertion counts around bound sites compared to unbound or background regions. Bias-corrected insertion signals improve specificity; use TOBIAS ATACorrect output if available to account for Tn5 sequence preferences.

## Related tools

- **TOBIAS ATACorrect** (Bias-correction of Tn5 cutsite signal to remove sequence preferences of Tn5 transposase, improving accuracy of insertion position counts for downstream footprinting) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculate footprint scores from corrected Tn5 insertion signals across genomic windows to quantify footprint depth and distinguish bound sites) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Aggregate and visualize insertion count distributions across multiple sites to display footprint profiles and validate extraction results) — https://github.com/loosolab/TOBIAS
- **SAMtools** (Parse and manipulate BAM files to extract and filter aligned ATAC-seq reads for Tn5 insertion coordinate extraction)

## Examples

```
samtools view -F4 -q30 sample.bam | awk '{split($NF,a,/[MD]/); pos=$4; for(i=1;i<=length(a);i++) if(a[i]~"^[0-9]+$") pos+=a[i]; print pos}' | bedtools intersect -a motifs.bed -b stdin -wo | awk -v win=100 '{if($NF-$2>=0 && $NF-$2<=2*win) count[$1":"($2+win)][int(($NF-$2)/5)]++} END {for(r in count) for(b in count[r]) print r,b,count[r][b]}' > insertion_counts.matrix
```

## Evaluation signals

- Bound sites exhibit visibly lower insertion counts in the central window region (footprint) compared to flanking regions and unbound sites; unbound sites show uniform insertion distribution across the window.
- Aggregated insertion counts across position bins sum to the total number of sites analyzed per class, confirming complete and non-duplicative counting.
- Mean insertion counts per position bin follow expected monotonic or dipolar patterns: bound sites show depleted center with elevated flanks; unbound sites show relatively flat profiles.
- Positional insertion matrix dimensions match the specified window size (e.g., 200 positions for ±100 bp) and number of site classes, with no missing or NaN values within bins containing sites.
- Comparison of insertion profiles between TOBIAS-corrected and uncorrected BAM-derived counts shows reduced noise and clearer footprint depletion signal in the corrected output, validating bias correction impact.

## Limitations

- Single-cell ATAC-seq requires pseudobulk aggregation by cell type cluster; raw scATAC-seq data lacks sufficient coverage per coordinate for reliable insertion detection, and clustering quality directly impacts footprinting clarity.
- Footprint signal is weak or absent in regions with low chromatin accessibility or low sequencing depth; coverage must be adequate to resolve positional insertion distributions above noise.
- Fixed-width window size is arbitrary; footprint extent and clarity depend on biologically appropriate window definition—too small windows may miss flanking signals, too large windows dilute depletion contrast.
- Tn5 sequence bias can obscure true insertion patterns if not corrected; bias-corrected signal (e.g., from TOBIAS ATACorrect) is strongly recommended to distinguish genuine footprints from transposase preference artifacts.

## Evidence

- [other] Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites within each class (bound/unbound).: "Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites"
- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position.: "Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position."
- [readme] The assay applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome: "The assay applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome"
- [readme] It is important to note that the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis.: "It is important to note that the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis."
