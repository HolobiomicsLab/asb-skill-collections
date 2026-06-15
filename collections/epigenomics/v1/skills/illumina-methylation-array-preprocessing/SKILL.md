---
name: illumina-methylation-array-preprocessing
description: Use when your input is raw .idat files or a beta-valued matrix from Illumina HumanMethylation450 or EPIC arrays, and you need to remove unreliable probes (those with detection p-value > 0.01 or insufficient bead counts) before performing differential methylation or other downstream analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3674
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
  - BMIQ
  - SWAN
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

# Illumina methylation array preprocessing

## Summary

Preprocessing and quality control of Illumina methylation array data (450K and EPIC) via detection p-value and bead count filtering, followed by type-2 probe correction and normalization. This skill removes low-quality probes and corrects technical biases prior to downstream analysis.

## When to use

Your input is raw .idat files or a beta-valued matrix from Illumina HumanMethylation450 or EPIC arrays, and you need to remove unreliable probes (those with detection p-value > 0.01 or insufficient bead counts) before performing differential methylation or other downstream analyses. Apply this skill early in the pipeline when data quality and probe reliability directly affect downstream statistical power.

## When NOT to use

- Input is already a curated, pre-normalized feature matrix from a published study without raw .idat or detection p-value metadata — skip to downstream analysis.
- Your array platform is not Illumina 450K or EPIC (e.g., custom or non-Illumina bisulfite sequencing data) — choose a platform-specific preprocessing pipeline.
- You have already applied aggressive probe filtering (< 5,000 probes remaining) — additional filtering may eliminate too much data to support statistical inference.

## Inputs

- .idat files (raw Illumina methylation intensity data)
- beta-valued matrix (pre-imported methylation beta values)
- HumanMethylation450 or EPIC array sample metadata (sample IDs, phenotypes)

## Outputs

- Filtered and normalized beta-value matrix
- Quality control report (probes retained vs. removed, detection p-value and bead count distributions)
- Corrected type-2 probe intensity values
- Batch-effect diagnostics (optional SVD visualizations)

## How to apply

Load the raw methylation array data using ChAMP's data import functions (from .idat files or a beta-valued matrix). Apply champ.filter() with default parameters to execute two successive filtering steps: (1) removal of probes with detection p-value > 0.01, indicating unreliable signal, and (2) removal of probes with fewer than 3 beads in at least 5% of samples, which reflects insufficient technical replication. After filtering, apply type-2 probe correction using SWAN, PBC, or BMIQ (default is BMIQ) to adjust for the distinct hybridization kinetics of Infinium type-2 probes. Finally, apply Functional Normalization or another normalization method to correct for technical variation while preserving biological signal. Document probe retention rates and quality metrics (detection p-value distributions, bead count distributions pre- and post-filtering) to validate the filtering and correction steps.

## Related tools

- **ChAMP** (Main preprocessing and analysis pipeline for Illumina methylation arrays; provides data loading, filtering, type-2 probe correction, normalization, and quality control functions) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (Data and annotation package supporting ChAMP; provides CpG-probe manifests and test datasets for 450K, EPIC v1, EPIC v2, and mouse arrays) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (Alternative methylation array analysis package offering Functional Normalization and other preprocessing methods compatible with ChAMP)
- **BMIQ** (Type-2 probe correction method (default in ChAMP) to adjust for Infinium type-2 probe bias)
- **SWAN** (Alternative type-2 probe correction method available in ChAMP)

## Evaluation signals

- Probe count comparison: pre-filter vs. post-filter probe counts should show removal of probes with detection p-value > 0.01; exact retention percentage should be documented.
- Bead count distribution: verify that probes with < 3 beads in ≥ 5% of samples are removed by examining bead count histograms before and after filtering.
- Detection p-value distribution: all remaining probes should have detection p-value ≤ 0.01; no probes in the filtered matrix should exceed this threshold.
- Type-2 probe correction validation: type-2 probe beta values should show reduced systematic bias relative to type-1 probes (visible as reduced clustering by probe type in quality control plots).
- Quality control report completeness: documentation must include number of probes retained/removed, reason codes (detection p-value vs. bead count), and summary statistics for both filtering stages.

## Limitations

- Default filtering thresholds (detection p-value > 0.01, < 3 beads in ≥ 5% samples) may be overly stringent for small sample sets or underpowered studies, reducing probe coverage.
- No methods section was provided in the source article, so filter step rationale and alternative parameter choices are not explicitly justified.
- ChAMP development version (GitHub) is noted as 'under intensive modification and upgrade'; users should rely on the formally released Bioconductor version for stable, peer-reviewed implementations.
- Functional Normalization requires sufficient samples (typically ≥ 8) to estimate control probe variation; small pilot studies may require alternative normalization strategies.
- SVD batch effect diagnostics require metadata on known batch variables; unmeasured or confounded batch factors will not be detected.

## Evidence

- [other] champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe.: "champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per"
- [readme] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] Type-2 probe correction methods include SWAN, Peak Based Correction (PBC) and BMIQ (the default choice): "Type-2 probe correction methods include SWAN, Peak Based Correction (PBC) and BMIQ (the default choice)"
- [intro] The popular Functional Normalization function offered by the minfi package is also available: "The popular Functional Normalization function offered by the minfi package is also available"
- [intro] a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
- [readme] Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1: "Current latest version: `2.29.1`, which support EPICv2, but it must be used along with ChAMPdata >= 2.23.1"
