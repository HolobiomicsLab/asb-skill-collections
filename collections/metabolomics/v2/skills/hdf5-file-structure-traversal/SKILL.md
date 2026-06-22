---
name: hdf5-file-structure-traversal
description: Use when when you have converted multidimensional mass spectrometry data (or other complex data) into MZA HDF5 format and need to understand the file hierarchy, validate the conversion output, extract metadata tables and array structure, or access spectra across different programming environments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MZA
  - h5py
  - rhdf5
  - HDF5
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data
- using generic HDF5 libraries available (e.g., h5py and rhdf5)
- the MZA simple data structure based on the HDF5 format
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

# HDF5 File Structure Traversal

## Summary

Systematically enumerate and extract the hierarchical structure, metadata, and datasets within HDF5 files using language-agnostic generic libraries. This skill enables cross-platform, cross-language inspection of complex multidimensional data stored in HDF5 format without requiring proprietary vendor tools.

## When to use

When you have converted multidimensional mass spectrometry data (or other complex data) into MZA HDF5 format and need to understand the file hierarchy, validate the conversion output, extract metadata tables and array structure, or access spectra across different programming environments (Python, R, etc.). Use this skill particularly when you need to programmatically inspect top-level groups (Arrays_intensity, Arrays_mz, Arrays_mzbin), dataset dimensions, data types, and metadata table columns before downstream analysis.

## When NOT to use

- Input data is already loaded in memory as a Python/R object or feature table; use direct object inspection instead of file traversal.
- You only need to access a single known spectrum array (e.g., Scan 630); direct dataset read is more efficient than full traversal.
- File is in a different format (mzML, .raw, .d, NetCDF) that has not been converted to MZA HDF5; convert first using MZA tool.

## Inputs

- MZA HDF5 file (.mza extension) containing converted multidimensional mass spectrometry data
- File path to HDF5 file accessible on local filesystem or network storage

## Outputs

- Hierarchical map of all top-level groups and datasets in the file
- Metadata table extracted as structured data (rows = spectra, columns = properties like Scan, MSLevel, RetentionTime, IonMobilityTime)
- Dataset shape, data type, and dimension information for each array
- Serialized structure report (JSON or text format)
- Cross-language validation report confirming consistency between Python and R reads

## How to apply

Load the MZA HDF5 file using a generic HDF5 library (h5py in Python or rhdf5 in R). Traverse the file hierarchy starting from the root to enumerate all top-level groups and datasets. For each group and dataset, extract structural metadata including dimensions, data types, dataset shapes, and any HDF5 attributes (such as CCS calibration coefficients: CCScalDT, CCScalSLIM, CCScalTIMS). Parse the metadata HDF5 dataset to understand spectrum properties (Scan, MSLevel, RetentionTime, IonMobilityBin, etc.). Serialize the extracted structure to a human-readable format (JSON or text report). Validate consistency across programming languages by reading the same file in both Python and R and comparing outputs to confirm lossless round-trip access. Check for partitioning (MzaPath column) when files contain many spectra, as datasets are split across numbered groups (e.g., Arrays_intensity1, Arrays_intensity2) to optimize HDF5 read performance.

## Related tools

- **h5py** (Generic HDF5 library for Python-based traversal and metadata extraction from MZA files)
- **rhdf5** (Generic HDF5 library for R-based traversal and metadata extraction from MZA files)
- **MZA** (Produces the HDF5 files being traversed by converting proprietary vendor mass spectrometry formats) — https://github.com/PNNL-m-q/mza

## Examples

```
import h5py
with h5py.File('sample.mza', 'r') as f:
    print('Top-level keys:', list(f.keys()))
    for key in f.keys():
        print(f'{key}: {type(f[key])}, shape={f[key].shape if hasattr(f[key], "shape") else "group"}')
    metadata = f['Metadata'][:]
    print(f'Metadata shape: {metadata.shape}, columns: {metadata.dtype.names}')
```

## Evaluation signals

- All top-level groups (Arrays_intensity, Arrays_mz, Arrays_mzbin, metadata table) are successfully enumerated and their object types (group vs. dataset) are correctly identified.
- Metadata table is extracted with all expected columns (Scan, MSLevel, Polarity, Activation, RetentionTime, IonMobilityTime, etc.) and row count matches the number of spectra in the file.
- Dataset shapes, data types (e.g., float32, int32), and dimension counts are correctly reported for each array.
- Cross-language validation shows identical structure and metadata when the same MZA file is read in both Python (h5py) and R (rhdf5), confirming lossless access.
- For ion-mobility spectra, Full_mz_array and MzaPath partitioning (numbered groups) are correctly identified and reported.

## Limitations

- Traversal performance may degrade on files with extremely large numbers of datasets (>10,000 spectra in a single group); MZA mitigates this by partitioning across numbered groups, but traversal logic must account for MzaPath column to identify partition indices.
- CCS calibration coefficients (CCScalDT, CCScalSLIM, CCScalTIMS) are only present if detected during conversion to MZA; absence does not indicate file corruption but rather that the input instrument/method did not provide them.
- Metadata table column interpretation depends on the instrument type and acquisition method (e.g., IonMobilityTime units differ: milliseconds for DT/SLIM, 1/k0 Vs/cm² for TimsTOF); schema validation alone cannot detect semantic errors.
- Zero-intensity values are omitted from Arrays_intensity and corresponding m/z arrays for storage efficiency; traversal does not recover the original dense spectrum representation.

## Evidence

- [other] MZA converts multidimensional mass spectrometry data to a simple data structure based on HDF5 format, enabling access via generic HDF5 libraries such as h5py and rhdf5 across any programming language and operating system.: "MZA converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format. Once converted, MZA files can be easily"
- [other] The workflow involves loading the MZA HDF5 file, traversing the hierarchy, extracting metadata and structural information, and serializing to a human-readable format.: "1. Load the MZA HDF5 file using h5py (Python) or rhdf5 (R) generic HDF5 library. 2. Traverse and enumerate all top-level groups and datasets in the file hierarchy. 3. Extract metadata and structural"
- [readme] MZA file structure consists of a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Metadata table columns represent spectrum properties such as scan number, MS level, activation type, retention time, and ion mobility arrival time.: "each row in the metadata table (see csv files in test_data) represents a spectrum and the columns represent the properties of the spectrum such as scan number (unique to each spectrum), MS level,"
- [readme] Spectra are stored in two jagged arrays omitting zero-intensity values, with groups named Arrays_intensity and Arrays_mz, and individual datasets named by Scan value.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table: Arrays_intensity (HDF5 group):"
- [readme] CCS calibration coefficients are included as HDF5 datasets if detected during conversion, with format-specific parameter sets.: "These are included as an HDF5 dataset if detected during conversion to MZA: CCScalDT = [Tfix, Beta] for Agilent DT; CCScalSLIM = [C0, C1, C2, C3] for SLIM; CCScalTIMS = [C0, C1, C2, C3, C4, C5, C6,"
- [readme] MzaPath column in metadata indicates partition index for multi-group files, addressing HDF5 performance by distributing datasets across numbered groups.: "Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups"
