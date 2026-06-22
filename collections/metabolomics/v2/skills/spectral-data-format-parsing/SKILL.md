---
name: spectral-data-format-parsing
description: Use when when you have raw LC-MS/MS data files in mzML, mzXML, or vendor-specific formats and need to load them into a Java-based mass spectrometry analysis framework for downstream spectral analysis, fragmentation tree computation, or metabolite identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SIRIUS
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
---

# spectral-data-format-parsing

## Summary

Parse and validate LC-MS/MS spectral data from vendor-neutral file formats (mzML, mzXML, vendor formats) into a structured, in-memory representation with indexed MS1 and MS/MS hierarchies. This skill is essential for ingesting raw mass spectrometry data into computational metabolite analysis pipelines.

## When to use

When you have raw LC-MS/MS data files in mzML, mzXML, or vendor-specific formats and need to load them into a Java-based mass spectrometry analysis framework for downstream spectral analysis, fragmentation tree computation, or metabolite identification. Use this skill as the entry point before any molecular formula determination, isotope pattern analysis, or structure prediction.

## When NOT to use

- Input is already a parsed spectral table or feature matrix — use this skill only on raw instrument output.
- Your input data is in 2D peak matrix or centroided MS/MS-only format without MS1 context — this skill expects full LC-MS/MS hierarchies.
- You are working with in silico or theoretical spectra that do not require vendor file parsing — skip directly to structure prediction.

## Inputs

- raw LC-MS/MS data file (mzML format)
- raw LC-MS/MS data file (mzXML format)
- vendor-specific mass spectrometry data file

## Outputs

- structured spectrum objects with indexed MS1 and MS/MS hierarchies
- SIRIUS serialized spectral dataset
- validated spectral metadata (precursor m/z, retention time, collision energy, fragment assignments)

## How to apply

Load raw LC-MS/MS data files (mzML, mzXML, or vendor formats) into the SIRIUS Java framework using the built-in data importer. Parse and validate spectral metadata including precursor m/z, retention time, collision energy, and fragment ion assignments from the input files. Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation. Perform quality checks including verification of non-zero ion counts, valid mass ranges, and metadata completeness before outputting the validated spectral dataset in SIRIUS serialized format. This ensures that downstream analyses operate on consistently formatted, validated spectra rather than raw instrument output.

## Related tools

- **SIRIUS** (Java framework that accepts parsed LC-MS/MS data and provides the built-in data importer, spectrum object construction, and quality control for format validation) — https://github.com/sirius-ms/sirius

## Evaluation signals

- All input files are successfully read without parser errors or exceptions.
- Spectral metadata fields (precursor m/z, retention time, collision energy) are non-null and within physically plausible ranges for the instrument and ionization mode.
- Ion count for each spectrum is greater than zero; no spectra are empty or contain only zero-intensity peaks.
- MS1 and MS/MS peak assignments are correctly indexed and hierarchically linked in the spectrum object tree.
- Output serialized format can be round-tripped (deserialized and re-serialized) without data loss or structure corruption.

## Limitations

- Parser support is limited to mzML, mzXML, and vendor formats; other formats (e.g., Bruker .d, Waters .raw) may require prior conversion.
- Quality checks verify only metadata completeness and range validity, not spectral correctness or biological plausibility — garbage input may still produce valid serialized output.
- High-resolution spectra with very dense peak lists may require increased memory allocation within the SIRIUS Java framework.
- Retention time validation assumes the input file contains valid RT data; some vendor formats or preprocessing pipelines may omit or zero-fill RT fields.

## Evidence

- [other] SIRIUS is implemented as a Java-based software framework designed to accept LC-MS/MS data as input for downstream analysis.: "SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other "small molecules of biological interest"."
- [other] The parsing workflow loads multiple vendor formats and constructs indexed spectrum hierarchies.: "1. Load raw LC-MS/MS data files (mzML, mzXML, or vendor formats) into the SIRIUS Java framework using the built-in data importer. 2. Parse and validate spectral metadata (precursor m/z, retention"
- [readme] The SIRIUS framework integrates multiple downstream tools, indicating format compatibility is critical.: "SIRIUS integrates a collection of our tools, including CSI:FingerID (with COSMIC), ZODIAC, CANOPUS. In particular, both the graphical user interface and the command line version of SIRIUS seamlessly"
