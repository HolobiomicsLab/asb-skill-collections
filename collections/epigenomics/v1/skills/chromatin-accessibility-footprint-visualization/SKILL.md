---
name: chromatin-accessibility-footprint-visualization
description: Use when use this skill after performing Tn5 bias correction and footprint scoring on ATAC-seq BAM files when you need to inspect the spatial distribution of Tn5 insertions around transcription factor binding sites, validate footprinting quality, or communicate differential TF occupancy patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0204
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS PlotAggregate
  - TOBIAS PlotHeatmap
  - TOBIAS PlotTracks
  - TOBIAS ScoreBigwig
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

# chromatin-accessibility-footprint-visualization

## Summary

Visualize transcription factor footprints in ATAC-seq data by aggregating corrected Tn5 insertion signals around known transcription factor binding sites, enabling direct inspection of protein-induced depletion patterns and comparative analysis across conditions.

## When to use

Use this skill after performing Tn5 bias correction and footprint scoring on ATAC-seq BAM files when you need to inspect the spatial distribution of Tn5 insertions around transcription factor binding sites, validate footprinting quality, or communicate differential TF occupancy patterns across conditions to stakeholders. Specifically triggered when you have corrected bigwig files and motif coordinates (.bed) or differential binding results and wish to examine aggregate insertion patterns.

## When NOT to use

- Input BAM files have not undergone Tn5 bias correction; uncorrected insertion signals contain substantial sequence bias artifacts that will obscure true footprints.
- You lack annotated transcription factor binding site coordinates or motif predictions; visualization aggregates only meaningful signal when centered on true/predicted TFBS regions.
- Data is single-cell ATAC-seq without pseudobulk aggregation per cell type; individual cell resolution lacks sufficient read depth to visualize footprints clearly.

## Inputs

- Bias-corrected bigwig files (output from TOBIAS ATACorrect: *_corrected.bw)
- Transcription factor binding site coordinates (BED format with motif instances or known TFBS)
- BAM file(s) of ATAC-seq reads (for PlotTracks locus-specific views)
- Optional: Footprint score bigwig files (output from ScoreBigwig)
- Optional: Differential binding results table (output from BINDetect, for condition labeling)

## Outputs

- Aggregated footprint visualization plots (PDF or PNG)
- Heatmaps showing per-site Tn5 insertion patterns across conditions
- IGV-style track plots showing cutsites, footprints, and local genomic context
- Summary figures highlighting top differential TFs with occupancy change magnitudes

## How to apply

Apply TOBIAS visualization tools (PlotAggregate, PlotHeatmap, or PlotTracks) to aggregate the bias-corrected Tn5 insertion signal (from ATACorrect output) over regions of interest, typically centered on transcription factor binding sites (from motif scanning or known TFBS annotations). The visualization should reveal the characteristic 'footprint' — a visible depletion of Tn5 insertions flanked by elevated insertion counts at the boundaries of protein-bound sites. Select visualization type based on analysis goal: use PlotAggregate for genome-wide aggregate signal patterns across multiple sites per TF, PlotHeatmap for per-site patterns and condition comparisons, and PlotTracks for locus-specific inspection of nearby regulatory elements. Export results as publication-quality PDF or PNG files with clear labeling of conditions, TF names, and occupancy changes where applicable.

## Related tools

- **TOBIAS ATACorrect** (Perform Tn5 insertion bias correction on ATAC-seq BAM files to generate corrected bigwig files used as input for visualization) — https://github.com/loosolab/TOBIAS/wiki/ATACorrect
- **TOBIAS PlotAggregate** (Aggregate corrected Tn5 insertion signals across multiple TFBS sites to produce genome-wide consensus footprint patterns) — https://github.com/loosolab/TOBIAS/wiki/PlotAggregate
- **TOBIAS PlotHeatmap** (Generate heatmaps and aggregates of ATAC-seq signals to visualize per-site footprint variation and condition-specific changes) — https://github.com/loosolab/TOBIAS/wiki/PlotHeatmap
- **TOBIAS PlotTracks** (Plot IGV-style genomic signals (cutsites, footprints, coverage) across selected loci for detailed locus-specific inspection) — https://github.com/loosolab/TOBIAS/wiki/PlotTracks
- **TOBIAS ScoreBigwig** (Calculate footprint enrichment scores from corrected cutsites; outputs used to color or filter visualization regions) — https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig
- **TOBIAS BINDetect** (Identify differentially bound transcription factors; results table used to select and label TFs for visualization) — https://github.com/loosolab/TOBIAS/wiki/BINDetect

## Examples

```
TOBIAS PlotAggregate --bed motif_sites.bed --bw condition1_corrected.bw condition2_corrected.bw --output footprint_aggregate.pdf --title 'TF Footprint Patterns Across Conditions'
```

## Evaluation signals

- Visualized footprints show characteristic Tn5 insertion depletion pattern centered on known/predicted TFBS, with elevated insertions at flanking boundaries (positive control: match literature footprint shapes for known regulatory TFs).
- Aggregate plots span sufficient numbers of sites per TF (typically ≥20–50 motif instances) to produce smooth, interpretable consensus signal; heatmaps show per-site variation without overwhelming noise.
- Condition-specific plots reveal expected occupancy differences: increased insertions within footprint region (suggesting reduced occupancy) or decreased insertions (suggesting increased occupancy) in target condition relative to control, with statistical significance reported when applicable.
- Output PDF/PNG files are publication-ready with labeled axes, condition legends, TF names, and if applicable, log2 fold-change or p-value annotations; resolution sufficient for print (≥300 dpi) and inline figure inclusion.
- Locus-specific tracks (PlotTracks) correctly align ATAC-seq insertion signals with reference genome annotations and show expected signal enrichment within defined open chromatin peaks.

## Limitations

- Visualization quality depends critically on the depth and complexity of ATAC-seq data; low-coverage samples or shallow sequencing may yield noisy or uninterpretable footprints even after bias correction.
- Footprints are most detectable at high-occupancy TF binding sites and may be absent or very weak for transient or low-affinity interactions; absence of a visible footprint does not confirm absence of binding.
- Single-cell ATAC-seq data requires aggregation into pseudobulk samples per cell type or condition to achieve sufficient read depth for footprinting visualization; quality of clustering and cell type definition directly impacts footprint clarity.
- Visualization does not quantify occupancy changes alone; differential binding analysis (via BINDetect) is required to assign statistical significance to observed occupancy differences between conditions.

## Evidence

- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [readme] TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data: "TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data"
- [readme] Visualization of footprints within and across different conditions: "Visualization of footprints within and across different conditions"
- [readme] PlotAggregate: Plot aggregated ATAC-seq signals in combinations of .bed/.bw to visualize footprints: "PlotAggregate: Plot aggregated ATAC-seq signals in combinations of .bed/.bw to visualize footprints"
- [readme] PlotHeatmap: Plot heatmaps and aggregates of ATAC-seq signals in combinations of .bed/.bw to visualize footprints: "PlotHeatmap: Plot heatmaps and aggregates of ATAC-seq signals in combinations of .bed/.bw to visualize footprints"
- [readme] Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters.: "Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from"
