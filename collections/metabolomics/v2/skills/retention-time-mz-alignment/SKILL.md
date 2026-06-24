---
name: retention-time-mz-alignment
description: Use when processing raw LC/MS data (mzML or mzXML format) from multi-sample
  cohorts where retention time or intensity drift is suspected due to batch effects,
  instrument calibration drift, or variable run order.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - mzEmbed
  - mzLearn
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1101/2025.01.26.634927v3
  title: mzLearn
evidence_spans:
- mzEmbed, a framework for developing pre-trained generative models and fine-tuning
  them for specific tasks for untargeted metabolomics datasets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzlearn_cq
    doi: 10.1101/2025.01.26.634927v3
    title: mzLearn
  dedup_kept_from: coll_mzlearn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.01.26.634927v3
  all_source_dois:
  - 10.1101/2025.01.26.634927v3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-mz-alignment

## Summary

Autonomous correction of retention time (RT) and m/z drift across LC/MS samples caused by batch effects and run-order variation, enabling consistent feature detection and quantification without manual parameter tuning. This skill is essential for large-scale metabolomics cohorts where instrumental drift would otherwise compromise signal reproducibility.

## When to use

Apply this skill when processing raw LC/MS data (mzML or mzXML format) from multi-sample cohorts where retention time or intensity drift is suspected due to batch effects, instrument calibration drift, or variable run order. This is particularly critical when handling large-scale datasets (hundreds to thousands of files) where manual per-file parameter adjustment is infeasible, or when downstream pre-trained generative models require aligned, normalized feature matrices as input.

## When NOT to use

- Input is already a processed feature table (e.g., from xcms, MS-DIAL, or another peak picker) — skip directly to downstream annotation or modeling.
- Targeted LC/MS or SRM/MRM data where m/z and RT windows are pre-defined — mzLearn is designed for untargeted discovery.
- Very small cohorts (<5 files) where batch drift estimation is unreliable or where manual parameter tuning is more practical than automated learning.

## Inputs

- Raw LC/MS data files (mzML or mzXML format)
- Multi-sample cohort (no minimum size, but scalability tested to 2,075 files)

## Outputs

- Feature abundance table (CSV or mzTab format) with columns: median retention time, m/z value, normalized intensity per sample
- Detected metabolite signals defined by m/z and RT coordinates

## How to apply

Load raw LC/MS data files in mzML format into mzLearn, which autonomously learns signal characteristics across the cohort through iterative refinement. The algorithm corrects for retention time drift by identifying consistent m/z and RT landmarks across samples and realigning features to median RT and m/z values within each feature group. Intensity normalization is performed across samples to correct for run-order and batch-dependent intensity drift. The output is a two-dimensional feature abundance table with median RT and m/z coordinates and normalized intensities, requiring no user-specified RT tolerance, mass tolerance, or smoothing parameters. This zero-parameter design ensures reproducible signal detection even in the absence of QC samples or reference standards.

## Related tools

- **mzLearn** (Primary signal detection and RT/m/z drift correction engine; autonomously learns signal characteristics and iteratively refines alignment without user parameters) — github.com/ReviveMed/mzEmbed
- **mzEmbed** (Framework that integrates mzLearn outputs (aligned feature matrices) for downstream pre-trained generative model development and fine-tuning) — github.com/ReviveMed/mzEmbed

## Examples

```
python -m mz_learn.run_signal_detection --input_dir /path/to/raw_mzml_files --output_csv /path/to/feature_table.csv
```

## Evaluation signals

- Output feature table has shape [n_samples, n_features] with no missing values in RT or m/z columns; all intensities are normalized (e.g., z-scored or log-transformed with consistent mean and variance across samples).
- Retention time distribution across samples for the same m/z feature shows reduced variance post-correction compared to raw data; RT drift (linear or systematic shift across run order) is eliminated.
- Mass accuracy is preserved: m/z values remain within the instrument's typical accuracy range (e.g., <5 ppm for Orbitrap, <10 ppm for Q-TOF); no systematic m/z shift as a function of sample index or batch.
- Feature reproducibility: the same metabolite signal is detected across replicate or similar biological samples at consistent RT and m/z, with intensity variation explained by biological differences rather than instrumental drift.
- Output is compatible with downstream mzEmbed pretraining pipeline: feature matrix shape is [n_samples, feature_count] with no null entries, and intensity values are numeric and normalized.

## Limitations

- Zero-parameter design assumes sufficient sample diversity and cohort size (tested at 2,075 files) to learn robust signal characteristics; very small or homogeneous cohorts may produce suboptimal alignment.
- Iterative learning depends on stable instrument performance; extreme instrumental malfunction or calibration failure during a run may introduce artifacts that mzLearn cannot correct without explicit user intervention.
- Output is a 2D feature table and does not include ion mobility, fragment spectra, or other orthogonal dimensions; multi-dimensional data (e.g., LC–IMS–MS) would require custom preprocessing.
- No built-in metabolite annotation or MS/MS spectral matching; the feature table must be passed to downstream annotation tools for compound identification.

## Evidence

- [readme] mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user.: "mzLearn is a data-driven algorithm designed to autonomously detect metabolite signals from raw LC/MS data without requiring input parameters from the user."
- [readme] iteratively learning signal characteristics to ensure high-quality signal detection: "iteratively learning signal characteristics to ensure high-quality signal detection"
- [readme] mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order.: "mzLearn autonomously refines signal detection, correcting for retention time (rt) and intensity drifts caused by batch effects and run order."
- [readme] A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples.: "A two-dimensional table of detected features defined by median rt and m/z values, with normalized intensities across samples."
- [readme] Capable of handling large-scale datasets (e.g., 2,075 files in a single run).: "Capable of handling large-scale datasets (e.g., 2,075 files in a single run)."
- [other] Apply the data-driven signal detection algorithm to identify peaks and features across the mass-to-charge and retention time dimensions without requiring manual parameter optimization.: "Apply the data-driven signal detection algorithm to identify peaks and features across the mass-to-charge and retention time dimensions without requiring manual parameter optimization."
