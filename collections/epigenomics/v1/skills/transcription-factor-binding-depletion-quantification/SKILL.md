---
name: transcription-factor-binding-depletion-quantification
description: Use when after bias-correcting ATAC-seq cutsite signal (using ATACorrect or equivalent) when you have a set of genomic regions of interest (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3125
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

# transcription-factor-binding-depletion-quantification

## Summary

Quantify transcription factor occupancy by measuring Tn5 insertion depletion patterns in bias-corrected ATAC-seq signal within accessible chromatin regions. This skill converts local insertion depletion signatures into per-base footprint scores that reflect the magnitude of protein-induced chromatin protection.

## When to use

Apply this skill after bias-correcting ATAC-seq cutsite signal (using ATACorrect or equivalent) when you have a set of genomic regions of interest (e.g., ATAC-seq peaks, called footprints, or motif sites) and need to quantify the strength of transcription factor binding footprints by detecting characteristic insertion depletion at each base pair position.

## When NOT to use

- Input ATAC-seq signal has not been corrected for Tn5 sequence bias—apply ATACorrect first
- No defined set of genomic regions to score (ScoreBigwig requires explicit region boundaries)
- Input regions are from a different assay (DNase-seq, ChIP-seq, MNase-seq) that do not exhibit Tn5 insertion bias patterns

## Inputs

- bias-corrected ATAC-seq bigWig file (output from ATACorrect or equivalent bias-correction tool)
- BED file defining accessible chromatin regions or sites to score (e.g., ATAC-seq peaks or footprint regions)

## Outputs

- footprint score bigWig file (per-base quantification of insertion depletion magnitude)
- validation report confirming bigWig format and score distribution

## How to apply

Load the bias-corrected ATAC-seq bigWig file (containing Tn5 insertion signal after sequence-preference correction) and supply a BED file defining the genomic regions to score. Apply TOBIAS ScoreBigwig, which analyzes the local distribution of insertions within each region to compute footprint scores by measuring the magnitude of insertion depletion—regions with strong protein binding show deeper depletion. The tool outputs a bigWig file where each position contains a footprint score reflecting the observed depletion pattern. Validate the output bigWig for correct format and non-empty score distributions across the regions of interest.

## Related tools

- **TOBIAS ScoreBigwig** (Computes footprint scores from bias-corrected ATAC-seq signal by measuring insertion depletion within genomic regions) — https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig
- **TOBIAS ATACorrect** (Prerequisite tool for bias-correcting ATAC-seq cutsite signal with respect to Tn5 transposase sequence preference (must be run before ScoreBigwig)) — https://github.com/loosolab/TOBIAS/wiki/ATACorrect
- **TOBIAS BINDetect** (Downstream tool for estimating differential transcription factor binding based on computed footprint scores) — https://github.com/loosolab/TOBIAS/wiki/BINDetect
- **TOBIAS PlotAggregate** (Visualization tool for validating footprint scores by plotting aggregated ATAC-seq signals and footprints) — https://github.com/loosolab/TOBIAS/wiki/PlotAggregate

## Examples

```
TOBIAS ScoreBigwig --signal bias_corrected.bw --regions peaks.bed --outdir footprints_out
```

## Evaluation signals

- Output bigWig file is valid and readable; file size and content structure match expected format
- Score distribution across regions is non-empty and shows expected range (negative scores at depletion sites for bound regions, near-zero or positive for unbound regions)
- Footprint scores show expected spatial pattern: depletion centered on known transcription factor binding motifs or experimentally validated binding sites
- Comparison with visualizations (PlotAggregate or PlotHeatmap outputs) confirms that high footprint scores correspond to visible insertion depletion in aggregated signal plots
- Downstream BINDetect analysis successfully ingests footprint scores and produces bound/unbound predictions consistent with known biology

## Limitations

- Footprint score quality depends critically on the accuracy of upstream bias correction (ATACorrect); systematic biases in bias-correction propagate to footprint scores
- Scoring is most reliable in high-coverage regions; low sequencing depth leads to noisy score estimates and reduced ability to detect subtle depletion
- Method detects protein-induced chromatin depletion patterns but does not distinguish between different types of protein-DNA interactions (e.g., TF binding vs. nucleosome positioning); post-hoc filtering by motif or BINDetect is required
- Requires pre-defined region boundaries; de novo footprint detection (without anchoring to known regions) requires separate peak-calling or motif-scanning steps

## Evidence

- [readme] TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data: "**TOBIAS** is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data"
- [readme] The local distribution of Tn5 insertions reveals transcription factor binding through characteristic depletion patterns: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] ScoreBigwig computes footprint scores by measuring signal depletion within each region: "Apply ScoreBigwig (part of TOBIAS) to compute footprint scores by measuring signal depletion within each region, generating a bigWig output where each position reflects the magnitude of the observed"
- [readme] ScoreBigwig calculates footprint scores from corrected cutsites: "[ScoreBigwig](https://github.com/loosolab/TOBIAS/wiki/ScoreBigwig): Calculate footprint scores from corrected cutsites"
- [readme] Bias correction precedes footprint scoring in the TOBIAS workflow: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase"
