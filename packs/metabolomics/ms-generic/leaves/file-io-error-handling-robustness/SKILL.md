---
name: file-io-error-handling-robustness
description: Use when when designing or integrating a file parser for mass spectrometry formats (.raw Thermo RAW format, .mzml XML-based format) in a metabolomics processing pipeline, or when reading legacy or heterogeneous instrument output where file integrity cannot be guaranteed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - bmxp
  - bmxp.Chroma
  - C
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- They are written in Python and C
- pip install bmxp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# file-io-error-handling-robustness

## Summary

Implement defensive file I/O and error handling to ensure robust reading of mass spectrometry data files (.raw, .mzml) that may be malformed, truncated, or incomplete. This skill is essential in metabolomics pipelines where raw instrument data forms the critical input layer and upstream corruption directly cascades to all downstream analyses.

## When to use

When designing or integrating a file parser for mass spectrometry formats (.raw Thermo RAW format, .mzml XML-based format) in a metabolomics processing pipeline, or when reading legacy or heterogeneous instrument output where file integrity cannot be guaranteed. Apply this skill if your input data originates from multiple instruments, batches, or long-term storage, or if downstream modules depend on guaranteed structured output.

## When NOT to use

- Input is already in a validated, structured format (e.g., feature table, processed mzML with verified schema compliance) — skip to downstream modules like Eclipse or Gravity.
- Data integrity is pre-guaranteed by instrument vendor certification or prior successful processing — error handling overhead may be unnecessary, though logging remains advisable.
- Partial data loss is acceptable in your workflow — if you can tolerate lossy parsing, a simpler non-defensive parser may suffice, but this is not recommended for metabolomics QC pipelines.

## Inputs

- .raw files (Thermo RAW format with spectral metadata, scan information, ion data)
- .mzml files (XML-serialized spectral and chromatographic data)
- Reference .raw and .mzml files for validation against known fidelity

## Outputs

- Structured spectral objects or dictionaries with unified schema (scan number, retention time, m/z values, intensities, precursor information)
- Error logs and diagnostic messages documenting parsing failures, record offsets, and validation mismatches
- Validation report confirming data fidelity against reference files

## How to apply

Implement a layered error handling strategy: (1) Design the file format handler to detect file corruption early (e.g., verify magic bytes, XML well-formedness, or Thermo RAW header integrity) before attempting full deserialization. (2) Wrap format-specific parsers in try-catch blocks that gracefully degrade: catch malformed records and either skip them with logging, attempt partial reconstruction, or halt with a diagnostic error message. (3) Define a validation layer that compares parsed output against known reference files or schema invariants (e.g., retention time monotonicity, m/z value ranges, intensity positivity). (4) Log all exceptions with file path, record offset, and error context so that failures are reproducible and traceable. (5) Return unified data structures (scan number, retention time, m/z values, intensities, precursor information) only when validation passes; propagate errors upward if data fidelity cannot be confirmed. This approach ensures downstream modules (Eclipse, Gravity, Blueshift, Formation) receive only trustworthy input.

## Related tools

- **bmxp.Chroma** (Primary file I/O module that reads and parses .raw and .mzml files with error handling into unified data structures for BMXP pipeline) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/chroma/readme.md
- **Python** (Implementation language for file parsers, exception handling, and validation logic)
- **C** (Optional low-level performance optimization for high-throughput file parsing and binary format handling)

## Examples

```
from bmxp.chroma import ChromaParser; parser = ChromaParser(); spectrum_data = parser.read_file('sample.raw', validate_against_reference='reference.raw'); print(f'Parsed {len(spectrum_data)} scans with {len(spectrum_data[0].mz_values)} m/z values')
```

## Evaluation signals

- Parsed output conforms to the unified schema: all records include scan number, retention time, m/z values, intensities, and precursor information with no null/NaN fields except where biologically expected.
- Retention time values are monotonically increasing within each file, and m/z values fall within expected instrument range (typically 50–2000 m/z for metabolomics).
- Intensities are non-negative and within a reasonable dynamic range; outliers or negative values trigger validation warnings or errors.
- Error logs exist for all skipped or partially reconstructed records, with file path and byte offset, allowing manual inspection of corruption sites.
- Comparison of parsed output against reference .raw and .mzml files shows bit-exact or high-fidelity match for spectral metadata, scan count, and feature abundances (e.g., cosine similarity > 0.99 for reconstructed ion currents).

## Limitations

- Thermo RAW format is proprietary and vendor-specific; parsing may require reverse-engineered specifications or vendor SDKs, limiting portability.
- mzML XML deserialization can be memory-intensive for large files (multi-GB instrument outputs); stream-based parsing or chunking may be necessary.
- Truncated files at the end-of-file boundary may lose the last few scans without warning; a checksum or file-size sanity check should precede parsing.
- Malformed but parseable records (e.g., zero-intensity scans, missing precursor m/z) may pass syntax validation but fail semantic validation; explicit schema checks are essential.
- Legacy or proprietary mass spectrometry formats not in {.raw, .mzml} are outside Chroma's scope; custom parsers must be developed and validated independently.

## Evidence

- [other] Chroma is designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing in the BMXP pipeline.: "Chroma is a standalone module designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing in the BMXP pipeline."
- [other] Error handling must be implemented to ensure robust reading of malformed or truncated files.: "Implement file I/O and error handling to ensure robust reading of malformed or truncated files."
- [other] Parsers must extract and reconstruct data into unified structures abstracting both .raw and .mzml formats.: "Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information)."
- [other] Validation against reference files confirms data fidelity of parsed output.: "Validate the structured output against known reference .raw and .mzml files to confirm fidelity of parsed data."
- [readme] Chroma reads .raw and .mzml files at the start of the BMXP metabolomics processing pipeline.: "Chroma - Read .raw and .mzml files"
