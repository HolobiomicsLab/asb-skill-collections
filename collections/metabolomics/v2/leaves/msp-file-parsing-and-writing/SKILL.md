---
name: msp-file-parsing-and-writing
description: Use when you have one or more .msp spectral library files (NIST format)
  that need to be ingested for metadata curation, enrichment via web services, or
  export after transformation. Use this skill as the entry and exit point for any
  .msp-based annotation or analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MSMetaEnhancer
  - CIR
  - CTS
  - PubChem
  - IDSM
  - BridgeDb
  - Python
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.21105/joss.04494
  title: msmetaenhancer
evidence_spans:
- MSMetaEnhancer is a tool used for `.msp` files annotation
- 'Converter Builder: Automatically discovers and instantiates available converters'
- 'fetched from the following services: CIR, CTS, PubChem, IDSM, and BridgeDb'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msmetaenhancer
    doi: 10.21105/joss.04494
    title: msmetaenhancer
  dedup_kept_from: coll_msmetaenhancer
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.04494
  all_source_dois:
  - 10.21105/joss.04494
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msp-file-parsing-and-writing

## Summary

Load, manipulate, and export mass spectrometry spectral library records in .msp (NIST MS Search) format using MSMetaEnhancer's Application class. This skill enables structured reading and writing of compound metadata (name, SMILES, InChI, CAS number) and spectral annotations for batch processing and enrichment workflows.

## When to use

You have one or more .msp spectral library files (NIST format) that need to be ingested for metadata curation, enrichment via web services, or export after transformation. Use this skill as the entry and exit point for any .msp-based annotation or analysis pipeline.

## When NOT to use

- Input is already in a different spectral format (mzML, mzXML, NetCDF) — use format-specific parsers instead.
- You need to perform real-time streaming analysis of very large .msp files (>10 GB) without loading into memory — consider chunked or streaming parsers.
- You only need to extract a few scattered records — direct text parsing may be faster than initializing the full Application class.

## Inputs

- .msp file (NIST MS Search format with compound metadata and spectral records)

## Outputs

- .msp file (annotated or curated NIST MS Search format)
- in-memory spectra record collection (Application object)

## How to apply

Initialize the MSMetaEnhancer Application class and use its `load_data()` method with file_format='msp' to parse the input .msp file into an in-memory record structure. After performing transformations (e.g., metadata enrichment via converters, curation), call `save_data()` with file_format='msp' to serialize the annotated records back to an output .msp file. The Application class abstracts the line-by-line parsing of .msp fields (compound name, formula, SMILES, InChI, CAS number, spectrum peaks) and maintains metadata integrity throughout the workflow. Verify correct parsing by spot-checking that key metadata fields (name, InChI, SMILES, CAS) are present and non-null in loaded records before proceeding to annotation steps.

## Related tools

- **MSMetaEnhancer** (Application class for loading, manipulating, and saving .msp spectral library files) — https://github.com/RECETOX/MSMetaEnhancer
- **Python** (Runtime language for executing MSMetaEnhancer Application workflow)

## Examples

```
app = Application(); app.load_data('sample.msp', file_format='msp'); app.save_data('sample_out.msp', file_format='msp')
```

## Evaluation signals

- Loaded spectra record count matches the number of compound entries in the input .msp file (verify via line-count heuristic or explicit record iteration).
- All expected metadata fields (name, formula, SMILES, InChI, CAS number) are present in ≥50% of records after parsing; missing fields are represented as null or empty string, not exceptions.
- Output .msp file is valid NIST format: each record contains required headers (Name:, Formula:), followed by peak data in m/z intensity pairs; file opens without parse errors in external MS Search tools.
- Round-trip consistency: loading, saving, and re-loading the same .msp file produces identical metadata and peak records (no silent data loss or corruption).
- Metadata fields retain their original values (no unexpected transformations) unless explicitly modified by downstream curation or annotation steps.

## Limitations

- The Application class loads the entire .msp file into memory; very large spectral libraries (>100,000 compounds) may cause memory exhaustion on systems with <4 GB RAM.
- Custom or non-standard .msp extensions not recognized by the parser (e.g., vendor-specific metadata fields) may be silently dropped or cause parsing errors.
- No built-in validation of chemical structure consistency (e.g., whether SMILES and InChI represent the same compound); incorrect or malformed structures are written as-is to output.

## Evidence

- [other] Load a sample .msp spectra file into the MSMetaEnhancer Application class.: "Load a sample .msp spectra file into the MSMetaEnhancer Application class."
- [other] Save the annotated spectra to an output .msp file.: "Save the annotated spectra to an output .msp file."
- [readme] It adds metadata like SMILES, InChI, and CAS number fetched from the following services: "It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR], [CTS], [PubChem], [IDSM], and [BridgeDb]."
- [readme] import your .msp file: "app.load_data('sample.msp', file_format='msp')"
- [readme] export .msp file: "app.save_data('sample_out.msp', file_format='msp')"
