---
name: tf-binding-site-classification
description: Use when you have aligned ATAC-seq BAM files, corrected Tn5 insertion bias and computed footprint scores (via TOBIAS ATACorrect and ScoreBigwig), a motif database in JASPAR or compatible format, and you need to assign occupancy states (bound/unbound) and confidence scores at specific TF binding.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0445
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_0749
  tools:
  - TOBIAS
  - TOBIAS BINDetect
  - TOBIAS ScoreBigwig
  - TOBIAS ATACorrect
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

Classify transcription factor binding sites as bound or unbound by comparing footprint depletion scores at known motif locations across ATAC-seq conditions, using TOBIAS BINDetect to generate per-motif occupancy predictions and differential binding metrics. This skill bridges nucleosome-free chromatin signal analysis to discrete binding state estimates required for regulatory network interpretation.

## When to use

You have aligned ATAC-seq BAM files, corrected Tn5 insertion bias and computed footprint scores (via TOBIAS ATACorrect and ScoreBigwig), a motif database in JASPAR or compatible format, and you need to assign occupancy states (bound/unbound) and confidence scores at specific TF binding sites to compare binding changes across experimental conditions (e.g., early embryo development timepoints, treatment vs. control).

## When NOT to use

- Input is single-end ATAC-seq with very low read depth (<5M reads per sample); footprints will be too noisy to reliably detect binding occupancy.
- You are analyzing ChIP-seq or CUT&RUN data instead of ATAC-seq; this skill is specifically designed for footprint-based inference from transposase insertion patterns and will not apply to antibody-enriched chromatin.
- Motif database is not in a TOBIAS-compatible format (JASPAR, TRANSFAC, MEME); format conversion via TOBIAS FormatMotifs is required first.
- Footprint scores have not been corrected for Tn5 insertion bias; uncorrected scores will produce systematic false positives at sequence-biased sites unrelated to protein binding.

## Inputs

- Aligned ATAC-seq BAM file(s) with corrected Tn5 cutsites
- Footprint score bigWig file(s) (output from TOBIAS ScoreBigwig)
- Motif database in JASPAR or TRANSFAC format (PWM file)
- Peak/open chromatin regions in BED format (optional, for restricting analysis scope)
- Sample metadata or condition labels (for comparing across treatments/timepoints)

## Outputs

- BINDetect results table (TSV/CSV) with columns: motif_id, chrom, start, end, occupancy_state (bound/unbound), binding_probability, p_value, log2_fold_change (if multi-condition)
- Per-motif summary statistics (total sites called, fraction bound per condition)
- Visualization-ready BED files of bound TFBS coordinates
- Differential occupancy ranking (motifs with largest condition-specific changes)

## How to apply

Load corrected footprint score bigWig files and scan a motif database (JASPAR-format PWMs) across the genome to identify candidate TF binding sites. Run TOBIAS BINDetect with footprint scores, motif match coordinates, and sample condition metadata to compute per-motif binding probabilities and occupancy estimates by comparing signal intensity at bound vs. flanking sequences. BINDetect applies a statistical model that distinguishes high footprint depletion (protein-bound) from baseline chromatin accessibility. Parse the BINDetect output table to extract occupancy predictions, binding probability scores, and condition-specific differential occupancy metrics. Format results as a structured CSV/TSV with columns for TF motif ID, genomic coordinates (chr:start-end), occupancy state assignment, confidence/p-value, and quantitative binding metrics per condition. The occupancy call relies on the underlying assumption that protein binding creates measurable Tn5 insertion depletion patterns detectable above noise.

## Related tools

- **TOBIAS BINDetect** (Core tool for computing binding occupancy predictions from footprint scores and motif matches; outputs per-motif occupancy table and differential binding statistics) — https://github.com/loosolab/TOBIAS
- **TOBIAS ScoreBigwig** (Prerequisite: calculates footprint depletion scores from bias-corrected ATAC-seq cutsites, which BINDetect uses as input signal) — https://github.com/loosolab/TOBIAS
- **TOBIAS ATACorrect** (Prerequisite: corrects Tn5 insertion bias in ATAC-seq cutsite signal before footprint scoring) — https://github.com/loosolab/TOBIAS
- **TOBIAS FormatMotifs** (Utility to convert and standardize motif database formats (JASPAR, TRANSFAC, MEME) for use with BINDetect) — https://github.com/loosolab/TOBIAS
- **TOBIAS PlotAggregate / PlotHeatmap** (Visualization tools to aggregate footprint signals at predicted bound vs. unbound sites, for visual validation of occupancy calls) — https://github.com/loosolab/TOBIAS

## Examples

```
TOBIAS BINDetect --signals corrected_footprints.bw --motifs jaspar_motifs.txt --genome genome.fa --peaks open_regions.bed --outdir bindetect_results --cores 8
```

## Evaluation signals

- Output BINDetect table contains non-null entries for occupancy_state (bound/unbound) for >90% of motif sites; missing calls indicate convergence or filtration issues in the statistical model.
- Binding probability scores are bounded in [0, 1] and show distinct bimodal or left-skewed distribution (many unbound sites with low probability, fewer high-probability bound sites), consistent with sparse occupancy in open chromatin.
- Footprint visualization at predicted bound sites (via PlotAggregate) shows visible Tn5 insertion depletion centered on the motif, whereas unbound sites show uniform accessibility; mismatches suggest poor occupancy prediction.
- Differential occupancy metrics (log2_fold_change, p_value) are statistically meaningful and replicate across biological replicates; large variance between replicates suggests noise or inadequate bias correction.
- Top differentially occupied motifs correspond to known developmental regulators or condition-relevant factors (e.g., pluripotency factors in embryonic samples, cell-type-specific TFs in differentiated samples); random or implausible TF hits indicate overfitting or poor filtering.

## Limitations

- TOBIAS footprinting assumes that protein binding creates detectable Tn5 insertion depletion; weak-binding or transient interactions may not produce sufficient signal to discriminate from noise, leading to false negatives in occupancy calling.
- The method relies on high-quality motif databases; incomplete, redundant, or low-specificity PWMs will produce spurious binding predictions and confound differential occupancy estimates.
- Originally developed for bulk ATAC-seq; application to single-cell ATAC-seq (scATAC-seq) requires generating pseudobulk BAM files from cell-type clusters, and quality depends critically on cell clustering and per-cell sequencing depth.
- Occupancy predictions are relative to footprint signal and do not directly measure binding kinetics or absolute occupancy fraction; quantitative interpretation requires comparison across conditions or cell types.
- No changelog or version tracking provided in the README; reproducibility across software versions or parameter tuning (BINDetect threshold settings) is not explicitly documented.

## Evidence

- [readme] the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_: "the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_"
- [other] TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data, enabling detection of transcription factor occupancy through analysis of Tn5 insertion patterns: "TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data"
- [other] Run TOBIAS BINDetect with the footprint scores and motif matches as input, comparing signal intensity at motif sites across experimental conditions to discriminate bound from unbound sites.: "Run TOBIAS BINDetect with the footprint scores and motif matches as input, comparing signal intensity at motif sites across experimental conditions to discriminate bound from unbound sites"
- [other] Parse BINDetect output table containing per-motif occupancy predictions, binding probabilities, and differential occupancy scores across conditions.: "Parse BINDetect output table containing per-motif occupancy predictions, binding probabilities, and differential occupancy scores across conditions"
- [readme] Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from scATAC-seq cell type clusters.: "Although TOBIAS was originally developed for bulk experiments, it can also be applied to single-cell resolution data. To do that, we recommend generating individual pseudobulk BAM files from"
- [readme] Estimation of bound/unbound transcription factor binding sites: "Estimation of bound/unbound transcription factor binding sites"
