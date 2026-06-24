---
name: hierarchical-dataset-metadata-extraction
description: Use when when you have received an MZA-format HDF5 file (or other hierarchical
  HDF5-based scientific data) and need to understand its internal structure before
  downstream processing, share it across programming languages (Python, R), or document
  its schema for reproducibility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MZA
  - h5py
  - rhdf5
  - HDF5
  techniques:
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional
  mass spectrometry (MS) data
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hierarchical-dataset-metadata-extraction

## Summary

Extract and enumerate metadata and structural information (dimensions, data types, dataset shapes) from hierarchically organized HDF5 files, particularly those containing multidimensional mass spectrometry data organized into groups and datasets. This skill enables programmatic inspection and documentation of complex scientific data structures for cross-language and cross-platform reuse.

## When to use

When you have received an MZA-format HDF5 file (or other hierarchical HDF5-based scientific data) and need to understand its internal structure before downstream processing, share it across programming languages (Python, R), or document its schema for reproducibility. Use this skill as an initial inspection step when the file's group hierarchy, dataset organization, or metadata layout is unknown or needs validation.

## When NOT to use

- The HDF5 file structure is already fully documented and validated by prior inspection.
- You need to extract and process actual spectral intensity or m/z values, not merely their metadata structure—use data access and visualization skills instead.
- The input is not HDF5-based (e.g., raw vendor binary formats, CSV, NetCDF) and lacks hierarchical group structure to enumerate.

## Inputs

- MZA HDF5 file (.mza extension)
- Raw vendor mass spectrometry data files (Agilent .d, Bruker .d with ion mobility, Thermo .raw, mzML) prior to conversion to MZA

## Outputs

- Hierarchical metadata report (JSON or text)
- Enumeration of groups and datasets with dimensions and data types
- Cross-language verification comparison (e.g., Python vs. R output equivalence)
- Schema documentation suitable for data sharing and reproducibility

## How to apply

Load the MZA HDF5 file using a generic HDF5 library (h5py in Python or rhdf5 in R). Traverse the file hierarchy recursively to enumerate all top-level groups (e.g., Arrays_intensity, Arrays_mz, Arrays_mzbin) and datasets (e.g., metadata table, Full_mz_array, CCS calibration coefficients). For each dataset and group, extract and record metadata: name, shape, data type, dimensions, and any attached attributes. Serialize the extracted structure to a human-readable format such as JSON or a text report. This approach is grounded in the MZA data model: a metadata table describing spectra, separate groups holding 1D intensity and m/z arrays named by scan number, and optional ion-mobility or calibration datasets. Validate consistency by reading the same file in multiple languages and comparing outputs.

## Related tools

- **h5py** (Generic HDF5 library for traversing and reading HDF5 file hierarchy, groups, datasets, and metadata in Python)
- **rhdf5** (Generic HDF5 library for traversing and reading HDF5 file hierarchy, groups, datasets, and metadata in R)
- **MZA** (Command-line tool that converts multidimensional mass spectrometry data from proprietary vendor formats to MZA HDF5 structure prior to metadata extraction) — https://github.com/PNNL-m-q/mza
- **HDF5** (Underlying hierarchical data format standard defining the file structure and group/dataset model for MZA files)

## Examples

```
import h5py
with h5py.File('data.mza', 'r') as f:
    def print_structure(name, obj):
        print(f'{name}: shape={obj.shape if hasattr(obj, "shape") else "N/A"}, dtype={obj.dtype if hasattr(obj, "dtype") else "group"}')
    f.visititems(print_structure)
```

## Evaluation signals

- All top-level groups (Metadata, Arrays_intensity, Arrays_mz, Arrays_mzbin, Full_mz_array) are enumerated and present in the output report.
- Dataset dimensions, data types (e.g., numeric, character), and shapes match the MZA specification: metadata as a table with rows=spectra and columns=properties (Scan, MSLevel, RetentionTime, IonMobilityBin, etc.); 1D arrays in groups named by scan number.
- Metadata column names and value types conform to the documented schema (e.g., Scan: numeric; MSLevel: 1 or 2; Polarity: POS or NEG; IonMobilityTime: numeric in milliseconds or Vs/cm²).
- Cross-language output comparison (Python h5py vs. R rhdf5) yields identical group/dataset names, shapes, and data types with no discrepancies.
- Optional CCS calibration coefficient datasets (CCScalDT, CCScalTIMS, CCScalSLIM) are detected and correctly labeled if present in the file.

## Limitations

- MZA files may use partitioned HDF5 groups (e.g., Arrays_intensity1, Arrays_intensity2) when spectra count is high; the extraction must handle and report all partitions to provide a complete structural picture.
- Ion-mobility spectra store m/z values as indices (mzbins) rather than direct m/z arrays, requiring separate lookup in Full_mz_array; metadata extraction alone does not resolve these references—cross-validation requires data-level access.
- The tool assumes the input file adheres to the MZA specification; corrupted or non-standard HDF5 files may yield incomplete or inconsistent metadata.
- Extraction of CCS calibration coefficients depends on their presence during conversion; older MZA files or those converted without CCS detection will lack these datasets.

## Evidence

- [other] Traverse and enumerate all top-level groups and datasets in the file hierarchy.: "Traverse and enumerate all top-level groups and datasets in the file hierarchy."
- [other] Extract metadata and structural information (dimensions, data types, dataset shapes) for each group and dataset.: "Extract metadata and structural information (dimensions, data types, dataset shapes) for each group and dataset."
- [other] Serialize the extracted structure to a human-readable format (JSON or text report).: "Serialize the extracted structure to a human-readable format (JSON or text report)."
- [other] Demonstrate cross-language access by reading the same file in both Python and R, comparing outputs to verify consistency.: "Demonstrate cross-language access by reading the same file in both Python and R, comparing outputs to verify consistency."
- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Metadata (HDF5 dataset): each row in the metadata table represents a spectrum and the columns represent the properties of the spectrum such as scan number (unique to each spectrum), MS level, activation (i.e., ion fragmentation type), retention time, ion mobility arrival time, etc.: "Metadata (HDF5 dataset): each row in the metadata table represents a spectrum and the columns represent the properties of the spectrum such as scan number (unique to each spectrum), MS level,"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group) contains 1D arrays with indexes to Full_mz_array.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group) contains 1D arrays with indexes to Full_mz_array."
- [readme] These are included as an HDF5 dataset if detected during conversion to MZA: CCScalDT = [Tfix, Beta] for Agilent DT; CCScalSLIM = [C0, C1, C2, C3] for SLIM; CCScalTIMS = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9] for Bruker TimsTOF.: "These are included as an HDF5 dataset if detected during conversion to MZA: CCScalDT = [Tfix, Beta] for Agilent DT; CCScalSLIM = [C0, C1, C2, C3] for SLIM; CCScalTIMS = [C0, C1, C2, C3, C4, C5, C6,"
