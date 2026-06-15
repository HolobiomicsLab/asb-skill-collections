---
name: chromatin-accessibility-occupancy-prediction
description: Use when after you have (1) corrected ATAC-seq BAM files for Tn5 insertion bias using ATACorrect, (2) computed per-base footprint scores using ScoreBigwig, (3) obtained a motif database (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3511
  tools:
  - TOBIAS
  - TOBIAS ATACorrect
  - TOBIAS ScoreBigwig
  - TOBIAS BINDetect
  - TOBIAS FormatMotifs
  - TOBIAS PlotAggregate / PlotHeatmap
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

# Reconstruct the transcription factor occupancy prediction step that classifies TF binding from footprint scores at motif sites

## Summary

This skill uses TOBIAS BINDetect to classify transcription factor occupancy (bound vs. unbound) at specific genomic locations by comparing corrected ATAC-seq footprint scores and Tn5 insertion depletion patterns across conditions and motif positions. It bridges ATAC-seq signal preprocessing and binding site annotation by assigning occupancy states and differential binding metrics to known or predicted TF binding motifs.

## When to use

Apply this skill after you have (1) corrected ATAC-seq BAM files for Tn5 insertion bias using ATACorrect, (2) computed per-base footprint scores using ScoreBigwig, (3) obtained a motif database (e.g., JASPAR PWMs in TOBIAS-compatible format), and (4) want to infer which TF binding sites are actually occupied in your experimental samples and how occupancy differs across conditions or cell states. Use it specifically when you observe visible Tn5 insertion depletion (footprints) around regulatory regions and need to map those patterns to known TF motifs.

## When NOT to use

- Input data are not ATAC-seq or have not undergone Tn5 bias correction; TOBIAS BINDetect is optimized for bias-corrected Tn5 cutsites and will produce unreliable occupancy calls if applied to uncorrected or non-ATAC data.
- You lack a motif database or prior TF annotation; BINDetect requires known PWMs to scan and match, so de novo motif discovery or ChIP-seq peak matching would be the wrong entry point.
- Your goal is to discover novel TF binding sites rather than classify occupancy at known motifs; use ab initio footprint clustering or machine learning-based motif discovery instead.
- Single-cell ATAC-seq without adequate pseudobulk aggregation; the README notes that single-cell quality and clustering are paramount, and direct single-cell BAM analysis may produce noisy footprints.

## Inputs

- Corrected ATAC-seq BAM file (output from TOBIAS ATACorrect)
- Footprint score bigWig files (output from TOBIAS ScoreBigwig)
- Peak/regulatory region BED file
- Motif database in JASPAR or TOBIAS-compatible PWM format
- Sample metadata or condition labels for comparative occupancy analysis

## Outputs

- BINDetect output table (TSV) with per-motif occupancy predictions
- Binding probability scores and confidence intervals per motif site
- Differential occupancy scores across experimental conditions
- Structured CSV/TSV table with columns: TF motif ID, genomic coordinates (chr:start-end), occupancy state (bound/unbound), occupancy probability, condition-specific binding metrics

## How to apply

Load the corrected ATAC-seq footprint scores (output from ScoreBigwig as bigWig files) and peak/BED files into TOBIAS BINDetect along with a motif database containing position weight matrices (PWMs) for your TFs of interest. BINDetect scans for motif matches genome-wide, then at each motif occurrence it compares the signal intensity (footprint depth and width) at the motif site relative to flanking regions across your experimental conditions. The tool applies a statistical model to discriminate bound from unbound sites by examining whether the footprint signal deviates significantly from the background chromatin accessibility; it outputs per-motif occupancy predictions with binding probabilities, confidence scores, and differential occupancy metrics (e.g., log2 fold-change in binding between conditions). Parse the BINDetect output table to extract TF-specific binding estimates, filter by confidence thresholds if needed, and format results as structured CSV/TSV with columns for motif ID, genomic coordinates, occupancy state, and condition-specific binding metrics for downstream interpretation or integration with other datasets.

## Related tools

- **TOBIAS ATACorrect** (Prerequisite: corrects Tn5 insertion bias in raw ATAC-seq BAM files to normalize cutsites prior to footprinting) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Prerequisite: calculates footprint scores from corrected cutsites and produces bigWig signal files consumed by BINDetect) — https://github.com/loosolab/TOBIAS
- **TOBIAS BINDetect** (Core tool: performs motif scanning and occupancy prediction by comparing footprint scores at motif sites across conditions) — https://github.com/loosolab/TOBIAS
- **TOBIAS FormatMotifs** (Utility: converts and prepares motif databases (e.g., JASPAR PWMs) into TOBIAS-compatible formats) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate / PlotHeatmap** (Validation and visualization: aggregate ATAC-seq signals at predicted bound/unbound sites to visually confirm footprint patterns) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS BINDetect --signals condition_A_corrected.bw condition_B_corrected.bw --peaks peaks.bed --motifs JASPAR_PWMs.txt --outdir bindetect_results --conditions CondA CondB
```

## Evaluation signals

- BINDetect output file is created and contains per-motif rows with non-null occupancy probability values in expected range [0, 1].
- Genomic coordinates in output match the motif scanning results; spot-check a subset of reported binding sites against the original peak/BED file and motif PWM matches.
- Occupancy predictions cluster appropriately by condition: bound sites in condition A should have higher occupancy scores in condition A than condition B if differential binding is real; visual inspection via PlotAggregate should show deeper footprints at high-occupancy sites.
- Confidence/p-value columns are present and show reasonable distribution; sites with extreme outlier occupancy scores should have correspondingly low confidence if signal is noisy.
- Output row count and motif coverage align with input: total reported binding sites should reflect the number of motif matches in the genome and peaks analyzed (spot-check using bedtools intersect or similar).

## Limitations

- BINDetect assumes that footprint depth/width at a motif site is a reliable proxy for TF occupancy; this may fail if multiple TFs bind in close proximity, if the motif PWM is poorly calibrated, or if chromatin remodeling obscures true occupancy patterns.
- Single-cell ATAC-seq analysis requires high-quality cell clustering and pseudobulk aggregation; the README explicitly notes that 'the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis' and recommends PEAKQC for cell QC beforehand.
- Motif database quality and specificity directly impact results; off-target motif matches or incomplete PWM sets will produce spurious occupancy calls. Cross-validation with independent data (e.g., ChIP-seq) is recommended.
- BINDetect is designed for bulk or well-aggregated ATAC-seq and may underperform on sparse, low-coverage, or degraded samples where footprints are weak or absent.
- No changelog is available (as noted in the article), limiting reproducibility and version-specific interpretation of occupancy thresholds or model changes.

## Evidence

- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [readme] TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data: "TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data"
- [other] Run TOBIAS BINDetect with the footprint scores and motif matches as input, comparing signal intensity at motif sites across experimental conditions to discriminate bound from unbound sites.: "Run TOBIAS BINDetect with the footprint scores and motif matches as input, comparing signal intensity at motif sites across experimental conditions to discriminate bound from unbound sites"
- [other] Parse BINDetect output table containing per-motif occupancy predictions, binding probabilities, and differential occupancy scores across conditions.: "Parse BINDetect output table containing per-motif occupancy predictions, binding probabilities, and differential occupancy scores across conditions"
- [readme] It is important to note that the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis.: "the quality of the single cells and the cell clustering is paramount for achieving a clean footprinting analysis"
- [readme] BINDetect: Estimation of differentially bound motifs based on scores, sequence and motifs: "BINDetect: Estimation of differentially bound motifs based on scores, sequence and motifs"
