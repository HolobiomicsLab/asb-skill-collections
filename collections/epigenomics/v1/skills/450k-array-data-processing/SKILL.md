---
name: 450k-array-data-processing
description: Use when you have raw .idat files or beta-valued matrices from HumanMethylation450 (450k) arrays and need to remove low-quality probes, correct for technical artifacts (batch effects, type-2 probe bias), and normalize the data before performing differential methylation analysis or DMR detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3238
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0091
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
  - ComBat
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

# 450k-array-data-processing

## Summary

Comprehensive quality control and preprocessing pipeline for Illumina HumanMethylation450 array data, encompassing probe filtering, normalization, batch correction, and type-2 probe adjustment to produce a curated methylation matrix suitable for downstream statistical analysis.

## When to use

Apply this skill when you have raw .idat files or beta-valued matrices from HumanMethylation450 (450k) arrays and need to remove low-quality probes, correct for technical artifacts (batch effects, type-2 probe bias), and normalize the data before performing differential methylation analysis or DMR detection.

## When NOT to use

- Input is already a normalized, batch-corrected, publication-ready feature table from a prior preprocessing study
- You are analyzing EPIC array data (use EPIC-specific parameters and annotation instead)
- Raw signal intensities or unnormalized .idat files are not available and cannot be recovered

## Inputs

- .idat files from HumanMethylation450 array experiments
- Beta-valued methylation matrix (probes × samples)

## Outputs

- Filtered and normalized beta-valued methylation matrix
- Quality control report (probe counts before/after filtering, bead count distributions)
- QC plots (detection p-value distributions, bead count histograms, batch effect visualizations)

## How to apply

Load raw 450k array data using ChAMP's data import functions (from .idat files or a beta-valued matrix). Apply champ.filter() with default parameters to remove probes with detection p-value > 0.01 and probes with fewer than 3 beads in at least 5% of samples. Select a type-2 probe correction method (SWAN, Peak Based Correction, or BMIQ—BMIQ is default). Apply functional normalization or other available normalization approaches. If batch effects are detected via SVD analysis, apply ComBat correction. Generate QC plots and a filtered probe matrix documenting the number of probes retained and removed at each filtering step. The rationale is that these sequential steps remove unreliable measurements, correct systematic biases introduced by array chemistry and batching, and ensure the final methylation values are comparable across samples.

## Related tools

- **ChAMP** (Primary pipeline for data import, filtering, normalization, batch effect analysis and correction, type-2 probe correction, and differential methylation detection on 450k arrays) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data package providing CpG-probe manifests and annotation for 450k arrays; must be installed alongside ChAMP) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative/complementary package offering functional normalization and other 450k analysis methods integrated into ChAMP)
- **ComBat** (Batch effect correction method implemented in ChAMP for correction of multiple batch effects)

## Examples

```
library(ChAMP); myLoad <- champ.load(directory='./idat_files/'); myFiltered <- champ.filter(myLoad); myNorm <- champ.norm(myFiltered, method='BMIQ'); myCombat <- champ.runCombat(myNorm, pd=pheno)
```

## Evaluation signals

- Pre- and post-filter probe counts agree with expected removal rates for detection p-value > 0.01 threshold
- Bead count distributions show that probes with < 3 beads in ≥ 5% of samples have been successfully removed
- QC plots (e.g., methylation density plots) exhibit expected distributions after normalization and show reduced batch effects post-ComBat correction
- Normalized beta-values fall within the expected [0, 1] range with no missing values after filtering
- SVD analysis post-filtering shows batch effects have been adequately controlled or corrected, as evidenced by reduced batch-associated variance

## Limitations

- Default filtering thresholds (detection p-value > 0.01, < 3 beads in ≥ 5% of samples) may be suboptimal for datasets with very low or very high sample sizes; threshold adjustment may be needed
- Type-2 probe bias correction methods (SWAN, PBC, BMIQ) assume consistent probe performance across samples; severe technical artifacts or unusual sample compositions may not be fully corrected
- ComBat batch correction assumes batch effects are primarily additive and does not model interactions between batch and biological covariates; inappropriate batch variable specification can introduce bias
- The article/README does not provide guidance on parameter tuning for normalization method selection; choice between functional normalization and alternatives requires domain knowledge or empirical validation

## Evidence

- [other] champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe.: "champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples"
- [readme] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods: "The ChAMP package is designed for the analysis of Illumina Methylation beadarray data (EPIC and 450k) and provides a pipeline that integrates currently available 450k and EPIC analysis methods"
- [intro] Type-2 probe correction methods include SWAN, Peak Based Correction (PBC) and BMIQ (the default choice): "Type-2 probe correction methods include SWAN, Peak Based Correction (PBC) and BMIQ (the default choice)"
- [intro] for correction of multiple batch effects the ComBat method has been implemented: "for correction of multiple batch effects the ComBat method has been implemented"
- [intro] a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
