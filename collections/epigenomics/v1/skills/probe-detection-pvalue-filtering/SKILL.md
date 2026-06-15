---
name: probe-detection-pvalue-filtering
description: Use when immediately after loading raw methylation array data (.idat files or beta-valued matrix) from HumanMethylation450 (450k) or EPIC arrays when conducting primary quality control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - ChAMP
  - ChAMPdata
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

# probe-detection-pvalue-filtering

## Summary

Remove low-quality DNA methylation probes by filtering out those with detection p-value > 0.01 using ChAMP's default filtering function. This is a standard quality-control step applied early in the 450k and EPIC array analysis pipeline to exclude probes with unreliable signal intensity measurements.

## When to use

Apply this skill immediately after loading raw methylation array data (.idat files or beta-valued matrix) from HumanMethylation450 (450k) or EPIC arrays when conducting primary quality control. Use it before normalization, type-2 probe correction, or downstream statistical analysis to ensure that only probes with confident detection calls are carried forward.

## When NOT to use

- Data has already undergone detection p-value filtering in an upstream pipeline
- Working with pre-filtered public datasets where probe quality has already been vetted
- Analysis requires retention of all probes, including low-confidence ones, for methodological reasons (e.g., benchmarking filtering algorithms themselves)

## Inputs

- Raw methylation array data from HumanMethylation450 or EPIC arrays (.idat files)
- Beta-valued matrix (M-values or beta values) from methylation arrays
- Detection p-value matrix (one p-value per probe per sample)

## Outputs

- Filtered probe matrix with low-confidence probes removed
- Pre- and post-filter probe count comparison
- Quality control report documenting filtering statistics

## How to apply

Load your 450k or EPIC methylation array dataset using ChAMP's data import functions (from .idat files or beta-valued matrix). Apply champ.filter() with default parameters, which automatically removes probes with detection p-value > 0.01 in the first filtering step. This threshold reflects Illumina's standard confidence threshold for detected signal above background noise. Verify filtering success by comparing probe counts before and after filtering; probes with p-value > 0.01 should be absent from the post-filter matrix. Document the number of probes retained and removed in a quality control report for transparency and reproducibility.

## Related tools

- **ChAMP** (Primary tool providing champ.filter() function with default detection p-value and bead count filtering) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package providing methylation array annotations and test datasets required for ChAMP analysis) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative or complementary package for DNA methylation array analysis and quality control)

## Examples

```
library(ChAMP); myLoad <- champ.load(directory='path/to/idat/files'); myFilter <- champ.filter(myLoad)
```

## Evaluation signals

- Pre-filter probe count should be higher than post-filter count; document the absolute and percentage of probes removed
- All remaining probes in the post-filter matrix should have detection p-value ≤ 0.01; spot-check the p-value distribution before and after
- Sample counts should remain unchanged; filtering removes probes, not samples
- Quality control plot should show clear separation between removed (p > 0.01) and retained (p ≤ 0.01) probes
- Filtered dataset should be compatible with downstream normalization and statistical analysis steps without errors

## Limitations

- Detection p-value threshold (0.01) is fixed by ChAMP's default; custom thresholds may require alternative tools or manual filtering
- Filtering is applied uniformly across all samples; no per-sample or per-group thresholds are available in the default champ.filter() function
- The method assumes that Illumina's detection p-value calculation is reliable; performance may degrade with degraded or contaminated samples
- champ.filter() applies two successive steps (detection p-value AND bead count filtering); if only p-value filtering is desired, the function cannot be split without custom code

## Evidence

- [other] champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe.: "champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01"
- [intro] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading"
- [intro] a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
- [intro] The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C): "The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)"
- [readme] Currently, ChAMPdata support: * 450K Array * EPIC V1 Array * EPIC V2 Array: "Currently, ChAMPdata support: * 450K Array * EPIC V1 Array * EPIC V2 Array"
