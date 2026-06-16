---
name: mass-spectrometry-data-import
description: Use when when beginning a new mass spectrometry analysis workflow with raw spectral data files in mzML, mzXML, msp, MGF, or JSON format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - pytest
  - Python
derived_from:
- doi: 10.21105/joss.02411
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.21105/joss.02411
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
---

# mass-spectrometry-data-import

## Summary

Load raw mass spectrometry spectral data from standard file formats (mzML, mzXML, msp, MGF, JSON) into matchms Spectrum objects for downstream processing and analysis. This is the foundational step that transforms heterogeneous file formats into a uniform, in-memory representation suitable for cleaning, filtering, and similarity comparisons.

## When to use

When beginning a new mass spectrometry analysis workflow with raw spectral data files in mzML, mzXML, msp, MGF, or JSON format. Use this skill whenever you need to load spectra from public databases or instrument-generated files before applying metadata validation, peak filtering, or similarity scoring.

## When NOT to use

- If spectral data is already loaded in memory as Spectrum objects from a prior workflow step.
- If the input file is in an unsupported format not listed in matchms documentation (e.g., raw vendor binary formats without prior conversion).
- If the task requires only metadata inspection without needing the full peak intensity data (consider metadata-only parsing if available).

## Inputs

- Spectral data file in mzML format
- Spectral data file in mzXML format
- Spectral data file in msp format
- Spectral data file in MGF format
- Spectral data file in JSON format
- File path or URI to spectral data

## Outputs

- Spectrum collection (Python object list or iterable)
- Array of Spectrum objects with parsed peaks and metadata

## How to apply

Use matchms import functions (e.g., `import_spectra()` or format-specific loaders) to read the spectral data file and parse it into a collection of Spectrum objects. The import operation automatically handles format-specific parsing rules and metadata extraction. After import, verify that the spectrum collection contains the expected number of spectra and that critical metadata fields (precursor m/z, instrument type, retention time) are populated. The imported spectra are then passed directly to subsequent cleaning, filtering, or comparison steps in the workflow.

## Related tools

- **matchms** (Core library providing spectral data import functions and Spectrum object representation) — https://github.com/matchms/matchms
- **Python** (Programming language and runtime for executing matchms import operations)

## Examples

```
from matchms.importing_utils import load_from_mgf
spectra = load_from_mgf('library.mgf')
print(f'Loaded {len(spectra)} spectra')
```

## Evaluation signals

- Spectrum collection size matches the expected number of spectra in the input file (or summary reported by the import function).
- All Spectrum objects contain valid peaks (m/z and intensity pairs) with m/z values in expected range (e.g., 0–2000 m/z).
- Critical metadata fields (precursor_mz, instrument_type, spectrum_id) are non-null for all or most spectra (compare against file statistics).
- No exceptions or warnings raised during import; import completes in expected time (< seconds for typical libraries).
- Exported spectrum collection (to MGF or JSON) maintains equivalent peak and metadata content as original file.

## Limitations

- Matchms supports only the listed formats (mzML, mzXML, msp, MGF, JSON); other vendor-proprietary formats require prior conversion.
- Import does not validate or clean metadata; metadata errors in the source file are preserved in the imported Spectrum objects.
- Large spectral libraries (hundreds of thousands of spectra) may require significant memory; sparse or streaming import is not covered in this step.
- Metabolomics-USI format is mentioned as supported in the README but not detailed in the workflow cards; compatibility depends on the specific USI variant.

## Evidence

- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Load spectral data from a file (MGF, MSP, or mzML format) using matchms import functions: "Load spectral data from a file (MGF, MSP, or mzML format) using matchms import functions"
- [readme] It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data"
