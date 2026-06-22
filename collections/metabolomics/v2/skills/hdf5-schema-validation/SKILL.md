---
name: hdf5-schema-validation
description: Use when after converting proprietary vendor mass spectrometry files (Thermo .raw, Agilent .d, Bruker .d, or mzML) to MZA HDF5 format using the MZA executable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MZA
  - HDF5
  - h5py
  - rhdf5
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data
- the MZA simple data structure based on the HDF5 format
- using generic HDF5 libraries available (e.g., h5py and rhdf5)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mza_cq
    doi: 10.1021/acs.jproteome.2c00313
    title: MZA
  dedup_kept_from: coll_mza_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00313
  all_source_dois:
  - 10.1021/acs.jproteome.2c00313
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HDF5 Schema Validation

## Summary

Verify that converted mass spectrometry data conforms to the MZA HDF5 schema by validating the structure, metadata table, and array organization. This skill ensures data integrity and interoperability after vendor format conversion.

## When to use

After converting proprietary vendor mass spectrometry files (Thermo .raw, Agilent .d, Bruker .d, or mzML) to MZA HDF5 format using the MZA executable. Apply this skill to confirm the output file structure matches the MZA specification before downstream access or analysis, particularly when working with multidimensional data (LC-IM-MS) or when sharing converted files.

## When NOT to use

- Input is a native vendor binary file (.raw, .d, .mzML) — apply MZA conversion first
- Validating non-mass-spectrometry HDF5 files not conforming to the MZA specification
- Checking intensity thresholds or peak quality — use intensity threshold filtering during MZA conversion, not schema validation

## Inputs

- MZA HDF5 file (.mza)
- Expected metadata schema specification
- Optional: reference MZA file for comparison

## Outputs

- Validation report (pass/fail per schema component)
- HDF5 structure summary (groups, datasets, shapes)
- Metadata table integrity report
- Optional: corrected or flagged datasets

## How to apply

Load the output .mza HDF5 file using a generic HDF5 library (h5py in Python or rhdf5 in R). Validate the presence of three required HDF5 components: (1) a Metadata dataset containing a table with mandatory columns (Scan, MzaPath, MSLevel, Polarity, RetentionTime, IonMobilityBin, etc.); (2) Arrays_intensity group containing 1D datasets named by Scan values; (3) Arrays_mz (or Arrays_mzbin for ion mobility data) group. For ion mobility spectra, confirm the presence of Full_mz_array if mzbins are used. Verify that Scan numbers are unique, intensity and m/z arrays are jagged (omit zero values), and optional CCS calibration datasets (CCScalDT, CCScalTIMS, CCScalSLIM) are present only if detected during conversion. Check that the MzaPath column correctly maps to HDF5 group partitions when multiple groups exist due to large spectrum counts.

## Related tools

- **h5py** (Python library for reading and validating HDF5 file structure, metadata, and datasets in .mza files)
- **rhdf5** (R package for reading and validating HDF5 file structure, metadata, and datasets in .mza files)
- **MZA** (Command-line converter that produces the .mza HDF5 output to be validated) — https://github.com/PNNL-m-q/mza/releases

## Examples

```
import h5py
with h5py.File('output.mza', 'r') as f:
    assert 'Metadata' in f and 'Arrays_intensity' in f and 'Arrays_mz' in f
    metadata = f['Metadata'][:]
    assert all(col in metadata.dtype.names for col in ['Scan', 'MSLevel', 'RetentionTime'])
    for scan in metadata['Scan']: assert str(scan) in f['Arrays_intensity']
```

## Evaluation signals

- Metadata dataset contains all required columns (Scan, MSLevel, Polarity, RetentionTime, IonMobilityBin, etc.) with correct data types and no null values in mandatory fields
- Each Scan value in Metadata is unique and maps to exactly one dataset in Arrays_intensity and Arrays_mz (or Arrays_mzbin)
- Arrays_intensity and Arrays_mz datasets are jagged (variable length per spectrum) and contain no zero-intensity values
- For ion mobility spectra: Full_mz_array is present and Arrays_mzbin references valid indices into it; IonMobilityBin=0 row contains summed spectrum
- MzaPath partition indices correctly route to the intended group (e.g., MzaPath=1 accesses Arrays_intensity1 and Arrays_mzbin1)

## Limitations

- Validation does not assess quantitative accuracy or peak assignment correctness — only structural conformance to MZA schema
- Ion mobility calibration coefficients (CCScalDT, CCScalTIMS, CCScalSLIM) are optional and only present if detected during conversion; their absence does not constitute a validation failure for non-IM data or when calibration is unavailable
- Partitioning of groups (MzaPath field) is automatic and depends on file size; validation must account for variable partition counts across files
- Validation requires knowledge of the expected metadata schema; slight variations in optional columns or future schema extensions may cause false negatives if the validator is overly strict

## Evidence

- [other] Verify the output HDF5 file is created and conforms to the MZA schema by validating structure and metadata using h5py or rhdf5: "Verify the output HDF5 file is created and conforms to the MZA schema by validating structure and metadata using h5py or rhdf5."
- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group):"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values common for all spectra in the file.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values"
- [readme] CCS calibration coefficients: These are included as an HDF5 dataset if detected during conversion to MZA: "CCS calibration coefficients: These are included as an HDF5 dataset if detected during conversion to MZA"
- [readme] Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups instead of storing many datasets within one group.: "Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups"
