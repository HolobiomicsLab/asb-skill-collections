---
name: conditional-dispatch-logic-implementation
description: Use when when accepting a file path as input in an MSI data processing pipeline and you need to determine which data reader module to instantiate before calling get_image_data() or load_pixels(). This arises when building a multi-vendor instrument workflow (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSIGen
  - Python
  - pyBaf2Sql
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- MSIGen provides tools for processing mass spectrometry imaging data acquired in line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
- If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# conditional-dispatch-logic-implementation

## Summary

Implement a file-format–aware dispatch mechanism that routes mass spectrometry imaging data files (Thermo .raw, Agilent .d, Bruker .baf/.tdf/.tsf, or .mzML) to their corresponding MSIGen processing modules. This skill ensures that the correct vendor-specific or open-source data handler is selected and invoked based on file extension, enabling seamless support for heterogeneous instrument formats.

## When to use

When accepting a file path as input in an MSI data processing pipeline and you need to determine which data reader module to instantiate before calling get_image_data() or load_pixels(). This arises when building a multi-vendor instrument workflow (e.g., processing data from both Thermo and Bruker instruments in the same batch) or when the input format is not known at compile time.

## When NOT to use

- The input file has already been converted to a normalized intermediate format (e.g., NumPy array, .mzML) — dispatch logic applies only at the raw format detection stage.
- You are building a single-instrument-vendor pipeline with a known fixed format — hardcoding the module reference is simpler and faster than dynamic dispatch.
- The file path string is malformed, missing an extension, or the file does not exist on disk — perform validation before dispatching.

## Inputs

- file_path: string (e.g., '/data/sample.raw', 'experiment.d', 'output.mzML')
- supported_format_list: [string] (optional; list of allowed extensions for validation)

## Outputs

- module_handler: Python module or callable object (e.g., MSIGen.raw, MSIGen.mzml)
- format_type: string (canonical format identifier, e.g., 'thermo_raw', 'bruker_baf', 'open_mzml')

## How to apply

Extract the file extension from the input path string and implement conditional logic (if/elif chain or dispatch dictionary) that maps each extension to its corresponding MSIGen module object: .raw → MSIGen.raw, .d → MSIGen.D (with pyBaf2Sql dependency check for .baf format), .baf → MSIGen.baf, .tsf → MSIGen.tsf, .tdf → MSIGen.tdf, .mzML → MSIGen.mzml. For Bruker .baf files specifically, verify that pyBaf2Sql is installed; if not, raise a descriptive error directing the user to install from GitHub. Return the selected module object or a callable handler; if the extension is unrecognized, raise a clear exception listing supported formats. This design pattern ensures robust handling of vendor format diversity and provides actionable error messages when dependencies are missing.

## Related tools

- **MSIGen** (Provides format-specific module objects (MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tsf, MSIGen.tdf, MSIGen.mzml) that are selected and invoked by the dispatch logic.) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Dependency required for processing Bruker .baf format files; dispatch logic must verify its installation before routing .baf files.) — https://github.com/gtluu/pyBaf2Sql
- **Python** (Language for implementing the conditional dispatch logic; requires version >=3.9 and <=3.11.)

## Examples

```
if file_path.endswith('.raw'): handler = msigen.raw; elif file_path.endswith('.d'): handler = msigen.D; elif file_path.endswith('.baf'): import importlib; pyBaf2Sql = importlib.util.find_spec('pyBaf2Sql') or raise ImportError('pip install git+https://github.com/gtluu/pyBaf2Sql'); handler = msigen.baf; elif file_path.endswith(('.tsf', '.tdf', '.mzML')): handler = getattr(msigen, file_path.split('.')[-1].lower()); else: raise ValueError(f'Unsupported format. Supported: .raw, .d, .baf, .tsf, .tdf, .mzML')
```

## Evaluation signals

- File extension extraction is case-insensitive and correctly isolates the suffix from the full path (e.g., '.raw' from 'C:/data/experiment.raw').
- Each supported format (Thermo, Agilent, Bruker .baf/.tsf/.tdf, open-source .mzML) is mapped to its correct MSIGen module without fallback or aliasing errors.
- Dispatch returns a callable or module object that can be immediately passed to downstream functions like get_image_data() without type mismatch.
- Unsupported extensions raise an exception with a message listing all valid formats (e.g., 'Unsupported format. Supported formats: .raw, .d, .baf, .tsf, .tdf, .mzML').
- For Bruker .baf format, the dispatch logic detects missing pyBaf2Sql and raises a clear error with installation instructions (e.g., 'pip install git+https://github.com/gtluu/pyBaf2Sql') rather than failing downstream.

## Limitations

- Dispatch is based solely on file extension; it does not validate that the file content matches the declared format (e.g., a .raw file with incorrect vendor headers).
- pyBaf2Sql is a platform-specific dependency (requires .dll on Windows, .so on Linux); dispatch logic must account for OS-specific installation paths and may fail if the library is not installed.
- The logic does not handle compressed or archived formats (.zip, .tar.gz) — if raw files are bundled, they must be extracted before dispatch.
- MSIGen support is designed with nano-DESI MSI in mind; dispatch succeeds for other MSI acquisition modes, but data quality or correctness is not guaranteed.

## Evidence

- [other] How does MSIGen determine which data processing module to apply based on the input file format (Thermo .raw, Agilent .d, Bruker .baf/.tdf/.tsf, or .mzML)?: "How does MSIGen determine which data processing module to apply based on the input file format (Thermo .raw, Agilent .d, Bruker .baf/.tdf/.tsf, or .mzML)?"
- [other] 1. Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). 2. Implement conditional dispatch logic that maps each supported extension to its corresponding MSIGen module: MSIGen.raw for Thermo .raw files, MSIGen.D for Agilent .d, MSIGen.tsf for Bruker .tsf, MSIGen.baf for Bruker .baf (requiring pyBaf2Sql), MSIGen.tdf for Bruker .tdf, and MSIGen.mzml for open-source .mzML files. 3. Return the selected module object or callable handler. 4. Raise a clear exception if the file extension is unsupported or unrecognized.: "Implement conditional dispatch logic that maps each supported extension to its corresponding MSIGen module: MSIGen.raw for Thermo .raw files, MSIGen.D for Agilent .d, MSIGen.tsf for Bruker .tsf,"
- [readme] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [other] MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types.: "MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types."
- [intro] is designed with nano-DESI MSI in mind: "is designed with nano-DESI MSI in mind"
