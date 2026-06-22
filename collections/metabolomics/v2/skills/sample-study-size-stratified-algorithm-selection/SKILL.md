---
name: sample-study-size-stratified-algorithm-selection
description: Use when when beginning mass alignment in a multi-sample LC-MS metabolomics study, before constructing the MassGrid.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)
  - asari mass_functions module (nn_cluster_by_mz_seeds)
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- See [MassGrid.build_grid_sample_wise](MassGrid.build_grid_sample_wise), [MassGrid.add_sample](MassGrid.add_sample). See [MassGrid.build_grid_by_centroiding](MassGrid.build_grid_by_centroiding),
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-study-size-stratified-algorithm-selection

## Summary

A performance-conscious strategy for selecting between pairwise and nearest-neighbor mass alignment algorithms based on study sample count. This skill enables asari to scale across small (≤10 samples) and large studies by choosing algorithmically matched approaches that balance CPU and memory use.

## When to use

When beginning mass alignment in a multi-sample LC-MS metabolomics study, before constructing the MassGrid. The decision depends on the total sample count in your project: small studies benefit from pairwise anchor-track prioritization, while large studies require binning-based nearest-neighbor clustering to avoid quadratic scaling.

## When NOT to use

- Study has already been aligned into a feature table or composite map—the algorithm selection applies only at the mass track alignment stage, before composite peak detection.
- Sample count or mass track data are unavailable or incomplete—study size determination requires exact sample enumeration.
- Samples have been preprocessed with external alignment tools (e.g., XCMS, MZmine) that have already produced a unified m/z grid—this skill targets the initial asari-native alignment decision.

## Inputs

- sample count (integer)
- mass track list per sample (m/z, intensity, retention time tuples)
- anchor mass track identifiers (13C/12C isotopes or Na/H adducts)
- mz_tolerance parameter (ppm)

## Outputs

- MassGrid (aligned consensus m/z across samples)
- _mass_grid_mapping.csv (mapping of aligned mass track identifiers to consensus m/z and sample membership)
- recalibrated m/z values (if pairwise path, when systematic difference >1 ppm)

## How to apply

First, count the number of LC-MS samples in your study. If ≤10 samples, use pairwise sample-wise alignment: identify the reference sample by counting anchor mass tracks (13C/12C isotopes or Na/H adducts) and select the one with the highest count; then align anchor tracks between each sample and the reference list, recalibrating all m/z values if systematic difference exceeds 1 ppm, before aligning remaining mass tracks. For studies with >10 samples, use nearest-neighbor clustering by m/z: bin all sample mass tracks using histogram-based m/z seed detection (ensuring 2 peaks separated by at least mz_tolerance), then construct consensus m/z for each bin as the mean of median m/z and m/z at highest intensity. In both paths, generate _mass_grid_mapping.csv documenting aligned mass track identifiers, consensus m/z values, and sample membership.

## Related tools

- **asari mass_functions module (nn_cluster_by_mz_seeds)** (Implements nearest-neighbor clustering by m/z seeds for large-study alignment path) — https://github.com/shuzhao-li/asari
- **asari MassGrid class (build_grid_sample_wise, add_sample, build_grid_by_centroiding, bin_track_mzs)** (Constructs and populates the aligned MassGrid; dispatches between pairwise and binning-based strategies) — https://github.com/shuzhao-li/asari
- **Python** (Language for implementing study-size check and invoking asari mass functions)

## Examples

```
python3 -m asari.main process -i mydir/projectx_dir --mode pos
```

## Evaluation signals

- Sample count threshold (≤10 vs. >10) is correctly identified and logged at workflow start; verify in asari project.json or console output.
- _mass_grid_mapping.csv is generated with consistent m/z consensus values (mean of median m/z and highest-intensity m/z) across all aligned bins or pairwise pairs.
- For pairwise path: reference sample is the one with the highest count of anchor mass tracks; verify by counting 13C/12C or Na/H adducts in asari output.
- For pairwise path: systematic m/z drift >1 ppm triggers recalibration; confirm by comparing pre- and post-calibration m/z values in output.
- Nearest-neighbor bins show 2+ peaks separated by ≥mz_tolerance in large studies; verify histogram-based seed detection in intermediate pickle files or audit logs.

## Limitations

- Threshold of ≤10 samples is empirically motivated but may require tuning for specific instrument types, ionization modes, or sample complexity; no adaptive optimization is reported.
- Anchor mass track identification relies on prior knowledge of isotope (13C/12C) and adduct (Na/H) m/z differences; isotopically labeled or non-standard adducts may not be recognized.
- The 1 ppm recalibration threshold is fixed and may not account for mass calibration drift over long run sequences or across different instrument platforms.
- Nearest-neighbor clustering seed detection requires 2+ peaks separated by mz_tolerance; sparse or low-intensity mass tracks may not form reliable seeds in large studies.
- GC-MS workflow and MS/MS-specific alignment strategies are handled separately (GC-MS workflow added in version 1.16.6); this skill applies primarily to LC-MS data.

## Evidence

- [other] if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method: "if ≤10 samples, use pairwise alignment with anchor mass track prioritization; else use nearest-neighbor clustering method."
- [other] Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional algorithm selection.: "Asari is designed as a scalable program that uses performance-conscious approaches, operating with disciplined memory and CPU use, enabling it to handle studies of varying sizes through conditional"
- [other] For small studies, perform pairwise sample-wise alignment: align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1 ppm, then align remaining mass tracks.: "For small studies, perform pairwise sample-wise alignment: align anchor mass tracks first between each sample and reference list, recalibrate all sample m/z values if systematic difference exceeds 1"
- [other] For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance.: "For large studies, bin all sample mass tracks by m/z using nearest-neighbor clustering with histogram-based m/z seed detection, ensuring 2 peaks separated by at least mz_tolerance."
- [other] Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity.: "Construct consensus m/z for each aligned bin as mean of median m/z and m/z at highest intensity."
- [readme] Scalable, performance conscious, disciplined use of memory and CPU: "Scalable, performance conscious, disciplined use of memory and CPU"
