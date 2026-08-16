---
name: spectrum-random-access-retrieval-via-bracket-notation
description: Use when when you need to retrieve specific spectra from mzML files by custom identifier (integer or string) rather than sequential iteration, especially when the mzML file uses non-standard index formatting that requires a regex pattern to parse spectrum IDs and file offsets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pymzML
  - Python
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pymzml_cq
    doi: 10.1093/bioinformatics/bty046
    title: pymzml
  dedup_kept_from: coll_pymzml_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty046
  all_source_dois:
  - 10.1093/bioinformatics/bty046
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-random-access-retrieval-via-bracket-notation

## Summary

Enable random access retrieval of mass spectrometry spectra from mzML files using bracket notation and custom index patterns. This skill allows direct spectrum lookup by identifier without sequential file parsing, essential for efficient analysis of large mzML datasets with non-standard indexing schemes.

## When to use

When you need to retrieve specific spectra from mzML files by custom identifier (integer or string) rather than sequential iteration, especially when the mzML file uses non-standard index formatting that requires a regex pattern to parse spectrum IDs and file offsets. Use this when file size or analysis design makes random access more efficient than sequential parsing.

## When NOT to use

- mzML file uses standard index format already parseable by default pymzML Reader (use standard Reader instead for clarity).
- Analysis requires sequential access to all spectra in order; bracket notation adds overhead if you must iterate through all records anyway.
- mzML file is not indexed or custom index information is not available in the file or separately documented.

## Inputs

- mzML file path (string)
- Custom index_regex pattern with named groups 'ID' and 'offset' (string)
- Spectrum identifier: integer or string matching the custom index scheme

## Outputs

- Spectrum object (pymzML Spectrum instance)
- XML element containing spectrum metadata and peak data

## How to apply

Define a regular expression pattern with named groups 'ID' and 'offset' that matches the custom identifier scheme in your mzML file (e.g., for Manuels_customs_ids.mzML). Instantiate pymzML.run.Reader on the mzML file path, passing the custom index_regex parameter containing your pattern. The Reader parses the regex during initialization to extract spectrum identifiers and their byte offsets in the file. Invoke bracket notation (e.g., run[custom_id] or run[1]) to trigger the __getitem__ random-access function, which retrieves the spectrum at that index from the file without scanning prior records. Verify the returned object is a valid Spectrum instance by inspecting its ID attribute and XML element structure.

## Related tools

- **pymzML** (Parser and random-access interface for mzML files; implements Reader class with __getitem__ method and index_regex parameter to enable spectrum retrieval by custom identifier) — https://github.com/pymzml/pymzML
- **Python** (Host language for pymzML; provides regex module and cElementTree XML parsing underlying the custom index parsing)

## Examples

```
import re
from pymzml.run import Reader
index_regex = r'id=(?P<ID>[^\s]+)\soffset=(?P<offset>\d+)'
run = Reader('Manuels_customs_ids.mzML', index_regex=index_regex)
spectrum = run[1]  # retrieve spectrum at custom index 1
```

## Evaluation signals

- Returned Spectrum object has a valid .ID attribute matching the requested custom identifier.
- Spectrum object's XML element can be parsed and contains expected CVParam and binaryDataArray child nodes.
- Bracket notation access is O(1) relative to file size (no sequential scan through preceding spectra).
- Multiple calls to bracket notation with different custom IDs retrieve distinct, correct spectra without file re-initialization.
- Regex pattern successfully parses all custom identifiers and offsets from the mzML index without errors or missed entries.

## Limitations

- Custom index_regex pattern must have exactly named groups 'ID' and 'offset'; malformed patterns will cause Reader instantiation to fail or silently skip entries.
- Random access is only as accurate as the offset values extracted by the regex; incorrect offsets will corrupt spectrum parsing.
- Regex-based indexing requires prior knowledge of the mzML file's non-standard index structure; no automatic detection of format is available.
- Large mzML files require sufficient memory to hold the parsed regex index structure during Reader initialization.

## Evidence

- [other] pymzML.run.Reader accepts an index_regex parameter containing named groups 'ID' and 'offset' to parse custom index formats: "pymzML.run.Reader accepts an index_regex parameter containing named groups 'ID' and 'offset' to parse custom index formats"
- [other] the regex pattern is applied during initialization to extract spectrum identifiers and their file offsets, enabling bracket-notation access via run[custom_id]: "the regex pattern is applied during initialization to extract spectrum identifiers and their file offsets, enabling bracket-notation access via run[custom_id]"
- [other] a new class needs to be written, which implements a `read` and a `__getitem__` function: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
- [other] parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go. The index used can be either an integer or a string: "parse the data blockwise, so every piece of data, which should be accessible by indexing is written in one go. The index used can be either an integer or a string"
- [readme] Module to parse mzML data in Python based on cElementTree: "Module to parse mzML data in Python based on cElementTree"
- [readme] random access in compressed files: "random access in compressed files"
