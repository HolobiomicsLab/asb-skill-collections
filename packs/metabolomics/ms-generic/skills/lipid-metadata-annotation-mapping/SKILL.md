---
name: lipid-metadata-annotation-mapping
description: Use when when exporting in-memory generated spectra as MSP-format spectral libraries, you must first map each spectrum record to required MSP fields (NAME, PRECURSORMZ, SPECTRUM) and optional metadata annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - Excalibur
  - LSG
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04518
  all_source_dois:
  - 10.1021/acs.analchem.2c04518
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-metadata-annotation-mapping

## Summary

Map and annotate generated lipid mass spectra with metadata fields (lipid class, fatty acid composition, adduct type, m/z, intensity) required for MSP spectral library export. This skill ensures complete and standards-compliant annotation of synthetic spectra before serialization.

## When to use

When exporting in-memory generated spectra as MSP-format spectral libraries, you must first map each spectrum record to required MSP fields (NAME, PRECURSORMZ, SPECTRUM) and optional metadata annotations. Apply this skill when transitioning from the lipid generation and fragmentation step to file serialization, to ensure no spectrum lacks identifying metadata or violates MSP structural requirements.

## When NOT to use

- Input spectra are already in a validated MSP file format with complete metadata — proceed directly to export.
- You are exporting to CSV format (Excalibur precursor list or Skyline transition list) — MSP-specific metadata mapping is unnecessary.
- Spectra lack lipid class or fatty acid composition information — annotation mapping cannot proceed until these are available.

## Inputs

- In-memory spectra data structure with generated lipid mass spectra
- Lipid class annotations
- Fatty acid composition metadata
- Adduct type annotations
- m/z and intensity peak pair arrays

## Outputs

- Annotated spectrum records with mapped MSP fields
- Metadata-enriched spectrum objects ready for MSP serialization
- Validation report of annotation completeness

## How to apply

Load the in-memory spectra data structure containing generated lipid mass spectra with their corresponding m/z, intensity, and metadata (lipid class, fatty acid composition, adduct type). For each spectrum record, construct or extract the NAME field (typically lipid class + fatty acid composition + adduct notation), map the precursor m/z value to PRECURSORMZ, and organize peak pairs into the SPECTRUM field. Validate that all required fields are populated and conform to MSP format standards (proper line breaks, field delimiters, peak pair syntax). Document or flag any records with missing or malformed metadata before proceeding to file writing.

## Related tools

- **LSG** (Generates in-memory lipid mass spectra with class, composition, and adduct metadata; provides the spectra data structure requiring annotation mapping before MSP export) — https://github.com/98104781/LSG/releases/tag/v1.3.0

## Evaluation signals

- All spectrum records contain populated NAME, PRECURSORMZ, and SPECTRUM fields conforming to MSP standard syntax.
- Lipid class, fatty acid composition, and adduct type are present and correctly represented in the NAME field annotation.
- Peak pairs in SPECTRUM field are ordered and formatted with correct delimiters (typically m/z intensity pairs separated by spaces or tabs).
- Validation report confirms 100% of records passed structural and completeness checks before MSP file writing.
- Exported MSP file parses without errors when ingested by Excalibur or other MSP-compatible spectral library software.

## Limitations

- Metadata annotation relies on the completeness of the upstream lipid generation step; missing or incorrect lipid class or composition annotations cannot be recovered at this stage.
- The skill addresses mapping and validation only; it does not generate fragmentation patterns or m/z values — those must come from the LSG spectrum generation module.
- No guidance is provided for handling edge cases such as multiply-charged species or non-standard adduct types not covered by peer-reviewed fragmentation rules used by LSG.

## Evidence

- [other] Load the in-memory spectra data structure containing generated lipid mass spectra with their corresponding m/z, intensity, and metadata (lipid class, fatty acid composition, adduct type).: "Load the in-memory spectra data structure containing generated lipid mass spectra with their corresponding m/z, intensity, and metadata (lipid class, fatty acid composition, adduct type)."
- [other] Serialize each spectrum record to MSP format, including required fields (NAME, PRECURSORMZ, SPECTRUM with peak pairs) and optional metadata annotations.: "Serialize each spectrum record to MSP format, including required fields (NAME, PRECURSORMZ, SPECTRUM with peak pairs) and optional metadata annotations."
- [readme] Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts.: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [readme] Spectral libraries can be exported with the file extension '.MSP' selected.: "Spectral libraries can be exported with the file extension '.MSP' selected."
- [other] Validate the output file for structural integrity and completeness of all spectrum records.: "Validate the output file for structural integrity and completeness of all spectrum records."
