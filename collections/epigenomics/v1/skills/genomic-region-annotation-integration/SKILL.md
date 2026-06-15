---
name: genomic-region-annotation-integration
description: Use when after bias-correcting ATAC-seq cutsite signal (via ATACorrect) when you have a bias-corrected bigWig file and need to compute per-position footprint scores within defined accessible regions (peaks, called footprints, or regulatory regions) to detect and quantify transcription factor.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0204
  tools:
  - TOBIAS
  - ATACorrect
  - ScoreBigwig
  - PlotAggregate
  - BINDetect
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

# Reconstruct the footprint scoring step that converts bias-corrected ATAC-seq signal into per-base footprint scores

## Summary

This skill converts bias-corrected ATAC-seq insertion signal into footprint scores by measuring Tn5 insertion depletion patterns within accessible chromatin regions. It quantifies the magnitude of transcription factor binding footprints at base-pair resolution for downstream differential binding and visualization.

## When to use

Apply this skill after bias-correcting ATAC-seq cutsite signal (via ATACorrect) when you have a bias-corrected bigWig file and need to compute per-position footprint scores within defined accessible regions (peaks, called footprints, or regulatory regions) to detect and quantify transcription factor occupancy through characteristic insertion depletion.

## When NOT to use

- Input bigWig is uncorrected or not yet bias-corrected; use ATACorrect first.
- You have no defined accessible chromatin regions; define peaks or regulatory regions before scoring.
- The goal is only bulk chromatin accessibility quantification without transcription factor binding inference; standard peak calling and quantification suffices.

## Inputs

- bias-corrected bigWig file (from ATACorrect)
- BED file of accessible genomic regions (ATAC-seq peaks or footprint regions)

## Outputs

- footprint-score bigWig file (per-base footprint scores across input regions)

## How to apply

Load the bias-corrected bigWig file (output from ATACorrect) and supply a BED file of accessible genomic regions where footprint scoring should occur. Use TOBIAS ScoreBigwig to measure signal depletion at each base within those regions, generating a bigWig output where each position reflects the magnitude of observed insertion depletion. The tool operates on the principle that protein-bound sites show visible depletion of Tn5 insertions, quantifying this depletion as a footprint score. Validate the output bigWig for correct format (valid header, coordinate ranges), non-zero score distributions, and consistency with input region boundaries.

## Related tools

- **ATACorrect** (Bias-correct raw ATAC-seq cutsite signal prior to footprint scoring) — https://github.com/loosolab/TOBIAS/wiki/ATACorrect
- **ScoreBigwig** (Core tool that computes footprint scores from corrected cutsites within regions) — https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig
- **PlotAggregate** (Visualize aggregated footprint scores across multiple regions to validate scoring output) — https://github.com/loosolab/TOBIAS/wiki/PlotAggregate
- **BINDetect** (Use footprint scores as input for differential binding estimation) — https://github.com/loosolab/TOBIAS/wiki/BINDetect

## Examples

```
TOBIAS ScoreBigwig --signal corrected.bw --regions peaks.bed --output footprint_scores.bw
```

## Evaluation signals

- Output bigWig file is valid, contains non-empty numeric scores, and matches the coordinate range of input regions.
- Footprint scores show expected depletion pattern (negative or reduced values) at known transcription factor binding motif sites within input regions.
- Aggregated footprint plots (via PlotAggregate) show clear valley or depletion signature centered at binding sites, consistent with protein-induced insertion depletion.
- Score distribution is non-trivial (not uniform or constant across regions); signal-to-noise ratio is adequate for downstream binding detection.

## Limitations

- Footprint scoring quality depends critically on upstream bias-correction quality; residual Tn5 sequence bias will introduce noise.
- Requires high-quality, high-depth ATAC-seq data; low-coverage or poorly clustered scATAC-seq pseudobulk samples will produce weak or noisy footprints.
- Scoring is sensitive to the choice of accessible region boundaries; overly broad or narrow region definition affects footprint magnitude and interpretability.
- Single-cell ATAC-seq application requires pseudobulk aggregation by cell type; README notes that single-cell quality and clustering are paramount for clean footprinting results.

## Evidence

- [other] Load the bias-corrected bigWig file and a set of accessible genomic regions (e.g., ATAC-seq peaks or called footprint regions). Apply ScoreBigwig (part of TOBIAS) to compute footprint scores by measuring signal depletion within each region, generating a bigWig output where each position reflects the magnitude of the observed insertion depletion pattern.: "Apply ScoreBigwig (part of TOBIAS) to compute footprint scores by measuring signal depletion within each region, generating a bigWig output where each position reflects the magnitude of the observed"
- [intro] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data, which operates by analyzing the local distribution of Tn5 insertions to detect transcription factor binding through characteristic depletion patterns.: "TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data"
- [readme] ScoreBigwig: Calculate footprint scores from corrected cutsites: "ScoreBigwig: Calculate footprint scores from corrected cutsites"
- [readme] It is important to note that the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis.: "the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis"
