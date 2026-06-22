---
name: peak-detection-and-mass-alignment
description: Use when when you have raw LC-MS/MS data files (.mzML, .raw, or vendor formats) from multiple samples and need to identify reproducible molecular features across the cohort before annotation or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MZmine2
  - Optimus
  - OpenMS
  techniques:
  - LC-MS
  - direct-infusion-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
- '[Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)'
- or [Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-detection-and-mass-alignment

## Summary

Automated detection of LC-MS peaks across all samples and alignment of their m/z and retention time dimensions to construct a unified, sample-normalized feature list. This is the foundational preprocessing step that converts raw MS/MS data into quantifiable molecular features for downstream molecular networking and bioassay correlation.

## When to use

When you have raw LC-MS/MS data files (.mzML, .raw, or vendor formats) from multiple samples and need to identify reproducible molecular features across the cohort before annotation or statistical analysis. Trigger this skill whenever you aim to compare molecular composition across samples or link molecular features to bioassay results.

## When NOT to use

- Input is already a preprocessed feature table or quantification matrix—skip to annotation or statistical analysis.
- Data is from direct-infusion MS (no chromatography separation)—use alternative peak clustering strategies that do not rely on retention time alignment.
- Samples are highly heterogeneous in LC gradient, column chemistry, or instrument tuning—alignment will fail or produce spurious features; re-harmonize acquisition parameters first.

## Inputs

- raw LC-MS/MS data files (mzML, NetCDF, or vendor formats)
- sample metadata or experimental design file (optional for batch processing)

## Outputs

- feature quantification matrix (CSV or tabular format) with m/z, retention time, and per-sample intensities
- aligned feature list with unified m/z and retention time coordinates
- MS/MS spectral summary (.MGF file or equivalent) for downstream annotation

## How to apply

Load raw MS/MS data files into MZmine2 or Optimus (OpenMS-based). Apply mass detection to identify peaks across all samples using appropriate instrument-specific parameters (e.g., noise level, minimum peak height). Build chromatogram features by grouping detected peaks within tolerance windows for both m/z and retention time dimensions. Align features across samples to construct a unified feature list, then fill missing feature values across samples where peaks were not detected in certain runs. Export the processed feature table with m/z, retention time, and per-sample abundance columns. Validate that the output feature table contains consistent m/z precision (typically ≤5 ppm for high-resolution MS) and retention time alignment, with minimal missing values after gap-filling.

## Related tools

- **MZmine2** (Open-source tool for mass detection, peak grouping, retention time alignment, and gap-filling in LC-MS feature detection.) — http://mzmine.github.io/
- **Optimus** (KNIME-based workflow that wraps OpenMS algorithms for LC-MS feature detection, quantification, alignment, and optional filtering and normalization.) — https://github.com/MolecularCartography/Optimus
- **OpenMS** (C++ library providing state-of-the-art LC-MS feature detection and quantification algorithms used by Optimus.)

## Evaluation signals

- Feature table contains no null or NaN values in m/z or retention time columns; gap-filling has been applied.
- m/z values are consistent across replicates (within instrument mass accuracy tolerance, typically ≤5 ppm for high-resolution MS).
- Retention time coordinates for the same molecular feature vary by <2–3 min across samples (depending on LC stability).
- Per-sample intensity columns contain non-negative numeric values; internal standards or quality-control features show expected intensity rank order.
- Feature count is reasonable for the sample complexity and LC-MS method (e.g., 500–5000 features for typical untargeted metabolomics); extreme counts suggest over/under-parameterization of mass or chromatogram thresholds.

## Limitations

- Alignment accuracy depends on consistent LC-MS instrumental tuning and gradient reproducibility across samples; severe drift or column degradation will degrade feature alignment.
- Gap-filling and alignment algorithms may introduce spurious features if noise thresholds are too lenient, or eliminate true low-abundance features if thresholds are too strict.
- Direct-infusion MS data cannot be aligned by retention time; alternative approaches (spectral clustering or cosine similarity) are required.
- The workflow does not validate or perform MS/MS-based confirmation of detected features; follow-up annotation or targeted MS/MS experiments are needed for metabolite identification.
- Processing large sample cohorts (>100 runs) may require substantial RAM (2+ GB per 100 runs) and multicore CPU resources; memory and compute constraints may force iterative or distributed execution.

## Evidence

- [other] Load raw MS/MS data files into MZmine2 or Optimus (OpenMS). Apply mass detection to identify peaks across all samples. Build chromatogram features by grouping detected peaks across retention time and m/z dimensions. Align features across samples to construct a unified feature list. Fill missing feature values across samples where peaks were not detected. Export the processed feature table with m/z, retention time, and per-sample abundance columns to a quantification file.: "Load raw MS/MS data files into MZmine2 or Optimus (OpenMS). Apply mass detection to identify peaks across all samples. Build chromatogram features by grouping detected peaks across retention time and"
- [readme] Optimus employes the state-of-the-art LC-MS feature detection and quantification algorithms by OpenMS which are joined into a handy pipeline with a modern workflow management software KNIME with additional features implemented by us.: "Optimus employes the state-of-the-art LC-MS feature detection and quantification algorithms by OpenMS which are joined into a handy pipeline with a modern workflow management software KNIME"
- [readme] Detection of LC-MS features in each run. Alignment and quantification of features detected across all the runs.: "Detection of LC-MS features in each run. Alignment and quantification of features detected across all the runs."
- [readme] a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS: "a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS"
- [readme] The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform: "The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS)"
