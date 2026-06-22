---
name: mass-spectrometry-tune-data-loading
description: Use when you have positive- or negative-mode tune reference compound data stored in HDF5 format (e.g., example_tune_pos.h5) and need to extract the tune mass spectrum for CCS calibration. This skill is the entry point before applying deimos.calibration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - deimos
  - ProteoWizard
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.1c05017
  title: deimos
evidence_spans:
- DEIMoS is a Python application programming interface
- DEIMoS is a Python application programming interface and command-line tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deimos_cq
    doi: 10.1021/acs.analchem.1c05017
    title: deimos
  dedup_kept_from: coll_deimos_cq
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

# mass-spectrometry-tune-data-loading

## Summary

Load collision cross section (CCS) calibration tune reference data from HDF5 files using DEIMoS, preparing standardized tune compounds for downstream calibration workflows. This skill is essential for establishing the m/z–CCS relationship required for accurate ion mobility spectrometry analysis.

## When to use

You have positive- or negative-mode tune reference compound data stored in HDF5 format (e.g., example_tune_pos.h5) and need to extract the tune mass spectrum for CCS calibration. This skill is the entry point before applying deimos.calibration.tunemix() to establish a calibration model with known m/z and CCS values.

## When NOT to use

- Input data is already in processed feature table format (peaks detected and aligned); use deimos.load() only on raw or tune reference data.
- Data is stored in non-HDF5 formats (e.g., raw mzML, NetCDF); convert using ProteoWizard msconvert or appropriate format-specific loader first.
- You are loading sample data for feature detection rather than tune reference compounds; tune data serves a calibration-specific role and should not be used as analysis samples.

## Inputs

- HDF5 file containing tune reference data (e.g., example_tune_pos.h5)
- key parameter specifying the dataset path within the HDF5 file (string, typically 'ms1')

## Outputs

- Tune mass spectrum DataFrame with columns including m/z, intensity, and optional drift_time/retention_time dimensions
- Structured data object ready for calibration function input

## How to apply

Use deimos.load() with the HDF5 tune data file path and specify the key parameter (typically 'ms1' for mass spectrometry data). The function returns a structured DataFrame containing m/z, intensity, and other spectral dimensions for the tune reference compounds. Extract the loaded tune data object for subsequent calibration. The loaded data should span the expected m/z range of the tune mix (e.g., m/z 118.086255–1521.971475 for positive-mode compounds) and contain intensity values for all reference compound peaks.

## Related tools

- **deimos** (Provides the deimos.load() function to parse and deserialize HDF5 tune data into memory-efficient DataFrames) — https://github.com/pnnl/deimos
- **Python** (Runtime environment for executing deimos.load() and downstream calibration workflows)
- **ProteoWizard** (Used to convert tune data from other formats (e.g., native vendor formats) to mzML before HDF5 conversion if needed)

## Examples

```
tune_pos = deimos.load('example_tune_pos.h5', key='ms1')
```

## Evaluation signals

- Returned DataFrame contains expected columns: m/z, intensity, and (optionally) drift_time, retention_time, or other dimensions
- m/z values span the known range of tune reference compounds (e.g., 118.086–1521.971 for positive-mode mix)
- Intensity values are non-negative and non-zero for all reference compound peaks
- DataFrame can be passed without error to deimos.calibration.tunemix() for CCS calibration
- Row count and data shape are consistent with the number of scans/spectra in the tune file

## Limitations

- HDF5 file must be properly formatted with the specified key present; missing or malformed keys will raise KeyError
- Loading large tune datasets may require significant memory; no streaming or chunked loading option is documented
- deimos.load() is largely agnostic to instrument type but relies on HDF5 data structure conforming to DEIMoS conventions
- Tune data quality depends on upstream data acquisition and conversion; corrupted or incomplete tune files will propagate errors to calibration

## Evidence

- [results] tune_pos = deimos.load('example_tune_pos.h5', key='ms1'): "tune_pos = deimos.load('example_tune_pos.h5', key='ms1')"
- [other] Load the positive-mode tune data from example_tune_pos.h5 using deimos.load() with key 'ms1': "Load the positive-mode tune data from example_tune_pos.h5 using deimos.load() with key 'ms1'"
- [readme] DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool: "DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application programming interface and command-line tool"
- [other] m/z 118.086255–1521.971475 with known CCS values: "m/z 118.086255–1521.971475 with known CCS values"
- [results] Conversion to mzML from several other formats can be performed using the free and open-source ProteoWizard msconvert utility: "Conversion to mzML from several other formats can be performed using the free and open-source ProteoWizard msconvert utility"
