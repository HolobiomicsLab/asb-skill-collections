---
name: pymzml-reader-initialization-with-custom-parameters
description: Use when you have an mzML file (e.g. Manuels_customs_ids.mzML) with non-standard
  custom index identifiers that cannot be parsed by pymzML's default index parser.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pymzML
  - Python
  - ElementTree
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/bty046
  title: pymzml
evidence_spans:
- In order to make pymzML accept other kinds of mzML data (e.g databases), one can
  implement an own wrapper
- from pymzml import spec
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

# pymzml-reader-initialization-with-custom-parameters

## Summary

Initialize a pymzML Reader object with custom parameters (particularly index_regex) to enable random-access retrieval of spectra from mzML files with non-standard index formats. This skill is essential when mzML files use custom identifier schemes that deviate from the standard spectrum index layout.

## When to use

You have an mzML file (e.g. Manuels_customs_ids.mzML) with non-standard custom index identifiers that cannot be parsed by pymzML's default index parser. You need random-access spectrum retrieval via bracket notation and can provide or derive a regular expression pattern with named groups 'ID' and 'offset' that matches your file's custom identifier scheme.

## When NOT to use

- Your mzML file uses standard spectrum index format — use default Reader initialization without index_regex parameter
- You do not know the structure of the custom identifier scheme and cannot construct a matching regex pattern
- You need only sequential (iterator-based) access to spectra rather than random access by custom ID

## Inputs

- mzML file path (string) with custom index identifiers
- Regular expression pattern (string) with named groups 'ID' and 'offset' matching the custom index format

## Outputs

- Spectrum object (from pymzML.spec) with parsed XML element and metadata
- Random-access Reader object configured for the custom mzML file

## How to apply

Define a regular expression pattern with named capture groups 'ID' (for spectrum identifiers) and 'offset' (for file byte offsets) that matches the custom index format in your mzML file. Import pymzML.run.Reader and instantiate it by passing both the mzML file path and your custom index_regex parameter. The Reader will apply the regex during initialization to parse the custom index structure. Use bracket notation (e.g., run[custom_id]) to retrieve individual spectra via the __getitem__ random-access function. Verify retrieval by checking that the returned object is a valid Spectrum instance with accessible ID and XML element attributes.

## Related tools

- **pymzML** (Parser and random-access interface for mzML data; provides Reader class with index_regex parameter support and Spectrum object model) — https://github.com/pymzml/pymzML
- **Python** (Host language for pymzML; regex module and control flow)
- **ElementTree** (XML parsing backend (cElementTree) used internally by pymzML to parse mzML structure and spectrum elements)

## Examples

```
from pymzML.run import Reader; import re; regex = r'(?P<ID>custom_\d+)_offset_(?P<offset>\d+)'; run = Reader('Manuels_customs_ids.mzML', index_regex=regex); spectrum = run['custom_1']; print(spectrum.ID, spectrum.xmlElement)
```

## Evaluation signals

- Reader object initializes without error and accepts the custom index_regex parameter
- Bracket notation retrieval run[custom_id] returns a non-None Spectrum object
- Returned Spectrum object has valid ID and XML element attributes matching the custom identifier
- Multiple random-access calls with different custom IDs retrieve distinct, correct spectra
- No fallback to sequential parsing or index rebuild is required after Reader initialization

## Limitations

- The regex pattern must correctly capture both 'ID' and 'offset' named groups; malformed patterns will fail silently or raise parsing exceptions during initialization
- The index_regex approach assumes the custom identifiers and offsets are present and parseable in the mzML file structure; entirely missing or corrupted index data cannot be recovered
- Performance of custom regex parsing depends on pattern complexity; overly complex patterns may slow Reader initialization for large files

## Evidence

- [other] pymzML.run.Reader accepts an index_regex parameter containing named groups 'ID' and 'offset': "pymzML.run.Reader accepts an index_regex parameter containing named groups 'ID' and 'offset' to parse custom index formats"
- [other] Define custom regex with named groups matching custom identifier scheme: "Define a custom index_regex pattern with named groups 'ID' and 'offset' that matches the identifier scheme in Manuels_customs_ids.mzML"
- [other] Bracket notation invocation and verification: "Invoke the bracket notation run[1] to retrieve the spectrum at custom index 1 using the __getitem__ random-access function. Verify the returned object is a valid Spectrum instance by checking its ID"
- [intro] pymzML random access capability: "Module to parse mzML data in Python... ability to write and read indexed gzip files"
- [intro] Custom API implementation for random access: "a new class needs to be written, which implements a `read` and a `__getitem__` function"
