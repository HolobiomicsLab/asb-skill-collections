---
name: tn5-insertion-bias-correction
description: Use when you have aligned ATAC-seq BAM files from Tn5-based chromatin accessibility assays and need to perform footprinting analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
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

# Tn5 insertion bias correction

## Summary

Corrects systematic sequence preferences in Tn5 transposase insertion patterns within ATAC-seq data to reveal true transcription factor footprints. This bias correction is essential for accurate downstream footprinting analysis, as uncorrected insertion bias can obscure protein-bound depletion patterns.

## When to use

Apply this skill when you have aligned ATAC-seq BAM files from Tn5-based chromatin accessibility assays and need to perform footprinting analysis. The skill is triggered when raw insertion signal contains confounding transposase sequence preferences that would mask the depletion patterns (footprints) characteristic of transcription factor binding.

## When NOT to use

- Input is non-Tn5 based chromatin data (e.g., ChIP-seq, DNase-seq, or other accessibility assays) — this skill is specific to Tn5 insertion patterns.
- ATAC-seq data is already corrected by another tool — applying bias correction twice may remove legitimate signal.
- You only need peak-level summary statistics and do not require base-pair resolution footprinting — bias correction adds computational cost for minimal benefit in coarse workflows.

## Inputs

- aligned ATAC-seq reads (BAM format)
- reference genome sequence (FASTA format)
- peak regions (BED format, optional but recommended)

## Outputs

- bias-corrected cutsite signal (bigWig format)
- uncorrected signal track (bigWig format)
- modeled Tn5 bias track (bigWig format)
- expected bias track (bigWig format)
- diagnostic PDF report (ATACorrect.pdf)

## How to apply

Load the aligned ATAC-seq BAM file along with the corresponding reference genome FASTA sequence. Run TOBIAS ATACorrect, which models Tn5 insertion bias directly from the input BAM data by learning the sequence-dependent cutting preferences of the transposase. ATACorrect generates four output tracks: uncorrected cutsite signal, modeled bias signal, expected bias signal, and the final bias-corrected signal. The corrected bigWig file removes the learned sequence bias while preserving the footprint signal (insertion depletion around protein-bound sites), producing output suitable for downstream footprint scoring and transcription factor binding analysis.

## Related tools

- **TOBIAS ATACorrect** (Primary tool that models and applies Tn5 insertion bias correction to ATAC-seq cutsite signal) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Downstream tool to calculate footprint scores from the bias-corrected signal produced by ATACorrect) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (Downstream tool that uses bias-corrected footprint scores to estimate differential transcription factor binding) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS ATACorrect --bam reads.bam --genome genome.fa --peaks peaks.bed --outdir results --prefix sample
```

## Evaluation signals

- Bias-corrected bigWig signal exhibits reduced sequence-dependent variability compared to uncorrected track, with visible footprints (insertion depletion) more prominent around known transcription factor binding motifs.
- Modeled bias track (bias.bw) captures the transposase sequence preference learned from the BAM data; compare to expected.bw to confirm the bias model captures real systematic preferences.
- Diagnostic PDF report (atacorrect.pdf) should show clear separation between uncorrected, bias, and corrected signals, with corrected signal aligned to sequence features.
- Downstream footprint scores (from ScoreBigwig on corrected signal) should show stronger correlation with transcription factor binding predictions compared to scores computed on uncorrected signal.
- All four output bigWig files are properly formatted with matching genomic coordinates and can be loaded into genome browsers for visual inspection.

## Limitations

- ATACorrect requires sufficient coverage depth to accurately model Tn5 bias; sparse ATAC-seq data may result in overfitted or unreliable bias models.
- The skill assumes the input BAM file is properly aligned and duplicate-marked; poor quality input reads will propagate errors into the bias model.
- Bias correction models learned from one biological condition may not transfer directly to very different chromatin states or cell types with substantially different accessibility patterns.
- The tool is designed for bulk ATAC-seq; single-cell ATAC-seq requires aggregation into pseudobulk BAM files per cell type cluster for reliable bias modeling, as noted in the README.

## Evidence

- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase.: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase."
- [other] ATAC-seq generates signal data from Tn5 transposase insertions at accessible chromatin sites, which contain information about transcription factor binding through patterns of insertion depletion (footprints) around protein-bound regions.: "ATAC-seq generates signal data from Tn5 transposase insertions at accessible chromatin sites, which contain information about transcription factor binding through patterns of insertion depletion"
- [readme] The local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_.: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] Load aligned ATAC-seq BAM file and corresponding reference genome FASTA. Run TOBIAS ATACorrect to model Tn5 insertion bias from the BAM data and apply correction to generate bias-corrected signal. Convert corrected signal to bigWig format for visualization and downstream footprinting analysis.: "Load aligned ATAC-seq BAM file and corresponding reference genome FASTA. Run TOBIAS ATACorrect to model Tn5 insertion bias from the BAM data and apply correction to generate bias-corrected signal."
- [readme] Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters.: "Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from"
