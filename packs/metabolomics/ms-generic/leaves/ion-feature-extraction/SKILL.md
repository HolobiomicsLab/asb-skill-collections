---
name: ion-feature-extraction
description: Use when you have raw mass-spectrometry data files (mzML, mzXML, or vendor
  formats) from untargeted metabolomics experiments and need to identify and quantify
  differential metabolic ion peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - openNAU
  - MetaQC
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: OpenNAU
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_opennau_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21147/j.issn.1000-9604.2023.05.11
  all_source_dois:
  - 10.21147/j.issn.1000-9604.2023.05.11
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-feature-extraction

## Summary

Extract aligned ion features from raw untargeted metabolomics mass-spectrometry data by detecting peaks across m/z and retention-time dimensions, aligning peaks across replicates, and consolidating them into a unified feature abundance matrix. This skill is essential for converting raw instrument output into quantifiable metabolic features for downstream statistical and annotation workflows.

## When to use

Apply this skill when you have raw mass-spectrometry data files (mzML, mzXML, or vendor formats) from untargeted metabolomics experiments and need to identify and quantify differential metabolic ion peaks. Use it as the first major processing step after data acquisition, before quality control filtering or statistical testing, to establish a consistent feature table across all samples.

## When NOT to use

- Input is already a processed feature table or abundance matrix — skip directly to quality control and statistical testing.
- Data is from targeted metabolomics with predefined m/z and retention-time windows — use targeted feature extraction instead.
- Raw data files are corrupted or missing critical metadata (m/z array, retention time, intensity values) — validate file integrity first.

## Inputs

- Raw mass-spectrometry data files in mzML format
- Raw mass-spectrometry data files in mzXML format
- Raw mass-spectrometry data files in vendor-specific formats

## Outputs

- Feature abundance matrix (rows: features with m/z, retention time, identifier; columns: sample intensities)
- Feature table with unified ion identifiers across replicates

## How to apply

Load raw mass-spectrometry files into the openNAU raw mass data extraction module and apply peak detection to identify ion signals across the m/z and retention-time dimensions. Apply peak alignment and feature grouping to consolidate peaks from replicate injections into unified features, ensuring that the same metabolic ion across technical replicates is represented as a single row. Extract intensity values for each feature across all samples and compile into a feature abundance matrix with rows representing features (identified by m/z, retention time, and unique identifier) and columns representing sample-wise intensities. Validate that alignment thresholds (m/z tolerance, retention-time window) are appropriate for your instrument and chromatographic method.

## Related tools

- **openNAU** (Performs raw mass data extraction, peak detection, peak alignment, feature grouping, and feature abundance matrix compilation for untargeted metabolomics) — https://github.com/zjuRong/openNAU
- **MetaQC** (Quality control component of openNAU for validation of extracted features) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Feature table has non-zero intensity values for each sample in the matrix and no missing values within aligned features across replicates.
- Replicate samples show correlated feature intensity profiles (e.g., Pearson r > 0.8 for technical replicates), indicating successful peak alignment.
- Number of extracted features is consistent with expected metabolic complexity for the organism/tissue and experimental design (no suspiciously low or high counts).
- Feature identifiers (m/z, retention time) are unique and non-redundant; no duplicate rows exist in the output table.
- m/z and retention-time values fall within instrument-specific expected ranges and show expected distributions (e.g., m/z > 50, retention time > 0).

## Limitations

- Peak detection sensitivity depends on signal-to-noise ratio; low-abundance features may be missed, particularly in complex samples with high background noise.
- Peak alignment relies on retention-time consistency; poor chromatographic reproducibility or instrument drift can lead to misalignment or duplicate features.
- Requires careful tuning of m/z and retention-time tolerance parameters for each instrument platform; suboptimal thresholds can cause under- or over-grouping of features.
- Features cannot be annotated or validated to specific metabolites at this step; further database matching and confirmation are required downstream.

## Evidence

- [other] Peak detection and alignment rationale: "Apply peak detection to identify ion signals across the mass-to-charge and retention-time dimensions. Perform peak alignment and feature grouping to consolidate peaks from replicate injections into"
- [other] Output specification: "Output the extracted feature table with rows as features (m/z, retention time, identifier) and columns as sample intensities."
- [other] Input file format support: "Load raw mass-spectrometry data files (mzML, mzXML, or vendor formats) into the openNAU raw mass data extraction module."
- [readme] Software integration and scope: "It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks."
- [readme] Complete workflow establishment: "Finally, a complete analysis system platform for untargeted metabolomics was established."
