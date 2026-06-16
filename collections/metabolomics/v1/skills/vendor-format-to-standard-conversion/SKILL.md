---
name: vendor-format-to-standard-conversion
description: Use when when ingesting raw LC-MS/MS output from a mass spectrometry instrument and you need to prepare it for metabolite identification, fragmentation tree computation, or molecular formula annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - SIRIUS
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
---

# vendor-format-to-standard-conversion

## Summary

Convert raw LC-MS/MS data from vendor-specific formats (mzML, mzXML, or instrument-native formats) into a structured, validated intermediate representation suitable for downstream metabolite analysis. This step ensures data integrity and enables seamless integration with standardized mass spectrometry processing pipelines.

## When to use

When ingesting raw LC-MS/MS output from a mass spectrometry instrument and you need to prepare it for metabolite identification, fragmentation tree computation, or molecular formula annotation. Specifically when input files are in vendor formats (Thermo, Bruker, Waters, etc.), mzML, or mzXML and must be parsed into a framework-agnostic in-memory representation before downstream analysis.

## When NOT to use

- Input is already a processed, normalized spectral library or feature table (e.g., mzTab, MGF from a database search).
- Data has already been converted to SIRIUS internal format in a prior workflow step.
- Input is a single-stage MS spectrum without tandem (MS/MS) fragmentation data; isotope pattern analysis may not require full conversion.

## Inputs

- Raw LC-MS/MS data file (vendor format: .raw, .d, .ms, or standard format: mzML, mzXML)
- Spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments)

## Outputs

- Structured spectrum objects with indexed MS1 and MS/MS hierarchies
- Validated spectral dataset in SIRIUS serialized format
- Quality-checked dataset (non-zero ion counts, valid mass ranges, metadata completeness verified)

## How to apply

Load raw LC-MS/MS data files (mzML, mzXML, or vendor formats) into the SIRIUS Java framework using the built-in data importer. Parse and validate spectral metadata including precursor m/z, retention time, collision energy, and fragment ion assignments from the input files. Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation. Perform basic quality checks (non-zero ion counts, valid mass ranges, metadata completeness) and output the validated spectral dataset in SIRIUS serialized format. The conversion ensures that heterogeneous vendor formats are normalized into a common object model before fragmentation tree analysis or isotope pattern evaluation.

## Related tools

- **SIRIUS** (Java framework that accepts LC-MS/MS data via built-in data importer, parses vendor and standard formats, validates spectral metadata, and constructs in-memory spectrum objects) — https://github.com/sirius-ms/sirius

## Evaluation signals

- All spectrum objects contain non-zero ion counts and valid m/z values within expected mass range for the instrument.
- Precursor m/z, retention time, and collision energy fields are populated and internally consistent (no missing critical metadata).
- MS1 and MS/MS data hierarchies are correctly indexed; fragment peaks are associated with their parent precursor.
- Serialized output in SIRIUS format can be successfully deserialized and re-loaded without parsing errors.
- Comparison of ion counts and peak positions between input raw file and SIRIUS output shows no loss of spectral information (1:1 correspondence of peaks above noise threshold).

## Limitations

- Vendor format support depends on availability of format specifications; proprietary or legacy instrument formats may lack robust importers.
- Quality checks (non-zero ion counts, valid mass ranges) apply uniform thresholds that may not be optimal for all instrument types or sample matrices.
- No changelog is provided in the repository; version history of import format compatibility is not documented.
- Metadata completeness validation may fail silently or with limited user feedback if optional fields (e.g., collision energy) are absent from the input file.

## Evidence

- [other] Load raw LC-MS/MS data files (mzML, mzXML, or vendor formats) into the SIRIUS Java framework using the built-in data importer.: "Load raw LC-MS/MS data files (mzML, mzXML, or vendor formats) into the SIRIUS Java framework using the built-in data importer."
- [other] Parse and validate spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments) from the input files.: "Parse and validate spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments) from the input files."
- [other] Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation.: "Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation."
- [other] Perform basic quality checks (non-zero ion counts, valid mass ranges, metadata completeness) and output the validated spectral dataset in SIRIUS serialized format.: "Perform basic quality checks (non-zero ion counts, valid mass ranges, metadata completeness) and output the validated spectral dataset in SIRIUS serialized format."
- [readme] SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other "small molecules of biological interest".: "SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other "small molecules of biological interest"."
