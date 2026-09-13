---
name: peak-detection-mass-spectrometry
description: Use when you have raw mass-spectrometry data files (mzML, mzXML, or vendor
  formats) from untargeted metabolomics experiments and need to extract differential
  metabolic ion peaks for downstream statistical or annotation analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - openNAU
  - MetaQC
  - MARC
  techniques:
  - LC-MS
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

# peak-detection-mass-spectrometry

## Summary

Identify ion signals across mass-to-charge and retention-time dimensions in raw untargeted metabolomics data to construct a feature abundance matrix. This is the first quantitative step in untargeted metabolomics pipelines that transforms vendor or mzML/mzXML files into aligned, intensity-normalized feature tables.

## When to use

You have raw mass-spectrometry data files (mzML, mzXML, or vendor formats) from untargeted metabolomics experiments and need to extract differential metabolic ion peaks for downstream statistical or annotation analysis. This skill is essential when your starting point is unprocessed chromatographic–mass data and your goal is a unified feature abundance matrix across replicate injections.

## When NOT to use

- Input is already a processed feature table or abundance matrix — peak detection has already been applied.
- Data is from targeted metabolomics with predefined m/z and retention-time windows — use targeted extraction methods instead.
- Raw data files are corrupted or in unsupported formats — preprocessing or format conversion is required first.

## Inputs

- Raw mass-spectrometry data files in mzML format
- Raw mass-spectrometry data files in mzXML format
- Vendor-specific mass spectrometry raw data formats

## Outputs

- Feature abundance matrix (rows = features with m/z, retention time, identifier; columns = sample intensities)
- Aligned and grouped feature table
- Peak detection report with quality control metrics

## How to apply

Load raw mass-spectrometry data into the openNAU raw mass data extraction module. Apply peak detection to identify ion signals across the mass-to-charge and retention-time dimensions. Perform peak alignment to consolidate peaks from replicate injections and feature grouping to unify signals. Extract intensity values for each feature across all samples and compile into a feature abundance matrix with rows as features (defined by m/z, retention time, and identifier) and columns as sample intensities. Quality control is applied during this process to filter noise and confirm peak fidelity.

## Related tools

- **openNAU** (Raw mass data extraction module for untargeted metabolomics; performs peak detection, alignment, and feature grouping on vendor or mzML/mzXML files) — https://github.com/zjuRong/openNAU
- **MetaQC** (Quality control for identification of differential metabolic ion peaks within the openNAU platform) — https://github.com/zjuRong/openNAU
- **MARC** (Reference metabolomics database construction and annotation integration within openNAU) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Feature abundance matrix schema: rows contain m/z and retention-time identifiers; columns contain sample-level intensities; no null values in intensity columns.
- Peak alignment quality: replicates of the same biological sample cluster with consistent feature m/z and retention-time values (tolerance thresholds should be documented, e.g., ±5 ppm in m/z).
- Feature count stability: the number of detected features is consistent across batches of similar samples and matches expected metabolite diversity for the organism/tissue type.
- Intensity distribution: feature intensity values span expected dynamic range (typically 2–3 orders of magnitude); no single feature dominates >50% of total signal unless it is a known dominant metabolite.
- Quality control metrics: reported number of detected peaks, aligned features, and filtered noise peaks should document data reduction rationale.

## Limitations

- Peak detection sensitivity depends on signal-to-noise ratio; low-abundance features may be missed in complex matrices.
- Peak alignment assumes consistent retention-time shifts across replicates; severe instrumental drift can degrade feature consolidation.
- The software requires appropriate parameter tuning for different mass-spectrometry instruments and ionization methods; default parameters may not suit all metabolomics workflows.
- Feature grouping does not resolve isomeric or isobaric ions; post-hoc annotation and MS/MS fragmentation data are required for confident metabolite assignment.

## Evidence

- [other] Load raw mass-spectrometry data files (mzML, mzXML, or vendor formats) into the openNAU raw mass data extraction module. Apply peak detection to identify ion signals across the mass-to-charge and retention-time dimensions.: "Load raw mass-spectrometry data files (mzML, mzXML, or vendor formats) into the openNAU raw mass data extraction module. Apply peak detection to identify ion signals across the mass-to-charge and"
- [other] Perform peak alignment and feature grouping to consolidate peaks from replicate injections into unified features. Extract intensity values for each feature across all samples and compile into a feature abundance matrix.: "Perform peak alignment and feature grouping to consolidate peaks from replicate injections into unified features. Extract intensity values for each feature across all samples and compile into a"
- [readme] The software includes extraction of raw mass data and quality control for the identification of differential metabolic ion peaks.: "The software includes extraction of raw mass data and quality control for the identification of differential metabolic ion peaks."
- [readme] A complete analysis system platform for untargeted metabolomics was established.: "A complete analysis system platform for untargeted metabolomics was established."
