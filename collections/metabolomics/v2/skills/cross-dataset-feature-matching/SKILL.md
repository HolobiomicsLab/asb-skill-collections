---
name: cross-dataset-feature-matching
description: Use when you have two or more feature tables in HDF5 format with detected
  features characterized by m/z, drift time, retention time, and intensity, and you
  need to match corresponding features across samples to account for systematic shifts
  caused by instrument variation or tuning differences.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Python
  - HDF5
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python
  application programming interface and command-line tool
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c05017
  all_source_dois:
  - 10.1021/acs.analchem.1c05017
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-dataset-feature-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Align detected features across multiple mass spectrometry samples by exploiting multi-dimensional similarity in mass, drift time, and retention time to construct a reference-based coordinate transformation model. This reduces instrument variation and increases confidence in feature identification across datasets.

## When to use

You have two or more feature tables in HDF5 format with detected features characterized by m/z, drift time, retention time, and intensity, and you need to match corresponding features across samples to account for systematic shifts caused by instrument variation or tuning differences. Use this skill when features in different samples represent the same underlying compounds but have drifted in one or more dimensions.

## When NOT to use

- Input feature tables contain fewer than two dimensions (m/z and one other; drift time and retention time are required for reference-based alignment to be effective).
- No suitable in-study reference sample is available or reference sample has too few detected features to establish a reliable fit model.
- Features have already been aligned or data is already in a unified coordinate space.

## Inputs

- Feature table in HDF5 format with columns: m/z, drift time, retention time, intensity
- Reference sample feature table (HDF5)
- Two or more sample feature tables (HDF5) to be aligned

## Outputs

- Aligned feature table in HDF5 format with adjusted m/z, drift time, and retention time coordinates
- Alignment fit transform model (residuals and fit parameters per dimension)

## How to apply

Load each feature table into memory using deimos.load() specifying the HDF5 key and the four required columns (mz, drift_time, retention_time, intensity). Apply deimos.alignment.align() in reference-based alignment mode, which constructs a linear or polynomial fit model for each dimension by matching detected features against an in-study reference sample, minimizing residuals across all dimensions simultaneously. The fit transform is then applied to adjust the coordinates of other samples to align with the reference coordinate system. Export the aligned feature table using deimos.save() with appropriate HDF5 key and compression settings. Success depends on the quality of feature detection upstream and sufficient overlap of features between samples to enable robust fitting.

## Related tools

- **DEIMoS** (Provides deimos.load(), deimos.alignment.align(), and deimos.save() functions to load feature tables, perform reference-based multi-dimensional alignment, and export aligned results.) — http://github.com/pnnl/deimos
- **Python** (Programming language and runtime environment for executing DEIMoS API calls and scripting the alignment workflow.)
- **HDF5** (File format for storing and retrieving multi-dimensional feature tables with structured column access.)

## Examples

```
import deimos
data_A = deimos.load('sample_A.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
data_ref = deimos.load('reference.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
data_A_aligned = deimos.alignment.align(data_A, data_ref, mode='reference-based')
deimos.save(data_A_aligned, 'sample_A_aligned.h5', key='ms1', compression='gzip')
```

## Evaluation signals

- Alignment residuals (fit quality) should be reported for each dimension; r² values close to 0.9999 indicate excellent fits as demonstrated in the article.
- Verify that coordinate ranges in aligned samples are now comparable to the reference sample (e.g., m/z, drift time, retention time should be within expected instrument tolerances).
- Check that the number of features is preserved after alignment; features should not be dropped unless explicitly filtered.
- Visual inspection: plot aligned features from multiple samples in m/z vs drift time vs retention time space; clusters should now overlap between samples.
- Cross-check a subset of features with known identity across samples to confirm they now share similar multi-dimensional coordinates after alignment.

## Limitations

- Alignment quality depends on the selection of a representative reference sample with sufficient detected features and good coverage across the m/z, drift time, and retention time space.
- Systematic non-linear drift in instrument response that cannot be captured by a simple fit model may result in residual misalignment.
- Features that are present in some samples but absent in the reference sample cannot be aligned and remain in their original coordinates.
- The method assumes that the same features are detectable across samples; highly variable detection (e.g., due to sample preparation differences) can degrade alignment confidence.

## Evidence

- [other] Reference-based alignment constructs a model for each dimension of a sample by putatively matching detected features against an in-study reference sample, minimizing the residual, and subsequently applying the fit transform to align coordinates.: "Reference-based alignment constructs a model for each dimension of a sample by putatively matching detected features against an in-study reference sample, minimizing the residual, and subsequently"
- [intro] Algorithm implementations simultaneously utilize all dimensions to increase alignment/feature matching confidence among datasets: "algorithm implementations simultaneously utilize all dimensions to (ii) increase alignment/feature matching confidence among datasets"
- [other] Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions.: "Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions."
- [other] Apply deimos.alignment.align() using reference-based alignment mode to match features across the two datasets by exploiting multi-dimensional similarity in mass, drift time, and retention time.: "Apply deimos.alignment.align() using reference-based alignment mode to match features across the two datasets by exploiting multi-dimensional similarity in mass, drift time, and retention time."
- [other] Export the aligned feature table to HDF5 format using deimos.save() with appropriate key and compression settings.: "Export the aligned feature table to HDF5 format using deimos.save() with appropriate key and compression settings."
