---
name: hdf5-feature-table-loading
description: Use when you have mass spectrometry feature data stored in HDF5 format (.h5 files) and need to load specific dimensional columns (m/z, drift time, retention time, intensity) for multi-dimensional alignment, CCS calibration, or isotope detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - DEIMoS
  - Python
  - h5py
  techniques:
  - ion-mobility-MS
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

# HDF5 Feature Table Loading

## Summary

Load multidimensional mass spectrometry feature tables from HDF5 files using DEIMoS, specifying mass, drift time, retention time, and intensity dimensions for downstream processing. This skill is essential for preparing aligned or raw feature data in N-dimensional formats for feature alignment, calibration, or spectral analysis workflows.

## When to use

Use this skill when you have mass spectrometry feature data stored in HDF5 format (.h5 files) and need to load specific dimensional columns (m/z, drift time, retention time, intensity) for multi-dimensional alignment, CCS calibration, or isotope detection. Apply it as the first step in any DEIMoS workflow operating on pre-detected or previously aligned feature tables.

## When NOT to use

- Input is already loaded in memory as a pandas DataFrame or NumPy array — use directly without calling deimos.load()
- Data is in mzML or other raw instrument format — first convert using ProteoWizard msconvert or load using DEIMoS with accession parameters
- HDF5 file structure or key names are unknown — inspect file structure first using h5py or similar tools

## Inputs

- HDF5 file (.h5) containing feature table data
- Key string identifying the dataset group within the HDF5 file
- List of column names (e.g., 'mz', 'drift_time', 'retention_time', 'intensity')

## Outputs

- Tabular feature table (pandas DataFrame) with dimensions: features × (m/z, drift_time, retention_time, intensity, ...)
- In-memory feature data structure ready for multi-dimensional operations

## How to apply

Call deimos.load() with the HDF5 file path, specifying the key parameter to identify the dataset group within the file (e.g., 'A', 'ms1') and the columns parameter as a list of dimension names to extract (['mz', 'drift_time', 'retention_time', 'intensity']). The function returns a pandas DataFrame or similar tabular structure with rows representing detected features and columns representing the requested dimensions. The multi-dimensional structure enables subsequent operations to exploit all dimensions simultaneously for improved feature separation and alignment confidence. Verify the output contains all expected dimensions and that intensity values are non-negative; typical downstream operations may threshold intensity (e.g., to 500 or 1000 counts) or filter by feature count before further processing.

## Related tools

- **DEIMoS** (Python API and command-line tool providing deimos.load() function for HDF5 feature table import) — http://github.com/pnnl/deimos
- **h5py** (Low-level HDF5 inspection and debugging when deimos.load() behavior must be understood or file structure must be explored)

## Examples

```
ms1 = deimos.load('example_data.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])
```

## Evaluation signals

- Output DataFrame contains exactly the requested columns (m/z, drift_time, retention_time, intensity) with correct data types (numeric for all dimensions)
- Feature count and intensity range match expectations from the source HDF5 file (e.g., row count, min/max intensity values)
- No NaN or infinite values present in loaded dimensions, or NaN values are expected and documented
- Downstream multi-dimensional operations (alignment, calibration) execute without dimension-mismatch errors
- Loaded data shape is consistent with study design (e.g., expected number of features per sample)

## Limitations

- deimos.load() requires the HDF5 file to follow DEIMoS internal structure conventions; files from other tools may require key/column name translation
- Large HDF5 files may load entirely into memory; partitioned or chunked reading is not discussed in the article
- Column name specification is case-sensitive and must match exactly the stored dimension names in the HDF5 group

## Evidence

- [other] Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions.: "Load two feature tables in HDF5 format using deimos.load() with keys and columns parameters specifying mz, drift_time, retention_time, and intensity dimensions."
- [results] ms1 = deimos.load('example_data.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity']): "ms1 = deimos.load('example_data.h5', key='ms1', columns=['mz', 'drift_time', 'retention_time', 'intensity'])"
- [readme] DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation: "DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation"
- [readme] algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity: "algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, thus improving detection sensitivity"
