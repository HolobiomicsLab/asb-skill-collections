---
name: methylation-region-identification
description: Use when you have loaded normalized methylation beta-value matrices from Illumina EPIC or 450k arrays and need to move beyond single-CpG differential methylation testing to identify multi-CpG regions with coordinated differential methylation signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - ChAMP
  - ChAMPdata
  - Bumphunter
  - DMRcate
  - minfi
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# methylation-region-identification

## Summary

Identify differentially methylated regions (DMRs) in DNA methylation array data (EPIC or 450k) using ChAMP's integration of bumphunter-based detection. This skill applies statistical region-level analysis to detect contiguous genomic regions with coordinated methylation changes between sample groups.

## When to use

You have loaded normalized methylation beta-value matrices from Illumina EPIC or 450k arrays and need to move beyond single-CpG differential methylation testing to identify multi-CpG regions with coordinated differential methylation signals. Use this skill when your analysis goal requires region-level rather than probe-level inference, or when you want to aggregate statistical evidence across neighboring CpGs to improve power and biological interpretability.

## When NOT to use

- Your input is already a pre-computed feature matrix or region-level methylation summary (DMRs would be double-counted).
- You have fewer than ~3–4 samples per group, as bumphunter-based region detection relies on adequate statistical power from replicate samples.
- Your analysis requires fixed-width genomic windows rather than data-driven region boundaries (use fixed-window tiling instead).

## Inputs

- Normalized DNA methylation beta-value matrix (EPIC or 450k array)
- Sample group/phenotype labels
- ChAMP-compatible methylation object (from champ.load() or external normalization)

## Outputs

- List of detected differentially methylated regions (DMRs) with genomic coordinates
- DMR summary table (position, size, CpG count, statistical significance)
- DMR count summary

## How to apply

Load your normalized EPIC or 450k methylation dataset into ChAMP (either from .idat files or a pre-normalized beta-value matrix). Call champ.DMR() with bumphunter-based detection to scan the genome for contiguous regions of differential methylation across your sample groups. The function applies bumphunter's algorithm to identify candidate regions by smoothing and thresholding methylation differences, then filters regions based on minimum CpG count (regions with only 1–2 CpGs are excluded by default). Extract and count the detected DMRs from the function output; typical results on simulated EPIC data yield approximately 4700+ DMRs depending on the simulation parameters and CpG density filtering thresholds.

## Related tools

- **ChAMP** (Primary R package providing champ.DMR() function for bumphunter-based differentially methylated region detection) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package providing EPIC and 450k array annotations and reference datasets (e.g., EPICSimData) required by ChAMP) — https://github.com/YuanTian1991/ChAMPdata
- **Bumphunter** (Underlying statistical algorithm for region detection; integrated into ChAMP.DMR())
- **DMRcate** (Alternative DMR detection method available in ChAMP as comparison or alternative to bumphunter)
- **minfi** (Normalization methods (e.g., Functional Normalization) compatible with ChAMP preprocessing pipeline)

## Examples

```
library(ChAMP); data(EPICSimData); champ.dmr.result <- champ.DMR(arraytype='EPIC', method='bumphunter'); print(paste('Total DMRs detected:', nrow(champ.dmr.result[[1]])))
```

## Evaluation signals

- DMR count is consistent with expected range for your dataset and array type (e.g., ~4700+ for EPIC simulation data with default CpG filtering).
- Each detected DMR contains ≥3 CpGs (single-CpG and 2-CpG regions are excluded by champ.DMR()).
- DMR genomic coordinates are non-overlapping and span multiple consecutive array probes.
- Statistical significance (p-value or adjusted p-value) is reported for each DMR and is consistent with bumphunter's smoothing and permutation-based inference.
- Comparison with alternative DMR methods (DMRcate, Probe Lasso) shows substantial overlap in detected regions, confirming robustness.

## Limitations

- Simulated or real datasets containing very sparse CpG coverage may yield fewer DMRs than expected, because regions with only 1–2 CpGs are filtered out by champ.DMR().
- Bumphunter's performance depends on adequate sample replication within groups; small sample sizes (<3 per group) reduce statistical power.
- DMR detection is sensitive to the choice of methylation normalization method applied upstream; different normalization approaches (SWAN, BMIQ, Functional Normalization) can affect region boundaries and counts.
- The method assumes that nearby CpGs share coordinated methylation signals; highly fragmented or isolated differential signals may be missed.

## Evidence

- [intro] For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate: "For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate"
- [other] The EPIC simulation dataset contains fewer than 5000 DMRs (approximately 4700+) because some simulated DMRs contain only 1-2 CpGs, which are not regarded as DMRs in champ.DMR() function.: "The EPIC simulation dataset contains fewer than 5000 DMRs (approximately 4700+) because some simulated DMRs contain only 1-2 CpGs, which are not regarded as DMRs in champ.DMR() function."
- [intro] For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData): "For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData)"
- [intro] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods: "The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods"
