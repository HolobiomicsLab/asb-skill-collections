---
name: spectrum-object-schema-design
description: Use when when building a mass spectrometry data import pipeline that must ingest spectra from multiple file formats and produce a unified, queryable representation suitable for metadata validation, peak filtering, and similarity comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-object-schema-design

## Summary

Design and implement a Spectrum object schema that normalizes heterogeneous mass spectrometry data formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) into a unified data structure. This schema serves as the foundation for consistent metadata extraction, peak list representation, and downstream processing in mass spectrometry workflows.

## When to use

When building a mass spectrometry data import pipeline that must ingest spectra from multiple file formats and produce a unified, queryable representation suitable for metadata validation, peak filtering, and similarity comparisons. Use this skill at the start of any matchms-based workflow to establish the canonical in-memory representation of spectral data.

## When NOT to use

- If spectral data is already loaded into memory as matchms Spectrum objects — the schema design step is upstream of parsing.
- If you only need to work with a single, homogeneous spectral data format — the unifying value of a schema is diminished.
- If your workflow does not require preservation of metadata or only consumes peak m/z and intensity values — a simpler tuple-based representation may suffice.

## Inputs

- Raw mass spectrometry spectral data files in one or more of: mzML, mzXML, msp, MGF, JSON, metabolomics-USI formats
- Format-specific documentation or example files defining metadata and peak list structure for each supported format

## Outputs

- Spectrum object schema (Python class definition with type hints and field documentation)
- A set of parser functions, one per supported file format, that return matchms Spectrum object instances
- Unit test suite (pytest) validating parser correctness for representative samples in each format

## How to apply

Design a Spectrum object class in Python that includes fields for both metadata (e.g., precursor m/z, ionization mode, compound name) and peak data (m/z and intensity pairs). Document the schema as class attributes with type hints and docstrings. For each supported format (mzML, mzXML, msp, MGF, JSON, metabolomics-USI), create a dedicated parser function that extracts format-specific fields, maps them to the canonical Spectrum schema, and constructs instances. Validate that all parsers handle edge cases (missing metadata, variable peak list lengths, format-specific conventions) consistently. Use pytest to unit-test each parser against representative samples in each format, ensuring round-trip fidelity where applicable. The schema should be flexible enough to accommodate optional metadata while enforcing required fields (e.g., peaks array, precursor m/z).

## Related tools

- **Python** (Language for defining the Spectrum object class, implementing parser functions, and writing schema validation logic)
- **pytest** (Framework for unit testing parser correctness and ensuring Spectrum object construction from each file format)
- **matchms** (The library whose Spectrum object schema is being designed and whose parser module will be implemented) — https://github.com/matchms/matchms

## Examples

```
# Define Spectrum schema in Python
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Spectrum:
    peaks: List[Tuple[float, float]]  # [(m/z, intensity), ...]
    metadata: Dict[str, any]
    precursor_mz: float

# Parse mzML file using format-specific parser
from matchms.importing import load_from_mzml
spectra = load_from_mzml('sample.mzML')

# Validate schema conformance with pytest
pytest tests/test_parsers.py -v
```

## Evaluation signals

- All parser functions successfully construct Spectrum objects with identical metadata and peak lists when ingesting the same data in different formats (cross-format consistency check).
- Unit tests pass for representative samples in each of the six supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) without errors or warnings.
- Spectrum objects conform to the schema: all required fields are populated, optional fields are gracefully handled (None or defaults), and peak data arrays have consistent structure (m/z, intensity pairs).
- Existing matchms tests remain unbroken after schema and parser integration, confirmed by running `pytest` on the full test suite.
- Metadata round-trip validation: metadata extracted by parsers can be read back and compared to original file values with acceptable fidelity (accounting for format-specific precision or unit conversions).

## Limitations

- The schema must accommodate heterogeneous metadata across formats — some formats may lack certain fields (e.g., instrument type, collision energy), necessitating optional fields or defaults that may reduce data completeness.
- File format specifications may be incomplete or may have multiple conventions in use; parsers must handle variant encodings, which may require heuristic detection or user-supplied hints.
- Large spectral files (especially mzML/mzXML with dense peak lists) may consume significant memory when loaded as Spectrum objects; streaming or lazy-loading strategies may be needed for production workflows.
- Some formats (e.g., metabolomics-USI) may require external API calls or network access to resolve spectral data, introducing latency and failure modes outside the schema design itself.

## Evidence

- [other] Matchms supports loading mass spectrometry spectra from six file formats: mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "Matchms supports loading mass spectrometry spectra from six file formats: mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [other] Design Spectrum object schema and file format parsers for mzML, mzXML, msp, MGF, JSON, and metabolomics-USI using Python.: "Design Spectrum object schema and file format parsers for mzML, mzXML, msp, MGF, JSON, and metabolomics-USI using Python."
- [other] Implement individual parser functions that extract metadata and peak lists from each format and construct matchms Spectrum objects.: "Implement individual parser functions that extract metadata and peak lists from each format and construct matchms Spectrum objects."
- [other] Write unit tests using pytest to validate correct parsing and Spectrum object construction for representative samples in each format.: "Write unit tests using pytest to validate correct parsing and Spectrum object construction for representative samples in each format."
- [readme] transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
