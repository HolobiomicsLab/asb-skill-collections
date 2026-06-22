---
name: spectral-library-msp-serialization
description: Use when after generating in-memory lipid spectra (with m/z, intensity, and metadata such as lipid class, fatty acid composition, and adduct type) when you need to export those spectra as a reusable MSP-format spectral library for downstream identification tasks in Excalibur, Skyline, or NIST MS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - Excalibur
  - LSG
derived_from:
- doi: 10.1021/acs.analchem.2c04518
  title: Lipid Spectrum Generator
evidence_spans:
- Excalibur compatible precursor list (for DDA analysis via orbitrap)
- https://github.com/98104781/LSG/releases/tag/v1.3.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipid_spectrum_generator_cq
    doi: 10.1021/acs.analchem.2c04518
    title: Lipid Spectrum Generator
  dedup_kept_from: coll_lipid_spectrum_generator_cq
schema_version: 0.2.0
---

# spectral-library-msp-serialization

## Summary

Serializes in-memory generated lipid mass spectra to MSP (NIST MS Search) format for export as searchable spectral libraries. This skill bridges synthetic spectrum generation to standard MS library formats required by database search and DDA workflows.

## When to use

Apply this skill after generating in-memory lipid spectra (with m/z, intensity, and metadata such as lipid class, fatty acid composition, and adduct type) when you need to export those spectra as a reusable MSP-format spectral library for downstream identification tasks in Excalibur, Skyline, or NIST MS Search tools.

## When NOT to use

- Input spectra are empirical (not computationally generated) — use direct MS instrument export instead
- Target output format is CSV precursor lists or Skyline transition lists — select '.CSV' extension for those export modes instead
- Spectra have not been generated with respect to lipid class, fatty acid composition, and adducts — generate or annotate those metadata first

## Inputs

- In-memory spectra data structure (generated lipid mass spectra with m/z, intensity pairs)
- Spectrum metadata (lipid class, fatty acid composition, adduct type, precursor m/z)
- Fragmentation pattern annotations

## Outputs

- .MSP file (NIST MS Search format spectral library)
- Validated spectral library with NAME, PRECURSORMZ, and SPECTRUM fields per record

## How to apply

Load the in-memory spectra data structure containing generated lipid mass spectra with their corresponding m/z, intensity, and metadata fields (lipid class, fatty acid composition, adduct type). For each spectrum record, serialize to MSP format by populating required fields (NAME, PRECURSORMZ, SPECTRUM with peak pairs) and optional metadata annotations following MSP standard conventions. Write the formatted spectral records sequentially to a file with '.MSP' extension, ensuring proper line breaks and field delimiters conform to MSP structural standards. Finally, validate the output file for structural integrity and completeness of all spectrum records to confirm compliance with MSP schema.

## Related tools

- **LSG** (Generates in-memory lipid mass spectra with respect to class, fatty acid composition, and adducts; provides MSP export functionality) — https://github.com/98104781/LSG/releases/tag/v1.3.0
- **Excalibur** (Consumes exported MSP spectral libraries for DDA analysis via Orbitrap instrument control)

## Evaluation signals

- Output .MSP file parses without syntax errors and loads into NIST MS Search or Excalibur without validation warnings
- All spectrum records contain mandatory fields: NAME, PRECURSORMZ, and SPECTRUM (peak pairs with m/z and intensity)
- Peak pairs in SPECTRUM field are represented as space-separated 'mz intensity' pairs on a single line, with multiple pairs separated by appropriate delimiters per MSP standard
- Metadata annotations (lipid class, fatty acid composition, adduct) are preserved in NAME or optional comment fields
- File structure integrity: no truncated records, proper line breaks between spectrum blocks, and line count matches expected record count × lines-per-record

## Limitations

- MSP format export depends on correct in-memory spectrum generation; invalid fragmentation patterns or metadata will serialize but produce unusable library entries
- The LSG program generates spectra based on fragmentation patterns from peer-reviewed studies; coverage may not include all lipid species or adduct combinations of interest
- MSP format does not support all optional metadata fields; complex lipid annotations may need truncation or external supplementary documentation

## Evidence

- [other] Load the in-memory spectra data structure and serialize to MSP format: "Load the in-memory spectra data structure containing generated lipid mass spectra with their corresponding m/z, intensity, and metadata (lipid class, fatty acid composition, adduct type). 2."
- [other] Write formatted records to .MSP extension file with validation: "Write the formatted spectral records sequentially to a file with '.MSP' extension, ensuring proper line breaks and field delimiters conform to MSP standards. 4. Validate the output file for"
- [readme] MSP export as alternative to CSV formats: "Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may"
- [readme] Lipids generated with respect to class, fatty acid composition, and adducts: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
