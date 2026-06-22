---
name: module-loader-implementation
description: Use when you have mass spectrometry imaging data in multiple vendor or open-source formats and need to programmatically route each file to its correct processing handler based on file extension, avoiding hardcoded conditional chains and enabling extensible format support.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# module-loader-implementation

## Summary

Implement a file format dispatcher that maps input file extensions (.raw, .d, .baf, .tsf, .tdf, .mzML) to their corresponding MSIGen data processing modules, enabling runtime selection of the appropriate vendor-specific or open-source parser without manual code branching.

## When to use

Use this skill when you have mass spectrometry imaging data in multiple vendor or open-source formats and need to programmatically route each file to its correct processing handler based on file extension, avoiding hardcoded conditional chains and enabling extensible format support.

## When NOT to use

- Input file is already parsed into an in-memory data structure (NumPy array, pandas DataFrame); skip directly to processing workflow steps.
- File extension cannot be reliably determined from the path (e.g., extensionless files or ambiguous naming); preprocessing to normalize filenames is required first.
- Data format is not in the supported set (Thermo .raw, Agilent .d, Bruker .baf/.tsf/.tdf, or .mzML); consider format conversion or alternative tools.

## Inputs

- file path string (e.g., '/data/sample.raw', '/data/experiment.d')
- file extension (extracted from path; e.g., '.raw', '.baf', '.mzML')

## Outputs

- MSIGen module object or callable handler (e.g., MSIGen.raw, MSIGen.baf)
- exception object (descriptive message on unsupported format)

## How to apply

Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). Implement conditional dispatch logic that maps each supported extension to its corresponding MSIGen module: MSIGen.raw for Thermo .raw files, MSIGen.D for Agilent .d, MSIGen.tsf for Bruker .tsf, MSIGen.baf for Bruker .baf (which requires the pyBaf2Sql dependency to be installed), MSIGen.tdf for Bruker .tdf, and MSIGen.mzml for open-source .mzML files. Return the selected module object or callable handler for downstream processing. Raise a clear, descriptive exception if the file extension is unsupported or unrecognized, including the offending extension in the error message to aid debugging.

## Related tools

- **MSIGen** (Provides vendor-specific (.raw, .d, .baf, .tsf, .tdf) and open-source (.mzML) data processing modules that are selected and instantiated by the loader) — https://github.com/LabLaskin/MSIGen
- **pyBaf2Sql** (Required dependency for parsing Bruker .baf format files; must be installed before MSIGen.baf module can be used) — https://github.com/gtluu/pyBaf2Sql
- **Python** (Language in which conditional dispatch logic and exception handling are implemented; version >=3.9 and <=3.11 required)

## Examples

```
# Python snippet demonstrating module dispatch
file_path = '/data/sample.baf'
extension = file_path.split('.')[-1].lower()
module_map = {'raw': 'MSIGen.raw', 'baf': 'MSIGen.baf', 'tdf': 'MSIGen.tdf', 'tsf': 'MSIGen.tsf', 'd': 'MSIGen.D', 'mzml': 'MSIGen.mzml'}
if extension not in module_map:
    raise ValueError(f'Unsupported file format: .{extension}')
selected_module = module_map[extension]
print(f'Routing {file_path} to {selected_module}')
```

## Evaluation signals

- Verify the correct module is returned by checking the type or identity of the returned object against the expected module class for each input extension.
- Test all six supported file extensions (.raw, .d, .baf, .tsf, .tdf, .mzML) independently and confirm no crosstalk or misrouting occurs.
- Confirm that an exception with a clear, actionable message is raised and caught when an unsupported extension (e.g., '.xyz', '.img') is provided.
- For .baf format, verify that the dispatcher can only succeed if pyBaf2Sql is installed; check that a helpful error message guides installation if the dependency is missing.
- Confirm the module object returned is immediately usable by downstream processing code (e.g., can be instantiated with file path and processing parameters without type errors).

## Limitations

- Dispatch is based solely on file extension; if a file is misnamed or has the wrong extension for its actual content, the wrong module will be selected and likely fail during processing.
- Bruker .baf format support requires pyBaf2Sql to be installed separately; the dispatcher should validate this dependency is available before returning MSIGen.baf or raise an informative error.
- Does not perform schema validation or content inspection to verify the selected module is truly compatible with the file's internal structure; relies on file extension as a proxy for format identity.
- Extension matching is case-sensitive in most implementations; files with uppercase extensions (e.g., '.RAW', '.D') may not be recognized without preprocessing to lowercase.

## Evidence

- [other] MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types.: "MSIGen provides premade files for converting data to images using a GUI, jupyter notebook, or from the command line, with support for multiple vendor formats and data types."
- [other] Accept a file path string as input and extract the file extension; map each supported extension to its corresponding MSIGen module.: "Accept a file path string as input and extract the file extension (e.g., .raw, .d, .baf, .tsf, .tdf, .mzML). Implement conditional dispatch logic that maps each supported extension to its"
- [readme] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [other] Raise a clear exception if the file extension is unsupported or unrecognized.: "Raise a clear exception if the file extension is unsupported or unrecognized."
- [readme] MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format: "MSIGen is designed for converting mass spectrometry imaging (MSI) data from the raw line-scan data to a visualizable format"
