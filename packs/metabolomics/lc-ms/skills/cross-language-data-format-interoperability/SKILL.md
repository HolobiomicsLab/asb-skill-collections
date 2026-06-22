---
name: cross-language-data-format-interoperability
description: Use when you have mass spectrometry data (LC–MS/MS, ion mobility, DIA) converted to MZA format and need to read or analyze it in multiple programming languages (Python and R), or share datasets with collaborators using different environments without requiring proprietary vendor libraries or format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3957
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZA
  - h5py
  - rhdf5
  - HDF5
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00313
  title: MZA
evidence_spans:
- MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data
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

# cross-language-data-format-interoperability

## Summary

Access and manipulate multidimensional mass spectrometry data stored in vendor-neutral HDF5 format using generic HDF5 libraries (h5py, rhdf5) across Python, R, and other programming languages without format conversion. This skill enables interoperable workflows for MS data analysis by leveraging the MZA format's simple, language-agnostic HDF5 structure.

## When to use

You have mass spectrometry data (LC–MS/MS, ion mobility, DIA) converted to MZA format and need to read or analyze it in multiple programming languages (Python and R), or share datasets with collaborators using different environments without requiring proprietary vendor libraries or format re-conversion.

## When NOT to use

- Input is a proprietary vendor format (.raw, .d) and MZA conversion has not yet been performed; use MZA command-line tool first.
- You require access to raw detector signals, frame metadata, or calibration coefficients not exposed in the simplified MZA structure.
- Your workflow depends on real-time streaming or incremental writes to the HDF5 file; MZA files are structured for read-heavy post-conversion access.

## Inputs

- MZA-format HDF5 file (.mza extension)
- Vendor MS data file (Agilent .d, Bruker .d with ion mobility, Thermo .raw, or mzML) — optional, needed only for initial MZA conversion

## Outputs

- Parsed metadata table (pandas DataFrame or R data.frame) with spectrum properties (Scan, MSLevel, RetentionTime, IonMobilityTime, TIC, etc.)
- Spectrum-level m/z and intensity arrays (NumPy arrays or R vectors)
- Aggregated summaries (e.g., total ion current by retention time, ion mobility distributions)
- Cross-language consistency report (optional)

## How to apply

Load an MZA HDF5 file using h5py (Python) or rhdf5 (R), then traverse the three HDF5 groups (Metadata, Arrays_intensity, Arrays_mz or Arrays_mzbin for ion mobility data) to extract spectra. For each spectrum, retrieve intensity and m/z values by querying the group using the Scan identifier from the metadata table. Optionally apply intensity thresholds during conversion (–intensityThreshold parameter) to reduce file size. Verify cross-language consistency by reading the same file in both Python and R and comparing metadata row counts and intensity distributions. The MZA structure omits zero-intensity values, so reconstruct full spectra by pairing m/z and intensity arrays per Scan, and use Full_mz_array for ion mobility data where m/z is indexed via Arrays_mzbin.

## Related tools

- **MZA** (Converts multidimensional mass spectrometry data from vendor formats to HDF5; produces the .mza files read by this skill) — https://github.com/PNNL-m-q/mza
- **h5py** (Python library for reading and writing HDF5 files; used to load MZA data in Python workflows)
- **rhdf5** (R package for reading and writing HDF5 files; used to load MZA data in R workflows)
- **HDF5** (Underlying binary format standard on which MZA data structure is based; enables language-agnostic access)

## Examples

```
import h5py
import pandas as pd
with h5py.File('data.mza', 'r') as f:
    metadata = pd.DataFrame(f['Metadata'][:])
    scan_630_mz = f['Arrays_mz/630'][:]
    scan_630_intensity = f['Arrays_intensity/630'][:]
```

## Evaluation signals

- Metadata table can be loaded identically in both Python (via h5py + pandas) and R (via rhdf5), with matching row counts and column names.
- Intensity and m/z arrays for a given Scan value are identical (within floating-point precision) when read in Python and R.
- Total ion current (TIC) metadata column matches the sum of intensity values across all m/z bins for each spectrum.
- Ion mobility data: Arrays_mzbin indices correctly reference rows in Full_mz_array; no out-of-bounds indexing occurs.
- File size reduction is consistent with –intensityThreshold parameter used during conversion (lower threshold → larger file).

## Limitations

- MZA files omit zero-intensity values (sparse storage), so full spectra must be reconstructed by pairing m/z and intensity arrays; missing m/z values have zero intensity by definition.
- For ion mobility data, m/z values are stored as indexes (mzbins) to a shared Full_mz_array, not per-spectrum; reconstructing full spectral data requires index lookup.
- Partitioning into multiple HDF5 groups (Arrays_intensity0, Arrays_intensity1, etc.) may occur for very large files; the MzaPath metadata column indicates which partition to query.
- CCS calibration coefficients (CCScalDT, CCScalTIMS, CCScalSLIM) are only present if detected during conversion; their absence does not prevent data access but limits ion mobility interpretation.
- MZA binary depends on vendor libraries (Agilent Mass Hunter, Thermo MSFileReader, Bruker TDF-SDK) and currently runs on Windows natively or via Wine/Docker on Unix-like systems; conversion must precede data access.

## Evidence

- [readme] MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.: "MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure"
- [readme] Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5).: "Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5)."
- [readme] The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.: "The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum."
- [readme] Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table: Arrays_intensity (HDF5 group): contains 1D arrays with intensity values. Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.: "Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the 'Scan' value in the metadata table: Arrays_intensity (HDF5 group):"
- [readme] For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values common for all spectra in the file.: "For IM spectra the m/z dimension is stored as indexes (mzbins): Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array. Full_mz_array (HDF5 dataset): 1D array of full m/z values"
- [readme] Example scripts are provided in the respective folders. R requires the rhdf5 package and Python requires the h5py, hdf5plugin, numpy and matplotlib packages: "Example scripts are provided in the respective folders. R requires the rhdf5 package and Python requires the h5py, hdf5plugin, numpy and matplotlib packages"
