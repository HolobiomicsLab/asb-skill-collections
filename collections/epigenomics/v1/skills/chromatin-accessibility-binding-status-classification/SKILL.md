---
name: chromatin-accessibility-binding-status-classification
description: Use when you have ATAC-seq BAM files aligned to a reference genome, a set of transcription factor motif locations (BED format), and you need to determine which motifs are actually occupied by proteins in your cell type or condition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_0749
  tools:
  - TOBIAS
  - ATACorrect
  - ScoreBigwig
  - BINDetect
  - PlotAggregate
  - PlotHeatmap
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

# chromatin-accessibility-binding-status-classification

## Summary

Classify transcription factor binding sites as bound or unbound by analyzing the spatial distribution of Tn5 insertion depletion patterns (footprints) in ATAC-seq data. This skill leverages the characteristic nucleosome-positioning signal around protein-bound motifs to distinguish occupied from vacant regulatory sites.

## When to use

You have ATAC-seq BAM files aligned to a reference genome, a set of transcription factor motif locations (BED format), and you need to determine which motifs are actually occupied by proteins in your cell type or condition. Use this skill when chromatin accessibility alone is insufficient—you require binding status labels for downstream differential binding analysis, network inference, or kinetic studies.

## When NOT to use

- Input is single-cell ATAC-seq without pseudobulk aggregation by cell type or condition—individual cell resolution lacks sufficient read depth for reliable footprint detection; use the SC-Framework to generate pseudobulk BAM files first.
- Tn5 insertion bias has not been corrected—biased cutsites can mimic or obscure true footprints; apply ATACorrect before classification.
- You only have summary peak calls (BED) without aligned reads—footprint analysis requires base-pair-resolution insertion positions from BAM files.

## Inputs

- ATAC-seq BAM file (aligned reads with insertion coordinates)
- Reference genome FASTA
- Transcription factor motif coordinates (BED format with motif centers)
- ATAC-seq peaks or chromatin accessibility signal (optional; for thresholding accessible sites)

## Outputs

- Bound/unbound classification labels per motif site
- Footprint score matrix (insertion counts by position bin and site class)
- Aggregated insertion profiles (BED and BigWig or heatmap visualizations)
- Statistical summaries of positional insertion distributions per class

## How to apply

Extract Tn5 insertion coordinates from aligned ATAC-seq reads in fixed-width windows (e.g., ±100 bp) centered on each motif site. Aggregate insertion counts per genomic position bin across all sites within each candidate class. Compute positional distribution statistics (mean, standard deviation, or normalized footprint scores) to quantify the characteristic depletion of insertions around protein-bound motifs—the 'footprint' signal that distinguishes bound from unbound sites. Sites exhibiting strong, focal depletion patterns are classified as bound; those with flat or noisy insertion profiles are classified as unbound. The classification threshold is typically determined by comparing observed insertion profiles to background distributions or by fitting score cutoffs empirically from known positive/negative controls. Visualization as aggregated insertion heatmaps or line plots confirms the expected nucleosome positioning around bound sites.

## Related tools

- **ATACorrect** (Corrects Tn5 transposase sequence bias in cutsites before footprint analysis to prevent false or artifactual insertion patterns) — https://github.com/loosolab/TOBIAS/wiki/ATACorrect
- **ScoreBigwig** (Calculates per-position footprint scores from corrected insertion cutsites, generating the signal used to classify binding status) — https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig
- **BINDetect** (Estimates differential binding across conditions using footprint scores and motif sequences; produces final bound/unbound classifications) — https://github.com/loosolab/TOBIAS/wiki/BINDetect
- **PlotAggregate** (Visualizes aggregated ATAC-seq insertion profiles across bound versus unbound site classes to validate classification quality) — https://github.com/loosolab/TOBIAS/wiki/PlotAggregate
- **PlotHeatmap** (Generates heatmap and aggregate visualizations of insertion signals to inspect footprint patterns supporting binding status calls) — https://github.com/loosolab/TOBIAS/wiki/PlotHeatmap

## Examples

```
TOBIAS ATACorrect --bam reads.bam --genome genome.fa --peaks peaks.bed --outdir corrected/ && TOBIAS ScoreBigwig --signal corrected/reads_corrected.bw --regions motifs.bed --output footprint_scores.bw && TOBIAS BINDetect --motifs motifs.pfm --signals footprint_scores.bw --peak-regions peaks.bed --output bindetect_results/
```

## Evaluation signals

- Aggregated insertion profiles for bound sites show a clear focal depletion (footprint) centered on the motif, while unbound sites exhibit flat or noisy insertion distributions across the window.
- Statistical comparison of mean insertion counts at the motif center versus flanking regions (e.g., ±50 bp) should show significant depletion for bound sites (e.g., p < 0.05 by t-test) and no significant difference for unbound sites.
- Footprint scores computed by ScoreBigwig or equivalent show bimodal or multimodal separation between bound and unbound site populations, enabling threshold-based classification.
- Reproducibility check: the same motif sites classified as bound in replicate ATAC-seq experiments should show consistent footprint patterns; Spearman correlation of positional insertion profiles across replicates should be > 0.7 for high-confidence classifications.
- Visual inspection of IGV-style track plots (PlotTracks) reveals nucleosome-scale (~147 bp) phasing of insertions flanking bound sites, consistent with nucleosome positioning by protein occupancy.

## Limitations

- Footprint detection requires high-coverage ATAC-seq data (typically ≥10M reads per sample); shallow sequencing yields noisy insertion profiles that confound bound/unbound classification.
- Tn5 insertion bias must be corrected beforehand (ATACorrect); uncorrected bias can produce spurious depletion patterns that mimic or mask true footprints.
- Single-cell ATAC-seq requires aggregation into pseudobulk BAM files by cell type or condition; insufficient cell recovery per cluster yields low read depth and unreliable footprints. The quality of clustering is paramount—poorly defined cell populations produce mixed or absent footprint signals.
- Motif database quality and representativeness affects classification accuracy; low-quality or incomplete motif sets may miss true binding sites or include non-functional motifs.
- The method assumes a uniform nucleosome positioning pattern around bound sites; highly variable or asymmetric nucleosome positioning (e.g., in certain chromatin states or during dynamic processes) can reduce footprint contrast and lower classification confidence.

## Evidence

- [other] Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites within each class (bound/unbound).: "Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). Aggregate insertion counts per position bin across all sites"
- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] ATAC-seq data exhibits a visible depletion of Tn5 insertions around chromatin sites bound by transcription factor proteins, a signal pattern known as footprints that distinguishes bound from unbound motif locations.: "ATAC-seq data exhibits a visible depletion of Tn5 insertions around chromatin sites bound by transcription factor proteins, a signal pattern known as footprints that distinguishes bound from unbound"
- [other] Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position. Tabulate results as a matrix of insertion counts by position and site class; generate visualization showing insertion profiles across bound and unbound sites to confirm footprint depletion signal in bound sites.: "Compute positional distribution statistics (mean, standard deviation) of Tn5 insertions for each window position. Tabulate results as a matrix of insertion counts by position and site class; generate"
- [readme] Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters.: "we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters. This can be done using the sc-framework. It is important to note that the quality of the single cells and"
