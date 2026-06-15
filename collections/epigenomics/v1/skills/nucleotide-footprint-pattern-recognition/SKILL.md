---
name: nucleotide-footprint-pattern-recognition
description: Use when you have aligned ATAC-seq BAM files and want to discriminate between transcription factor binding sites that are actually occupied by protein versus sites with matching sequence motifs that are unbound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3511
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS BINDetect
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

# nucleotide-footprint-pattern-recognition

## Summary

Identify and quantify transcription factor occupancy by detecting the characteristic depletion of Tn5 insertion signals around protein-bound DNA motifs in ATAC-seq data. This skill reveals footprints—localized regions of accessibility reduction caused by protein binding—which distinguish occupied from unoccupied transcription factor binding sites.

## When to use

Apply this skill when you have aligned ATAC-seq BAM files and want to discriminate between transcription factor binding sites that are actually occupied by protein versus sites with matching sequence motifs that are unbound. Use it when your research question requires quantifying the extent of transcription factor occupancy genome-wide or identifying condition-specific changes in binding kinetics across regulatory regions.

## When NOT to use

- Input ATAC-seq data is not from bulk chromatin or has insufficient sequencing depth (<10 million reads); low coverage compromises the statistical power to detect footprints. Single-cell data requires aggregation into pseudobulk BAM files per cell cluster first.
- Transcription factor motif coordinates are unavailable or of poor quality; footprinting requires known or predicted binding site locations to anchor the analysis window.
- Your primary goal is to identify novel transcription factor binding sites de novo rather than to quantify occupancy at known motif locations; footprinting detects occupancy signal but does not perform motif discovery.

## Inputs

- ATAC-seq aligned reads (BAM format)
- Reference genome sequence (FASTA)
- Transcription factor motif coordinate annotations (BED format with classified bound/unbound status or accessibility signal values for classification)
- Open chromatin peak coordinates (BED format, optional but recommended for ATACorrect)
- Transcription factor position weight matrices or motif annotations

## Outputs

- Bias-corrected ATAC-seq cut-site signal (BigWig format)
- Footprint score matrix (insertion counts by genomic position × site class)
- Positional insertion distribution statistics (mean and standard deviation per bin)
- Aggregate footprint visualization (plot showing insertion profiles for bound vs. unbound sites)
- Bound/unbound classification confidence scores or differential binding estimates

## How to apply

First, correct Tn5 insertion bias in your ATAC-seq BAM file using ATACorrect, which accounts for the sequence preference of Tn5 transposase and produces a bias-corrected cut-site signal. Next, extract Tn5 insertion positions from aligned reads in fixed-width windows (e.g., ±100 bp) flanking known transcription factor motif coordinates, classifying each site as bound or unbound based on accessibility or binding signal thresholds. Aggregate insertion counts per genomic position bin across all sites within each class (bound/unbound) to compute positional distribution statistics (mean, standard deviation). Generate visualization comparing the positional insertion profiles between bound and unbound sites; bound sites should exhibit visible depletion (the footprint signature) in the center region, whereas unbound sites show relatively uniform insertion signal across the window. Evaluate footprint quality by confirming that the depleted region is flanked by elevated insertion counts (nucleosome positioning effect) and that bound sites show significantly lower insertion counts at the motif center than flanking positions.

## Related tools

- **TOBIAS ATACorrect** (Correct Tn5 insertion bias in ATAC-seq BAM files to produce bias-corrected cut-site signal suitable for footprint detection) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculate footprint scores from bias-corrected cut-site signals at transcription factor binding sites) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (Estimate bound versus unbound transcription factor binding sites and detect differential binding based on footprint scores and motif sequences) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Visualize aggregated Tn5 insertion profiles across bound and unbound sites to confirm footprint depletion signal) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotHeatmap** (Generate heatmaps of ATAC-seq signals across binding sites to display footprint patterns and compare across conditions) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS ATACorrect --bam reads.bam --genome genome.fa --peaks peaks.bed --outdir corrected_signals
```

## Evaluation signals

- Bound transcription factor binding sites exhibit visually detectable depletion of Tn5 insertions in the center region (footprint) relative to flanking positions; unbound sites show relatively uniform insertion distribution across the analysis window.
- The insertion count at the motif center in bound sites is significantly lower than in unbound sites at the same genomic coordinates (e.g., statistical test p < 0.05 or effect size > 2-fold difference).
- Flanking regions (±50–100 bp from motif center) show elevated Tn5 insertion counts in bound sites, consistent with nucleosome positioning at accessible chromatin boundaries.
- Reproducibility across biological replicates: footprint profiles from independent ATAC-seq experiments of the same cell type show consistent depletion patterns at the same transcription factor motif locations.
- Sensitivity and specificity controls: applying the method to scrambled motif coordinates or non-transcription-factor protein binding sites yields flat (non-depleted) insertion profiles, confirming that observed footprints are not artifacts.

## Limitations

- Footprint detection requires high-quality ATAC-seq data with sufficient read depth (bulk experiments: >10 million reads per sample); shallow sequencing produces noisy positional distributions that mask footprint signals. Single-cell ATAC-seq requires aggregation into pseudobulk BAM files with careful cell clustering and quality assessment (using tools like PEAKQC) to achieve clean footprints.
- Footprint visibility depends on accurate prior knowledge of transcription factor binding site locations (motif coordinates); misaligned or incomplete motif annotations will reduce signal-to-noise ratio and produce false negatives.
- The method detects only protein-induced accessibility changes; transcription factors that do not occlude Tn5 access (e.g., those binding in open chromatin without creating physical barriers) may not produce detectable footprints.
- Bias correction quality depends on the availability of a high-quality reference genome sequence; genomes with poor assembly or high sequence complexity may yield inaccurate bias models.
- Overlapping or closely-spaced binding sites at the same locus can produce conflicting or averaged footprint signals that obscure occupancy information for individual sites.

## Evidence

- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] ATAC-seq data exhibits a visible depletion of Tn5 insertions around chromatin sites bound by transcription factor proteins, a signal pattern known as footprints that distinguishes bound from unbound motif locations.: "ATAC-seq data exhibits a visible depletion of Tn5 insertions around chromatin sites bound by transcription factor proteins, a signal pattern known as footprints that distinguishes bound from unbound"
- [readme] Correction of Tn5 insertion bias: "Correction of Tn5 insertion bias"
- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase.: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase"
- [other] Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). 4. Aggregate insertion counts per position bin across all sites within each class (bound/unbound).: "Extract Tn5 insertion positions from aligned reads in fixed-width windows flanking each motif site (e.g. ±100 bp around the motif center). 4. Aggregate insertion counts per position bin across all"
- [readme] we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters: "we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters"
- [readme] It is important to note that the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis: "It is important to note that the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis"
