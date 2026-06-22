---
name: error-handling-for-unsupported-formats
description: Use when building a file format dispatcher or initialization routine that must accept user-provided file paths and map them to format-specific processing modules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MSIGen
  - Python
  - pyBaf2Sql
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
---

# error-handling-for-unsupported-formats

## Summary

Implement format validation and exception handling to reject unsupported mass spectrometry imaging file types and provide clear diagnostic feedback. This skill ensures robust dispatch logic that fails fast with actionable error messages when input file extensions do not match MSIGen's supported vendor formats (.raw, .d, .baf, .tdf, .tsf, .mzML) or open-source standards.

## When to use

Apply this skill when building a file format dispatcher or initialization routine that must accept user-provided file paths and map them to format-specific processing modules. Use it whenever the system must gracefully handle unknown, misspelled, or unsupported file extensions before attempting to instantiate or call format-specific handlers (e.g., MSIGen.raw, MSIGen.D, MSIGen.baf). This is especially critical in interactive environments (GUI, Jupyter notebook, CLI) where users may provide malformed or incompatible input without prior validation.

## When NOT to use

- Do not use this skill if the file path has already been validated and the format is known to be supported; proceed directly to format-specific initialization.
- Do not use this skill as a substitute for runtime format validation during actual file I/O; it validates only the extension, not file integrity or internal structure.
- Do not use this skill if your workflow accepts only a single, hard-coded format (e.g., only .mzML); simpler conditional logic is more appropriate than a dispatcher.

## Inputs

- file_path: string (full or relative path to mass spectrometry imaging data file)
- file_extension: string (extracted from file path, e.g., '.raw', '.d', '.baf', '.tdf', '.tsf', '.mzML')

## Outputs

- module_handler: MSIGen module object or callable (e.g., MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tdf, MSIGen.tsf, MSIGen.mzml) ready for downstream data processing
- exception: structured error object (if format is unsupported) with diagnostic details and list of valid formats

## How to apply

Extract the file extension from the input file path string (e.g., using `os.path.splitext()` or string manipulation). Validate the extension against a whitelist of supported formats: .raw (Thermo), .d (Agilent), .baf (Bruker, requires pyBaf2Sql), .tdf (Bruker), .tsf (Bruker), and .mzML (open-source). If the extension is recognized, proceed to conditional dispatch logic that returns the corresponding MSIGen module object (e.g., MSIGen.raw, MSIGen.D, MSIGen.tsf, MSIGen.baf, MSIGen.tdf, MSIGen.mzml). If the extension is unrecognized or unsupported, raise a clear, structured exception that includes: (1) the invalid extension provided, (2) the full list of supported formats, and (3) guidance on how to obtain or convert data to a supported format. This early validation prevents silent downstream failures and reduces debugging time in batch or automated pipelines.

## Related tools

- **MSIGen** (Target framework providing format-specific modules (MSIGen.raw, MSIGen.D, MSIGen.baf, MSIGen.tdf, MSIGen.tsf, MSIGen.mzml) dispatched by this skill) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Optional dependency required for Bruker .baf format support; validation should check for this dependency if .baf extension is provided) — https://github.com/gtluu/pyBaf2Sql
- **Python** (Language for implementing file extension parsing, conditional dispatch, and exception raising; MSIGen requires Python >=3.9 and <=3.11)

## Examples

```
```python
def get_format_handler(file_path):
    import os
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    handlers = {'.raw': 'MSIGen.raw', '.d': 'MSIGen.D', '.baf': 'MSIGen.baf', '.tdf': 'MSIGen.tdf', '.tsf': 'MSIGen.tsf', '.mzml': 'MSIGen.mzml'}
    if ext not in handlers:
        raise ValueError(f"Unsupported format '{ext}'. Supported: {', '.join(handlers.keys())}")
    return handlers[ext]

handler = get_format_handler('sample.raw')  # Returns 'MSIGen.raw'
```
```

## Evaluation signals

- Unsupported file extension (e.g., '.xyz', '.raw2', '.TXT') triggers a structured exception with the invalid extension and the complete list of supported formats.
- Supported extension (e.g., '.raw', '.d', '.mzML') returns a valid module object or callable without exception.
- Case sensitivity is handled correctly: extensions like '.RAW' or '.Raw' are either normalized or explicitly rejected with clear messaging.
- Error message includes actionable guidance (e.g., 'To use .baf format, install pyBaf2Sql via: pip install git+https://github.com/gtluu/pyBaf2Sql') when an optional dependency is required.
- Dispatcher does not attempt to instantiate or load the format-specific module until the extension has been validated; exception is raised before any I/O or format-specific code is invoked.

## Limitations

- Extension validation alone does not guarantee file format integrity; a file with a .raw extension may be corrupted or internally malformed. This skill detects only the extension; downstream format-specific handlers must perform deeper validation.
- Case sensitivity in extension matching may vary by file system (case-insensitive on Windows, case-sensitive on Linux/macOS). Normalization (e.g., `.lower()`) is recommended but requires explicit implementation.
- Optional dependencies (e.g., pyBaf2Sql for .baf) are not checked by this skill; if a supported extension is dispatched but its required dependency is missing, the error will occur downstream in the format-specific module.
- Extensions alone may be ambiguous or insufficient for some Bruker formats (.tsf, .tdf, .baf all map to distinct modules); the dispatcher must map to the correct module, not just validate the extension.

## Evidence

- [methods] workflow_step_1_and_2: "Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). Implement conditional dispatch logic that maps each supported extension to its"
- [methods] workflow_step_4: "Raise a clear exception if the file extension is unsupported or unrecognized."
- [methods] supported_formats: "MSIGen.raw for Thermo .raw files, MSIGen.D for Agilent .d, MSIGen.tsf for Bruker .tsf, MSIGen.baf for Bruker .baf (requiring pyBaf2Sql), MSIGen.tdf for Bruker .tdf, and MSIGen.mzml for open-source"
- [readme] pyBaf2Sql_dependency: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [intro] multiple_interfaces: "MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types"
