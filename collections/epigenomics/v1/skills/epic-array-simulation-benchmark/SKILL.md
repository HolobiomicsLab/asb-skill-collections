---
name: epic-array-simulation-benchmark
description: Use when when developing or validating a DNA methylation array analysis pipeline using ChAMP, you need an independent ground-truth dataset to confirm that DMR detection is working correctly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3295
  tools:
  - ChAMP
  - ChAMPdata
  - Bumphunter
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

# epic-array-simulation-benchmark

## Summary

Validate DMR detection pipelines by reproducing expected DMR counts from the EPICSimData simulation dataset using ChAMP's bumphunter-based method. This skill benchmarks whether a methylation analysis workflow correctly identifies simulated differentially methylated regions and reveals detection thresholds (e.g., minimum CpG count per DMR).

## When to use

When developing or validating a DNA methylation array analysis pipeline using ChAMP, you need an independent ground-truth dataset to confirm that DMR detection is working correctly. The EPICSimData simulation dataset is purpose-built for this: it contains synthetically injected DMRs with known locations and sizes, making it ideal for verifying that your champ.DMR() implementation produces the expected number of detected regions and behaves consistently with published benchmarks.

## When NOT to use

- Input data is real patient or tissue samples, not a simulation — use this skill only for benchmarking; real data requires domain-specific interpretation and validation against biological phenotypes.
- You need to detect DMRs in a dataset where some regions legitimately contain only 1–2 CpGs — bumphunter's minimum CpG threshold may filter valid signal; consider alternative methods (Probe Lasso, DMRcate) if single-probe regions are biologically relevant.
- The goal is to identify cell-type-specific methylation patterns or infer cell composition — simulation benchmarking does not validate biological applicability in heterogeneous tissue samples.

## Inputs

- EPICSimData methylation beta-value matrix (loaded via data(EPICSimData))
- ChAMP-compatible EPIC array annotation and sample metadata

## Outputs

- DMR detection result object with list of identified regions
- DMR count (integer; expected ~4700+)
- DMR genomic coordinates and statistics (chr, start, end, p-value, etc.)

## How to apply

Load the EPICSimData simulation dataset in R using data(EPICSimData), then execute the champ.DMR() function with the bumphunter-based detection method on the loaded methylation matrix. Extract and count the number of DMRs from the function output. Compare the observed count to the expected range (approximately 4700 or higher). If the count is significantly lower than expected, investigate whether the detection method is filtering out simulated DMRs that contain fewer than the minimum required CpGs (typically 2–3 CpGs per region in bumphunter). This reveals whether your normalization and preprocessing steps are preserving signal fidelity or whether detection thresholds need adjustment.

## Related tools

- **ChAMP** (Core DMR detection pipeline; executes champ.DMR() with bumphunter backend to identify differentially methylated regions in EPIC array data) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Provides EPICSimData simulation dataset, EPIC array annotations, and probe manifests required for loading and interpreting the benchmark dataset) — https://github.com/YuanTian1991/ChAMPdata
- **Bumphunter** (Underlying bumphunter-based DMR detection algorithm integrated into ChAMP; applies spatial clustering and statistical testing to identify regions of coordinated methylation change)
- **minfi** (Optional preprocessing and normalization (e.g., Functional Normalization) used upstream of ChAMP DMR detection)

## Examples

```
data(EPICSimData); champ_dmr <- champ.DMR(beta=EPICSimData$beta, pheno=EPICSimData$pd$Sample_Group, method='bumphunter'); length(champ_dmr$BumphunterDMR)
```

## Evaluation signals

- DMR count is within expected range (≥4700 detected regions); significant deviation suggests preprocessing or detection parameter misconfiguration.
- Simulated DMRs with 3+ CpGs are consistently recovered; simulated DMRs with 1–2 CpGs are filtered out, consistent with bumphunter's minimum region size threshold.
- Statistical power and false discovery rate are consistent with published ChAMP/bumphunter benchmarks (e.g., FDR < 0.05 for detected regions).
- DMR genomic coordinates (chr, start, end) overlap expected simulation injection regions; validate by comparing detected vs. injected DMR positions.
- Reproducibility across multiple runs with identical inputs yields identical or near-identical DMR counts and region sets (no stochastic variation beyond random seed control).

## Limitations

- EPICSimData contains synthetically injected DMRs and may not capture real-world confounders (batch effects, cell-type heterogeneity, tissue-specific background noise) present in clinical samples.
- Bumphunter requires minimum region size (typically 2–3 CpGs); simulated regions below this threshold are discarded by design, reducing observed vs. expected DMR count. If your pipeline must detect single-CpG signals, use alternative methods (Probe Lasso, DMRcate).
- Benchmark results depend on upstream preprocessing steps (normalization method, Type-2 probe correction, batch adjustment); if preprocessing differs from the original simulation study, DMR recovery may change.
- The simulation does not reflect all EPIC array design features (e.g., cross-reactive probes, SNP-affected CpGs); validation on real data is still required before clinical application.

## Evidence

- [other] Finding from task_id=task_003 on expected DMR count and threshold behavior: "The EPIC simulation dataset contains fewer than 5000 DMRs (approximately 4700+) because some simulated DMRs contain only 1-2 CpGs, which are not regarded as DMRs in champ.DMR() function."
- [other] Workflow for loading and running DMR detection on EPICSimData: "Load EPICSimData simulation dataset using data(EPICSimData) in R. Execute champ.DMR() function on the loaded EPIC simulation data to detect differentially methylated regions using the"
- [intro] ChAMP overview and integration of DMR detection methods: "For the identification of Differentially Methylated Regions (DMRs), ChAMP offers the new Probe Lasso method, in addition to previous DMR detection functions Bumphunter and DMRcate"
- [intro] EPICSimData availability and loading procedure: "For the EPIC Simulation Data Set, user may use following code to load it: data(EPICSimData)"
- [intro] ChAMP comprehensive pipeline scope: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
