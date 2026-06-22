---
name: mass-spectrometry-data-integration
description: Use when you have multiple mzML or HDF5 feature tables from the same study acquired on the same or similar instruments and need to align feature coordinates across samples to correct for systematic shifts in mass-to-charge, drift time, or retention time caused by instrumental drift, column aging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DEIMoS
  - Python
  - ProteoWizard
  - HDF5
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool
- import deimos
- is a Python application programming interface and command-line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
schema_version: 0.2.0
---

# mass-spectrometry-data-integration

## Summary

Reference-based alignment in DEIMoS integrates multi-dimensional mass spectrometry data across samples by matching detected features in N-dimensional space (mass, drift time, retention time) and applying a fitted transform to harmonize feature coordinates. This skill is essential when instrument variation, retention time shifts, or drift time calibration differences create systematic offsets between datasets that must be corrected before joint analysis.

## When to use

Apply this skill when you have multiple mzML or HDF5 feature tables from the same study acquired on the same or similar instruments and need to align feature coordinates across samples to correct for systematic shifts in mass-to-charge, drift time, or retention time caused by instrumental drift, column aging, or calibration variation. The skill is triggered by evidence of misalignment (e.g., the same ion appearing at different retention times or drift times across replicates) and is a prerequisite for downstream joint feature detection, quantification, or statistical comparison.

## When NOT to use

- Input data are already aligned or were acquired on different instrument platforms (DEIMoS is instrument-agnostic for N-dimensional data, but alignment assumes comparable acquisition conditions).
- Single-sample analysis where no cross-sample alignment is needed (apply feature detection directly instead).
- Feature tables are incomplete or lack one or more of the required dimensions (mz, drift_time, retention_time, intensity); alignment requires all dimensions to exploit multi-dimensional similarity.

## Inputs

- mzML.gz file (raw mass spectrometry data with accession metadata for retention_time and drift_time)
- HDF5 feature table with keys specifying sample identifiers and columns for mz, drift_time, retention_time, and intensity
- Reference sample feature table (HDF5 format, same dimensional schema as test samples)

## Outputs

- Aligned feature table (HDF5 format) with adjusted mz, drift_time, and retention_time coordinates
- Fit transform model (internal to deimos.alignment.align; includes residuals and r-squared metric)

## How to apply

Load two or more feature tables in HDF5 format using deimos.load() with explicit specification of the mz, drift_time, retention_time, and intensity columns. Select one sample as a reference (typically a quality control or pooled sample injected throughout the study). Apply deimos.alignment.align() in reference-based mode, which constructs a predictive model for each dimension by putatively matching detected features in the test sample against the reference sample, minimizing residuals, and then applies the learned fit transform to adjust all feature coordinates. Before alignment, apply intensity thresholds (e.g., threshold=500 or 1000) to remove noise and ensure robust feature matching. Export the aligned feature table to HDF5 format using deimos.save() with appropriate key and compression settings. Verify alignment quality by examining the r-squared goodness-of-fit statistic (typically >0.999) and visually comparing pre- and post-alignment feature positions in the multi-dimensional space.

## Related tools

- **DEIMoS** (Primary framework providing reference-based alignment implementation via deimos.alignment.align() and multi-dimensional feature matching) — https://github.com/pnnl/deimos
- **Python** (Execution environment and language for deimos API calls and data manipulation (import deimos, deimos.load, deimos.save))
- **ProteoWizard** (Upstream tool for converting raw mass spectrometry formats to mzML (required input format for DEIMoS))
- **HDF5** (Data storage format for feature tables input and output (loaded/saved via deimos.load() and deimos.save()))

## Examples

```
data_A = deimos.load('example_alignment.h5', key='A'); data_B = deimos.load('example_alignment.h5', key='B'); data_A_aligned = deimos.alignment.align(data_A, data_B, method='reference'); deimos.save(data_A_aligned, 'aligned_output.h5', key='A_aligned', compression='gzip')
```

## Evaluation signals

- r-squared goodness-of-fit statistic for the alignment transform is >0.9999 (e.g., 0.9999784552958134), indicating high-quality fit and minimal residual error.
- Feature coordinate ranges (mz, drift_time, retention_time) in aligned output are continuous and free of discontinuities or outlier clusters that would indicate failed transforms.
- Isotopic signatures are preserved or improved post-alignment (isotopologues remain co-localized in multi-dimensional space).
- When comparing pre- and post-alignment feature positions from the same ion across samples, the standard deviation of coordinates decreases or remains stable (alignment reduces variance, not increases it).
- Output HDF5 file is valid and contains all expected keys and columns as specified in deimos.save() call; no data loss or corruption.

## Limitations

- Reference-based alignment assumes the reference sample is representative of the study cohort and free of major composition bias; a poor reference will propagate misalignment to all test samples.
- The method is sensitive to the choice of intensity threshold applied before alignment; thresholds too high may exclude valid low-intensity features, while thresholds too low may include noise and degrade feature matching confidence.
- DEIMoS operates on N-dimensional data largely agnostic to acquisition instrumentation, but alignment robustness depends on sufficient dimensional overlap and similarity between reference and test samples; cross-instrument alignment is not validated.
- No changelog or version history is provided in the repository documentation, limiting traceability of algorithmic changes between releases.

## Evidence

- [other] Reference-based alignment constructs a model for each dimension of a sample by putatively matching detected features against an in-study reference sample, minimizing the residual, and subsequently applying the fit transform to align coordinates.: "Reference-based alignment constructs a model for each dimension of a sample by putatively matching detected features against an in-study reference sample, minimizing the residual, and subsequently"
- [other] Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions.: "Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions."
- [other] Apply deimos.alignment.align() using reference-based alignment mode to match features across the two datasets by exploiting multi-dimensional similarity in mass, drift time, and retention time.: "Apply deimos.alignment.align() using reference-based alignment mode to match features across the two datasets by exploiting multi-dimensional similarity in mass, drift time, and retention time."
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [results] Threshold intensity values to 500: "Threshold intensity values to 500"
- [results] r-squared: 0.9999784552958134: "r-squared: 0.9999784552958134"
