---
name: dna-methylation-block-detection-analysis
description: Use when you have loaded normalized methylation data from EPIC or 450k arrays and need to identify differentially methylated blocks rather than individual CpG sites or DMRs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0654
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
  - Shiny
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

# dna-methylation-block-detection-analysis

## Summary

Detection and visualization of differentially methylated blocks (DMBs) in EPIC and 450k DNA methylation array data using ChAMP's champ.Block() function. This skill identifies contiguous genomic regions with coordinated differential methylation patterns that may represent functional regulatory units.

## When to use

Apply this skill when you have loaded normalized methylation data from EPIC or 450k arrays and need to identify differentially methylated blocks rather than individual CpG sites or DMRs. Use it after quality control, normalization, and batch correction are complete, and when you have defined comparison groups (case vs. control) in your sample metadata.

## When NOT to use

- Input data has not been normalized and batch-corrected; quality control and preprocessing must precede block detection
- You need single-CpG-level differential methylation analysis rather than regional/block-level patterns—use probe-level DMR detection (champ.DMR with Probe Lasso, Bumphunter, or DMRcate) instead
- Sample size is very small (< 4 samples per group) or phenotype groups are not clearly defined in metadata

## Inputs

- Normalized beta-value matrix (numeric matrix with CpG probes as rows, samples as columns)
- ExpressionSet object containing methylation data and sample metadata
- Sample phenotype/group labels (e.g., case/control assignments)

## Outputs

- Block detection results table (genomic coordinates, effect sizes, p-values)
- Block.GUI() interactive visualization interface
- Differentially methylated block annotations with probe ranges and statistical summaries

## How to apply

Load the preprocessed methylation dataset (beta-value matrix or ExpressionSet object) into the R environment. Call champ.Block() with the appropriate arraytype parameter (either 'EPIC' or '450K') to detect contiguous blocks of differential methylation across your sample groups. The function will perform block-level statistical testing to identify regions where multiple adjacent probes show coordinated methylation differences. Launch the Block.GUI() interactive visualization interface to inspect, filter, and explore detected blocks by genomic location, effect size, and statistical significance. Verify output by checking that block boundaries align with genomic features and that the number and magnitude of detected blocks are consistent with the expected biology of your comparison (note: negative results—absence of blocks—may be valid for certain datasets, particularly simulation data).

## Related tools

- **ChAMP** (Primary tool for executing champ.Block() function and Block.GUI() visualization interface) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Provides CpG probe annotations and array manifests required for block coordinate mapping) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative or complementary tool for methylation array normalization prior to block detection)
- **Shiny** (Underlying framework for Block.GUI() interactive visualization interface)

## Examples

```
data(EPICSimData); champ.Block(arraytype='EPIC'); Block.GUI()
```

## Evaluation signals

- Block detection runs without error and returns a non-empty or appropriately empty results table depending on the dataset (e.g., simulation data such as EPICSimData may legitimately yield no blocks)
- Block coordinates (start, end, chromosome) align with valid genomic ranges and respect probe ordering on the array
- Block.GUI() launches successfully and renders block annotations with interactive filtering and visualization controls
- Statistical measures (p-values, effect sizes) fall within expected ranges (e.g., p-values in [0,1], effect sizes bounded by beta-value range [0,1])
- Detected blocks show concordance with probe-level DMR results when both block and DMR analyses are performed on the same dataset

## Limitations

- Block detection sensitivity depends on normalization quality and batch correction; inadequate preprocessing may produce spurious or missed blocks
- Synthetic or highly balanced simulation datasets (e.g., EPICSimData) may legitimately yield zero differentially methylated blocks, which is expected behavior and not a failure
- Block detection is designed for EPIC and 450k arrays; EPICv2 support requires ChAMP version 2.29.1 or later used with ChAMPdata >= 2.23.1
- The method requires contiguous probe coverage; sparse or gapped probe regions may not form coherent blocks
- No methods section was available in the source article to detail statistical thresholds, block size criteria, or p-value adjustment strategies used by champ.Block()

## Evidence

- [intro] For users who need to find Differentially Methylated Blocks, the new version of ChAMP includes a function to detect these: "For users who need to find Differentially Methylated Blocks, the new version of ChAMP includes a function to detect these"
- [other] Call champ.Block() function with arraytype='EPIC' to perform differentially methylated block detection on the simulation dataset.: "Call champ.Block() function with arraytype='EPIC' to perform differentially methylated block detection on the simulation dataset."
- [other] Launch Block.GUI() interactive interface to visualize and inspect the block detection results.: "Launch Block.GUI() interactive interface to visualize and inspect the block detection results."
- [other] No differentially methylated blocks are detected when champ.Block() is executed on the EPICSimData simulation dataset with arraytype='EPIC' parameter.: "No differentially methylated blocks are detected when champ.Block() is executed on the EPICSimData simulation dataset with arraytype='EPIC' parameter."
- [readme] Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"
