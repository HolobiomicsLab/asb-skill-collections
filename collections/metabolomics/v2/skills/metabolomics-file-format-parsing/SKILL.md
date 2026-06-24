---
name: metabolomics-file-format-parsing
description: Use when you have mwTab-formatted files from the Metabolomics Workbench
  containing MS or NMR experimental metadata and tabular data sections (e.g., METABOLITES,
  DATA blocks), and need to load them into memory for downstream conversion, validation,
  or analysis rather than manual text parsing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - jsonschema
  - mwtab
  - pandas
  - Python 3.6+
  - R
  - SMART (Data Import module)
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
- doi: 10.1021/acs.analchem.5c03225
  title: ''
evidence_spans:
- The ``mwtab`` package is a Python library
- jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwtab_python_library_for_restful_access_cq
    doi: 10.3390/metabo11030163
    title: mwtab Python Library for RESTful Access
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_mwtab_python_library_for_restful_access_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11030163
  all_source_dois:
  - 10.3390/metabo11030163
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-file-format-parsing

## Summary

Parse mwTab-formatted files containing Mass Spectrometry (MS) and Nuclear Magnetic Resonance (NMR) experimental data from the Metabolomics Workbench into structured in-memory MWTabFile objects. This skill enables programmatic access to metabolomics archival data through standardized file reading and object instantiation.

## When to use

You have mwTab-formatted files from the Metabolomics Workbench containing MS or NMR experimental metadata and tabular data sections (e.g., METABOLITES, DATA blocks), and need to load them into memory for downstream conversion, validation, or analysis rather than manual text parsing.

## When NOT to use

- Input is already a JSON representation of mwTab data — use the JSON directly instead of re-parsing.
- Input is raw MS/NMR spectral data in mzML, mzXML, or NetCDF format — use a specialized mass spectrometry parser (e.g., pymzml, pyopenms) instead.
- You only need to validate schema compliance without programmatic access to parsed objects — use jsonschema validation directly on the raw file.

## Inputs

- mwTab-formatted text file (from Metabolomics Workbench archival)
- ANALYSIS_ID string (for remote file fetching via URL)
- File path or file handle to local mwTab file

## Outputs

- MWTabFile object (in-memory representation with metadata and tabular blocks)
- Parsed block dictionary (keys accessible via mwfile.keys())
- Study metadata (study_id, analysis_id, source attributes)

## How to apply

Use the mwtab.fileio.read_files function to load mwTab-formatted files by their ANALYSIS_ID or file paths, parsing the text structure into blocks and key-value metadata. For each parsed file, instantiate an MWTabFile object from the mwtab.mwtab module to represent the data as an in-memory Python object with structured access to study_id, analysis_id, source attributes, and block keys. The mwtab parser respects the mwTab format's block-based structure—metadata headers followed by tabular sections—and preserves column names and data types during instantiation. Validate the parsed structure against the jsonschema-defined JSON schema to confirm structural correctness before proceeding to downstream steps.

## Related tools

- **mwtab** (Core library providing read_files function and MWTabFile object class for parsing mwTab format) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Handles tabular data sections (METABOLITES, DATA blocks) during parsing, preserving column names and data types)
- **jsonschema** (Validates parsed MWTabFile structure against JSON schema definition to confirm correctness)
- **Python 3.6+** (Runtime environment for executing mwtab parsing code)

## Examples

```
import mwtab
for mwfile in mwtab.read_files("1", "2"):
    print("STUDY_ID:", mwfile.study_id)
    print("ANALYSIS_ID:", mwfile.analysis_id)
    print("Blocks:", list(mwfile.keys()))
```

## Evaluation signals

- Returned MWTabFile object has non-null study_id, analysis_id, and source attributes matching input metadata
- Block keys (accessible via mwfile.keys()) correspond to expected sections (e.g., METABOLITES, DATA)
- Parsed tabular data preserves original column names and row counts without truncation or type coercion errors
- jsonschema validation passes with no structural errors when comparing parsed object to mwTab JSON schema
- Multiple successive calls to read_files with different ANALYSIS_IDs yield distinct MWTabFile objects with non-overlapping data

## Limitations

- mwtab requires Python 3.6+ and may not work with legacy Python 2.x environments.
- Remote file fetching via ANALYSIS_ID depends on live Metabolomics Workbench API availability; network failures will raise exceptions.
- Tabular data sections with non-standard column types or missing headers may cause pandas parsing to fail silently or produce truncated objects.
- No changelog found in the repository, making it difficult to track breaking changes between versions.

## Evidence

- [readme] The mwtab package facilitates reading and writing files in mwTab format used by the Metabolomics Workbench for archival of Mass Spectrometry (MS) and Nuclear Magnetic Resonance (NMR) experimental data.: "The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear"
- [other] Load an mwTab file using the mwtab.fileio.read_files function to parse the text structure, then instantiate an MWTabFile object.: "Load an mwTab-formatted file using the mwtab.fileio.read_files function to parse the text structure. 2. Instantiate an MWTabFile object from mwtab.mwtab to represent the parsed data in memory."
- [other] Validate converted structures against jsonschema-defined JSON schema to confirm structural correctness.: "Write the JSON output to a file with proper formatting and validation against the jsonschema-defined JSON schema to confirm structural correctness."
- [other] Process each MWTabFile instance one at a time in a for-loop from the generator.: "Process each :class:`~mwtab.mwtab.MWTabFile` instance: Process ``mwTab`` files in a for-loop, one file at a time."
- [readme] The mwtab package can be used as a library for accessing and manipulating data stored in mwTab format files.: "As a library for accessing and manipulating data stored in ``mwTab`` format files."
