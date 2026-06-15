---
name: atac-seq-footprint-scoring
description: Use when you have completed Tn5 insertion bias correction on ATAC-seq reads and now need to quantify footprint signal strength (signal depletion around TF-bound sites) across accessible chromatin regions before classifying individual TF binding sites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - TOBIAS
  - TOBIAS ScoreBigwig
  - TOBIAS ATACorrect
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

# ATAC-seq footprint scoring

## Summary

Convert bias-corrected ATAC-seq signal into per-base footprint scores that quantify transcription factor binding through Tn5 insertion depletion patterns. This intermediate step bridges raw cutsite bias correction and downstream TF occupancy classification by measuring signal magnitude at each genomic position.

## When to use

You have completed Tn5 insertion bias correction on ATAC-seq reads and now need to quantify footprint signal strength (signal depletion around TF-bound sites) across accessible chromatin regions before classifying individual TF binding sites. Use this skill when your input is a bias-corrected bigWig file and a set of genomic intervals (peaks, footprint regions, or open chromatin windows) and your goal is to generate position-specific footprint magnitude scores.

## When NOT to use

- Input BAM/cutsite data has not been bias-corrected for Tn5 sequence preferences — run TOBIAS ATACorrect first
- Input regions are not open chromatin or accessible regions — ScoreBigwig requires regions with measurable ATAC-seq signal
- Goal is to classify individual TF binding sites as bound/unbound — that requires downstream motif matching and BINDetect, not scoring alone

## Inputs

- Bias-corrected bigWig file (from TOBIAS ATACorrect; e.g., *_corrected.bw)
- Genomic intervals in BED format (accessible chromatin peaks, footprint regions, or regulatory regions)

## Outputs

- Footprint scores bigWig file (per-base signal depletion magnitude across input regions)
- Optional: footprint score summary statistics (mean, median, distribution across regions)

## How to apply

Load the bias-corrected bigWig file (output from TOBIAS ATACorrect) and a corresponding set of accessible genomic regions in BED format. Apply TOBIAS ScoreBigwig, which computes footprint scores by measuring signal depletion magnitude within each region, generating a bigWig output where each genomic position reflects the observed insertion depletion pattern intensity. The tool integrates the corrected signal across the region and assigns scores that represent the magnitude of the footprint signal. Validate the output bigWig file for correct format (chromatin regions present, valid score distributions), non-empty signal coverage, and absence of NaN or infinite values before passing to downstream motif-based TF binding classification.

## Related tools

- **TOBIAS ScoreBigwig** (Primary tool for computing footprint scores from bias-corrected ATAC-seq signal across genomic regions) — https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig
- **TOBIAS ATACorrect** (Prerequisite tool for correcting Tn5 insertion bias before footprint scoring) — https://github.com/loosolab/TOBIAS/wiki/ATACorrect
- **TOBIAS BINDetect** (Downstream tool for classifying TF binding at motif sites using footprint scores) — https://github.com/loosolab/TOBIAS/wiki/BINDetect
- **TOBIAS PlotAggregate** (Visualization tool for validating footprint scores across aggregated regions) — https://github.com/loosolab/TOBIAS/wiki/PlotAggregate

## Examples

```
TOBIAS ScoreBigwig --signal bias_corrected.bw --regions peaks.bed --output footprint_scores.bw
```

## Evaluation signals

- Output bigWig file contains valid numeric scores at all positions within input regions with no NaN or infinite values
- Footprint score distribution shows expected negative values or depletion patterns (lower signal intensity at TF-bound sites) when compared to flanking sequence
- Score statistics (mean, median, range) fall within biologically plausible range for ATAC-seq depletion magnitude (typically standardized or log-scale values)
- When visualized with PlotAggregate or PlotHeatmap, scores show characteristic footprint shape — valley of reduced signal flanked by elevated signal at TF motif sites
- Reproducibility: identical input bias-corrected bigWig and region BED files yield identical footprint score bigWig output

## Limitations

- Footprint scoring requires sufficiently deep ATAC-seq coverage; shallow sequencing yields weak or uninformative depletion signal
- Quality of bias correction directly impacts footprint score reliability; systematic Tn5 biases remaining after ATACorrect will distort scoring
- Scoring does not distinguish between bound and unbound TF sites — it measures depletion magnitude only; occupancy classification requires motif matching and BINDetect
- Footprint signals may be obscured in regions with multiple overlapping TF binding sites or high nucleosome occupancy

## Evidence

- [other] Load the bias-corrected bigWig file and a set of accessible genomic regions (e.g., ATAC-seq peaks or called footprint regions). Apply ScoreBigwig (part of TOBIAS) to compute footprint scores by measuring signal depletion within each region, generating a bigWig output where each position reflects the magnitude of the observed insertion depletion pattern.: "Apply ScoreBigwig (part of TOBIAS) to compute footprint scores by measuring signal depletion within each region, generating a bigWig output where each position reflects the magnitude of the observed"
- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as footprints"
- [other] Validate the output bigWig file for correct format and non-empty score distributions.: "Validate the output bigWig file for correct format and non-empty score distributions"
- [readme] ScoreBigwig: Calculate footprint scores from corrected cutsites: "ScoreBigwig: Calculate footprint scores from corrected cutsites"
