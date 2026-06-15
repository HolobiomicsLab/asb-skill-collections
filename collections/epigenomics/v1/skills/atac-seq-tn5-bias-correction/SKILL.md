---
name: atac-seq-tn5-bias-correction
description: Use when you have raw ATAC-seq BAM files and need to perform footprinting analysis to detect transcription factor binding through Tn5 insertion patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3674
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

# ATAC-seq Tn5 Insertion Bias Correction

## Summary

Correct sequence-dependent Tn5 transposase insertion biases in ATAC-seq BAM files to produce unbiased genome-wide cutsite signals, enabling accurate downstream footprint detection and transcription factor occupancy analysis.

## When to use

You have raw ATAC-seq BAM files and need to perform footprinting analysis to detect transcription factor binding through Tn5 insertion patterns. Apply this skill before calculating footprint scores or running differential binding detection, as uncorrected bias will obscure true protein-bound footprints and inflate false positives.

## When NOT to use

- Input BAM file is from a non-ATAC assay (e.g., ChIP-seq, DNase-seq) where Tn5 bias is not the dominant systematic error
- You only have already-normalized ATAC-seq counts per peak and no access to the original BAM files with per-base cutsites
- Peak annotations are unavailable or of very poor quality, making it impossible to define the chromatin accessibility context for bias estimation

## Inputs

- ATAC-seq BAM file (aligned reads with cutsites)
- Reference genome FASTA file
- Peak annotations BED file (chromatin accessibility regions)

## Outputs

- Uncorrected cutsite bigWig file
- Tn5 insertion bias bigWig file
- Expected signal bigWig file
- Bias-corrected cutsite bigWig file
- ATACorrect diagnostic PDF report

## How to apply

Run TOBIAS ATACorrect on your BAM file, providing the aligned reads, reference genome in FASTA format, and peak annotations in BED format. The tool models the sequence preference of Tn5 transposase (which shows directional insertion bias at certain DNA sequences) and generates a bias track, expected signal track, and corrected cutsite signal. The corrected bigWig output represents the true Tn5 insertion pattern independent of sequence context, enabling reliable identification of the characteristic insertion depletion around protein-bound sites (footprints). Verify correction quality by visually inspecting the generated PDF report comparing uncorrected vs. corrected signals.

## Related tools

- **TOBIAS ATACorrect** (Performs Tn5 insertion bias correction on ATAC-seq BAM files to produce unbiased cutsite signal) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculates footprint enrichment scores from corrected cutsite bigWig files; downstream consumer of ATACorrect output) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (Identifies differentially bound transcription factors using footprint scores derived from bias-corrected signals) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS ATACorrect --bam reads.bam --genome genome.fa --peaks peaks.bed --outdir ./tobias_output
```

## Evaluation signals

- ATACorrect PDF report shows visible reduction in systematic bias patterns between uncorrected and corrected signal tracks, with expected signal closely matching corrected output
- Corrected bigWig file exhibits characteristic depletion of Tn5 insertions in regions corresponding to known or annotated transcription factor binding motifs
- Downstream footprint scores (from TOBIAS ScoreBigwig on corrected bigWigs) show greater dynamic range and statistical power to detect differential TF occupancy compared to uncorrected data
- File format validation: corrected bigWig files are valid and readable by standard bigWig parsers; BAM files produce corresponding corrected bigWig outputs with expected genomic coverage
- Bias correction consistently reduces per-nucleotide variance attributed to sequence context in the expected bias track

## Limitations

- Requires high-quality, deeply sequenced ATAC-seq data; poor-quality input BAM files (low coverage, adapter contamination, or misalignment) will produce unreliable bias estimates
- Correction performance depends on peak annotation quality; missing or misaligned peaks reduce the chromatin accessibility context available for training the bias model
- Single-cell ATAC-seq data requires pseudobulk aggregation by cell type or cluster prior to bias correction; direct correction of single-cell BAM files may fail due to insufficient per-cell coverage
- TOBIAS was originally developed for bulk experiments; while applicable to pseudobulk scATAC-seq, authors recommend quality assessment with PEAKQC beforehand to ensure sufficient cell clustering quality

## Evidence

- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase.: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase."
- [readme] The local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein—known as footprints.: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] Run TOBIAS ATACorrect to perform Tn5 insertion bias correction on BAM files.: "Run TOBIAS ATACorrect to perform Tn5 insertion bias correction on BAM files."
- [readme] Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters.: "Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from"
- [readme] The assay applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome.: "The assay applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome"
