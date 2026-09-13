---
name: vendor-file-format-specification-handling
description: Use when you have a raw MSI data file from an unknown or mixed set of
  vendors and need to apply format-specific data extraction, spectral parsing, or
  image reconstruction. The file extension alone must determine which parsing module
  (MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tdf, MSIGen.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MSIGen
  - Python
  - pyBaf2Sql
  techniques:
  - CE-MS
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in
  line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you are planning on using Bruker .d data in the .baf format, you will also need
  to install pyBaf2Sql from GitHub
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msigen_cq
    doi: 10.1021/jasms.4c00178
    title: MSIGen
  dedup_kept_from: coll_msigen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00178
  all_source_dois:
  - 10.1021/jasms.4c00178
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# vendor-file-format-specification-handling

## Summary

Route mass spectrometry imaging (MSI) data files to the correct processing module based on vendor-specific file format signatures. This skill ensures that instrument-native formats (Thermo .raw, Agilent .d, Bruker .baf/.tdf/.tsf) and open-source formats (.mzML) are handled by their corresponding data access libraries, avoiding format mismatch errors and enabling seamless multi-vendor workflows.

## When to use

You have a raw MSI data file from an unknown or mixed set of vendors and need to apply format-specific data extraction, spectral parsing, or image reconstruction. The file extension alone must determine which parsing module (MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tdf, MSIGen.tsf, or MSIGen.mzml) to instantiate. This is essential before invoking any downstream processing step that depends on correctly parsed m/z, intensity, mobility, or spatial coordinate arrays.

## When NOT to use

- The MSI data has already been converted to a vendor-neutral format (e.g., .mzML or NumPy array) and no further dispatch is needed.
- The file extension is ambiguous or the file header must be inspected to disambiguate format (e.g., distinguishing between .tsf and .tdf by binary magic number rather than extension alone).
- You are working exclusively with a single vendor's data type and hard-coded module import is acceptable; dispatch logic adds unnecessary complexity.

## Inputs

- file_path: string (full or relative path to a vendor or open-source MSI data file)
- supported_formats: list of strings (e.g., ['.raw', '.d', '.baf', '.tdf', '.tsf', '.mzML'])

## Outputs

- module_object: callable handler or module reference for the matched format (e.g., MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tdf, MSIGen.tsf, MSIGen.mzml)
- format_identifier: string (canonical format code, e.g., 'thermo_raw', 'agilent_d', 'bruker_baf', 'bruker_tdf', 'bruker_tsf', 'mzml')

## How to apply

Extract the file extension from the input file path (e.g., '.raw', '.d', '.baf', '.tdf', '.tsf', '.mzML'). Implement a conditional dispatch mapping each extension to its corresponding MSIGen module or handler: .raw → MSIGen.raw (Thermo), .d → MSIGen.D (Agilent), .baf → MSIGen.baf (Bruker, requires pyBaf2Sql), .tdf → MSIGen.tdf (Bruker TIMS), .tsf → MSIGen.tsf (Bruker), .mzML → MSIGen.mzml (open-source). For Bruker .baf files, verify that pyBaf2Sql is installed and the Baf2Sql DLL/.so is accessible. Return the selected module object or raise a clear exception (with file extension and supported types listed) if the extension is unrecognized or unsupported. This dispatch must complete before passing the file to the MSIGen generator and before any mass tolerance filtering or image normalization is applied.

## Related tools

- **MSIGen** (Dispatch target: provides modular data access libraries (MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tdf, MSIGen.tsf, MSIGen.mzml) for vendor-specific and open-source formats; returns parsed spectral and spatial data.) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Dependency for Bruker .baf format handling; wraps Bruker's Baf2Sql data access library to extract m/z, intensity, and frame metadata from .baf files.) — https://github.com/gtluu/pyBaf2Sql
- **Python** (Language for implementing conditional dispatch logic and file extension parsing (version ≥3.9 and <3.12 required for MSIGen compatibility).)

## Examples

```
file_path = 'sample.baf'; ext = file_path.split('.')[-1].lower(); module = {'raw': MSIGen.raw, 'd': MSIGen.D, 'baf': MSIGen.baf, 'tdf': MSIGen.tdf, 'tsf': MSIGen.tsf, 'mzml': MSIGen.mzml}.get(ext); assert module is not None, f'Unsupported format: .{ext}'
```

## Evaluation signals

- Correct module object is returned for each file extension (e.g., isinstance(returned_module, MSIGen.raw) for .raw files).
- Exception is raised with informative message (listing unsupported extension and supported types) when file extension is unrecognized.
- For Bruker .baf files, pyBaf2Sql import succeeds and Baf2Sql DLL/.so is accessible; for other formats, standard libraries load without ImportError.
- Downstream data extraction (e.g., get_image_data(), spectral array parsing) completes without format mismatch or binary read errors.
- File extension matching is case-insensitive or normalized (e.g., '.RAW' and '.raw' both dispatch to MSIGen.raw).

## Limitations

- Extension-based dispatch fails if file extension is missing, incorrect, or renamed; no fallback to binary magic number or file header inspection is provided in the skill scope.
- Bruker .baf format requires manual installation of pyBaf2Sql from GitHub; if not installed, dispatch will fail at import time with a clear error.
- The skill does not validate that the selected module is compatible with the downstream processing parameters (e.g., mobility_tolerance makes sense for .tdf but not .raw); semantic validation is the responsibility of the caller.
- No handling for compressed or archived formats (e.g., .zip, .tar.gz containing vendor data); only single-file extensions are supported.
- Windows and Linux Baf2Sql .dll/.so files are packaged with pyBaf2Sql; macOS support is not explicitly mentioned in available documentation.

## Evidence

- [other] Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). Implement conditional dispatch logic that maps each supported extension to its corresponding MSIGen module: "Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). Implement conditional dispatch logic that maps each supported extension to its"
- [other] Return the selected module object or callable handler. Raise a clear exception if the file extension is unsupported or unrecognized.: "Return the selected module object or callable handler. 4. Raise a clear exception if the file extension is unsupported or unrecognized."
- [other] MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types.: "MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types."
- [readme] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [readme] This package is a Python wrapper for Bruker's Baf2Sql data access library to be used with other Python packages.: "This package is a Python wrapper for Bruker's Baf2Sql data access library to be used with other Python packages."
