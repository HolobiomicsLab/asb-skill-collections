---
name: multi-dimensional-feature-alignment
description: Use when you have two or more feature tables in HDF5 format with detected peaks characterized across multiple dimensions (mz, drift_time, retention_time, intensity) and need to harmonize feature coordinates across samples to account for instrument variation, enabling downstream cross-sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - DEIMoS
  - Python
  - conda
  - pip
  - HDF5
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool
- import deimos
- is a Python application programming interface and command-line tool
- Use conda to create a virtual environment with required dependencies.
- 'Install DEIMoS using pip: pip install -e .'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos
schema_version: 0.2.0
---

# multi-dimensional-feature-alignment

## Summary

Align detected features across multiple samples by exploiting multi-dimensional similarity in mass, drift time, and retention time using reference-based coordinate transformation. This approach increases alignment confidence and reduces false feature matches compared to single-dimension methods.

## When to use

You have two or more feature tables in HDF5 format with detected peaks characterized across multiple dimensions (mz, drift_time, retention_time, intensity) and need to harmonize feature coordinates across samples to account for instrument variation, enabling downstream cross-sample analysis or quantification.

## When NOT to use

- Input data are in raw mzML/mzXML format — peak detection must occur first
- Feature table contains only a single sample — alignment requires ≥2 samples
- Features have not been detected and characterized in all required dimensions (mz, drift_time, retention_time) — dimensionality is essential to the algorithm

## Inputs

- Two or more feature tables in HDF5 format, each containing columns: mz, drift_time, retention_time, intensity
- One sample designated as the reference for coordinate transformation

## Outputs

- Aligned feature table in HDF5 format with coordinates transformed to reference sample space
- Fitted transformation model (residuals, coefficients per dimension)

## How to apply

Load feature tables using deimos.load() specifying the mz, drift_time, retention_time, and intensity dimensions. Apply deimos.alignment.align() in reference-based alignment mode, which constructs a multidimensional model for each sample by putatively matching detected features against an in-study reference sample, minimizing the residual fit, and applying the resulting transform to align all sample coordinates to the reference space. Export the aligned feature table to HDF5 using deimos.save(). Reference-based alignment leverages all dimensions simultaneously to improve separation between features and increase matching confidence.

## Related tools

- **DEIMoS** (Provides deimos.alignment.align() function for reference-based multidimensional feature alignment and deimos.load/save() for HDF5 I/O) — http://github.com/pnnl/deimos
- **Python** (Runtime environment for DEIMoS API and data manipulation)
- **HDF5** (File format for storing and retrieving feature tables with structured column metadata)

## Examples

```
data_A = deimos.load('sample_A.h5', key='features', columns=['mz', 'drift_time', 'retention_time', 'intensity']); data_ref = deimos.load('reference.h5', key='features', columns=['mz', 'drift_time', 'retention_time', 'intensity']); aligned = deimos.alignment.align(data_A, data_ref, mode='reference'); deimos.save(aligned, 'sample_A_aligned.h5', key='features', compression='gzip')
```

## Evaluation signals

- All output feature coordinates fall within expected chemical space (mz > 0, drift_time > 0, retention_time > 0)
- Aligned features from different samples cluster tightly in multidimensional space when plotted against the reference, indicating successful coordinate transformation
- Feature count in aligned table matches or exceeds input table count (no unexpected row loss)
- Fitted model reports low residuals and high r-squared (≥0.99 indicates good fit) for each dimension's transformation
- Cross-sample feature matching rates increase relative to unaligned data (quantified by overlap in matched feature IDs)

## Limitations

- Alignment quality depends on reference sample choice; an outlier or poorly ionizing reference can propagate errors to all aligned samples
- Algorithm assumes linear or polynomial relationships between sample and reference coordinates; nonlinear instrument drift may not be captured
- Requires sufficient overlap of detected features between sample and reference to fit a stable transformation model; sparse or disjoint feature sets may yield poor fits
- Multi-dimensional alignment is sensitive to missing or sparse data in any single dimension (e.g., samples with few drift_time measurements)
- DEIMoS is agnostic to instrument type but alignment parameters (e.g., matching tolerance windows) may require instrument-specific tuning

## Evidence

- [other] Reference-based alignment constructs a model for each dimension of a sample by putatively matching detected features against an in-study reference sample, minimizing the residual, and subsequently applying the fit transform to align coordinates.: "Reference-based alignment constructs a model for each dimension of a sample by putatively matching detected features against an in-study reference sample, minimizing the residual, and subsequently"
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to offer greater separation between features, thus improving detection sensitivity, increase alignment/feature matching confidence"
- [other] Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions. Apply deimos.alignment.align() using reference-based alignment mode to match features across the two datasets: "Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions. Apply deimos.alignment.align() using"
- [other] Export the aligned feature table to HDF5 format using deimos.save() with appropriate key and compression settings.: "Export the aligned feature table to HDF5 format using deimos.save() with appropriate key and compression settings."
