---
name: atac-seq-signal-normalization
description: Use when you have aligned ATAC-seq BAM files and need to detect transcription factor binding sites via footprint analysis. The skill is essential because raw Tn5 insertion signal contains systematic bias toward certain DNA sequences;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0622
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
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

# atac-seq-signal-normalization

## Summary

Correct ATAC-seq signal for Tn5 transposase insertion bias to enable accurate detection of transcription factor footprints. This skill applies the TOBIAS ATACorrect module to model and remove sequence-dependent insertion preferences, producing bias-corrected signal tracks suitable for footprinting analysis.

## When to use

Apply this skill when you have aligned ATAC-seq BAM files and need to detect transcription factor binding sites via footprint analysis. The skill is essential because raw Tn5 insertion signal contains systematic bias toward certain DNA sequences; correction is necessary before scoring footprints (depletion patterns around protein-bound regions) or comparing signal across genomic regions with different sequence composition.

## When NOT to use

- Input is already a bias-corrected signal track or normalized feature table — do not apply correction twice.
- ATAC-seq data lacks sufficient depth or quality (e.g. <10M unique fragments) — bias modeling will be unreliable.
- Analysis does not require footprint-level resolution — for broad chromatin accessibility assessment, bias correction may not be necessary.

## Inputs

- Aligned ATAC-seq reads (BAM format)
- Reference genome sequence (FASTA format)
- Open chromatin peak regions (BED format)

## Outputs

- Uncorrected cutsite signal (bigWig)
- Tn5 insertion bias model (bigWig)
- Expected bias-corrected signal (bigWig)
- Bias-corrected cutsite signal (bigWig)
- ATACorrect diagnostic plots (PDF)

## How to apply

Load aligned ATAC-seq BAM file, corresponding reference genome FASTA, and peak regions (BED format) into TOBIAS ATACorrect. The tool models the sequence preference of Tn5 transposase by examining the nucleotide context of insertion sites within open chromatin peaks, then applies this bias model to normalize the cutsite signal genome-wide. ATACorrect outputs both the bias model (as a bigWig track) and the bias-corrected signal; the corrected signal should show reduced spurious variation driven by sequence composition and enhanced visibility of footprints (insertional depletion around transcription factor binding sites). Evaluate success by visual inspection of corrected signal in genome browsers and comparison of footprint clarity before and after correction.

## Related tools

- **TOBIAS ATACorrect** (Corrects Tn5 insertion bias in ATAC-seq cutsite signal to enable footprint detection) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Calculates footprint scores from bias-corrected signal) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate** (Visualizes bias-corrected signal to validate footprint visibility) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS ATACorrect --bam reads.bam --genome genome.fa --peaks peaks.bed --outdir corrected_output
```

## Evaluation signals

- Bias-corrected signal tracks are output in standard bigWig format and load successfully in genome browsers (IGV, UCSC) without errors.
- Footprints (insertional depletion) are visibly sharper and more prominent in corrected signal compared to uncorrected signal when plotted at known transcription factor binding sites.
- The bias model (output bigWig) shows expected enrichment/depletion patterns linked to Tn5 sequence preferences (e.g. TA dinucleotide bias).
- Corrected signal retains biologically meaningful peaks in open chromatin regions and does not introduce artificial artifacts (e.g. negative values, extreme outliers).
- Downstream footprint scoring and motif binding detection (via TOBIAS BINDetect) produce consistent, interpretable results across different sequence contexts.

## Limitations

- Bias correction requires sufficient peak coverage depth; sparse ATAC-seq libraries may yield unreliable bias models.
- The correction assumes Tn5 insertion bias is uniform across the genome; cell-type or condition-specific biases are not modeled.
- Bias correction alone does not resolve other ATAC-seq artifacts (e.g. nucleosome positioning bias, PCR duplicates); these must be addressed separately.
- The README notes that single-cell ATAC-seq requires aggregation into pseudobulk BAM files per cell type cluster before applying ATACorrect; direct single-cell application is not recommended.
- No changelog is provided in the repository, limiting transparency about methodological changes across versions.

## Evidence

- [readme] ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase.: "ATACorrect corrects the cutsite-signal from ATAC-seq with regard to the underlying sequence preference of Tn5 transposase."
- [readme] The assay applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome.: "The assay applies a Tn5 Transposase to insert sequencing adapters into accessible chromatin, enabling mapping of regulatory regions across the genome"
- [readme] The local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein—known as footprints.: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] ATAC-seq generates signal data from Tn5 transposase insertions at accessible chromatin sites, which contain information about transcription factor binding through patterns of insertion depletion (footprints) around protein-bound regions.: "ATAC-seq generates signal data from Tn5 transposase insertions at accessible chromatin sites, which contain information about transcription factor binding through patterns of insertion depletion"
- [other] Load aligned ATAC-seq BAM file and corresponding reference genome FASTA. Run TOBIAS ATACorrect to model Tn5 insertion bias from the BAM data and apply correction to generate bias-corrected signal. Convert corrected signal to bigWig format for visualization and downstream footprinting analysis.: "Load aligned ATAC-seq BAM file and corresponding reference genome FASTA. Run TOBIAS ATACorrect to model Tn5 insertion bias from the BAM data and apply correction to generate bias-corrected signal."
